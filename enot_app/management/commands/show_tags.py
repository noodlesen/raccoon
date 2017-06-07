# import pytz
import json

# from operator import itemgetter
# from datetime import datetime

from enot_app.toolbox import get_russian_form


from enot_app.models import Quote, Tag


from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('--word',
                            action='store',
                            type=str,
                            default='',
                            dest='word')

    def handle(self, *args, **options):
        qs = Quote.objects.all()
        for q in qs:
            print()
            print(q.text)
            tags = json.loads(q.chd_data)['tags']
            for t in tags:
                print (t['id'], t['name'])
                tag = Tag.objects.get(id=t['id'])
                q.tags.add(tag)

