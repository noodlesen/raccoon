from django.core.management.base import BaseCommand, CommandError
from enot_app.tpapi import get_month_bids


class Command(BaseCommand):
    help = 'testing tpapi'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print (get_month_bids())
        pass