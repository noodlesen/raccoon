from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^bid-feed', views.bid_feed, name='bid_feed'),
]

