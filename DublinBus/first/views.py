from django.http import HttpResponse
from django.template import Context, loader
from . import models as m
from datetime import date
from datetime import timedelta
import datetime
import calendar
import json
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor
from flask_googlemaps import GoogleMaps, Map
from django.core import serializers


# Create your views here.
def index(request):
    #retrieve records from DB
    
    # Queries here
    routeList = m.GpsNov.objects.order_by('route').values_list('route', flat=True).distinct()
    
    
    # Anything which needs to be added to page should be added here (query results or any other variable)
    context = {
        "routeLists":routeList,
        
        }
    
    # Load template first/templates/index.html
    template = loader.get_template("index.html")

    # do not touch, returns values to template
    return HttpResponse(template.render(context, request))


def getResult(request):
  
    in_route=request.GET.get('travelroute')
    in_time=request.GET.get('traveltime')
    in_weather=request.GET.get('weather')
    in_direction=request.GET.get('direction')
    in_from=request.GET.get('from')
    in_to=request.GET.get('to')
    
    print("WEBSITE WEATHER", in_weather)

    
    #get day of week string
    strweek_day = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M').strftime('%A')
    #get time string
    strtime = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M').strftime('%H:%M')
    #get time date object
    time = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M')
   
  
    # create date difference to give us two times - one 5 mins before selected time, one 5 minutes after.
    # this time frame will be queried
    
    diff = timedelta(minutes=5)
    mintime = time - diff
    maxtime = time + diff

    #query database for route, day of week and 5 minutes before and after selected time
    #journeys = m.GpsNov.objects.raw('SELECT * FROM gps_nov WHERE Route = %s and day = %s and TIME(Departure) between %s and %s and Weather = %s' , [in_route, strweek_day, mintime.time(), maxtime.time(), in_weather])

    #cnt = 0
    #sum = 0
    #print(journeys)
    #total jourey duration and get average by dividing number of journeys
    #for x in journeys:
      # sum += x.duration
       #cnt += 1
       #print(x.id, x.route, x.day, x.weather, x.duration, x.departure, x.arrival)
        
    # get average minutes
    #average = sum/cnt
    #averagemins = average/60
    #averagemins = str(round(averagemins, 2))
    
    #filename = 'first/static/first/RFBR1_v0.1.mdl'
    #RFMODEL = joblib.load(filename)
    #test = pd.read_csv('first/static/first/SingleTest.csv')
    #pred = RFMODEL.predict(test)
    #print("this is a prediction TEST", pred)
    
    
    #filename = 'first/static/first/final.json'
    filename = open("first/static/first/final.json","r") 
    data = filename.read()
    
    #print(data)
    #RFMODEL = joblib.load(filename)
    #test = pd.read_csv('\\...path\SingleTest.csv')
    #pred = RFmodel.predict(test)
    #array([ 3749.82557749])
    context = {
        "journeys": journeys,
        
        }

    return HttpResponse(json.dumps({ 'average': averagemins}), content_type='application/json')


def getStops(request):
    
    in_route=request.GET.get('travelroute')
    in_direction=request.GET.get('direction')
    in_from=request.GET.get('from')
  #query database for route, day of week and 5 minutes before and after selected time
    #stops = m.MapStops.objects.raw('SELECT stop_id, location, Map_stop_id FROM map_stops WHERE Route = %s' , [in_route])
    retstr = ""
    
    
    stops = m.MapStops.objects.filter(route=in_route).filter(direction=in_direction)
    
        
        
      
    XMLSerializer = serializers.get_serializer("json")
    xml_serializer = XMLSerializer()
    xml_serializer.serialize(stops)
    data = xml_serializer.getvalue()    
    
    print(data) 
    return HttpResponse(data, content_type='application/json')

def getToStops(request):
    
    
    in_route=request.GET.get('travelroute')
    in_direction=request.GET.get('direction')
    in_from=request.GET.get('from')
  #query database for route, day of week and 5 minutes before and after selected time
    #stops = m.MapStops.objects.raw('SELECT stop_id, location, Map_stop_id FROM map_stops WHERE Route = %s' , [in_route])
    retstr = ""
    
    
    stops = m.MapStops.objects.filter(route=in_route).filter(direction=in_direction).filter(map_stop_id__gt=in_from)
    
        
        
      
    XMLSerializer = serializers.get_serializer("json")
    xml_serializer = XMLSerializer()
    xml_serializer.serialize(stops)
    data = xml_serializer.getvalue()    
    
    print(data) 
    print("test from stop var", in_from)
    return HttpResponse(data, content_type='application/json')


def getStopInt(request):
    
    in_route=request.GET.get('travelroute')
    in_direction=request.GET.get('direction')
    in_from=request.GET.get('from')
    in_to=request.GET.get('to')
  #query database for route, day of week and 5 minutes before and after selected time
    #stops = m.MapStops.objects.raw('SELECT stop_id, location, Map_stop_id FROM map_stops WHERE Route = %s' , [in_route])
    retstr = ""
    
    
    stops = m.MapStops.objects.filter(route=in_route).filter(direction=in_direction).filter(map_stop_id__gt=in_from).filter(map_stop_id__lte=in_to)
    
        
        
      
    XMLSerializer = serializers.get_serializer("json")
    xml_serializer = XMLSerializer()
    xml_serializer.serialize(stops)
    data = xml_serializer.getvalue()    
    
    print(data) 
    print("test to stop var", in_to)
    return HttpResponse(data, content_type='application/json')

