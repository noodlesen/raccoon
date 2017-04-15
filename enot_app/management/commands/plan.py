from django.core.management.base import BaseCommand
from enot_app.models import Status
from enot_app.planner import make_TP_plan


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

        isForced = options['force']
        
        syd = Status.get_yesterday(isForced)
        std = Status.get_today()

        if syd is not False or isForced:

            if not std.planner_started or isForced:
                if syd.planner_finished or isForced:
                    
                    std.planner_started = True
                    std.save()

                    res = make_TP_plan()

                    print ('Deleted ', res['deleted'])
                    print ('Added ', res['added'])

                    std.planner_finished = True
                    std.save()
                else:
                    print ('planner has not finished ok yesterday')
            else:
                print ('planner has already stared today')



