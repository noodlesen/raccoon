from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Bid, Destination
import random
from enot_app.toolbox import get_distance
from datetime import datetime, timedelta
import pytz 

class Command(BaseCommand):
    help = 'testing tpapi'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        Bid.objects.all().delete()
        mlat = 55.755826
        mlng = 37.6173
        moscow = Destination.objects.get(pk=390)
        #codes = []
        dests = []
        ds = Destination.objects.all()

        # for i in range(0, 49):
        #     d = random.choice(ds)
        #     if d.code not in codes:
        #         codes.append(d.code)
        #         dests.append(d)

        dests = random.sample(list(ds), 49)
        #print (codes)
        for d in dests:
            p = d.place
            print (d.name)
            #print (get_distance(mlat,mlng, p.lat, p.lng ))
            b = Bid()
            b.origin_code = 'MOW'
            b.destination_code = d.code
            b.destination_name = d.name
            b.one_way = 0
            b.price = 20000
            b.stops = 4
            b.trip_class = 0
            b.distance = get_distance(mlat,mlng, p.lat, p.lng )
            b.to_expose = 1
            b.found_at = datetime.utcnow().replace(tzinfo=pytz.utc)
            b.signature = d.code
            b.destination = d
            b.origin = moscow
            b.pre_rating = 100
            b.best_price = 1

            days = random.randrange(5,22)
            offset = random.randrange(14, 90)
            b.departure_date = datetime.today()+timedelta(days=offset)
            b.return_date = datetime.today()+timedelta(days=offset+days)
            b.chd_days = days

            b.save()

