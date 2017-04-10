from django.core.management.base import BaseCommand

from enot_app.rating import review
from enot_app.models import Trip


class Command(BaseCommand):
    """ Force rating on trips"""

    def handle(self, *args, **options):
        trips = Trip.objects.all()
        for t in trips:
            r = review(t)
            print (r)
            t.rt_price=r['rt_price']
            t.rt_comfort=r['rt_comfort']
            t.rating = r['rt_price']+r['rt_comfort']
            t.save()
        