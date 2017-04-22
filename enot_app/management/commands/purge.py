from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Bid, Trip

class Command(BaseCommand):

    def handle(self, *args, **options):

        i = input('Are you sure you want to purge all the bids and trips? (y/n)').lower()
        if i=='y':
            Bid.objects.all().delete()
            Trip.objects.all().delete()
