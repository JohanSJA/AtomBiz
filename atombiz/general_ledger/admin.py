from django.contrib import admin

from .models import *


class AccountSectionAdmin(admin.ModelAdmin):
    list_display = ['number', 'name']


class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'pandl', 'sequence', 'parent']
    list_filter = ['section', 'pandl']


class ChartMasterAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'group']
    list_filter = ['group']


admin.site.register(AccountSection, AccountSectionAdmin)
admin.site.register(AccountGroup, AccountGroupAdmin)
admin.site.register(ChartMaster, ChartMasterAdmin)
