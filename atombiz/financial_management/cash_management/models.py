from django.db import models

from common.currency.models import Currency

class CashBook(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    currency = models.ForeignKey(Currency)
    
    def __unicode__(self):
        return self.name
