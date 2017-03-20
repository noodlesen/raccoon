#delete

from django.core.management.base import BaseCommand, CommandError
from enot_app.models import Subscriber, Airline
from fuzzywuzzy import fuzz


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        with open('al_rating.txt','r') as f:
            not_found=[]
            lines = f.read().split('\n')
            for l in lines:
                s = l.split(' ')
                n1 = s[0]
                n2 = s[-1]
                name = ' '.join(s[1:-1]).strip()
                
                r = 155-int( int(n1)+int(n2)/2 )
                print (name, r)
            #     try:
            #         a = Airline.objects.get(name=name)
            #     except Airline.DoesNotExist:
            #         not_found.append(name)
            #     else:
            #         a.rating = r
            #         a.save()

            # nrobj = Airline.objects.filter(rating=None)
            # nr = [o.name for o in nrobj]
            
            # print(not_found)
            # for n in not_found:
            #     for r in nr:
            #         f = fuzz.ratio(n,r)
            #         if f > 70:
            #             print (n,'-',r, f)


