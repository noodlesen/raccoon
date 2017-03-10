from django.core.management.base import BaseCommand

from enot_app.models import Bid
from enot_app.rating import prerate


class Command(BaseCommand):
    """ Checks if Spiders TPQueries are up to date """

    def handle(self, *args, **options):
        bids = Bid.objects.all()
        i = 0
        for b in bids:
            print (i)
            i += 1
            pr = prerate(b)
            b.pre_rating = pr

            # days = (b.return_date-b.departure_date).days  # move to loader
            # b.chd_days=days

            b.save()
