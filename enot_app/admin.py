from django.contrib import admin
from .models import Subscriber
from enot_app.models import City, DayJob, Bid

# Register your models here.

admin.site.register(Subscriber)
admin.site.register(City)
admin.site.register(DayJob)
admin.site.register(Bid)
