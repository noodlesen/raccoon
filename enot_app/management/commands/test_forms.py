# import pytz
# import json

# from operator import itemgetter
# from datetime import datetime

from enot_app.toolbox import get_russian_form


from enot_app.models import Trip, Airport


from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--word',
                            action='store',
                            type=str,
                            default='',
                            dest='word')

    def handle(self, *args, **options):
        get_russian_form(options['word'], '')
