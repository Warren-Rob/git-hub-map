from django.shortcuts import render
from django.http import HttpResponse
from heat_map.models import User
from urllib import urlencode
import json
import requests

""" need to keep the users already mapped in the map --
    can't load all users every single time """

def index(request):
  users = User.objects.order_by('-location')
  users = User.objects.all()[:5]
  #[User(location='San Francisco', name="Tim", numcommits=2)]#DEBUG
               
  locations = {}
  for user in users:
    
    if user.location not in locations.keys():
      latlon = get_lat_long(user.location)
      if latlon != None:
        locations[user.location] = {'count': 1}
        locations[user.location].update(latlon)
        #print (locations)#DEBUG
    else:
      locations[user.location]['count'] += 1

  locations_json = json.dumps(locations)
  context = {'locations': locations_json}
  print(context)
  return render(request, 'heat_map/index.html', context)

def get_lat_long(location):
  print("in it")
  lat_long = {}
  location.replace(' ', '+')
  url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&{}'.format(urlencode({'address':location.encode('utf-8')}))
  r = requests.get(url);
  results = r.json()['results']
  if len(results) != 0: # address validity check
    coords = results[0]['geometry']['location']
    print coords
    return {'lat': coords['lat'], 'lon': coords['lng'] }

  return None

  
  
  
    
