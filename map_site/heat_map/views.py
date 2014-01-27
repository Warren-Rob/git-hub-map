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
    usersAtPlace = User.objects.filter(location = place.location)

    # still necessary? no more UID
    i = 0
    for u in usersAtPlace:
      userList.update({ i : u.name })
      i = i + 1

    locationList.update({
      place.location: {
        'lat': place.lat,
        'lon': place.lng,
        'users': userList
        }
      })

  locations_json = json.dumps(locationList)
  context = {'locations': locations_json}
  return render(request, 'heat_map/index.html', context)
