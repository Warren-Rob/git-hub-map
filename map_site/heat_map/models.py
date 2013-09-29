from django.db import models

class User(models.Model):
    pkey = models.IntegerField(primary_key=True)
    name = models.TextField()
    location = models.TextField()
    numcommits = models.IntegerField()

class Location(models.Model):
    place = models.TextField()
    lon = models.FloatField()
    lat = models.FloatField()

    def __unicode__(self):
        return self.name
