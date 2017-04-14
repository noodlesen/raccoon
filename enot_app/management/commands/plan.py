from datetime import datetime, timedelta

import pytz
from django.core.management.base import BaseCommand, CommandError

from enot_app.models import Destination, SpiderQueryTP, Status
#from enot_app.common import get_current_std


def plus_month(dt, n):
    sm = dt.month+n
    if sm > 12:
        nm = sm % 12
        ny = dt.year+1+floor(n/12)
        return dt.replace(month = nm, year = ny)
    else:
        return dt.replace(month = sm)

tz = pytz.timezone('Europe/Moscow')
now = datetime.now(tz)
past = tz.localize(datetime(1979,6,30,9,30,0))
never = tz.localize(datetime(2979,6,30,9,30,0))
this_month_start = now.replace(day=1).date()
this_month = this_month_start.month
next_month_start = plus_month(this_month_start,1)
after_next_month_start = plus_month(this_month_start,2)
months = [this_month_start, next_month_start, after_next_month_start]



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

                    ####

                    # get origin (Moscow is temp)
                    src = Destination.objects.get(code='MOW')

                    # get destinations
                    dests = Destination.objects.filter(enabled=True).exclude(code='MOW')

                    # delete obsolete entries
                    obs = SpiderQueryTP.objects.filter(expires_at__lte=now).delete()

                    # checking and adding queries
                    for d in dests:

                        for m in months:
                            try:
                                SpiderQueryTP.objects.get(
                                    start_date=m,
                                    origin=src,
                                    destination=d
                                )

                            except SpiderQueryTP.DoesNotExist:

                                exp_date = plus_month(m,1) - timedelta(days=1)

                                query=SpiderQueryTP(origin=src,
                                                    destination=d,
                                                    start_date=m,
                                                    requested_at=past,
                                                    expires_at=exp_date,
                                                    priority=1)
                                query.save()

                    ####
                    
                    std.planner_finished = True
                    std.save()
                else:
                    print ('planner has not finished ok yesterday')
            else:
                print ('planner has already stared today')



