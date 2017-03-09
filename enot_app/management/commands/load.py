""" Scheduled bid loader script """

import pytz
from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db.models import Q, F

from enot_app.models import Bid, SpiderQueryTP, Destination
from enot_app.tpapi import get_month_bids


def bid_cleanup(d):
    """ Cleaning up bids table """

    now = datetime.utcnow()
    today = datetime.today()
    last = now - timedelta(days=d)
    last = pytz.utc.localize(last)

    Bid.objects.filter(Q(found_at__lt=last)
                       | Q(departure_date__lte=today)
                       | Q(departure_date=F('return_date'))
                       ).delete()


WORK_TIME_LIMIT = 3300
REQUEST_DELAY = 1
BID_LIFETIME = 2


class Command(BaseCommand):
    """ Preloads some new bids using tpapi """

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        started_at = datetime.now()

        bid_cleanup(BID_LIFETIME)

        tz = pytz.timezone('Europe/Moscow')
        old_limit = tz.localize(datetime.now())-timedelta(days=1)

        print ("OLD ",old_limit)

        """ Browsing through queries """
        queries = SpiderQueryTP.objects.filter(requested_at__lt=old_limit).order_by('start_date')[:200]
        for q in queries:
            sleep(REQUEST_DELAY)
            if (datetime.now()-started_at).seconds >= WORK_TIME_LIMIT:
                print ('Reached work time limit - ', WORK_TIME_LIMIT, " sec")
                break
            print (q.origin.code, " >>> ", q.destination.code, q.requested_at)

            month_bids = get_month_bids(
                {"beginning_of_period": q.start_date.strftime('%Y-%m-%d'),
                 "destination": q.destination.code,
                 "origin": q.origin.code
                 }
            )

            q.requested_at=tz.localize(datetime.now())
            q.save()

            dest = Destination.objects.get(code=q.destination.code)

            sum_price = 0
            sum_bids = 0

            for b in month_bids['data']:
                found_at = datetime.strptime(
                    ':'.join(b['found_at'].split(':')[:-1])+'00',
                    '%Y-%m-%dT%H:%M:%S%z'
                )
                #found_at = pytz.utc.localize(found_at)
                departure_date = datetime.strptime(
                    b['depart_date'],
                    '%Y-%m-%d'
                )

                bid = Bid()
                bid.origin_code = b['origin']
                bid.destination_code = b['destination']
                bid.destination_name = q.destination.name.upper()
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

                # tmp:
                #bid.rating = int(bid.distance/bid.price*1000)
                bid.to_expose = True

                try:
                    bid.save()
                except IntegrityError as e:
                    print ("IntegrityError: ", bid.signature)
                    pass

            """ Updating destination stats """
            nbc = dest.total_bid_count+sum_bids
            if nbc >0:
                dest.avg_price = int(
                    (dest.average_price*dest.total_bid_count+sum_price)/nbc
                )
                dest.total_bid_count = nbc
                dest.save()





