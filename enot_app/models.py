import json
from datetime import datetime, timedelta
from pytz import timezone
from django.db import models, connection
from .toolbox import dictfetchall, get_hash

# Create your models here.


class GDirection(models.Model):
    eng_name = models.CharField(max_length=50)
    rus_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)


class GCountry(models.Model):
    code = models.CharField(max_length=2)
    eng_name = models.CharField(max_length=50)
    gdirection = models.ForeignKey(GDirection)
    rus_name = models.CharField(max_length=50)
    kdb_id = models.IntegerField()  # -
    slug = models.SlugField(max_length=50)


class GPlace(models.Model):
    eng_name = models.CharField(max_length=50)
    rus_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    eng_address = models.TextField()
    rus_address = models.TextField()
    b_number = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    gcountry = models.ForeignKey(GCountry)  # !!!
    UFI = models.IntegerField()
    types = models.CharField(max_length=100)
    google_place_id = models.CharField(max_length=50)
    image = models.CharField(max_length=50)  # ?
    fpid = models.IntegerField()  # -
    dup = models.IntegerField()  # -
    chd_airports = models.TextField()
    city_code = models.CharField(max_length=3)


class Destination(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    tmp_country = models.CharField(max_length=50)
    score = models.IntegerField()
    place = models.ForeignKey(GPlace)
    total_bid_count = models.IntegerField()
    average_price = models.IntegerField()
    enabled = models.BooleanField(default=True)

    @classmethod
    def get_structured(cls):
        cursor = connection.cursor()
        query = """
                SELECT ds.name, ds.code, p.slug as pslug, c.rus_name as cslug, c.id as cid, c.slug as cslug, d.rus_name as drn, d.id as did, d.slug as dslug
                FROM `enot_app_destination` as ds
                JOIN `enot_app_gplace` as p ON p.id = ds.place_id
                JOIN `enot_app_gcountry` as c ON c.id = p.gcountry_id
                JOIN `enot_app_gdirection` as d ON d.id = c.gdirection_id
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)

        res={}

        for r in rows:
            rd = {"name": r['name'], "code": r['code'], "slug": r['pslug']}

            if r['dslug'] in res.keys():
                if r['cslug'] in res[r['dslug']].keys():
                    res[r['dslug']] [r['cslug']] ['places'].append(rd)
                else:
                    res[r['dslug']] [r['cslug']]={"places": [rd] }
            else:
                res[r['dslug']]={}
                res[r['dslug']][r['cslug']]={"places": [rd] }


        return res


class Airport(models.Model):
    name = models.CharField(max_length=50, null=True)
    size = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    iata = models.CharField(max_length=3, null=True)
    city = models.CharField(max_length=50, null=True)
    city_code = models.CharField(max_length=3, null=True)
    country_code = models.CharField(max_length=2, null=True)
    country = models.CharField(max_length=50, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    alt = models.IntegerField(null=True)
    icao = models.CharField(max_length=4, null=True)
    timezone = models.IntegerField(null=True)
    dst = models.CharField(max_length=1, null=True)
    tzdata = models.CharField(max_length=50, null=True)




class SpiderQueryTP(models.Model):
    origin = models.ForeignKey(Destination, related_name='tpr_origin')
    destination = models.ForeignKey(Destination,
                                    related_name='tpr_destination'
                                    )
    start_date = models.DateField()
    requested_at = models.DateTimeField(default=datetime(1979,6,30,9,30,0,0,
                                        timezone('Europe/Moscow'))
                                        )
    expires_at = models.DateField()
    priority = models.IntegerField(default=0)


class Bid(models.Model):
    origin_code = models.CharField(max_length=3)
    origin = models.ForeignKey(Destination,
                               default=1,
                               related_name='bid_origin'
    )
    destination_code = models.CharField(max_length=3)
    destination = models.ForeignKey(Destination, 
                                    default=1,
                                    related_name='bid_destination'
    )
    destination_name = models.CharField(max_length=35)
    one_way = models.BooleanField()
    departure_date = models.DateField()
    return_date = models.DateField()
    price = models.IntegerField()
    stops = models.IntegerField()
    trip_class = models.IntegerField()
    distance = models.IntegerField()
    to_expose = models.BooleanField()
    found_at = models.DateTimeField()
    signature = models.CharField(max_length=50, unique=True)
    pre_rating = models.IntegerField(default=0)
    chd_days = models.IntegerField(default=0)  # cached days count for return flights

    @classmethod
    def get_best(cls):
        cursor = connection.cursor()
        query = """
                SELECT b.destination_name as name, min(b.price) as price, c.rus_name as crn, dir.rus_name as drn, dir.id as did
                FROM enot_app_bid as b
                JOIN enot_app_destination as d ON d.code = b.destination_code
                JOIN enot_app_gplace as p ON p.id=d.place_id
                JOIN enot_app_gcountry as c ON c.id=p.gcountry_id
                JOIN `enot_app_gdirection` as dir ON dir.id=c.`gdirection_id`
                GROUP BY b.destination_code
                ORDER BY name
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)


        #return rows
        res={}
        for r in rows:
            if r['drn'] not in res.keys():
                print('creating direction', r['drn'])
                res[r['drn']]={"name": r['drn'], "countries": {}}
            if r['crn'] not in res[r['drn']]['countries'].keys():
                print('creating country', r['crn'])
                res[r['drn']]['countries'][r['crn']] = {"name": r['crn'],
                                                        "places": []
                                                        }
            res[r['drn']]['countries'][r['crn']]['places'].append(r)

        return res


class Subscriber(models.Model):
    name = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=50)
    interval = models.IntegerField(default=1)
    confirmed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)
    tester = models.BooleanField(default=False)
    last_mail_sent_at = models.DateTimeField(null=True)
    invite_code = models.CharField(max_length=50)
    hsh = models.CharField(max_length=50, default='')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, email, invite, **kwargs):
        s = cls(email=email, invite_code=invite)
        s.email = email
        s.invite = invite
        if 'interval' in kwargs:
            s.interval = kwargs['interval']
        if 'premium' in kwargs:
            s.premium = kwargs['premium']
        if 'tester' in kwargs:
            s.tester = kwargs['tester']
        if 'name' in kwargs:
            s.name = kwargs['name']

        s.hsh = get_hash(email)

        return s



class Airline(models.Model):
    iata = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    rating = models.IntegerField(null=True)


class Trip(models.Model):
    origin_code = models.CharField(max_length=3)
    destination_code = models.CharField(max_length=3)
    return_code = models.CharField(max_length=3)
    price = models.IntegerField()
    currency = models.CharField(max_length=3)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    carriers = models.CharField(max_length=25)
    slices = models.TextField()
    rating = models.IntegerField(default=0)
    rt_comfort = models.IntegerField(default=0)
    rt_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    destination_name = models.CharField(max_length=50, null=True)
    destination = models.ForeignKey(Destination, null=True)  # use later?
    chd_days = models.IntegerField(null=True)
    pre_rating = models.IntegerField(null=True)
    distance = models.IntegerField(null=True)
    bid_price = models.IntegerField(null=True)

    #average_price = models.IntegerField(null=True) # add later?

    benefits = models.TextField(null=True)
    penalties = models.TextField(null=True)

    def get_slices(self):
        return json.loads(self.slices)

    # def review(self):
    #     benefits = []
    #     penalties = []
    #     rtc = 0  # comfort rating
    #     rtp = 0  # price rating

    #     slices = self.get_slices()

    #     if self.departure.hour >= 12:
    #         benefits.append({
    #             'kind': 'originDepartTime',
    #             'message': 'Удобное время вылета из Москвы'
    #         })
    #         rtc += 100

    #     if self.arrival.hour in range(8, 21):
    #         benefits.append({
    #             'kind': 'returnArrivalTime',
    #             'message': 'Удобное время возвращения в Москву'
    #         })
    #         rtc += 30

    #     """ Destination arrival time """

    #     dats = slices[0]['segments'][-1]['legs'][-1]['arrival']
    #     dat = datetime.strptime(dats.replace(':', ''), '%Y-%m-%dT%H%M%z')
    #     if dat.hour in range(10, 21):
    #         benefits.append({
    #             'kind': 'destinationArrivalTime',
    #             'message': 'Удобное время прибытия в пункт назначения'
    #         })
    #         rtc += 100

    #     """ Destination departure time """

    #     ddts = slices[-1]['segments'][0]['legs'][0]['departure']
    #     ddt = datetime.strptime(ddts.replace(':', ''), '%Y-%m-%dT%H%M%z')
    #     if ddt.hour > 10:
    #         benefits.append({
    #             'kind': 'destinationDepartureTime',
    #             'message': 'Удобное время вылета обратно'
    #         })
    #         rtc += 50

    #     """ Number of stops """

    #     """ total number of stops """
    #     tns = slices[0]['slice_stops']+slices[1]['slice_stops']
    #     if tns == 0:
    #         benefits.append({
    #             'kind': 'directFlight',
    #             'message': 'Прямые рейсы в обе стороны'
    #         })
    #         rtc += 200
    #     elif tns == 1:
    #         benefits.append({
    #             'kind': 'semiDirectFlight',
    #             'message': 'Прямой рейс в одну сторону'
    #         })
    #         rtc += 100
    #     elif tns > 2:
    #         penalties.append({
    #             'kind': 'moreThanTwoStops',
    #             'message': 'Много стыковок'
    #         })
    #         rtc -= 200

    #     for sln in range(0,2):
    #         times = []

    #         for sg in slices[sln]['segments']:
    #             for l in sg['legs']:
    #                 times.append(l['departure'])
    #                 times.append(l['arrival'])

    #         print (times)

    #         if len(times)>2:
    #             for n in range(1,len(times)-1,2):
    #                 t1 = datetime.strptime(times[n+1].replace(':', ''), '%Y-%m-%dT%H%M%z')
    #                 t0 = datetime.strptime(times[n].replace(':', ''), '%Y-%m-%dT%H%M%z')
    #                 st = (t1-t0).seconds
    #                 print(int(st/3600), int(st%3600/60))

    

    #     self.benefits = json.dumps(benefits)
    #     self.penalties = json.dumps(penalties)
    #     self.rt_comfort = rtc
    #     self.rt_price = rtp
    #     self.save()

    @classmethod
    def load_qpx(cls, qpx, bid_info={}):
        """ Makes Trip object from QPX response trip
        :param qpx: qpx trip dict
        :param bid_info: dict with related bid info (from sql)
        """
        t = cls(
            origin_code=qpx['origin'],
            destination_code=qpx['destination'],
            return_code=qpx['return'],
            price=qpx['price'],
            currency=qpx['currency'],
            departure=qpx['trip_departure'],
            arrival=qpx['trip_arrival'],
            carriers=', '.join(qpx['carriers']),
            slices=json.dumps(qpx['slices'])
        )

        if bid_info:
            t.destination_name = bid_info['destination_name']
            t.chd_days = bid_info['chd_days']
            t.pre_rating = bid_info['pre_rating']
            t.distance = bid_info['distance']

        return t


class Invite(models.Model):
    code = models.CharField(max_length=50)
    emitter = models.ForeignKey(Subscriber)
    created_at = models.DateTimeField(auto_now_add=True)
    released = models.BooleanField(default=False)
    released_at = models.DateTimeField(null=True)

    @classmethod
    def create(cls, emitter):
        inv = cls(emitter=emitter)
        inv.code = get_hash(str(inv.id))
        return inv


class Status(models.Model):
    stat_date = models.DateField(unique=True)
    qpx_requests = models.IntegerField(default=0)
    planner_started = models.BooleanField(default=False)
    planner_finished = models.BooleanField(default=False)
    loader_started = models.IntegerField(default=0)
    loader_finished = models.IntegerField(default=0)
    forced = models.BooleanField(default=False)

    @classmethod
    def get_today(cls):
        stats, created = cls.objects.get_or_create(
            stat_date=datetime.today()
        )
        return stats

    @classmethod
    def get_yesterday(cls, force=False):
        yesterday = datetime.today()-timedelta(days=1)
        try:
            stats = cls.objects.get(stat_date=yesterday)
        except cls.DoesNotExist:
            if force is False:
                print('Previous stats record does not exist')
                return False
            else:
                stats = cls(stat_date=yesterday,
                        forced=True)
                stats.save()
        return stats

