""" Builds the offers list for the mail """

from operator import itemgetter
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from datetime import datetime

from enot_app.models import Bid, Subscriber
from enot_app.toolbox import dictfetchall
from enot_app.qpxexpress import QPXExpressApi, QPXRequest, QPXResponse
from enot.settings import GOOGLE_API_KEY


class Command(BaseCommand):

    def handle(self, *args, **options):
        cursor = connection.cursor()
        query = """
                SELECT destination_name,
                       departure_date,
                       return_date,
                       distance,
                       price
                FROM enot_app_bid
                GROUP BY destination_name
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)

        subscribers = Subscriber.objects.filter(tester=True)

        for s in subscribers:
            

            for r in rows:
                rt =0
                d = r['distance']
                days = (r['return_date']-r['departure_date']).days
                if d > 1200 and d <= 2100:
                    rt += 100
                if d > 2100 and d <= 4000:
                    rt += 300
                    if days>21:
                        rt-=200
                if d > 4000 and d <= 8000:
                    rt += 200
                    if days>40 or days<7:
                        rt-=200
                if d > 8000:
                    rt += 100
                    if days>60 or days<14:
                        rt-=200
                rt += int(d/r['price']*1000)

                if days<3:
                    rt-=300

                r['rating']=rt
                r['days']=days


            rows = sorted(rows, key=itemgetter('rating'), reverse=True)[:50]

            for i,r in enumerate(rows):
                # print()
                # print(i,':')
                # print(r['destination_name'])
                # print(r['distance'], "km")
                # print(r['price'])
                # print("R",r['rating'])
                

                print ('%d: %s | %dд | %d км | %dр | R%d' %(i+1, r['destination_name'], r['days'], r['distance'], r['price'], r['rating']))




        print ()
        print (len(rows))

        qpx = QPXExpressApi(api_key=GOOGLE_API_KEY)

        req = QPXRequest(destination='BCN',
                         origin='MOW',
                         date=datetime(2017,6,3),
                         return_date=datetime(2017,6,29),
                         num_adults=1
                         )
        print (datetime.now())
        resp = qpx.search(req)
        print (datetime.now())

        print (resp.top_flights(num=30))


