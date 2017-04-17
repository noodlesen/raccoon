from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from enot_app.toolbox import now_in_moscow

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print (datetime.utcnow())
        print (now_in_moscow())