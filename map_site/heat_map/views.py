from django.shortcuts import render
from django.http import HttpResponse
from heat_map.models import User
from heat_map.models import Location
from urllib import urlencode
from django.core import serializers
import json
import requests

# index should only load the existing information 
# from the db, NOT request the data itself
def index(request):
  locationList = { }
  for place in Location.objects.all():
    # get all users with this location
    # return them in a list via dict

    userList = { }
    users = User.objects.filter(location = place.location)
    for u in users:
      userList.update({ u.uid: {'login': u.name }})

    locationList.update({place.location: {'lat': place.lat, 
                                          'lon': place.lng, 
                                          'users': userList
                                         }})

  locations_json = json.dumps(locationList)
  context = {'locations': locations_json}
  return render(request, 'heat_map/index.html', context)
