from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from datetime import datetime

from .models import Bid, Destination, Trip#, GPlace, GCountry, GDirection


# Create your views here.

@ensure_csrf_cookie
def main_page(request):
    trips = Trip.objects.filter(expose=True).order_by('-rating')
    return render(request, 'enot_app/test_letter.html',  {'trips': trips})

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
