""" Python client to use for requesting Google's QPX Express API. """
from __future__ import unicode_literals, absolute_import, generators, \
    print_function

import requests
import json
import re
from datetime import datetime

from enot_app.models import Aircraft


class QPXExpressApi(object):
    """ QPX Express API """

    def __init__(self, api_key=None):
        """ API Contrstructor
        :param api_key: Google API Key
        """
        self.api_key = api_key
        self.request_count = 0
        self.request_url = 'https://www.googleapis.com/qpxExpress/' + \
            'v1/trips/search?key={}'.format(api_key)

    def search(self, request):
        """ Search the API
        :param request: QPXRequest object

        returns QPXResponse object
        """
        headers = {'content-type': 'application/json'}
        resp = requests.post(self.request_url, data=request.get_json(),
                             headers=headers)
        #print (resp.json())
        self.request_count += 1
        return QPXResponse(resp.json())

    def estimate_api_costs(self):
        """ Estimate API costs based on current count. """
        return '${.2f}'.format((lambda x: x if x > 0 else 0)(
            (self.request_count - 50) * .035))


class QPXRequest(object):
    """ QPX Request formatter. """
    def __init__(self, origin, destination, date, num_adults, return_date=None):
        """ Create request object.
        :param origin: origin airport or IATA code
        :param destination: destination airport or IATA code
        :param date: datetime object
        :param num_adults: integer representing the number of adults
        :kwarg return_date: datetime object
        """
        self.origin = origin
        self.destination = destination
        self.date = date
        self.return_date = return_date
        self.num_adults = num_adults
        self.passengers = {
            'kind': 'qpxexpress#passengerCounts',
            'adultCount': num_adults,
        }
        self.slices = [{
            'kind': 'qpxexpress#sliceInput',
            'origin': origin,
            'destination': destination,
            'date': date.strftime('%Y-%m-%d')
        }]
        if return_date:
            self.slices.append({
                'kind': 'qpxexpress#sliceInput',
                'origin': destination,
                'destination': origin,
                'date': return_date.strftime('%Y-%m-%d')
            })

    def add_passengers(self, num_child, num_senior=0, num_inf_lap=0,
                       num_inf_seat=0):
        """ Add passengers to your request.
        :param num_child: integer representing number of children
        :kwarg num_senior: integer representing number of seniors
        :kwarg num_inf_lap: integer representing number of infants in lap
        :kwarg num_inf_seat: integer representing number of infants in seats
        """
        self.passengers['childCount'] = int(num_child)
        self.passengers['seniorCount'] = int(num_senior)
        self.passengers['infantInLapCount'] = int(num_inf_lap)
        self.passengers['infantInSeatCount'] = int(num_inf_seat)

    def get_json(self):
        """ Returns json representation to send to the API."""
        json_format = {'request': {}}
        json_format['request']['passengers'] = self.passengers
        json_format['request']['slice'] = self.slices
        json_format['request']['refundable'] = False
        return json.dumps(json_format)


class QPXResponse(object):
    """ QPX Response object. """
    def __init__(self, json_resp):
        self.raw_data = json_resp
        self.trip_options = json_resp.get('trips').get('tripOption')
        self.aircrafts = {}
        aircrafts = json_resp.get('trips').get('data').get('aircraft')
        if aircrafts:
            for aircraft in aircrafts:
                self.aircrafts[aircraft['code']] = aircraft['name']

    def sort_by_base_price(self):
        """ Sort all trips by base price, putting lowest first. """
        self.trip_options = sorted(self.trip_options,
                                     key=lambda x: float(re.search(
                                         r'\d+', x[
                                             'pricing'][0]['baseFareTotal']
                                     ).group(0)))

    def sort_by_total_price(self):
        """ Sort all trips by total price, putting lowest first. """
        self.trip_options = sorted(self.trip_options,
                                     key=lambda x: float(re.search(
                                         r'\d+', x['saleTotal']).group(0)))

    def sort_by_duration(self):
        """ Sort all trips by duration, putting shortest first. """
        self.trip_options = sorted(self.trip_options, key=lambda x:
                                     x['slice'][0]['duration'])

    def top_trips(self, num=10, sort='price'):
        """ Return a smaller (more readable) dictionary of top cheapest trips.
        :kwargs num: integer of how many to show (default: 10)
        :kwargs sort: 'price' or 'duration' sort method (default: 'price')

        returns sorted list with some (but not all) details for easy reading
        """
        if not self.trip_options:
            print('failed')
            return []
        if sort == 'price':
            self.sort_by_total_price()
        elif sort == 'duration':
            self.sort_by_duration()
        top_trips = []
        for trip in self.trip_options[:num]:
            sale = trip.get('saleTotal')

            ts = trip['slice']
            dts = ts[0]['segment'][0]['leg'][0]['departureTime']
            dts = dts.replace(':','')
            dt = datetime.strptime(dts,'%Y-%m-%dT%H%M%z')
            ats = ts[-1]['segment'][-1]['leg'][0]['arrivalTime']
            ats = ats.replace(':','')
            at = datetime.strptime(ats,'%Y-%m-%dT%H%M%z')
            trip_info = {'price': re.search(r'[\d.]+', sale).group(),
                         'currency': re.search(r'[^\d.]+', sale).group(),
                         'trip_departure': dt,
                         'trip_arrival': at,
                         'slices': [],
                         'carriers': []}

            for _slice in trip['slice']:
                segments = []
                for segment in _slice['segment']:
                    legs = []
                    trip_info['carriers'].append(segment['flight']['carrier'])
                    for leg in segment['leg']:
                        legs.append({
                            'type': 'leg',
                            'origin': leg['origin'],
                            'departure': leg['departureTime'],
                            'arrival': leg['arrivalTime'],
                            'destination': leg['destination'],
                            'aircraft': self.aircrafts[leg['aircraft']]
                        })
                        Aircraft.spot(self.aircrafts[leg['aircraft']])  # For stats
                    segments.append({
                        'type': 'segment',
                        'carrier': segment['flight']['carrier'],
                        'legs': legs,
                        'segment_stops': len(legs)-1
                    })

                slice_stops = sum([s['segment_stops'] for s in segments])
                slice_stops += len(segments)-1
                trip_info['slices'].append({
                    'type': 'slice',
                    'segments': segments,
                    'slice_stops': slice_stops
                })

                trip_info['origin']=trip_info['slices'][0]['segments'][0]['legs'][0]['origin']
                trip_info['destination']=trip_info['slices'][0]['segments'][-1]['legs'][-1]['destination']
                trip_info['return']=trip_info['slices'][-1]['segments'][-1]['legs'][-1]['destination']


            top_trips.append(trip_info)
        return top_trips
