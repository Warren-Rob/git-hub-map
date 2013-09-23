from django.db import models

class User(models.Model):
    name = models.TextField()
    location = models.TextField()
    numcommits = models.IntegerField()

    def __unicode__(self):
        return self.name
        
    
           



