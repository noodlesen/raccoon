""" Builds the offers list for the mail """

import json
from operator import itemgetter
from datetime import datetime

from django.core.management.base import BaseCommand

from enot.settings import GOOGLE_API_KEY
import enot_app.sentinel as sentinel
from enot_app.models import Bid, Trip
from enot_app.qpxexpress import QPXExpressApi, QPXRequest
from enot_app.rating import review


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--limit',
                            action='store',
                            type=int,
                            default=50,
                            dest='req_lim')

    def handle(self, *args, **options):

        sentinel.inform('started_trip_loader')

        bids = Bid.objects.filter(pre_rating__gt=0)
        dests = {}
        for b in bids:
            if b.destination_code not in dests.keys():
                dests[b.destination_code] = b
            else:
                pr = dests[b.destination_code].pre_rating
                fa = dests[b.destination_code].found_at
                if b.pre_rating > pr:
                    dests[b.destination_code] = b
                elif b.pre_rating == pr:
                    if b.found_at > fa:
                        dests[b.destination_code] = b

        dlist = sorted(
            [{"dest": k, "bid": v, "pr": v.pre_rating} for k, v in dests.items()],
            key=itemgetter('pr'),
            reverse=True
        )

        bids = [d['bid'] for d in dlist][:50]

        for i, b in enumerate(bids):
            print ('%d: [%d] %s | %dд | %d км | %dр | R%d' % (
                i+1,
                b.id,
                b.destination_name,
                b.chd_days,
                b.distance,
                b.price,
                b.pre_rating,
            ))

        qpx = QPXExpressApi(api_key=GOOGLE_API_KEY)

        started = datetime.now()
        for b in bids[:options['req_lim']]:

            req = QPXRequest('MOW',
                             b.destination_code,
                             b.departure_date,
                             1,
                             return_date=b.return_date
                             )

            if sentinel.allows('to_request_qpx'):
                resp = qpx.search(req)
                res = resp.top_trips(num=30)

                for r in res:
                    t = Trip.load_qpx(r, b)
                    rw = review(t)
                    t.benefits = json.dumps(rw['benefits'])
                    t.penalties = json.dumps(rw['penalties'])
                    t.carriers_names = json.dumps(rw['carriers'])
                    t.rt_comfort = rw['rt_comfort']
                    t.rt_price = rw['rt_price']
                    t.rt_eff = rw['rt_eff']
                    t.rating = rw['rt']
                    t.supply()
                    t.save()

        finished = datetime.now()
        print ('TIME ELAPSED: ', (finished-started).seconds)

        sentinel.inform('finished_trip_loader')


