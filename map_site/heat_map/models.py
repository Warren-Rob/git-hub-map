from django.db import models

# create database mapdb CHARACTER SET utf8 COLLATE utf8_general_ci;
class Location(models.Model):
  location = models.CharField(primary_key=True, max_length = 255)
  lat = models.FloatField()
  lng = models.FloatField()

  def __unicode__(self):
    return "%s: (lat: %3.10f, lng: %3.10f)" % (self.location, self.lat, self.lng)

class User(models.Model):
  name = models.TextField()
  location = models.ForeignKey(Location)

  def __unicode__(self):
    return "%s (%s)" % (self.name, self.location)

# owner no longer FK - don't want to use github api to get UID
class Repo(models.Model):
  rid = models.IntegerField(primary_key=True)
  name = models.TextField()
  owner = models.TextField()

  def __unicode__(self):
    return "%s (%d) owned by %s" % (self.name, self.rid, self.owner)

class PushEvent(models.Model):
  actor = models.ForeignKey(User)
  repo = models.ForeignKey(Repo)
  ref = models.TextField()
  size = models.IntegerField() # number of commits

