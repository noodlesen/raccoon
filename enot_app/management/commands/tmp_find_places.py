# import pytz
# import json

# from operator import itemgetter
# from datetime import datetime



from enot_app.models import Trip, Airport
# import enot_app.sentinel as sentinel

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        aps = Airport.objects.all()
        for ap in aps:
            ap.tmp_find_place()
