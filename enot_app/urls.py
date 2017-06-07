from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^letter', views.letter_page, name='letter_page'),
    url(r'^unsubscribe/(?P<hsh>\w+)', views.unsubscribe, name='unsubscribe'),
    url(r'^(?P<no>\d+)$', views.ticket_no, name='ticketno'),
]

