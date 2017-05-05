from django.core.management.base import BaseCommand, CommandError
from enot_app.mandrill import send_email
from enot_app.models import Trip


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        trips = Trip.objects.filter(expose=True, price__lt=35000).order_by('price')[:15]
        addresses = ['k.lapshov@gmail.com']
        places = [t.destination_name+': '+str(t.price) for t in trips][:6]
        subj = (', '.join(places)+'...').title()
        for addr in addresses:
            print (subj)
            send_email(sender="Улётные Билеты<mail@uletbilet.ru>",
                       to=addr,
                       subject=subj,
                       context={'trips': trips},
                       template='enot_app/test_letter.html')
      