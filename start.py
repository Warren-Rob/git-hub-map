#!/usr/bin/python
import os
import sqlite3
import requests

class Backend:
  """can use "if-modified-since" statement for updating periodically."""

  def __init__(self):
    self.login = "rforsythe"
    self.authToken = os.environ["AUTH0"]
    self.conn = sqlite3.connect("database.db")

  def getUserList(self):
    link = "https://api.github.com/users?since={0}"
    insertStr = "INSERT INTO user VALUES ('{0}', '{1}', null)"
    remaining = 5000
    lastUserId = 0
    c = self.conn.cursor()

    while (remaining > 0):
      r = requests.get(link.format(lastUserId), auth=(self.login, self.authToken))
      remaining = int(r.headers["x-ratelimit-remaining"])

      for userInfo in r.json():
        if userInfo["type"] == "User":
          name = userInfo["login"]
          loc = self.getUserLocation(user)
          print name, loc # debug
          if (loc != None):
            c.execute(insertStr.format(name, loc))
          self.conn.commit()

      lastUserId = len(r.json())

  def getUserLocation(self, user):
    link = "https://api.github.com/users/{0}".format(user)
    uinfo = requests.get(link, auth=(self.login, self.authToken)).json()

    if 'location' in uinfo and uinfo["location"] != "null":
      return uinfo['location']

    return None

be = Backend()
be.getUserList()
