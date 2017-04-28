from django.core.management.base import BaseCommand

from operator import itemgetter
from datetime import datetime

from enot_app.models import Trip, Status, Issue
import pytz
import json


class Command(BaseCommand):
    """ Force pre-rating on bids """

    def handle(self, *args, **options):
        Trip.objects.all().update(expose=False)
        midnight = pytz.utc.localize(datetime.utcnow().replace(hour=0, minute=0))
        print ('>>>>>>', midnight)
        Trip.objects.filter(created_at__lt=midnight).update(actual=False, expose=False) # remove?
        trips = Trip.objects.filter(rating__gt=0, actual=True)
        dests = {}
        for t in trips:
            if t.destination_code not in dests.keys():
                dests[t.destination_code] = t
            else:
                r = dests[t.destination_code].rating
                if t.rating > r:
                    dests[t.destination_code] = t
                elif t.rating == r:
                    if t.price > dests[t.destination_code].price:
                        dests[t.destination_code] = t

        dlist = sorted(
            [{"dest": k, "trip": v, "r": v.rating} for k,v in dests.items()],
            key=itemgetter('r'),
            reverse=True
        )


        trip_list = [d['trip'] for d in dlist]

        stop_list = []
        build = []

        for t in trip_list:
            t.expose = True
            t.save()
            b = '%s->%s :%d | %d' % (
                t.origin_code,
                t.destination_code,
                t.price,
                t.rating
            )
            build.append(b)
            stop_list.append(t.destination_code)

        iss = Issue()
        iss.build = json.dumps(build)
        iss.stop_list = json.dumps(stop_list)
        city = trip_list[0].origin_city
        city.last_issue_number += 1
        city.save()
        iss.city=city
        iss.number = city.last_issue_number
        iss.name = 'test name'
        iss.save()

        # st = Status.get_today()
        # st.build = json.dumps(build)
        # st.save()


