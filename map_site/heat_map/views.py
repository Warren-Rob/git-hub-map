from django.shortcuts import render
from django.http import HttpResponse
from heat_map.models import User
from heat_map.models import Location
from urllib import urlencode
from django.core import serializers
import json
import requests

def index(request):
  locationList = { }
  for place in Location.objects.all():
    if place.location == 'Antarctica':
      continue

    userList = { }
    users = User.objects.filter(location = place.location)

    for u in users:
      userList.update({u.uid: {'login': u.name }})

    locationList.update({place.location: {'lat': place.lat, 
                                          'lon': place.lng, 
                                          'users': userList
                                         }})

  locations_json = json.dumps(locationList)
  context = {'locations': locations_json}
  return render(request, 'heat_map/index.html', context)
