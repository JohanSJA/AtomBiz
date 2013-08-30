from django.db import models

from taxes.models import Province


class Location(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=64, unique=True)
    contact = models.CharField(max_length=32)
    address = models.TextField()
    tel = models.CharField(max_length=32, blank=True)
    fax = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    tax = models.ForeignKey(Province)
    internal_request = models.BooleanField(default=True, help_text='Allow or not internal request from this location.')
    
    class Meta:
        ordering = ['code']
    
    def __unicode__(self):
        return self.name


class Shipper(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name
