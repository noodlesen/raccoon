from django.core.management.base import BaseCommand, CommandError
from enot_app.mandrill import send_email
from enot_app.models import Trip


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        trips = Trip.objects.filter(expose=True).order_by('-rating')[:12]
        addresses = ['k.lapshov@gmail.com', 'k.lapshov@yandex.ru']
        for addr in addresses:
            send_email(sender="Улётные Билеты<mail@uletbilet.ru>",
                       to=addr,
                       subject="улетные билеты от 18 марта",
                       context={'trips': trips},
                       template='enot_app/test_letter.html')
      