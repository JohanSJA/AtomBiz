from django.db import models

class Currency(models.Model):
    POSITIONS = (
        ('after', 'After amount'),
        ('before', 'Before amount')
    )

    name = models.CharField(max_length=4, help_text='ISO 4217', unique=True)
    symbol = models.CharField(max_length=4, blank=True)
    rounding = models.DecimalField(max_digits=16, decimal_places=8, default=0.01, null=True, blank=True)
    active = models.BooleanField(default=True)
    position = models.CharField(max_length=8, choices=POSITIONS, default='after',
            help_text='Determine where the currency symbol should be placed after or before the amount.'
        )

    class Meta:
        verbose_name_plural = 'currencies'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class SequenceType(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Sequence(models.Model):
    name = models.CharField(max_length=64)
    type = models.ForeignKey(SequenceType)
    active = models.BooleanField(default=True)
    prefix = models.CharField(max_length=64, blank=True, help_text='Prefix value of the record for the sequence.')
    suffix = models.CharField(max_length=64, blank=True, help_text='Suffix value of the record for the sequence.')
    number_next = models.IntegerField('next number', default=1, help_text='Next number that will be used.')
    number_increment = models.IntegerField(default=1, help_text='The next number of the sequence will be incremented by this number.')
    padding = models.IntegerField(default=0, help_text="System will automatically some some '0' to the left of the 'Next number' to get the required padding size.")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
