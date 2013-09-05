from django.contrib import admin

from .models import *


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'decimal_places', 'hundreds_name', 'rate']


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Company)
