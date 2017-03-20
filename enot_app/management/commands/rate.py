from django.core.management.base import BaseCommand

from enot_app.models import Trip


class Command(BaseCommand):
    """ Test rate trips"""

    def handle(self, *args, **options):
        trips = Trip.objects.all()
        for t in trips:
            t.review()
        