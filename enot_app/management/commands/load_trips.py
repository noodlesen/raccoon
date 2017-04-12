""" Builds the offers list for the mail """

import json
import pytz
from operator import itemgetter
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from datetime import datetime

from enot_app.models import Bid, Subscriber, Airline, Trip, Status
from enot_app.toolbox import dictfetchall
from enot_app.qpxexpress import QPXExpressApi, QPXRequest, QPXResponse
#from enot_app.common import get_current_stats
from enot.settings import GOOGLE_API_KEY
from enot_app.rating import review





class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--limit',
                            action='store',
                            type=int,
                            default=50,
                            dest='req_lim')

    def handle(self, *args, **options):
        # cursor = connection.cursor()

        #         #       SELECT id,
        #         #        destination_id,
        #         #        destination_name,
        #         #        destination_code,
        #         #        departure_date,
        #         #        return_date,
        #         #        distance,
        #         #        price,
        #         #        stops,
        #         #        found_at,
        #         #        pre_rating,
        #         #        chd_days
        #         # FROM enot_app_bid
        #         # GROUP BY destination_name
        #         # ORDER BY pre_rating DESC

        # query = """
        #         SELECT 
        #            id,
        #            destination_id,
        #            destination_name,
        #            destination_code,
        #            departure_date,
        #            return_date,
        #            distance,
        #            price,
        #            stops,
        #            found_at,
        #            pre_rating,
        #            chd_days,
        #            Allbids.id,
        #            MAX(found_at) AS found_at
        #         FROM (
        #           SELECT 
        #              destination_code as dc,
        #              MAX(pre_rating) as rating
        #           FROM enot_app_bid
        #           GROUP BY destination_code
        #         ) AS Topbids
        #         LEFT JOIN enot_app_bid AS Allbids
        #         ON Topbids.dc = Allbids.destination_code AND Topbids.rating = Allbids.pre_rating
        #         GROUP BY destination_code
        #         ORDER BY pre_rating DESC
        #         """
        # cursor.execute(query)
        # bids = dictfetchall(cursor)


        bids = Bid.objects.filter(pre_rating__gt=0)
        dests = {}
        for b in bids:
            if b.destination_code not in dests.keys():
                dests[b.destination_code]=b
            else:
                pr = dests[b.destination_code].pre_rating
                fa = dests[b.destination_code].found_at
                if b.pre_rating > pr:
                    dests[b.destination_code]=b
                elif b.pre_rating == pr:
                    if b.found_at > fa:
                        dests[b.destination_code]=b

        dlist = sorted(
            [{"dest": k, "bid": v, "pr": v.pre_rating} for k,v in dests.items()],
            key=itemgetter('pr'),
            reverse=True
        )

        bids = [d['bid'] for d in dlist][:50]

        ####################

        # for b in bids:
        #     rt = b.pre_rating
        #     age = int((datetime.utcnow()-b.found_at).seconds/3600)
        #     rt -= 10*age
        #     b.age = age
        #     b.rating = rt

        # bids = sorted(bids, key=itemgetter('rating'), reverse=True)[:50]

        # for b in bids:
        #     avp = Bid.objects.get(pk=b['id']).destination.average_price
        #     b['average_price'] = avp

        for i,b in enumerate(bids):
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

            print (b)

            req = QPXRequest('MOW',
                             b.destination_code,
                             b.departure_date,
                             1,
                             return_date=b.return_date
                             )

            stats = Status.get_today()
            if stats.qpx_requests < 50:
                resp = qpx.search(req)
                stats.qpx_requests += 1
                stats.save()
                res = resp.top_trips(num=30)

                for r in res:
                    print()
                    print(r)

                    t = Trip.load_qpx(r, b)

                    rw = review(t)
                    t.benefits = json.dumps(rw['benefits'])
                    t.penalties = json.dumps(rw['penalties'])
                    t.rt_comfort = rw['rt_comfort']
                    t.rt_price = rw['rt_price']
                    t.rating = rw['rt']

                    t.save()
            else:
                print ("REQUESTS LIMIT EXCEEDED")


        finished = datetime.now()
        print ('TIME ELAPSED: ', (finished-started).seconds)

