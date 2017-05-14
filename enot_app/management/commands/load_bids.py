""" Scheduled bid loader script """

import pytz
from datetime import datetime, timedelta
from time import sleep
from random import choice

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Q, F

import enot_app.sentinel as sentinel
from enot_app.models import Bid, SpiderQueryTP, Destination, DayJob
from enot_app.tpapi import get_month_bids
from enot_app.rating import prerate
from enot_app.toolbox import now_in_moscow
from enot_app.planner import make_TP_plan


def bid_cleanup(d):
    """ Cleaning up bids table """

    now = datetime.utcnow()
    today = datetime.today()
    last = now - timedelta(days=d)
    print ('<<<', d, last)
    last = pytz.utc.localize(last)

    Bid.objects.filter(Q(found_at__lt=last)
                       | Q(departure_date__lte=today)
                       | Q(departure_date=F('return_date'))
                       ).delete()


WORK_TIME_LIMIT = 30  # 3300
REQUEST_DELAY = 4
BID_LIFETIME = 2


class Command(BaseCommand):
    """ Preloads some new bids using tpapi """

    def add_arguments(self, parser):

        parser.add_argument('--time',
                            action='store',
                            type=int,
                            default=WORK_TIME_LIMIT,
                            dest='wtl')

        parser.add_argument('--delay',
                            action='store',
                            type=int,
                            default=REQUEST_DELAY,
                            dest='rd')

        parser.add_argument('--lifetime',
                            action='store',
                            type=int,
                            default=BID_LIFETIME,
                            dest='lt')

        parser.add_argument('--force',
                            action='store_true',
                            dest='force')

    def handle(self, *args, **options):

        if sentinel.allows('to_load_bids', force=options['force']):

            wtl = options['wtl']
            rd = options['rd']
            lt = options['lt']
            print ('wtl: %d, rd: %d, lt: %d' % (wtl, rd, lt))

            if sentinel.have('to_run_planner'):
                if sentinel.allows('to_run_planner'):
                    sentinel.report('Have to run planner first...')
                    res = make_TP_plan()
                    print (res)
                    sentinel.finish('to_plan')

            started_at = datetime.now()

            moscow_time = now_in_moscow()

            bid_cleanup(lt)

            #old_limit = moscow_time - timedelta(days=1)

            """ Browsing through queries """
            srt = choice(['', '-'])+choice(['start_date', 'destination', 'id'])
            sentinel.report('Sorting order: %s' % srt)

            target_code = DayJob.get_target_code()
            sentinel.report("Today's code: "+target_code, src=__name__)
            target = Destination.objects.get(code=target_code)

            queries = SpiderQueryTP.objects.filter(
                #requested_at__lt=old_limit,
                origin=target
            ).order_by(srt)[:500]
            for q in queries:
                sleep(rd)
                if (datetime.now()-started_at).seconds >= wtl:
                    print ('Reached work time limit - ', wtl, " sec")
                    break
                sentinel.report(q.origin.code+" >>> "+q.destination.code)

                month_bids = get_month_bids(
                    {"beginning_of_period": q.start_date.strftime('%Y-%m-%d'),
                     "destination": q.destination.code,
                     "origin": q.origin.code
                     }
                )

                q.requested_at = moscow_time
                q.save()

                dest = Destination.objects.get(code=q.destination.code)

                sum_price = 0
                sum_bids = 0

                if month_bids['data']:
                    for b in month_bids['data']:
                        found_at = datetime.strptime(
                            ':'.join(b['found_at'].split(':')[:-1])+'00',
                            '%Y-%m-%dT%H:%M:%S%z'
                        )
                        departure_date = datetime.strptime(
                            b['depart_date'],
                            '%Y-%m-%d'
                        )

                        bid = Bid()
                        bid.origin_code = b['origin']
                        bid.destination_code = b['destination']
                        bid.destination_name = q.destination.name.upper()

                        bid.origin = Destination.objects.get(code=bid.origin_code)
                        bid.destination = Destination.objects.get(code=bid.destination_code)

                        bid.one_way = month_bids['params']['one_way'] == 'true'
                        bid.price = b['value']
                        sum_price += b['value']
                        sum_bids += 1
                        bid.trip_class = b['trip_class']
                        bid.stops = b['number_of_changes']
                        bid.distance = b['distance']
                        bid.departure_date = departure_date

                        bid.signature = b['origin']+b['destination']+str(b['value'])+str(b['number_of_changes'])+b['depart_date']

                        if 'return_date' in b.keys():
                            bid.return_date = datetime.strptime(
                                b['return_date'],
                                '%Y-%m-%d'
                            )
                            bid.signature += b['return_date']

                        bid.found_at = found_at
                        bid.pre_rating = prerate(bid)
                        bid.chd_days = (bid.return_date-bid.departure_date).days
                        bid.to_expose = True

                        try:
                            bid.save()
                        except IntegrityError:
                            print ("Signature exists: ", bid.signature)
                            pass

                    """ Updating destination stats """
                    nbc = dest.total_bid_count+sum_bids
                    if nbc > 0:
                        dest.avg_price = int(
                            (dest.average_price*dest.total_bid_count+sum_price)/nbc
                        )
                        dest.total_bid_count = nbc
                        dest.save()

            sentinel.finish('to_load_bids')





