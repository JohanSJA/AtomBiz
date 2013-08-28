from django.contrib import admin

from .models import *


class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'type', 'account_report']
    list_filter = ['type']


admin.site.register(FinancialReport, FinancialReportAdmin)
