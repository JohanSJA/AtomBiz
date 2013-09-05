from django.db import models


class Type(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Area(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Man(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32)
    tel = models.CharField(max_length=32)
    fax = models.CharField(max_length=32)
    commission_rate_1 = models.FloatField()
    breakpoint = models.DecimalField(max_digits=16, decimal_places=4)
    commission_rate_2 = models.FloatField()
    current = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'men'

    def __unicode__(self):
        return self.name
