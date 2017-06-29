from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core import management

from datetime import datetime
import calendar
from enot.settings import DEBUG

from .models import Bid, Destination, Trip, Subscriber, GCountry, GDirection


# Create your views here.

@login_required
def letter_page(request):

    preset = {'expose': True, 'price__lt': 35000, 'rating__gt': 100}

    g = request.GET
    sort = g.get('sort', 'rating')
    if sort != 'price':
        sort = '-rating'

    preset['price__lt'] = int(g.get('limit', 35000))

    c = g.get('country')
    if c:
        preset['destination__place__gcountry__slug'] = c

    d = g.get('dir')
    if d:
        preset['destination__place__gcountry__gdirection__slug'] = d


    md = g.get('min_distance')
    if md:
        preset['distance__gt'] = int(md)

    md = g.get('max_distance')
    if md:
        preset['distance__lt'] = int(md)

    m = g.get('month')
    if m:
        m = int(m)
        now = datetime.utcnow()
        ldn = calendar.monthrange(now.year,m)[1]
        year = now.year
        if m < now.month:
            year += 1
        fd = datetime(year, m, 1)
        ld = datetime(year, m, ldn)
        preset['departure__gte'] = fd
        preset['departure__lte'] = ld

    dm = g.get('days_min')
    if dm:
        preset['chd_days__gte'] = int(dm)

    dm = g.get('days_max')
    if dm:
        preset['chd_days__lte'] = int(dm)

    d = g.get('direct')
    if d:
        preset['direct'] = True

    n = g.get('new')
    if n:
        preset['new'] = True
    
    trips = Trip.objects.filter(**preset).order_by(sort)  # [:25]
    return render(request, 'enot_app/test_letter.html',  {'trips': trips, 'debug': DEBUG})


def main_page(request):
    return render(request, 'enot_app/main.html',  {})


def unsubscribe(request, hsh):
    try:
        s = Subscriber.objects.get(hsh=hsh)
    except Subscriber.DoesNotExist:
        pass
    else:
        s.delete()
    return render(request, 'enot_app/pricelist.html', {})


def ticket_no(request, no):
    try:
        t = Trip.objects.get(id=no)
    except Trip.DoesNotExist:
        return redirect('enot_app:outdated')
    return redirect(t.tplink)


def outdated(request):
    return render(request, 'enot_app/outdated.html', {})

def checkstring(dts):
    t = datetime.today()
    s = t.strftime('%d%m')
    print (s)
    return True if dts == s else False


@login_required
def build(request, dts):
    if checkstring(dts):
        print('BUILD')
        management.call_command('build')
    return redirect('enot_app:main_page')

@login_required
def mandrill(request, dts):
    pass
    #management.call_command('test_mandrill')


# @ensure_csrf_cookie
# #@cache_page(3600)
# def structured_feed(request):
#     feed_src = {}
#     bids = Bid.get_best_for_each_dest()
#     dirs = GDirection.objects.all()
#     for d in dirs:
#         feed_src[d.slug]={"rus_name": d.rus_name, "countries":{}, "places_count": 0}
#         for c in d.gcountry_set.all():
#             feed_src[d.slug][c.slug]={"rus_name": c.rus_name, "places":[]}

#     for b in bids:
#         feed_src[b['direction'].slug][b['country'].slug]["places"].append(
#             {
#                 "destination": b['dest'],
#                 "price": b['price']
#             }
#         )

#     return JsonResponse({'success':True, 'bids':feed_src}, safe=False)

# def bid_feed(request):
#     bids = list(Bid.objects.all().values()[:50])
#     for b in bids:
#         dd_url = datetime.strftime(b['departure_date'], '%Y-%m-%d')
#         b['departure_date'] = datetime.strftime(b['departure_date'], '%b %d')

#         rd_url = datetime.strftime(b['return_date'], '%Y-%m-%d')
#         b['return_date']= datetime.strftime(b['return_date'], '%b %d')

#         tpurl="http://aviasales.ru/?marker=14721&origin_iata=MOW"
#         b['href']=tpurl+"&destination_iata=%s&depart_date=%s&return_date=%s" % (b['destination_code'],dd_url, rd_url)

#         b['found_at']='none'
#     return JsonResponse({'success':True, 'bids': bids}, safe=False)


# def pricelist(request):
#     return render(request, 'enot_app/pricelist.html', {})


