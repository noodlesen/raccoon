import json
from datetime import datetime
from enot_app.models import Carrier, Aircraft, Airport
from enot.settings import TRAVEL_PAYOUTS_MARKER

from .toolbox import russian_plurals, now_in_moscow

Z1 = 1200
Z2 = 2100
Z3 = 4000
Z4 = 8000


def parse_qpx_datetime(qdt):
    return datetime.strptime(qdt.replace(':', ''), '%Y-%m-%dT%H%M%z')

def days_to_distance(days, dist):
    rt = 0

    if dist > Z1 and dist <= Z2:
        rt += 100
    if dist > Z2 and dist <= Z3:
        rt += 300
        if days > 21:
            rt -= 200
    if dist > Z3 and dist <= Z4:
        rt += 200
        if days > 40 or days < 7:
            rt -= 200
    if dist > Z4:
        rt += 100
        if days > 60 or days < 14:
            rt -= 200

    return rt


def prerate(bid):
    """ Evaluate pre-rating of the bid
    :prop bid: Bid object
    return pre-rating number
    """
    rt = 0
    dist = bid.distance
    days = (bid.return_date-bid.departure_date).days

    # days to distance
    rt = days_to_distance(days, dist)

    # price to distance
    eff = int(dist/bid.price*3000)
    rt += eff

    # penalty for shorties
    if days < 4:
        rt -= 300

    # penalty for longs
    if days > 31:
        rt -= 300

    # check weekdays
    wd = bid.departure_date.weekday()
    if wd == 3:
        rt += 50
    elif wd == 4 or wd == 5:
        rt += 100

    # check stops
    rt = rt-bid.stops*100

    # check average price
    ap = bid.destination.average_price
    rt = rt + int((ap-bid.price)/ap*1000)

    if bid.price < 15000:
        rt *= 1.5

    return rt


################################################

class Note:
    def __init__(self):
        self.benefits = []
        self.penalties = []
        self.messages = []

    def append_benefit(self, b):
        if b['message'] not in self.messages:
            self.benefits.append(b)
            self.messages.append(b['message'])

    def append_penalty(self, p):
        if p['message'] not in self.messages:
            self.penalties.append(p)
            self.messages.append(p['message'])


def review(trip):

    note = Note()

    benefits = []
    penalties = []
    rtc = 0  # comfort rating
    rtp = 0  # price rating


    ###
    ### Price factors
    ###

    eff = int(trip.distance/trip.price*1000)
    rtp1 = int(eff*1.5)
    rtp2 = int((trip.average_price-trip.price*0.8)/trip.average_price*500)
    rtp += rtp1 + rtp2

    ###
    ### Comfort factors 
    ###

    slices = trip.get_slices()

    rtc += days_to_distance(trip.chd_days, trip.distance)

    if trip.departure.hour >= 12:
        note.append_benefit({
            'kind': 'originDepartTime',
            'message': 'Удобное время вылета из Москвы',
            'show': False
        })
        rtc += 50

    if trip.arrival.hour in range(8, 21):
        note.append_benefit({
            'kind': 'returnArrivalTime',
            'message': 'Удобное время возвращения в Москву',
            'show': False
        })
        rtc += 20

    ### Destination arrival time

    dats = slices[0]['segments'][-1]['legs'][-1]['arrival']
    dat = datetime.strptime(dats.replace(':', ''), '%Y-%m-%dT%H%M%z')
    if dat.hour in range(10, 21):
        note.append_benefit({
            'kind': 'destinationArrivalTime',
            'message': 'Удобное время прибытия в пункт назначения',
            'show': False
        })
        rtc += 50

    ### Destination departure time

    ddts = slices[-1]['segments'][0]['legs'][0]['departure']
    ddt = datetime.strptime(ddts.replace(':', ''), '%Y-%m-%dT%H%M%z')
    if ddt.hour > 10:
        note.append_benefit({
            'kind': 'destinationDepartureTime',
            'message': 'Удобное время вылета обратно',
            'show': False
        })
        rtc += 20

    ### Number of stops

    """ total number of stops """
    tns = slices[0]['slice_stops']+slices[1]['slice_stops']
    if tns == 0:
        note.append_benefit({
            'kind': 'directFlight',
            'message': 'Прямые рейсы в обе стороны',
            'show': True
        })
        rtc += 300
    elif tns == 1:
        note.append_benefit({
            'kind': 'semiDirectFlight',
            'message': 'Прямой рейс в одну сторону',
            'show': True
        })
        rtc += 100
    elif tns > 2:
        note.append_penalty({
            'kind': 'moreThanTwoStops',
            'message': 'Много стыковок',
            'show': True
        })
        rtc -= 250

    ### Stops duration and aircrafts

    details = [{}, {}]
    sldr = ['туда', 'обратно']
    all_carriers = []

    for sln in range(0, 2):  # browse slices
        drs = sldr[sln]
        details[sln]['name'] = drs
        details[sln]['layovers'] = []
        #times = []

        all_legs = []

        for sg in slices[sln]['segments']:  # browse segments

            for l in sg['legs']:
                l['carrier'] = sg['carrier']  # marking legs with the carrier's code

                """ Parsing time format """
                l['departure'] = parse_qpx_datetime(l['departure'])
                l['arrival'] = parse_qpx_datetime(l['arrival'])

            all_legs.extend(sg['legs'])  # getting rid of segments

        legs_count = len(all_legs)
        hd_legs = []

        for ln in range(0, legs_count):  # browse all slice's legs

            this_leg = {}

            # checking aircraft
            acr = Aircraft.objects.get(name=l['aircraft']).rating
            if acr >= 150:
                note.append_benefit({
                    'kind': 'ratedAircraft',
                    'message': 'Хороший самолёт %s: %s' % (drs, l['aircraft']),
                    'show': True
                })
            rtc += acr
            this_leg['aircraft'] = l['aircraft']
            

            try:
                co = Carrier.objects.get(iata=l['carrier'])
            except Carrier.DoesNotExist:
                rtc -= 100
                note.append_penalty({
                    'kind': 'unknownCarrier',
                    'message': 'Неизвестная авиакомпания',
                    'show': False
                })
                cname = 'Неизвестно'
            else:
                cor = co.rating
                rtc += cor*2
                if cor > 50:
                    note.append_benefit({
                        'kind': 'ratedCarrier',
                        'message': 'Хорошая авиакомпания: %s' % co.name,
                        'show': True
                    })
                cname = co.name

            this_carrier = {'code': l['carrier'], 'name': cname}
            this_leg['carrier'] = this_carrier
            all_carriers.append(this_carrier)

            this_leg['origin_code'] = l['origin']
            this_leg['destination_code'] = l['destination']

            ### DRY VVV
            try:
                ap = Airport.objects.get(iata=l['origin'])
            except Airport.DoesNotExist:
                pass
            else:
                if ap.place:
                    city = ap.place.rus_name
                else:
                    city = ap.city
                this_leg['origin'] = { 'airport': ap.name, 'city': city }

            try:
                ap = Airport.objects.get(iata=l['destination'])
            except Airport.DoesNotExist:
                pass
            else:
                if ap.place:
                    city = ap.place.rus_name
                else:
                    city = ap.city
                this_leg['destination'] = { 'airport': ap.name, 'city': city }



            if legs_count > 1:  # if this slice have stops 

                if ln < legs_count-1:  # and this leg isn't the last one

                    t1 = all_legs[ln+1]['departure']
                    t0 = all_legs[ln]['arrival']
                    st = (t1-t0).seconds
                    fst = '%dч%dм' % (int(st / 3600), int(st % 3600 / 60))

                    this_leg['stop_time'] = st
                    this_leg['text_stop_time'] = fst

                    details[sln]['layovers'].append({
                        'city': this_leg['destination']['city'],
                        'stop_time': st,
                        'text_stop_time': fst
                    })

                    if st < 4000:
                        note.append_penalty({
                            'kind': 'veryShortStop',
                            'message': 'Очень короткая стыковка %s: %s' % (drs, fst),
                            'show': True
                        })
                        rtc -= 100
                    elif st > 3600 * 5:
                        note.append_penalty({
                            'kind': 'veryLongStop',
                            'message': 'Очень длинная стыковка %s: %s' % (drs, fst),
                            'show': True
                        })
                        rtc -= 200

            hd_legs.append(this_leg)

        details[sln]['legs'] = hd_legs

    ### Carriers number

    carriers_list = set([c['name'] for c in all_carriers])
    carriers = []
    carriers = [c for c in carriers_list if c not in carriers]
    carriers_text = ', '.join(carriers)

    lc = len(carriers)
    pen = 150*(lc-1)
    rtc -= pen
    if lc > 1:
        note.append_penalty({
            'kind': 'differentCarriers',
            'message': 'Несколько авиакомпаний',
            'show': True
        })



    rtc = 0 if rtc < 0 else rtc
    rtp = 0 if rtp < 0 else rtp

    rt = int(rtc*rtp/1000) if eff >= 100 else 0

    if len(penalties) == 0:
        rt += 50
    else:
        rt -= 50

    days_text = str(trip.chd_days)+" "+russian_plurals('день', trip.chd_days)
    days_to = (trip.departure-now_in_moscow()).days
    if days_to <= 0:
        days_to = 0
        trip.actual = False
        trip.expose = False
        trip.save()
    days_to_text = "через "+str(days_to)+" "+russian_plurals('день', days_to)

    ddate_url = datetime.strftime(trip.departure, '%Y-%m-%d')
    adate_url = datetime.strftime(trip.arrival, '%Y-%m-%d')

    tplink = "http://www.aviasales.ru/?marker=%d" % TRAVEL_PAYOUTS_MARKER
    tplink += "&origin_iata=%s&destination_iata=%s&depart_date=%s&return_date=%s" % (
        trip.origin_city.code, trip.destination_code, ddate_url, adate_url
    )

    #print (tplink, len(tplink))

    return({
        'rt_comfort': rtc,
        'rt_price': rtp,
        'rt_eff': eff,
        'rt': rt,
        'tplink': tplink,
        'hd': {
            'benefits': note.benefits,
            'penalties': note.penalties,
            'carriers': carriers_text,
            'details': details,
            'days_text': days_text,
            'days_to': days_to,
            'days_to_text': days_to_text
        }
    })
    
