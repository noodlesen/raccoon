""" Builds the offers list for the mail """

import json
import pytz
from operator import itemgetter
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from datetime import datetime

from enot_app.models import Bid, Subscriber, Airline, Trip, Stat
from enot_app.toolbox import dictfetchall
from enot_app.qpxexpress import QPXExpressApi, QPXRequest, QPXResponse
from enot.settings import GOOGLE_API_KEY





class Command(BaseCommand):

    def handle(self, *args, **options):
        cursor = connection.cursor()
        query = """
                SELECT id,
                       destination_name,
                       destination_code,
                       departure_date,
                       return_date,
                       distance,
                       price,
                       stops,
                       found_at,
                       pre_rating,
                       chd_days
                FROM enot_app_bid
                GROUP BY destination_name
                ORDER BY pre_rating DESC
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)

       # subscribers = Subscriber.objects.filter(tester=True)

        for r in rows:
            rt = r['pre_rating']
            age = int((datetime.utcnow()-r['found_at']).seconds/3600)
            rt -= 10*age
            r['age'] = age
            r['rating']=rt

        rows = sorted(rows, key=itemgetter('rating'), reverse=True)[:50]

        for i,r in enumerate(rows):
            print ('%d: [%d] %s | %dд | %d км | %dр | R%d | %dч ' %(i+1, r['id'], r['destination_name'], r['chd_days'], r['distance'], r['price'], r['rating'], r['age']))


        qpx = QPXExpressApi(api_key=GOOGLE_API_KEY)

        v = rows[0]

        # print(v)


        req = QPXRequest('MOW',
                         v['destination_code'],
                         v['departure_date'],
                         1,
                         return_date=v['return_date']
                         )
        stats = Stat.objects.get_or_create(stat_date=datetime.today())
        if stats.qpx_requests < 50:
            resp = qpx.search(req)
            stats.qpx_requests += 1
            stats.save()
            
            res = resp.top_trips(num=10)

            for r in res:
                print()
                print(r)
                print()

                t = Trip()
                t.origin_code = r['origin']
                t.destination_code = r['destination']
                t.return_code = r['return']
                t.price = r['price']
                t.currency = r['currency']
                t.departure = r['trip_departure']
                t.arrival = r['trip_arrival']
                t.carriers = ', '.join(r['carriers'])
                t.slices = json.dumps(r['slices'])

                t.save()
        else:
            print ("REQUESTS LIMIT EXCEEDED")


