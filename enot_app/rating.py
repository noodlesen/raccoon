import json
from datetime import datetime

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
    rt += int(dist/bid.price*1000)

    # penalty for shorties
    if days < 3:
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

    return rt


def review(trip):
    benefits = []
    penalties = []
    rtc = 0  # comfort rating
    rtp = 0  # price rating

    slices = trip.get_slices()

    if trip.departure.hour >= 12:
        benefits.append({
            'kind': 'originDepartTime',
            'message': 'Удобное время вылета из Москвы'
        })
        rtc += 100

    if trip.arrival.hour in range(8, 21):
        benefits.append({
            'kind': 'returnArrivalTime',
            'message': 'Удобное время возвращения в Москву'
        })
        rtc += 30

    ### Destination arrival time

    dats = slices[0]['segments'][-1]['legs'][-1]['arrival']
    dat = datetime.strptime(dats.replace(':', ''), '%Y-%m-%dT%H%M%z')
    if dat.hour in range(10, 21):
        benefits.append({
            'kind': 'destinationArrivalTime',
            'message': 'Удобное время прибытия в пункт назначения'
        })
        rtc += 100

    ### Destination departure time

    ddts = slices[-1]['segments'][0]['legs'][0]['departure']
    ddt = datetime.strptime(ddts.replace(':', ''), '%Y-%m-%dT%H%M%z')
    if ddt.hour > 10:
        benefits.append({
            'kind': 'destinationDepartureTime',
            'message': 'Удобное время вылета обратно'
        })
        rtc += 50

    ### Number of stops

    """ total number of stops """
    tns = slices[0]['slice_stops']+slices[1]['slice_stops']
    if tns == 0:
        benefits.append({
            'kind': 'directFlight',
            'message': 'Прямые рейсы в обе стороны'
        })
        rtc += 200
    elif tns == 1:
        benefits.append({
            'kind': 'semiDirectFlight',
            'message': 'Прямой рейс в одну сторону'
        })
        rtc += 100
    elif tns > 2:
        penalties.append({
            'kind': 'moreThanTwoStops',
            'message': 'Много стыковок'
        })
        rtc -= 200

    ### Stops duration

    for sln in range(0, 2):
        times = []

        for sg in slices[sln]['segments']:
            for l in sg['legs']:
                times.append(l['departure'])
                times.append(l['arrival'])

        print (times)

        if len(times) > 2:
            for n in range(1, len(times)-1, 2):
                t1 = datetime.strptime(times[n+1].replace(':', ''), '%Y-%m-%dT%H%M%z')
                t0 = datetime.strptime(times[n].replace(':', ''), '%Y-%m-%dT%H%M%z')
                st = (t1-t0).seconds
                print(int(st / 3600), int(st % 3600 / 60))
                if st<4000:
                    penalties.append({
                        'kind': 'veryShortStop',
                        'message': 'Очень короткая стыковка'
                    })
                    rtc -= 100
                elif st>3600*5:
                    penalties.append({
                        'kind': 'veryLongStop',
                        'message': 'Очень длинная стыковка'
                    })
                    rtc -= 200
        




    return({
        'benefits': benefits,#json.dumps(benefits),
        'penalties': penalties,#json.dumps(penalties),
        'rt_comfort': rtc,
        'rt_price': rtp
    })
