from django.db import models

class Type(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name
