import pytz
from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from enot_app.models import Bid, SpiderQueryTP
from enot_app.tpapi import get_month_bids


class Command(BaseCommand):
    help = 'Preloads some newbids from tpapi'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        tz = pytz.timezone('Europe/Moscow')
        time_limit = tz.localize(datetime.now())-timedelta(days=1)
        queries=SpiderQueryTP.objects.filter(requested_at__lt=time_limit).order_by('start_date')[:200]
        for q in queries:
            sleep(2)
            print (q.origin.code, " >>> ", q.destination.code)

            month_bids = get_month_bids(
                {"beginning_of_period": q.start_date.strftime('%Y-%m-%d'),
                 "destination": q.destination.code,
                 "origin": q.origin.code
                 }
            )

            sum_price = 0
            sum_bids = 0

            for b in month_bids['data']:
                #destination = b['destination']
                found_at = datetime.strptime(
                    ':'.join(b['found_at'].split(':')[:-1])+'00',
                    '%Y-%m-%dT%H:%M:%S%z'
                )
                departure_date = datetime.strptime(
                    b['depart_date'],
                    '%Y-%m-%d'
                )
                #price = b['value']

                bid = Bid()
                bid.origin_code = b['origin']
                bid.destination_code = b['destination']
                bid.destination_name = q.destination.name.upper()
                bid.one_way = month_bids['params']['one_way']=='true'
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
                    bid.signature+=b['return_date']

                bid.found_at = found_at

                # tmp:
                bid.rating=0
                bid.to_expose=True

                #bid.save()

                try:
                    bid.save()
                except IntegrityError as e:
                    print ("IntegrityError: ", bid.signature)
                    pass

                
  
