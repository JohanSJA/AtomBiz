from django.db import models
from django.contrib.auth.models import User, Group

from base.models import Sequence, Currency

class FinancialReport(models.Model):
    TYPES = (
        ('sum', 'View'),
        ('accounts', 'Accounts'),
        ('account_type', 'Account type'),
        ('account_report', 'Report value')
    )
    SIGNS = (
        (-1, 'Reverse balance sign'),
        (1, 'Preserve balance sign')
    )
    DISPLAY_DETAILS = (
        ('no_detail', 'No detail'),
        ('detail_flat', 'Display children flat'),
        ('detail_with_hierarchy', 'Display children with hierarchy')
    )
    STYLE_OVERWRITES = (
        (0, 'Automatic formatting'),
        (1, 'Main title 1 (bold, underlined)'),
        (2, 'Title 2 (bold)'),
        (3, 'Title 3 (bold, smaller)'),
        (4, 'Normal text'),
        (5, 'Italic text (smaller)'),
        (6, 'Smallest text')
    )

    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    type = models.CharField(max_length=16, choices=TYPES, default='sum')
    account_report = models.ForeignKey('self', related_name='subreports', null=True, blank=True)
    sign = models.IntegerField(choices=SIGNS, default=1)
    display_detail = models.CharField(max_length=32, choices=DISPLAY_DETAILS, default='detail_flat')

    def __unicode__(self):
        return self.name


class AccountType(models.Model):
    CLOSE_METHODS = (
        ('none', 'None'),
        ('balance', 'Balance'),
        ('detail', 'Detail'),
        ('unreconciled', 'Unreconciled')
    )
    REPORT_TYPES = (
        ('none', '/'),
        ('income', 'Profit & Loss (Income account)'),
        ('expense', 'Profit & Loss (Expense account)'),
        ('asset', 'Balance Sheet (Asset account)'),
        ('liability', 'Balance Sheet (Liability account)')
    )

    name = models.CharField(max_length=64)
    code = models.CharField(max_length=32)
    close_method = models.CharField(max_length=16, choices=CLOSE_METHODS, default='none',
            help_text="""Set here the method that will be used to generate the end of year journal entries for all the accounts of this type.<br />
            <br />
            'None' means that nothing will be done.<br />
            'Balance' will general be used for cash accounts.<br />
            'Detail' will copy each existing journal item of the previous year, even the reconciled ones.<br />
            'Unreconciled' will copy only the journal items that were unreconciled on the first day of the new fiscal year.""")
    report_type = models.CharField(max_length=16, choices=REPORT_TYPES, default='none',
            help_text='This field is used to generate legal reports: profit and loss, balance sheet.'
        )
    note = models.TextField('description', blank=True)

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.name


class Account(models.Model):
    TYPES = (
        ('view', 'View'),
        ('other', 'Regular'),
        ('receivable', 'Receivable'),
        ('payable', 'Payable'),
        ('liquidity', 'Liquidity'),
        ('consolidation', 'Consolidation'),
        ('closed', 'Closed')
    )
    CURRENCY_MODES = (
        ('current', 'At date'),
        ('average', 'Average rate')
    )

    name = models.CharField(max_length=256)
    currency = models.ForeignKey(Currency, null=True, blank=True,
            help_text='Forces all moves for this account to have this secondary currency.')
    code = models.CharField(max_length=64, unique=True)
    type = models.CharField('internal type', max_length=16, choices=TYPES, default='other',
            help_text="""The 'Internal Type' is used for features available on
            different types of accounts: views can not have journal items, consolidation are accounts that
            can have children accounts for multi-company consolidations, payable/receivable are for
            partners accounts (for debit/credit computations), closed for depreciated accounts.""")
    user_type = models.ForeignKey(AccountType, verbose_name='account type',
            help_text='Account Type is used for information purpose, to generate country-specific legal reports, and set the rules to close a fiscal year and generate opening entries.')
    financial_report = models.ManyToManyField(FinancialReport)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    reconcile = models.BooleanField('allow reconciliation', default=False,
            help_text='Check this box if this account allows reconciliation of journal items.')
    shortcut = models.CharField(max_length=16)
    note = models.TextField('internal notes', blank=True)
    active = models.BooleanField(default=True,
            help_text='If the active field is set to False, it will allow you to hide the account without removing it.')
    currency_mode = models.CharField(max_length=8, choices=CURRENCY_MODES, default='current',
            help_text="""This will select how the current currency rate for outgoing transactions is computed.
            In most countries the legal method is "average" but only a few software systems are able to
            manage this. So if you import from another software system you may have to use the rate at date.
            Incoming transactions always use the rate at date.
            """)

    def __unicode__(self):
        return self.name


# class TaxCode(models.Model):
#     name = models.CharField(max_length=64)
#     code = models.CharField(max_length=64)
#     info = models.TextField(blank=True)
#     parent = models.ForeignKey('self')
#     sign = models.FloatField()
#     not_printable = models.BooleanField()
#     sequence = models.IntegerField()

#     def __unicode__(self):
#         return self.name


# class Tax(models.Model):
#     TYPES = (
#         ('percent', 'Percentage'),
#         ('fixed', 'Fixed'),
#         ('balance', 'Balance')
#     )
#     TYPE_TAX_USES = (
#         ('sale', 'Sale'),
#         ('purchase', 'Purchase'),
#         ('all', 'All')
#     )

#     name = models.CharField(max_length=64, unique=True)
#     sequence = models.IntegerField(default=1)
#     amount = models.FloatField(default=0)
#     active = models.BooleanField(default=True)
#     type = models.CharField(max_length=8, choices=TYPES, default='percent')
#     account_collected = models.ForeignKey(Account)
#     account_paid = models.ForeignKey(Account)
#     parent = models.ForeignKey('self')
#     child_depend = models.BooleanField()
#     base_code = models.ForeignKey(TaxCode)
#     tax_code = models.ForeignKey(TaxCode)
#     base_sign = models.FloatField(default=1)
#     tax_sign = models.FloatField(default=1)
#     ref_base_code = models.ForeignKey(TaxCode)
#     ref_tax_code = models.ForeignKey(TaxCode)
#     ref_base_sign = models.FloatField(default=1)
#     ref_tax_code = models.FloatField(default=1)
#     include_base_amount = models.BooleanField(default=False)
#     price_include = models.BooleanField(default=False)
#     type_tax_use = models.CharField(max_length=8, choices=TYPE_TAX_USES, default='all')

#     class Meta:
#         ordering = ['sequence']

#     def __unicode__(self):
#         return self.name


# class Journal(models.Model):
#     TYPES = (
#         ('sale', 'Sale'),
#         ('sale_refund', 'Sale refund'),
#         ('purchase', 'Purchase'),
#         ('purchase_refund', 'Purchase refund'),
#         ('cash', 'Cash'),
#         ('bank', 'Bank and checks'),
#         ('general', 'General'),
#         ('situation', 'Opening/Closing situation')
#     )

#     with_last_closing_balance = models.BooleanField('Opening with last closing balance', default=False)
#     name = models.CharField(max_length=64, unique=True)
#     code = models.CharField(max_length=5, unique=True)
#     type = models.CharField(max_length=32, choices=TYPES)
#     account_type = models.ManyToManyField(AccountType)
#     account_control = models.ManyToManyField(Account)
#     default_credit_account = models.ForeignKey(Account)
#     default_debit_account = models.ForeignKey(Account)
#     centralization = models.BooleanField('centralized counterpart')
#     update_posted = models.BooleanField('allow cancelling entries')
#     group_invoice_lines = models.BooleanField()
#     sequence = models.ForeignKey(Sequence)
#     user = models.ForeignKey(User)
#     groups = models.ManyToManyField(Group)
#     currency = models.ForeignKey(Currency)
#     entry_posted = models.BooleanField()
#     allow_date = models.BooleanField('check date in period')
#     profit_account = models.ForeignKey(Account)
#     loss_account = models.ForeignKey(Account)
#     internal_account = models.ForeignKey(Account, verbose_name='internal transfers account')
#     cash_control = models.BooleanField(default=False)

#     class Meta:
#         ordering = ['-code']

#     def __unicode__(self):
#         return self.name
