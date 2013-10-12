import requests, gzip, json, os
from datetime import datetime
from celery.task import task
from urllib import urlencode, urlretrieve
from heat_map.models import User, Location

login = 'robforsythe'

@task(name='tasks.addEvents')
def addEvents():
  time = getDate()

  GHlink = 'http://data.githubarchive.org/{0}-{1}-{2}-{3}.json.gz'
  url = GHlink.format(time[0], time[1], time[2], time[3])
  events = fetchJSON(url)

  for e in events:
    etype = e['type']

    if validEvent(etype):
      actor = e['actor']
      repo = e['repository']

      if etype == 'CreateEvent':
        return;
      elif etype == 'IssuesEvent':
        return;
      elif etype == 'PushEvent':
        return;
      else:
        return;


      r = Repo(rid=repo['id'], name=repo['name'], owner=repo['owner'])


  link = 'https://api.github.com/users/{0}'
  newUsers = []

  for elt in arr:
    print elt
    uname = elt['actor_attributes']['login']

    try:
      User.objects.get(name=uname)
    except User.DoesNotExist:
      r = requests.get(link.format(uname), auth=(login, authToken))
      remaining = int(r.headers["x-ratelimit-remaining"])

      if remaining == 0:
        return None
      
      data = r.json()

      if data["type"] == "User":
        uid = int(data["id"])
        if 'location' in data and data["location"] != "null" and data['location'] != None:
          loc = data['location']
        else:
          # placeholder
          loc = 'Antarctica' 

          # returns { staticLocation, latitude, longitude }
        location = getLocation(loc)
        u = User(uid=uid, name=uname, location=staticLoc)
        newUsers.append(u)

  User.objects.bulk_create(newUsers)

def getDate():
  yr = str(datetime.now().year)
  mo = str(datetime.now().month)
  if len(mo) != 2:
    mo = '0' + mo
  day = str(datetime.now().day)
  if len(day) != 2:
    day = '0' + day
  hr = str(datetime.now().hour - 3)

  return [yr, mo, day, hr]


def fetchJSON(url):
  fname = url.split('/')[-1]
  urlretrieve(url, fname)
  content = gzip.open(fname).read()

  jsons = []
  arr = content.splitlines()
  for e in arr:
    jsons.append(json.loads(e))

  return jsons

def validEvent(event):
  return {
          'CreateEvent': True,
          'ForkEvent': True,
          'IssuesEvent': True,
          'PublicEvent': True,
          'PullRequestEvent': True,
          'PushEvent': True,
          'ReleaseEvent': True,
          'WatchEvent': True,
          }.get(event, False)

def getLocation(userInputLoc):
  userInputLoc.replace(' ', '+')

  link = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&{}'
  url = link.format(urlencode({'address':userInputLoc.encode('utf-8')}))
  r = requests.get(url)

  results = r.json()['results']

  if len(results) != 0:
    coords = results[0]['geometry']['location']
    pos = {'lat': coords['lat'], 'lng': coords['lng'] }
  else:
    pos = {'lat': -82.862751899999992, 'lng': -135.000000000000000}

  try:
    l = Location.objects.get(lat=pos['lat'], lng=pos['lng'])
  except Location.DoesNotExist:
    l = Location(location=name, lat=pos['lat'], lng=pos['lng'])
    l.save()

  return l
