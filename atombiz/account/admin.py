from django.contrib import admin

from .models import *


class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'type', 'account_report']
    list_filter = ['type']


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'close_method', 'report_type']
    list_filter = ['report_type']


class AccountAdmin(admin.ModelAdmin):
    pass


class TaxCodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(FinancialReport, FinancialReportAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(TaxCode, TaxCodeAdmin)
