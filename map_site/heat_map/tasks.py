import requests, gzip, json, os
from datetime import datetime
from celery.task import task
from urllib import urlencode, urlretrieve
from heat_map.models import User, Location, Repo, Event, CreateEvent, IssuesEvent, PushEvent

login = 'robforsythe'

@task(name='tasks.addEvents')
def addEvents():
  events = fetchJSON()

  for e in events:
    if validEvent(e['type']) and 'repository' in e:
      u = saveUser(e['actor'])

      if u == -1:
        break
      elif u == 0:
        continue
      else:
        r = saveRepo(e['repository'])
        saveEvent(e, u, r)


def saveUser(actor):
  try:
    u = User.objects.get(name=actor)
  except User.DoesNotExist:
    link = 'https://api.github.com/users/{0}'
    r = requests.get(link.format(actor), auth=(login, authToken))
    remaining = int(r.headers["x-ratelimit-remaining"])

    # how do we guarantee we extract all of the information?
    # switch login/auth? save position in file?
    if remaining == 0:
      print '***************OUT OF REQUESTS***************\n' * 3
      return None

    data = r.json()

    uid = data["id"]

    if 'location' in data and data['location'] != None:
      loc = data['location']
    else:
      loc = 'Antarctica'

    location = getLocation(loc)
    u = User(uid=uid, name=actor, location=location)
    u.save()

  return u


def saveRepo(repo):
  rid = repo['id']

  try:
    r = Repo.objects.get(rid=rid)
  except Repo.DoesNotExist:
    rname = repo['name']
    rowner = repo['owner']

    user = saveUser(rowner)

    r = Repo(rid=rid, name=rname, owner=user)
    r.save()

  return r


def saveEvent(event, user, repo):
  etype = event['type']

  if etype == 'CreateEvent':
    ctype = event['payload']['ref_type']

    c = CreateEvent(actor=user, repo=repo, ctype=ctype)
    c.save()

  elif etype == 'IssuesEvent':
    t = event['created_at']
    a = event['payload']['action']
    i = event['payload']['issue']

    i = IssuesEvent(actor=user, repo=repo, created_at=t, action=a, issue=i)
    i.save()

  elif etype == 'PushEvent':
    ptype = event['payload']['ref']

    p = PushEvent(actor=user, repo=repo, ref=ptype)
    p.save()

  else:
    e = Event(actor=user, repo=repo, etype=etype)
    e.save()


# soonest we can get is 3 hours back (PST)
# library for time calculations? (Babel, pytz)
def getDate():
  yr = str(datetime.now().year)
  mo = str(datetime.now().month)
  if len(mo) != 2:
    mo = '0' + mo

  day = str(datetime.now().day - 1)
  if len(day) != 2:
    day = '0' + day

  hr = str(datetime.now().hour)

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
