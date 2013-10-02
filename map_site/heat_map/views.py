from django.shortcuts import render
from django.http import HttpResponse
from heat_map.models import User
from heat_map.models import Location
from urllib import urlencode
from django.core import serializers
import json
import requests

def index(request):
  users = User.objects.order_by('-location')
  users = User.objects.all()

  # natural join?
  # compare databases
    # any user.location already in the location db, skip the user

  for user in users:
    try:
     Location.objects.get(location=user.location)
    except Location.DoesNotExist:
      latlon = get_lat_long(user.location)
      if latlon != None:
        Location(location=user.location, lng=latlon['lon'],
                 lat=latlon['lat']).save()

  locations = { }
  for loc in Location.objects.all():
    locations.update({loc.location: {'lat': loc.lat, 'lon': loc.lng}})

  locations_json = json.dumps(locations)
  context = {'locations': locations_json}
  return render(request, 'heat_map/index.html', context)

def get_lat_long(location):
  #print("in it")
  lat_long = {}
  location.replace(' ', '+')
  url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&{}'.format(urlencode({'address':location.encode('utf-8')}))
  r = requests.get(url);
  results = r.json()['results']
  if len(results) != 0: # address validity check
    coords = results[0]['geometry']['location']
    # print coords # debug
    return {'lat': coords['lat'], 'lon': coords['lng'] }

  return None
