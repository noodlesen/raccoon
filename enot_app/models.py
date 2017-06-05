import json
from datetime import datetime, timedelta
from operator import itemgetter
from pytz import timezone
from django.db import models, connection
from .toolbox import dictfetchall, get_hash, russian_plurals, now_in_moscow, week_day_name
from django.core.validators import MaxValueValidator, MinValueValidator

#from .rating import days_to_distance


class GDirection(models.Model):
    eng_name = models.CharField(max_length=50)
    rus_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)


class GCountry(models.Model):
    code = models.CharField(max_length=2)
    eng_name = models.CharField(max_length=50)
    gdirection = models.ForeignKey(GDirection)
    rus_name = models.CharField(max_length=50)
    kdb_id = models.IntegerField()  # LEGACY RESERVED
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
    gcountry = models.ForeignKey(GCountry)
    UFI = models.IntegerField()
    types = models.CharField(max_length=100)
    google_place_id = models.CharField(max_length=50)
    image = models.CharField(max_length=50)  # LEGACY RESERVED
    fpid = models.IntegerField()  # LEGACY RESERVED
    dup = models.IntegerField()  # RM
    chd_airports = models.TextField()  # change to many-to-many
    city_code = models.CharField(max_length=3)

    def __str__(self):
        return ('%s, %s' % (self.rus_name, self.gcountry.rus_name))

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'rus_name__icontains',)


class Destination(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    tmp_country = models.CharField(max_length=50)
    place = models.ForeignKey(GPlace)
    total_bid_count = models.IntegerField()
    average_price = models.IntegerField()
    enabled = models.BooleanField(default=True)
    rating = models.IntegerField(null=True)


class Airport(models.Model):
    name = models.CharField(max_length=50, null=True)
    size = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    iata = models.CharField(max_length=3, null=True)
    city = models.CharField(max_length=50, null=True)
    city_code = models.CharField(max_length=3, null=True)
    country_code = models.CharField(max_length=2, null=True)
    country = models.CharField(max_length=50, null=True)  # RM later
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    alt = models.IntegerField(null=True)
    icao = models.CharField(max_length=4, null=True)
    timezone = models.IntegerField(null=True)
    dst = models.CharField(max_length=1, null=True)
    tzdata = models.CharField(max_length=50, null=True)
    place = models.ForeignKey(GPlace, null=True)

    def form_from(self):
        if self.iata == 'ZIA':
            return 'Жуковского'
        else:
            return self.name


class SpiderQueryTP(models.Model):
    origin = models.ForeignKey(Destination, related_name='tpr_origin')
    destination = models.ForeignKey(Destination,
                                    related_name='tpr_destination'
                                    )
    start_date = models.DateField()
    requested_at = models.DateTimeField(
        default=datetime(1979, 6, 30, 9, 30, 0, 0,
                         timezone('Europe/Moscow')
                         )
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
    best_price = models.BooleanField(default=False)

    place = models.ForeignKey(GPlace, null=True)

    @classmethod
    def mark_best(cls):
        """later"""
        return None

    @classmethod
    def get_best(cls):  # RM later
        cursor = connection.cursor()
        query = """
                SELECT b.destination_name as name, min(b.price) as price, c.rus_name as crn, dir.rus_name as drn, dir.id as did, count(b.price) as pcount
                FROM enot_app_bid as b
                JOIN enot_app_destination as d ON d.code = b.destination_code
                JOIN enot_app_gplace as p ON p.id=d.place_id
                JOIN enot_app_gcountry as c ON c.id=p.gcountry_id
                JOIN `enot_app_gdirection` as dir ON dir.id=c.`gdirection_id`
                GROUP BY b.destination_code
                ORDER BY price
                """
        cursor.execute(query)
        rows = dictfetchall(cursor)

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

    @classmethod  # RM later
    def get_best_for_each_dest(cls, sort='pre_rating'):
        bids = cls.objects.filter(pre_rating__gt=0)
        if sort=='price':
            reverse = False
            attr = 'price'
            sort_key = 'price'
        else:
            reverse = True
            attr = 'pre_rating'
            sort_key = 'pr'

        dests = {}

        for b in bids:
            print (b.id)
            if b.destination_code not in dests.keys():
                dests[b.destination_code] = b
            else:
                pr = getattr(dests[b.destination_code], attr)
                fa = dests[b.destination_code].found_at
                if getattr(b, attr) > pr:
                    dests[b.destination_code] = b
                elif getattr(b, attr) == pr:
                    if b.found_at > fa:
                        dests[b.destination_code] = b

        dlist = sorted(
            [
                {
                    "dest": k,
                    "bid": v,
                    "pr": v.pre_rating,
                    "price": v.price,
                    "country": v.destination.place.gcountry,
                    "direction": v.destination.place.gcountry.gdirection
                } for k, v in dests.items()
            ],
            key=itemgetter(sort_key),
            reverse=reverse
        )
        return dlist

    def __str__(self):
        return ("%d: %s->%s >%d | %d" % (
            self.id,
            self.origin_code,
            self.destination_code,
            self.price,
            self.pre_rating
        ))


class Carrier(models.Model):
    iata = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    rating = models.IntegerField(null=True)


class Aircraft(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    @classmethod
    def spot(cls, name):
        ac, created = cls.objects.get_or_create(
            name=name
        )
        if not created:
            ac.count+=1
            ac.save()


class City(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=3)
    last_issue_number = models.IntegerField(null=True)

    def __str__(self):
        return ('%s (%s)' % (self.name, self.code))


class Trip(models.Model):
    origin_code = models.CharField(max_length=3) #?
    origin_city = models.ForeignKey(City, null=True)
    destination_code = models.CharField(max_length=3)
    destination = models.ForeignKey(Destination, null=True)  # use later?
    destination_name = models.CharField(max_length=50, null=True)
    return_code = models.CharField(max_length=3)
    price = models.IntegerField()
    currency = models.CharField(max_length=3)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    #carriers = models.CharField(max_length=25)  #RM
    slices = models.TextField()
    #route_points = models.TextField(null=True)  # RM
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    """ Rating fields """
    pre_rating = models.IntegerField(null=True)
    rating = models.IntegerField(default=0)
    rt_comfort = models.IntegerField(default=0)
    rt_price = models.IntegerField(default=0)
    rt_eff = models.IntegerField(default=0)
    #benefits = models.TextField(null=True)  # RM
    #penalties = models.TextField(null=True)  # RM

    """ Trip status """
    expose = models.BooleanField(default=False)
    actual = models.BooleanField(default=True)

    """ Additional fields """
    average_price = models.IntegerField(null=True)  # add later?
    chd_days = models.IntegerField(null=True)
    distance = models.IntegerField(null=True)
    bid_price = models.IntegerField(null=True)

    """ Template helpers """
    #days_text = models.CharField(max_length=10, null=True)  # RM
    #days_to_text = models.CharField(max_length=50, null=True)  # RM
    #carriers_names = models.TextField(null=True)  # RM
    #days_to = models.IntegerField(null=True)  # RM

    """ Human data """
    hd = models.TextField()

    def get_hd(self):
        return json.loads(self.hd)

    def get_slices(self):  # RM?
        return json.loads(self.slices)

    @classmethod
    def load_qpx(cls, qpx, bid={}):
        """ Makes Trip object from QPX response trip
        :param qpx: qpx trip dict
        :param bid_info: dict with related bid info (from sql)
        """
        t = cls(
            origin_code=qpx['origin'],
            destination_code=qpx['destination'],
            return_code=qpx['return'],
            price=int(qpx['price']),
            currency=qpx['currency'],
            departure=qpx['trip_departure'],
            arrival=qpx['trip_arrival'],
            #carriers=', '.join(qpx['carriers']),
            #route_points=json.dumps(qpx['route_points']),
            slices=json.dumps(qpx['slices'])
        )

        if bid:
            t.destination_name = bid.destination_name
            t.chd_days = bid.chd_days
            t.pre_rating = bid.pre_rating
            t.distance = bid.distance
            t.average_price = bid.destination.average_price
            t.destination_id = bid.destination_id
            t.bid_price = bid.price

        return t

    # def get_benefits(self):  # RM
    #     return json.loads(self.benefits)

    # def get_penalties(self):  # RM
    #     return json.loads(self.penalties)

    # def get_carriers(self):  # RM
    #     return json.loads(self.carriers_names)

    # def supply(self):  # RM
    #     self.days_text = str(self.chd_days)+" "+russian_plurals('день', self.chd_days)
    #     self.days_to = (self.departure-now_in_moscow()).days
    #     self.days_to_text = "через "+str(self.days_to)+" "+russian_plurals('день', self.days_to)

    def get_origin_airport_name(self, form=''):  # RM
        try:
            ap = Airport.objects.get(iata=self.origin_code)
        except Airport.DoesNotExist:
            return 'unknown'
        else:
            if form == 'from':
                return ap.form_from()
            else:
                return ap.name


### END OF TRIP MODEL





class Status(models.Model):
    stat_date = models.DateField(unique=True)
    qpx_requests = models.IntegerField(default=0)
    planner_started = models.BooleanField(default=False)
    planner_finished = models.BooleanField(default=False)
    loader_started = models.IntegerField(default=0)
    loader_finished = models.IntegerField(default=0)
    forced = models.BooleanField(default=False)
    build = models.TextField(null=True)
    api_request_in_progress = models.BooleanField(default=False)

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
                            forced=True
                            )
                stats.save()
        return stats


class DayJob(models.Model):
    day_number = models.IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(6),
            MinValueValidator(0)
        ]
    )
    city = models.ForeignKey(City)

    ALGORITHMS = (('TP', 'Aviasales only'), ('OTHER','Other'))
    algorithm = models.CharField(max_length=10, choices=ALGORITHMS, default='TP')

    def __str__(self):
        return ('%s(%d): %s' % (
            week_day_name(self.day_number),
            self.day_number,
            self.city.name
        ))

    @classmethod
    def get_target_code(cls):
        today = now_in_moscow().weekday()
        dj = cls.objects.get(day_number=today)
        return dj.city.code

    @classmethod
    def get_target(cls):
        today = now_in_moscow().weekday()
        dj = cls.objects.get(day_number=today)
        return dj.city

    @classmethod
    def get_all_codes(cls):
        return set([j.city.code for j in cls.objects.all()])

    @classmethod
    def get_all_origins(cls):
        return Destination.objects.filter(code__in=cls.get_all_codes())


class Issue(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(max_length=30)
    number = models.IntegerField(null=True)
    build = models.TextField(null=True)
    stop_list = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @classmethod
    def get_last_stoplist(cls, tgt):
        try:
            last_issue = cls.objects.filter(city=tgt).latest('created_at')
        except cls.DoesNotExist:
            sl = []
        else:
            sl = json.loads(last_issue.stop_list)
        return sl


class Subscriber(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, unique=True, null=True)
    city = models.ForeignKey(City, null=True)
    interval = models.IntegerField(default=1)
    confirmed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)
    tester = models.BooleanField(default=False)
    last_mail_sent_at = models.DateTimeField(null=True)
    invite_code = models.CharField(max_length=50)
    hsh = models.CharField(max_length=50, unique=True, null=True)
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


class Invite(models.Model):
    code = models.CharField(max_length=50)
    emitter = models.ForeignKey(Subscriber)
    created_at = models.DateTimeField(auto_now_add=True)
    released = models.BooleanField(default=False)
    released_at = models.DateTimeField(null=True)

    @classmethod
    def create(cls, emitter):
        inv = cls(emitter=emitter)
        inv.save()
        inv.code = get_hash(str(inv.id))
        return inv


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'name__icontains',)

    def __str__(self):
        return self.name


class Quote(models.Model):
    place = models.ForeignKey(GPlace, null=True)
    text = models.TextField()
    chd_data = models.TextField()  # RM?
    chd_rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)


class Card(models.Model):
    text = models.TextField()
    link = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    place = models.ForeignKey(GPlace, null=True)


