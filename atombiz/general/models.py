from django.db import models

from general_ledger.models import ChartMaster


class Currency(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField('ISO 4217 code', max_length=3, unique=True)
    country = models.CharField(max_length=64)
    hundreds_name = models.CharField('hundredths name', max_length=16, default='Cents')
    decimal_places = models.SmallIntegerField('Decimal places to display')
    rate = models.DecimalField(max_digits=16, decimal_places=4)
    
    class Meta:
        verbose_name_plural = 'currencies'
    
    def __unicode__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=64)
    number = models.CharField('official company number', max_length=32, blank=True)
    gst_no = models.CharField('tax authority reference', max_length=32, blank=True)
    address = models.TextField()
    telephone = models.CharField(max_length=32)
    fax = models.CharField(max_length=32, blank=True)
    email = models.EmailField()
    currency = models.ForeignKey(Currency)
    debtor_account = models.ForeignKey(ChartMaster, related_name='company_debtors')
    creditor_account = models.ForeignKey(ChartMaster, related_name='company_creditors')
    payroll_account = models.ForeignKey(ChartMaster, related_name='company_payrolls')
    good_received_account = models.ForeignKey(ChartMaster, related_name='company_good_received')
    retained_earning_account = models.ForeignKey(ChartMaster, related_name='company_retained_earnings')
    freight_account = models.ForeignKey(ChartMaster, related_name='company_freights')
    sales_exchange_account = models.ForeignKey(ChartMaster, related_name='company_sales_exchange')
    purchase_exchange_account = models.ForeignKey(ChartMaster, related_name='company_purchase_exchange')
    payment_discount_account = models.ForeignKey(ChartMaster, related_name='company_payment_discount')
    gl_link_debtors = models.BooleanField(default=True)
    gl_link_creditors = models.BooleanField(default=True)
    gl_link_stock = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'companies'
    
    def __unicode__(self):
        return self.name
    