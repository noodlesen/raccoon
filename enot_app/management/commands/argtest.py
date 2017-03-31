from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Subscriber


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            action='store_true',
                            dest='force',
                            default=False)

        parser.add_argument('--force',
                            action='store_true',
                            dest='force',
                            default=False)

    def handle(self, *args, **options):
        print(options['force'])