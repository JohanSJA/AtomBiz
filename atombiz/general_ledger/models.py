from django.db import models


class AccountSection(models.Model):
    number = models.SmallIntegerField(unique=True)
    name = models.CharField(max_length=64)
    
    class Meta:
        ordering = ['number']
    
    def __unicode__(self):
        return '{} ({})'.format(self.name, self.number)


class AccountGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    section = models.ForeignKey(AccountSection, verbose_name='section in accounts')
    pandl = models.BooleanField('profit and loss')
    sequence = models.SmallIntegerField('sequence in TB')
    
    class Meta:
        ordering = ['section']
    
    def __unicode__(self):
        return self.name
