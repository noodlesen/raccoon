from django.contrib import admin
from .models import Subscriber
from enot_app.models import City, DayJob, Bid, Card, GPlace, Tag, Hotel, Quote, Trip#, PlaceKeys

# Register your models here.

# class GPlaceAdmin(admin.ModelAdmin):


class CardAdmin(admin.ModelAdmin):
    raw_id_fields=('place', 'tags',)
    autocomplete_lookup_fields = {
        'fk': ['place'],
        'm2m': ['tags'],
    }
    list_display = ('place', 'text', 'link', 'published',)
    search_fields = ['text', 'place__rus_name', 'link']
    #list_filter = ['place']

class HotelAdmin(admin.ModelAdmin):
    raw_id_fields=('place',)
    autocomplete_lookup_fields = {
        'fk': ['place'],
        #'m2m': ['tags'],
    }

class QuoteAdmin(admin.ModelAdmin):
    raw_id_fields=('place','tags')
    autocomplete_lookup_fields = {
        'fk': ['place'],
        'm2m': ['tags'],
    }
    search_fields = ['text', 'place__rus_name']
    list_display = ('place', 'text',)

admin.site.register(Subscriber)
admin.site.register(City)
admin.site.register(DayJob)
admin.site.register(Bid)
admin.site.register(Trip)
admin.site.register(Tag)
admin.site.register(Card, CardAdmin)
admin.site.register(GPlace)
# admin.site.register(PlaceKeys)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Quote, QuoteAdmin)
