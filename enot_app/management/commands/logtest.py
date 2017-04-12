from django.core.management.base import BaseCommand, CommandError
import logging

from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'testing tpapi'


    def handle(self, *args, **options):
        logger = logging.getLogger('enot_mail')
        logger.error('Hello world')
        print('done')


        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'mail@uletbilet.ru',
        #     ['k.lapshov@gmail.com'],
        #     fail_silently=False,
        # )
