from django.contrib import admin

from .models import *

class CashBookAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency']
    list_filter = ['currency']

admin.site.register(CashBook, CashBookAdmin)
