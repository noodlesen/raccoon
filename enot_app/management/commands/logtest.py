from django.core.management.base import BaseCommand, CommandError
import logging
import enot_app.sentinel as sentinel



class Command(BaseCommand):
    help = 'testing tpapi'


    def handle(self, *args, **options):
        
        logger = logging.getLogger('elog')
        logger.info('this is info')
