import pytz
import json

from operator import itemgetter
from datetime import datetime

from django.core.management.base import BaseCommand

from enot_app.models import Trip, Issue
import enot_app.sentinel as sentinel


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--test',
                            action='store_true',
                            dest='test')

    def handle(self, *args, **options):
        if not options['test']:
            Trip.objects.all().update(expose=False)
            midnight = pytz.utc.localize(datetime.utcnow().replace(hour=0, minute=0))
            Trip.objects.filter(created_at__lt=midnight).update(actual=False)
            trips = Trip.objects.filter(rating__gt=0, actual=True)
            dests = {}
            dest_names = []
            for t in trips:
                if t.destination_name not in dest_names:
                    dest_names.append(t.destination_name)
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
                [{"dest": k, "trip": v, "r": v.rating} for k, v in dests.items()],
                key=itemgetter('r'),
                reverse=True
            )

            trip_list = [d['trip'] for d in dlist]

            if len(trip_list) > 0:

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
                iss.city = city
                iss.number = city.last_issue_number
                iss.name = 'test name'
                iss.save()

                sentinel.inform("build_complete")

            else:
                sentinel.report('No trips...')
        else:
            sentinel.inform("build_complete")



