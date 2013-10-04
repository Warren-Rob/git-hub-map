from django.db import models

class User(models.Model):
  pkey = models.IntegerField(primary_key=True)
  name = models.TextField()
  location = models.TextField()

  def __unicode__(self):
    return "%s (%s): %d" %(self.name, self.location, self.numcommits)

class Location(models.Model):
  location = models.TextField()
  lat = models.FloatField()
  lng = models.FloatField()

  def __unicode__(self):
    return "%s: (lat: %3.15f, lng: %3.15f)" %(self.name, self.lat, self.lng)
