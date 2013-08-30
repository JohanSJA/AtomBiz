from django.contrib import admin

from .models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'tax']


admin.site.register(Location, LocationAdmin)
admin.site.register(Shipper)
