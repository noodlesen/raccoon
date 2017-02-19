from django.shortcuts import render
from django.http import JsonResponse

from datetime import datetime

from .models import Bid


# Create your views here.


def main_page(request):
    return render(request, 'enot_app/main_page.html', {})

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
