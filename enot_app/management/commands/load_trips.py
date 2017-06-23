""" Builds the offers list for the mail """

import json
from operator import itemgetter
from datetime import datetime

from django.core.management.base import BaseCommand

from enot.settings import GOOGLE_API_KEY
import enot_app.sentinel as sentinel
from enot_app.models import Bid, Trip, DayJob, Issue
from enot_app.qpxexpress import QPXExpressApi, QPXRequest
from enot_app.rating import review
from enot_app.toolbox import get_hash


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--limit',
                            action='store',
                            type=int,
                            default=50,
                            dest='req_lim')

        parser.add_argument('--shift',
                            action='store',
                            type=int,
                            default=0,
                            dest='bid_shift')

        parser.add_argument('--test',
                            action='store_true',
                            dest='test')

    def handle(self, *args, **options):

        sentinel.inform('started_trip_loader')

        


        # bids = Bid.objects.filter(pre_rating__gt=0)
        # for b in bids:
        #     if b.destination_code not in dests.keys():
        #         dests[b.destination_code] = b
        #     else:
        #         pr = dests[b.destination_code].pre_rating
        #         fa = dests[b.destination_code].found_at
        #         if b.pre_rating > pr:
        #             dests[b.destination_code] = b
        #         elif b.pre_rating == pr:
        #             if b.found_at > fa:
        #                 dests[b.destination_code] = b

        # dlist = sorted(
        #     [{"dest": k, "bid": v, "pr": v.pre_rating} for k, v in dests.items()],
        #     key=itemgetter('pr'),
        #     reverse=True
        # )

        dlist = Bid.get_best_for_each_dest()

        target_city = DayJob.get_target()

        stop_list = Issue.get_last_stoplist(target_city)

        # print('STOPLIST')
        # print(stop_list)

        # bids = [d['bid'] for d in dlist if d['bid'].destination_code not in stop_list][bs:]
        bs = options['bid_shift']
        bids = [d['bid'] for d in dlist][bs:]



        for i, b in enumerate(bids):
            sentinel.report('%d: [%d] %s | %dд | %d км | %dр | R%d' % (
                i+1,
                b.id,
                b.destination_name,
                b.chd_days,
                b.distance,
                b.price,
                b.pre_rating,
            ))

        if not options['test']:
            qpx = QPXExpressApi(api_key=GOOGLE_API_KEY)  

            started = datetime.now()
            for b in bids[:options['req_lim']]:

                if True:  #b.destination_code not in stop_list:

                    req = QPXRequest(target_city.code,
                                     b.destination_code,
                                     b.departure_date,
                                     1,
                                     return_date=b.return_date
                                     )

                    if sentinel.allows('to_request_qpx'):

                        print('search')
                        resp = qpx.search(req)
                        res = resp.top_trips(num=30)

                        

                        for r in res:
                            t = Trip.load_qpx(r, b)
                            t.origin_city = target_city
                            rw = review(t)
                            t.rt_comfort = rw['rt_comfort']
                            t.rt_price = rw['rt_price']
                            t.rt_eff = rw['rt_eff']
                            t.rating = rw['rt']
                            t.tplink = rw['tplink']
                            t.direct = rw['direct']
                            t.hd = json.dumps(rw['hd'])
                            if b.destination_code not in stop_list:
                                t.new = True
                            t.save()
                            t.slug = get_hash(str(t.id))
                            t.save()

                else:
                    print(b.destination_code, 'is in the stop list — PASS')

            finished = datetime.now()
            print ('TIME ELAPSED: ', (finished-started).seconds)

            sentinel.inform('finished_trip_loader')
        else:
            print('TEST MODE')


