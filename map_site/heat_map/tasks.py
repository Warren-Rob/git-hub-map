import requests, os
from urllib import urlencode
from celery.task import task
from heat_map.models import User, Location

login = 'robforsythe'
authToken = 'b4439ecc6eca48565539a136219326c48c9feed4'

@task(name='tasks.populateDB')
def populateDB():
  link = "https://api.github.com/users?since={0}"
  if User.objects.count() == 0:
    lastUserId = 0
  else:
    lastUserId = User.objects.latest('uid').uid

  while (True):
    r = requests.get(link.format(lastUserId), auth=(login, authToken))
    remaining = int(r.headers["x-ratelimit-remaining"])
    if remaining == 0:
      break

    userList = []
    data = r.json()
    for userInfo in data:
      if userInfo["type"] == "User":
        uid = int(userInfo["id"])
        uname = userInfo["login"]
        loc = getUserLocation(uname)

        if loc == None:
          break

        print uname
        print loc

        # loc will always return a location
        u = User(uid=uid, name=uname, location=loc)
        userList.append(u)

    User.objects.bulk_create(userList)
    lastUserId = int(data[len(data)-1]['id'])

# first, get the location that the user provides (1)
# next, get the coordinates that google maps returns (2)
# last, store & return the location object (3)
def getUserLocation(user):
  # (1)
  link = "https://api.github.com/users/{0}".format(user)
  uinfo = requests.get(link, auth=(login, authToken)).json()

  if 'location' in uinfo and uinfo["location"] != None:
    loc = uinfo['location']
  else:
    loc = 'Antarctica'

  try:
    l = Location.objects.get(location = loc)
  except Location.DoesNotExist:
    # (2)
    lat_long = {}
    loc.replace(' ', '+')
    link = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&{}'
    url = link.format(urlencode({'address':loc.encode('utf-8')}))
    r = requests.get(url)
    #print r.headers
    
    # need a limit check
    #if r.headers['status'] == 'OVER_QUERY_LIMIT':
    #  return None

    # this will include lat and lng
    results = r.json()['results']

    if len(results) != 0: # address validity check
      coords = results[0]['geometry']['location']
      pos = {'lat': coords['lat'], 'lng': coords['lng'] }
    else:
      # placeholder - Antarctica!
      pos = {'lat': -82.862751899999992, 'lng': -135.000000000000000}

    # (3)
    try:
      l = Location.objects.get(lat=pos['lat'], lng=pos['lng'])
    except Location.DoesNotExist:
      l = Location(location=loc, lat=pos['lat'], lng=pos['lng'])
      l.save()

  return l

