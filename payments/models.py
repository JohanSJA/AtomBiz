from django.db import models


class Term(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=64)
    due_after_given = models.BooleanField('due after a given number of days')
    days = models.SmallIntegerField(help_text='days (or day in the following month)')

    def __unicode__(self):
        return self.code

    def due_in_month(self):
        if self.due_after_given:
            return None
        else:
            return self.days

    def due_in_day(self):
        if self.due_after_given:
            return self.days
        else:
            return None
