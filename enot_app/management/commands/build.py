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
                       price,
                       stops,
                       found_at
                FROM enot_app_bid
                GROUP BY destination_name
                ORDER BY price
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)

        subscribers = Subscriber.objects.filter(tester=True)

        for s in subscribers:
            
            for r in rows:
                """ Calculate common rating """
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

                wd = r['departure_date'].weekday()
                if wd == 3:
                    rt+=50
                elif wd == 4 or wd == 5:
                    rt+=100

                rt = rt-r['stops']*100

                age = int((datetime.utcnow()-r['found_at']).seconds/3600)
                rt -= 10*age

                r['age'] = age

                r['rating']=rt
                r['days']=days


            rows = sorted(rows, key=itemgetter('rating'), reverse=True)[:50]

            for i,r in enumerate(rows):
                print ('%d: %s | %dд | %d км | %dр | R%d | %dч ' %(i+1, r['destination_name'], r['days'], r['distance'], r['price'], r['rating'], r['age']))


        # qpx = QPXExpressApi(api_key=GOOGLE_API_KEY)

        # req = QPXRequest(destination='BCN',
        #                  origin='MOW',
        #                  date=datetime(2017,6,3),
        #                  return_date=datetime(2017,6,29),
        #                  num_adults=1
        #                  )
        # print (datetime.now())
        # resp = qpx.search(req)
        # print (datetime.now())

        # print (resp.top_flights(num=30))


