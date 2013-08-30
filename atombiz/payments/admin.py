from django.contrib import admin

from .models import *


class TermAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'due_in_month', 'due_in_day']


admin.site.register(Term, TermAdmin)
