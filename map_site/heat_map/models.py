from django.db import models

class User(models.Model):
    pkey = models.IntegerField(primary_key=True)
    name = models.TextField()
    location = models.TextField()
    numcommits = models.IntegerField()

    def __unicode__(self):
        return self.name
