from django.db import models

from taxes.models import Province, Group
from accounts.models import Master


class Location(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=64, unique=True)
    contact = models.CharField(max_length=32)
    address = models.TextField()
    tel = models.CharField(max_length=32, blank=True)
    fax = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    tax = models.ForeignKey(Province)
    internal_request = models.BooleanField(default=True, help_text='Allow or not internal request from this location.')

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.name


class Shipper(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    TYPES = (
        ('F', 'Finished Goods'),
        ('M', 'Raw Materials'),
        ('D', 'Dummy Item - (No movements)'),
        ('L', 'Labour')
    )

    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=1, choices=TYPES)
    gl = models.ForeignKey(Master, related_name='stock_cat', verbose_name='GL')
    wip_gl = models.ForeignKey(Master, related_name='stock_cat_wip', verbose_name='WIP GL')
    adjustment_gl = models.ForeignKey(Master, related_name='stock_cat_adj', verbose_name='adjustments GL')
    issues_gl = models.ForeignKey(Master, related_name='stock_cat_issues', verbose_name='internal stock issues GL')
    price_gl = models.ForeignKey(Master, related_name='stock_cat_price', verbose_name='price variance GL')
    usage_gl = models.ForeignKey(Master, related_name='stock_cat_usage', verbose_name='usage variance GL')

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        verbose_name_plural = 'units of measure'

    def __unicode__(self):
        return self.name


class Master(models.Model):
    MB_FLAGS = (
        ('A', 'Assembly'),
        ('K', 'Kit'),
        ('M', 'Manufactured'),
        ('G', 'Phantom'),
        ('B', 'Purchased'),
        ('D', 'Service/Labour')
    )

    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category)
    order_quantity = models.SmallIntegerField('economic order quantity')
    packaged_volume = models.DecimalField('packaged volume (cubic feet)', max_digits=16, decimal_places=4)
    packaged_weight = models.DecimalField('packaged weight (lbs)', max_digits=16, decimal_places=4)
    uom = models.ForeignKey(UnitOfMeasure, verbose_name='units of measure')
    mb_flag = models.CharField('assembly, kit, manufactured or service', max_length=1, choices=MB_FLAGS)
    discountinued = models.BooleanField()
    controlled = models.BooleanField('batch, serial or lot control')
    serialized = models.BooleanField()
    perishable = models.BooleanField()
    barcode = models.CharField(max_length=32)
    discount_category = models.CharField(max_length=4)
    tax_category = models.ForeignKey(Group)
    pan_size = models.FloatField()
    shrinkage_factor = models.FloatField()

    def __unicode__(self):
        return self.name


class Status(models.Model):
    location = models.ForeignKey(Location)
    stock = models.ForeignKey(Master)
    quantity = models.FloatField()
    reorder_level = models.IntegerField()

    class Meta:
        unique_together = ('location', 'stock')
        verbose_name_plural = 'statuses'

    def __unicode__(self):
        return '{} at {}'.format(self.stock, self.location)
