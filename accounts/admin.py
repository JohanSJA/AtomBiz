from django.contrib import admin

from .models import *


class SectionAdmin(admin.ModelAdmin):
    list_display = ['number', 'name']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'pandl', 'sequence', 'parent']
    list_filter = ['section', 'pandl']


class MasterAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'group']
    list_filter = ['group']


admin.site.register(Section, SectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Master, MasterAdmin)
