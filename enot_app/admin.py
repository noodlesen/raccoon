from django.contrib import admin
from .models import Subscriber
from enot_app.models import City, DayJob, Bid, Card, GPlace, Tag

# Register your models here.

# class GPlaceAdmin(admin.ModelAdmin):


class CardAdmin(admin.ModelAdmin):
    raw_id_fields=('place', 'tags',)
    autocomplete_lookup_fields = {
        'fk': ['place'],
        'm2m': ['tags'],
    }

admin.site.register(Subscriber)
admin.site.register(City)
admin.site.register(DayJob)
admin.site.register(Bid)
admin.site.register(Tag)
admin.site.register(Card, CardAdmin)
admin.site.register(GPlace)
