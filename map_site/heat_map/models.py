from django.db import models

class User(models.Model):
  name = models.TextField(primary_key=True)
  location = models.ForeignKey(Location, to_field='location')

  def __unicode__(self):
    return "%s (%s)" % (self.name, self.location)

class Location(models.Model):
  location = models.TextField()
  lat = models.FloatField()
  lng = models.FloatField()

  def __unicode__(self):
    return "%s: (lat: %3.15f, lng: %3.15f)" %(self.name, self.lat, self.lng)
