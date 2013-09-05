from django.contrib import admin

from .models import *


class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'tax']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'type', 'gl', 'adjustment_gl', 'issues_gl', 'price_gl', 'usage_gl', 'wip_gl']


admin.site.register(Location, LocationAdmin)
admin.site.register(Shipper)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UnitOfMeasure)
admin.site.register(Master)
admin.site.register(Status)
