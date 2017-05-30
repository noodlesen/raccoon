from django.core.management.base import BaseCommand

from enot_app.rating import review
from enot_app.models import Trip

import json


class Command(BaseCommand):
    """ Force rating on trips"""

    def handle(self, *args, **options):
        trips = Trip.objects.all()
        for t in trips:
            r = review(t)
            
            t.rt_price=r['rt_price']
            t.rt_comfort=r['rt_comfort']
            t.rt_eff=r['rt_eff']
            t.rating = r['rt']

            t.carriers_names = json.dumps(r['carriers'])
            t.benefits = json.dumps(r['benefits'])
            t.penalties = json.dumps(r['penalties'])

            t.supply()
            t.save()
        