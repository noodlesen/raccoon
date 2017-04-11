from django.core.management.base import BaseCommand

from operator import itemgetter

from enot_app.models import Bid
from enot_app.rating import prerate


class Command(BaseCommand):
    """ Force pre-rating on bids """

    def handle(self, *args, **options):
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

        bid_list = [v for k,v in dests.items()]
  
        for d in dlist:
            print()
            print(d['dest'])
            print(d['pr'])

        print (bid_list)



