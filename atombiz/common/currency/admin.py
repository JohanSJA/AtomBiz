from django.contrib import admin

from .models import *

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['iso_code', 'symbol']

admin.site.register(Currency, CurrencyAdmin)
