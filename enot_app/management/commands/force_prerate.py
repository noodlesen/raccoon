from django.core.management.base import BaseCommand

from enot_app.models import Bid
from enot_app.rating import prerate


class Command(BaseCommand):
    """ Force pre-rating on bids """

    def handle(self, *args, **options):
        bids = Bid.objects.all()
        i = 0
        for b in bids:
            print (i)
            i += 1
            b.pre_rating = prerate(b)
            b.save()
