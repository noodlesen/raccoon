import json
from datetime import datetime
from enot_app.models import Carrier, Aircraft

Z1 = 1200
Z2 = 2100
Z3 = 4000
Z4 = 8000


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

    if bid.price<15000:
        rt*=1.5

    return rt


def review(trip):

    print (trip.id)
    print (str(trip.days_to))
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
        benefits.append({
            'kind': 'originDepartTime',
            'message': 'Удобное время вылета из Москвы',
            'show': False
        })
        rtc += 50

    if trip.arrival.hour in range(8, 21):
        benefits.append({
            'kind': 'returnArrivalTime',
            'message': 'Удобное время возвращения в Москву',
            'show': False
        })
        rtc += 20

    ### Destination arrival time

    dats = slices[0]['segments'][-1]['legs'][-1]['arrival']
    dat = datetime.strptime(dats.replace(':', ''), '%Y-%m-%dT%H%M%z')
    if dat.hour in range(10, 21):
        benefits.append({
            'kind': 'destinationArrivalTime',
            'message': 'Удобное время прибытия в пункт назначения',
            'show': False
        })
        rtc += 50

    ### Destination departure time

    ddts = slices[-1]['segments'][0]['legs'][0]['departure']
    ddt = datetime.strptime(ddts.replace(':', ''), '%Y-%m-%dT%H%M%z')
    if ddt.hour > 10:
        benefits.append({
            'kind': 'destinationDepartureTime',
            'message': 'Удобное время вылета обратно',
            'show': False
        })
        rtc += 20

    ### Number of stops

    """ total number of stops """
    tns = slices[0]['slice_stops']+slices[1]['slice_stops']
    if tns == 0:
        benefits.append({
            'kind': 'directFlight',
            'message': 'Прямые рейсы в обе стороны',
            'show': True
        })
        rtc += 300
    elif tns == 1:
        benefits.append({
            'kind': 'semiDirectFlight',
            'message': 'Прямой рейс в одну сторону',
            'show': True
        })
        rtc += 100
    elif tns > 2:
        penalties.append({
            'kind': 'moreThanTwoStops',
            'message': 'Много стыковок',
            'show': True
        })
        rtc -= 250

    ### Stops duration and aircrafts

    for sln in range(0, 2):
        sldr = ['туда', 'обратно']
        drs = sldr[sln]
        times = []

        for sg in slices[sln]['segments']:
            for l in sg['legs']:
                times.append(l['departure'])
                times.append(l['arrival'])

                acr = Aircraft.objects.get(name=l['aircraft']).rating
                if acr >= 150:
                    benefits.append({
                        'kind': 'ratedAircraft',
                        'message': 'Хороший самолёт %s: %s' %(drs, l['aircraft']),
                        'show': True
                    })
                rtc += acr


        if len(times) > 2:
            for n in range(1, len(times)-1, 2):
                t1 = datetime.strptime(times[n+1].replace(':', ''), '%Y-%m-%dT%H%M%z')
                t0 = datetime.strptime(times[n].replace(':', ''), '%Y-%m-%dT%H%M%z')
                st = (t1-t0).seconds
                fst = '%dч%dм' % (int(st / 3600), int(st % 3600 / 60))
                if st<4000:
                    penalties.append({
                        'kind': 'veryShortStop',
                        'message': 'Очень короткая стыковка %s: %s' %(drs, fst),
                        'show': True
                    })
                    rtc -= 100
                elif st>3600*5:
                    penalties.append({
                        'kind': 'veryLongStop',
                        'message': 'Очень длинная стыковка %s: %s' %(drs, fst),
                        'show': True
                    })
                    rtc -= 200

    ### Carriers

    carriers = set(trip.carriers.split(', '))

    lc = len(carriers)
    pen = 150*(lc-1)
    rtc -= pen
    if lc > 1:
        penalties.append({
            'kind': 'differentCarriers',
            'message': 'Несколько авиакомпаний',
            'show': True
        })

    cn = []
    for c in carriers:
        try:
            co = Carrier.objects.get(iata=c)
        except Carrier.DoesNotExist:
            rtc -= 100
            penalties.append({
                'kind': 'unknownCarrier',
                'message': 'Неизвестная авиакомпания'
            })
        else:
            cor = co.rating
            cn.append(co.name)
            rtc += cor*2
            if cor > 50:
                benefits.append({
                    'kind': 'ratedCarrier',
                    'message': 'Хорошая авиакомпания: %s' % co.name,
                    'show': True
                })


    rtc = 0 if rtc < 0 else rtc
    rtp = 0 if rtp < 0 else rtp

    rt = int(rtc*rtp/1000) if eff >= 100 else 0

    if len(penalties) == 0:
        rt+=50
    else:
        rt-=50




    return({
        'benefits': benefits,
        'penalties': penalties,
        'rt_comfort': rtc,
        'rt_price': rtp,
        'rt_eff': eff,
        'rt': rt,
        'carriers':cn
    })
    
