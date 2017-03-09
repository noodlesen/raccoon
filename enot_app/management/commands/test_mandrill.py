from django.core.management.base import BaseCommand, CommandError
from enot_app.mandrill import send_email


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        send_email(sender="mail@uletbilet.ru",
                   to="k.lapshov@gmail.com",
                   subject="this is subject",
                   context={},
                   template='enot_app/test_letter.html')
        pass