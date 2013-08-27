from django.db import models
from django.core.exceptions import ValidationError

from common.currency.models import Currency

class PriceList(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    base_price_list = models.ForeignKey('self', null=True, blank=True)
    is_so_price_list = models.BooleanField(default=True)
    currency = models.ForeignKey(Currency)
    enforce_price_limit = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
    
    def clean(self):
        base = self.base_price_list
        
        while base:
            if self == self:
                raise ValidationError('This price list is already a base to the selected base price list.')
            base = base.base_price_list
            
