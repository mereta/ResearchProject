from django.http import HttpResponse
from django.template import Context, loader
from . import models as m
import datetime
import json
import pandas as pd
from sklearn.externals import joblib
from django.core import serializers
import csv


# Create your views here.
def index(request):
    #retrieve records from DB
    
    # Get routes from database
    routeList = m.GpsNov.objects.order_by('route').values_list('route', flat=True).distinct()
    
    
    # Anything which needs to be added to page should be added here (query results or any other variable)
    context = {
        "routeLists":routeList,
        
        }
    
    # Load template first/templates/index.html
    template = loader.get_template("index.html")

    # do not touch, returns values to template
    return HttpResponse(template.render(context, request))

#xhttp call to get result
def getResult(request):
    
    #get inputs
    in_route=request.GET.get('travelroute')
    in_time=request.GET.get('traveltime')
    in_weather=request.GET.get('weather')
    in_from=request.GET.get('from')
    in_to=request.GET.get('to')
    
    #check if weather is wet or dry
    if in_weather == "Wet":
        in_weather = 1
    else:
        in_weather = 0 

    
    #get day of week string
    strweek_day = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M').strftime('%w')
    #get time strings
    strtimehour = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M').strftime('%H')
    strtimemin = datetime.datetime.strptime(in_time, '%Y-%m-%d %H:%M').strftime('%M')
    strtimemin =float(strtimemin)/60
    strtimemin = str(strtimemin).replace("0.", "")
    time = str(strtimehour) + "." + str(strtimemin)


    with open('csvfile.csv', 'w') as c:
         writer = csv.writer(c)     
         writer.writerow(["Day","ScheduledDepart","StopID","Weather (1 = W, 0 = D)"])
         writer.writerow([str(strweek_day),time,str(in_from),str(in_weather)])
         writer.writerow([str(strweek_day),time,str(in_to),str(in_weather)])
    

    # get model based on route
    filename = "first/static/first/RFBR" + in_route + "_v0.1.mdl"
    RFMODEL = joblib.load(filename)
    csv1 = pd.read_csv('csvfile.csv')
    csv2 = [[str(strweek_day), time, str(in_from), str(in_weather)],[str(strweek_day), time, str(in_to), str(in_weather)]]
    
    pred = RFMODEL.predict(csv2)
   
    
    depart = str(pred[0]).split('.')
    arr = str(pred[1]).split('.')
   
    dephr = depart[0]
    depmin = depart[1]
    arrhr = arr[0]
    arrmin = arr[1]
    
    depart = dephr + ":" + str(int(depmin)*60)
    arr = arrhr + ":" + str(int(arrmin)*60)
   
    depart[0:3]
    
    #filename = 'first/static/first/final.json'
    filename = open("first/static/first/final.json","r") 
    data = filename.read()



    return HttpResponse(json.dumps({ 'depart': depart[0:5], 'arr': arr[0:5]}), content_type='application/json')

# get list of from stops
def getStops(request):
    
    #get inputs
    in_route=request.GET.get('travelroute')
    in_direction=request.GET.get('direction')
    

    #query database for route, day of week and 5 minutes before and after selected time
        
    stops = m.MapStops.objects.filter(route=in_route).filter(direction=in_direction)
         
    #translate stops into JSON format
    XMLSerializer = serializers.get_serializer("json")
    xml_serializer = XMLSerializer()
    xml_serializer.serialize(stops)
    data = xml_serializer.getvalue()    
    
    #return stops in JSON format
    return HttpResponse(data, content_type='application/json')


#get list of TO stops
def getToStops(request):
    
    
    in_route=request.GET.get('travelroute')
    in_direction=request.GET.get('direction')
    in_from=request.GET.get('from')
    
    #query database for route, direction and stops greater than fromstopid
    stops = m.MapStops.objects.filter(route=in_route).filter(direction=in_direction).filter(map_stop_id__gt=in_from)
    
    
        #translate stops into JSON format
    XMLSerializer = serializers.get_serializer("json")
    xml_serializer = XMLSerializer()
    xml_serializer.serialize(stops)
    data = xml_serializer.getvalue()    
    
    return HttpResponse(data, content_type='application/json')


#get list of TO stops
def getStopInt(request):
    
    in_route=request.GET.get('travelroute')
    in_direction=request.GET.get('direction')
    in_from=request.GET.get('from')
    in_to=request.GET.get('to')

    
    #query database for route, direction and stops greater than fromstopid
    stops = m.MapStops.objects.filter(route=in_route).filter(direction=in_direction).filter(map_stop_id__gt=in_from).filter(map_stop_id__lte=in_to)
    
    #translate stops into JSON format
    XMLSerializer = serializers.get_serializer("json")
    xml_serializer = XMLSerializer()
    xml_serializer.serialize(stops)
    data = xml_serializer.getvalue()    
    
    #print(data) 
    
    return HttpResponse(data, content_type='application/json')

