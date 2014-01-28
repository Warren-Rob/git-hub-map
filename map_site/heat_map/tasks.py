import datetime
import requests, gzip, json, os
from celery.task import task
from urllib import urlencode, urlretrieve
from heat_map.models import User, Location, Repo, PushEvent

# from heat_map.tasks import addEvents
@task(name='tasks.addEvents')
def addEvents():
  events = fetchJSON()

  for e in events:
    if e['type'] == 'PushEvent' and 'repository' in e:
      u = saveUser(e['actor_attributes'])
      r = saveRepo(e['repository'])
      ref = e['payload']['ref']
      size = e['payload']['size']

      p = PushEvent(actor=u, repo=r, ref=ref, size=size)
      p.save()


def saveUser(actor_attrs):
  try:
    u = User.objects.get(name=actor_attrs['login'])
  except User.DoesNotExist:
    if 'location' in actor_attrs and actor_attrs['location'] != None:
      loc = actor_attrs['location']
    else:
      loc = 'Antarctica'

    location = getLocation(loc)
    u = User(name=actor_attrs['login'], location=location)
    u.save()

  return u


def saveRepo(repo):
  rid = repo['id']

  try:
    r = Repo.objects.get(rid=rid)
  except Repo.DoesNotExist:
    rname = repo['name']
    rowner = repo['owner']

    r = Repo(rid=rid, name=rname, owner=rowner)
    r.save()

  return r


def getDate():
  threeHrsAgo = datetime.datetime.now() - datetime.timedelta(hours=3)

  yr = str(threeHrsAgo.year)
  mo = str(threeHrsAgo.month)
  day = str(threeHrsAgo.day)
  hr = str(threeHrsAgo.hour)

  if len(mo) != 2:
    mo = '0' + mo

  if len(day) != 2:
    day = '0' + day

  return [yr, mo, day, hr]


def fetchJSON():
  time = getDate()
  GHAlink = 'http://data.githubarchive.org/{0}-{1}-{2}-{3}.json.gz'
  url = GHAlink.format(time[0], time[1], time[2], time[3])

  fname = url.split('/')[-1]
  urlretrieve(url, fname)
  content = gzip.open(fname).read()
  print fname

  jsons = []
  arr = content.splitlines()
  for e in arr:
    jsons.append(json.loads(e))

  os.remove(fname)

  return jsons


def getLocation(userLocation):
  try:
    l = Location.objects.get(location=userLocation)
  except Location.DoesNotExist:
    userLocation.replace(' ', '+')

    link= 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&{}'
    url = link.format(urlencode({'address':userLocation.encode('utf-8')}))
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
      l = Location(location=userLocation, lat=pos['lat'], lng=pos['lng'])
      l.save()

  return l
