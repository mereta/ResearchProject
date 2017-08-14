from django.conf.urls import url
from . import views

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from DublinBus import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getResult/$', views.getResult, name='getResult'),
    #url(r'^mapMarkers$', views.mapMarkers, name='mapMarkers'),
    url(r'^getStops', views.getStops, name='getStops'),
    url(r'^getToStops', views.getToStops, name='getToStops'),
    url(r'^getStopInt', views.getStopInt, name='getStopInt'),
    #url(r'^getResult/(?P<travelroute>)/(?P<traveltime>)', views.getResult, name='getResult'),
    
]


