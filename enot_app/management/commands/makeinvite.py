from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Subscriber, Invite


class Command(BaseCommand):
    help = 'testing tpapi'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        email = input("Enter email: ")
        try:
            sbs = Subscriber.objects.get(email=email)
            print(sbs)
        except:
            print ('Unknown email')
            return()
        print (sbs)
        inv = Invite.create(sbs)
        inv.save()
