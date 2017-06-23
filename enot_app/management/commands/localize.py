import pytz
import json

from enot_app.toolbox import get_russian_form


from enot_app.models import Quote, Tag, Trip


from django.core.management.base import BaseCommand


class Command(BaseCommand):

    # def add_arguments(self, parser):

    #     parser.add_argument('--word',
    #                         action='store',
    #                         type=str,
    #                         default='',
    #                         dest='word')

    def handle(self, *args, **options):
        trips = Trip.objects.all()
        tz = pytz.timezone('Europe/Moscow')
        for t in trips:
            t.departure = tz.localize(t.departure)
            t.arrival = tz.localize(t.arrival)
            t.save()
        