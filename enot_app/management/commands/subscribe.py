from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Subscriber


class Command(BaseCommand):
    help = 'testing tpapi'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        email = input("Enter subscribers's email: ")
        s = Subscriber.create(email, 'root')
        s.save()