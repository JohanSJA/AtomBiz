from django.contrib import admin

from .models import *


class CreditStatusAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'disallow_invoices']


admin.site.register(CreditStatus, CreditStatusAdmin)
admin.site.register(Type)
admin.site.register(Customer)
admin.site.register(Branch)
