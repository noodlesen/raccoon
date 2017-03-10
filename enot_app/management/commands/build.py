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
                       found_at,
                       pre_rating,
                       chd_days
                FROM enot_app_bid
                GROUP BY destination_name
                ORDER BY pre_rating DESC
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)

        subscribers = Subscriber.objects.filter(tester=True)

        for s in subscribers:
            
            for r in rows:
                
                rt = r['pre_rating']

                age = int((datetime.utcnow()-r['found_at']).seconds/3600)
                rt -= 10*age

                r['age'] = age

                r['rating']=rt


            rows = sorted(rows, key=itemgetter('rating'), reverse=True)[:50]

            for i,r in enumerate(rows):
                print ('%d: %s | %dд | %d км | %dр | R%d | %dч ' %(i+1, r['destination_name'], r['chd_days'], r['distance'], r['price'], r['rating'], r['age']))


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


