from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Bid

class Command(BaseCommand):
    help = 'Preloads some newbids from tpapi'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print ("got it!")
        pass