from django.db import models

class Location(models.Model):
  location = models.CharField(primary_key=True, max_length = 255)
  lat = models.FloatField()
  lng = models.FloatField()

  def __unicode__(self):
    return "%s: (lat: %3.15f, lng: %3.15f)" %(self.location, self.lat, self.lng)

class User(models.Model):
  uid = models.IntegerField(primary_key=True)
  name = models.TextField()
  location = models.ForeignKey(Location)

  def __unicode__(self):
    return "%d: %s (%s)" % (self.uid, self.name, self.location)

  def __str__(self):
    return "%d: %s (%s)" % (self.uid, self.name, self.location)

  def __repr__(self):
    return "%d: %s (%s)" % (self.uid, self.name, self.location)
