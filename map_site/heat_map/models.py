from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
        
    
           



