from django.contrib import admin

from .models import *


class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'type', 'account_report']
    list_filter = ['type']


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'close_method', 'report_type']
    list_filter = ['report_type']


admin.site.register(FinancialReport, FinancialReportAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account)
admin.site.register(TaxCode)
admin.site.register(Tax)
admin.site.register(Journal)
