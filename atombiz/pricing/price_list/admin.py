from django.contrib import admin

from .models import *

class PriceListAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price_list', 'currency']
    list_filter = ['is_so_price_list', 'enforce_price_limit']

admin.site.register(PriceList, PriceListAdmin)
