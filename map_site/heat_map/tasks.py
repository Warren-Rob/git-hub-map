import requests, os
from celery import task
from heat_map.models import User

"""can use "if-modified-since" statement for updating periodically?"""

login = 'rforsythe'
authToken = os.environ['AUTH0']

@task(name='tasks.populateDB')
def populateDB():
  link = "https://api.github.com/users?since={0}"
  if User.objects.count() == 0:
    lastUserId = 0
  else:
    lastUserId = User.objects.latest('pkey').pkey

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

        if (loc != None):
          print uname, loc # debug
          u = User(pkey=uid, name=uname, location=loc, numcommits=0)
          u.save()

    lastUserId = int(data[len(data)-1]['id'])

def getUserLocation(user):
  link = "https://api.github.com/users/{0}".format(user)
  uinfo = requests.get(link, auth=(login, authToken)).json()

  if 'location' in uinfo and uinfo["location"] != "null":
    return uinfo['location']

  return None
