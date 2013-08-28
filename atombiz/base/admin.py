from django.contrib import admin

from .models import *

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol']
    list_filter = ['active']


class SequenceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class SequenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'number_next']
    list_filter = ['active']


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(SequenceType, SequenceTypeAdmin)
admin.site.register(Sequence, SequenceAdmin)
