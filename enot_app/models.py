from django.db import models, connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

# Create your models here.


class Bid(models.Model):
    origin_code = models.CharField(max_length=3)
    destination_code = models.CharField(max_length=3)
    destination_name = models.CharField(max_length=35)
    one_way = models.BooleanField()
    departure_date = models.DateField()
    return_date = models.DateField()
    price = models.IntegerField()
    stops = models.IntegerField()
    trip_class = models.IntegerField()
    distance = models.IntegerField()
    rating = models.IntegerField()
    to_expose = models.BooleanField()
    found_at = models.DateTimeField()
    snapshot = models.CharField(max_length=50)


class GDirection(models.Model):
    eng_name = models.CharField(max_length=50)
    rus_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)


class GCountry(models.Model):
    code = models.CharField(max_length=2)
    eng_name = models.CharField(max_length=50)
    gdirection = models.ForeignKey(GDirection)
    rus_name = models.CharField(max_length=50)
    kdb_id = models.IntegerField() #-
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
    gcountry = models.ForeignKey(GCountry) # !!!
    UFI = models.IntegerField()
    types = models.CharField(max_length=100)
    google_place_id = models.CharField(max_length=50)
    image = models.CharField(max_length=50) #?
    fpid = models.IntegerField() #-
    dup = models.IntegerField() #-
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

    @classmethod
    def get_structured(cls):
        cursor = connection.cursor()
        query = """
                SELECT ds.name, c.rus_name as crn, c.id as cid, c.slug as cslug, d.rus_name as drn, d.id as did, d.slug as dslug
                FROM `enot_app_destination` as ds
                JOIN `enot_app_gplace` as p ON p.id = ds.place_id
                JOIN `enot_app_gcountry` as c ON c.id = p.gcountry_id
                JOIN `enot_app_gdirection` as d ON d.id = c.gdirection_id
                """
        cursor.execute(query)
        #rows = cursor.fetchall()
        rows = dictfetchall(cursor)
        return rows










