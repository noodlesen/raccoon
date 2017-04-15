
from datetime import datetime, timedelta

from enot_app.models import Destination, SpiderQueryTP

import pytz

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

def make_TP_plan():
     # get origin (Moscow is temp)
    src = Destination.objects.get(code='MOW')

    # get destinations
    dests = Destination.objects.filter(enabled=True).exclude(code='MOW')

    # delete obsolete entries
    obs = SpiderQueryTP.objects.filter(expires_at__lte=now).delete()

    deleted = obs[0]

    added = 0
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
                added += 1

    return ({'deleted': deleted, 'added': added})