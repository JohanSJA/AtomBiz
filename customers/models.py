from django.db import models

from general.models import Currency
from sales.models import Type as SType, Area, Man
from payments.models import Term
from stocks.models import Location, Shipper
from taxes.models import Group


class CreditStatus(models.Model):
    code = models.SmallIntegerField(unique=True)
    name = models.CharField(max_length=32)
    disallow_invoices = models.BooleanField()

    class Meta:
        verbose_name_plural = 'credit statuses'
        ordering = ['code']

    def __unicode__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=64)
    address = models.TextField()
    sales_type = models.ForeignKey(SType)
    customer_type = models.ForeignKey(Type)
    since = models.DateField()
    discount = models.FloatField('discount percent')
    discount_code = models.CharField(max_length=4)
    payment_discount = models.FloatField('payment discount percent')
    credit_limit = models.DecimalField(max_digits=16, decimal_places=4)
    tax_reference = models.CharField(max_length=32)
    payment_terms = models.ForeignKey(Term)
    credit_status = models.ForeignKey(CreditStatus)
    currency = models.ForeignKey(Currency)
    po_in_so = models.BooleanField('PO line in SO')
    invoice_to_ho = models.BooleanField('invoicing to HO')

    def __unicode__(self):
        return self.name

    def invoicing_address(self):
        if self.invoice_to_ho:
            return 'Invoicing to HO'
        else:
            return 'Invoicing to Branch'


class Branch(models.Model):
    code = models.CharField(max_length=16)
    customer = models.ForeignKey(Customer)
    name = models.CharField(max_length=64)
    address = models.TextField()
    instructions = models.TextField(blank=True)
    delivery_days = models.SmallIntegerField('estimated delivery days')
    forward_date = models.SmallIntegerField('forward date after')
    salesman = models.ForeignKey(Man)
    area = models.ForeignKey(Area)
    draw_stock = models.ForeignKey(Location)
    phone = models.CharField(max_length=32)
    fax = models.CharField(max_length=32)
    email = models.EmailField()
    tax_group = models.ForeignKey(Group)
    transaction_on = models.BooleanField('transaction on branch')
    shipper = models.ForeignKey(Shipper)
    packlist_details = models.BooleanField('show company details and logo', default=True)
    postal_address = models.TextField()
    internal_code = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'branches'
        unique_together = ('code', 'customer')

    def __unicode__(self):
        return self.name
