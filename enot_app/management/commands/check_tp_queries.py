from datetime import datetime

import pytz
from django.core.management.base import BaseCommand, CommandError

from enot_app.models import Destination, SpiderQueryTP


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


class Command(BaseCommand):
    help = 'checks if Spiders TPQueries are up to date'

    def handle(self, *args, **options):
        # get origin (Moscow is temp)
        src = Destination.objects.get(code='MOW')

        # get destinations
        dests = Destination.objects.all().exclude(code='MOW')

        # delete obsolete entries
        obs = SpiderQueryTP.objects.filter(expires_at__lt=now).delete()

        # checking and adding queries
        for d in dests:

            try:
                n = SpiderQueryTP.objects.get(start_date=this_month_start, origin=src, destination=d)

            except SpiderQueryTP.DoesNotExist:

                query=SpiderQueryTP(origin=src,
                                    destination=d,
                                    start_date=this_month_start,
                                    requested_at=past,
                                    expires_at=next_month_start)
                query.save()



