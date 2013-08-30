from django.db import models

class CreditStatus(models.Model):
    code = models.SmallIntegerField(unique=True)
    name = models.CharField(max_length=32)
    disallow_invoices = models.BooleanField()
    
    class Meta:
        verbose_name_plural = 'credit statuses'
        ordering = ['code']
    
    def __unicode__(self):
        return self.name
