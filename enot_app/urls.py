from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^structured-feed', views.structured_feed, name='structured_feed'),
    url(r'^pricelist', views.pricelist, name='pricelist'),
    url(r'^unsubscribe/(?P<hsh>\w+)', views.unsubscribe, name='unsubscribe'),
]

