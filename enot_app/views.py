from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from datetime import datetime

from enot.settings import DEBUG

from .models import Bid, Destination, Trip, Subscriber#, GPlace, GCountry, GDirection


# Create your views here.

#@ensure_csrf_cookie
def letter_page(request):
    trips = Trip.objects.filter(expose=True, price__lt=35000, rating__gt=50).order_by('price')[:12]
    return render(request, 'enot_app/test_letter.html',  {'trips': trips, 'debug': DEBUG})

def main_page(request):
    trips = Trip.objects.filter(expose=True, price__lt=35000, rating__gt=50).order_by('price')[:12]
    return render(request, 'enot_app/test_letter.html',  {'trips': trips, 'debug': DEBUG})

def structured_feed(request):
    bids = Bid.get_best()
    return JsonResponse({'success':True, 'bids':bids}, safe=False)

def bid_feed(request):
    bids = list(Bid.objects.all().values()[:50])
    for b in bids:
        dd_url = datetime.strftime(b['departure_date'], '%Y-%m-%d')
        b['departure_date'] = datetime.strftime(b['departure_date'], '%b %d')

        rd_url = datetime.strftime(b['return_date'], '%Y-%m-%d')
        b['return_date']= datetime.strftime(b['return_date'], '%b %d')

        tpurl="http://aviasales.ru/?marker=14721&origin_iata=MOW"
        b['href']=tpurl+"&destination_iata=%s&depart_date=%s&return_date=%s" % (b['destination_code'],dd_url, rd_url)

        b['found_at']='none'
    return JsonResponse({'success':True, 'bids': bids}, safe=False)

def pricelist(request):
    return render(request, 'enot_app/pricelist.html', {})

def unsubscribe(request, hsh):
    try:
        s = Subscriber.objects.get(hsh=hsh)
    except Subscriber.DoesNotExist:
        pass
    else:
        s.delete()
    return render(request, 'enot_app/pricelist.html', {})
