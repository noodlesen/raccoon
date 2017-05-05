from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from enot_app.toolbox import get_hash
from enot_app.models import Trip

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        trips = Trip.objects.all()
        for t in trips:
            t.slug = get_hash(str(t.id))
            t.save()