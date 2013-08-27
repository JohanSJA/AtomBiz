from django.db import models

class Currency(models.Model):
    iso_code = models.CharField(max_length=3, unique=True, help_text='Three letter ISO 4217 Code')
    symbol = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name_plural = 'currencies'
    
    def __unicode__(self):
        return self.iso_code

    def get_symbol(self):
        if self.symbol:
            return self.symbol
        else:
            return self.iso_code
