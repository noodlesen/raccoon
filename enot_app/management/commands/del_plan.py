from django.core.management.base import BaseCommand
from enot_app.models import Status
from enot_app.planner import make_TP_plan
import enot_app.sentinel as sentinel


class Command(BaseCommand):
    """ Checks if Spiders TPQueries are up to date """


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
        
        if sentinel.allows('to_run_planner', force=options['force']):

            res = make_TP_plan()

            print ('Deleted ', res['deleted'])
            print ('Added ', res['added'])

            sentinel.finish('to_plan')
