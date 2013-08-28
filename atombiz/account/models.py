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


class TaxCode(models.Model):
    name = models.CharField('case name', max_length=64)
    code = models.CharField('case code', max_length=64, blank=True)
    info = models.TextField('description', blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    sign = models.FloatField('coefficent for parent', default=1.0,
            help_text='You can specify here the coefficient that will be used when consolidating the amount of this case into its parent. For example, set 1/-1 if you want to add/substract it.')
    not_printable = models.BooleanField('not printable in invoice', default=False,
            help_text="Check this box if you don't want any tax related to this tax code to appear in invoices.")
    sequence = models.IntegerField(null=True, blank=True,
            help_text="Determine the display order in the report 'Accounting \\ Reporting \\ Generic Reporting \\ Taxes \\ Taxes Report'")
    
    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.name


class Tax(models.Model):
    TYPES = (
        ('percent', 'Percentage'),
        ('fixed', 'Fixed'),
        ('balance', 'Balance')
    )
    TYPE_TAX_USES = (
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('all', 'All')
    )

    name = models.CharField('tax name', max_length=64, unique=True,
            help_text='This name will be displayed on reports.')
    sequence = models.IntegerField(default=1,
            help_text='The sequence field is used to order the tax lines from the lowest sequences to the higher ones. The order is important if you have a tax with several tax children. In this case, the evalution order is important.')
    amount = models.FloatField(default=0,
            help_text='For taxes of percentage, enter % ratio between 0-1')
    active = models.BooleanField(default=True,
            help_text='If the active field is set to False, it will allow you to hide the tax without removing it.')
    type = models.CharField('tax type', max_length=8, choices=TYPES, default='percent',
            help_text='The computation method for the tax amount.')
    account_collected = models.ForeignKey(Account, null=True, blank=True,
            verbose_name='invoice tax account', related_name='tax_collected',
            help_text='Set the account that will be set by default on invoice tax lines for invoices. Leave empty to use the expense account.')
    account_paid = models.ForeignKey(Account, null=True, blank=True,
            verbose_name='refund tax account', related_name='tax_paid',
            help_text='Set the account that will be set by default on invoice tax lines for refund. Leave empty to use the expense account.')
    parent = models.ForeignKey('self', verbose_name='parent tax account')
    child_depend = models.BooleanField('tax on children',
            help_text='Set if the tax computation is based on the computation of child taxes rather than on the total amount.')
    # Fields used for the Tax declaration
    base_code = models.ForeignKey(TaxCode, null=True, blank=True,
            verbose_name='account base code', related_name='tax_base',
            help_text='use this code for the tax declaration.')
    tax_code = models.ForeignKey(TaxCode, null=True, blank=True,
            verbose_name='account tax code', related_name='tax_tax',
            help_text='use this code for the tax declaration.')
    base_sign = models.FloatField(default=1, null=True, blank=True,
            help_text='Usually 1 or -1.')
    tax_sign = models.FloatField(default=1, null=True, blank=True,
            help_text='Usually 1 or -1.')
    # Same fields for refund invoices
    ref_base_code = models.ForeignKey(TaxCode, null=True, blank=True,
            verbose_name='refund base code', related_name='ref_tax_base',
            help_text='use this code for the tax declaration.')
    ref_tax_code = models.ForeignKey(TaxCode, null=True, blank=True,
            verbose_name='refund tax code', related_name='ref_tax_tax',
            help_text='use this code for the tax declaration.')
    ref_base_sign = models.FloatField(default=1, null=True, blank=True,
            help_text='Usually 1 or -1.')
    ref_tax_code = models.FloatField(default=1, null=True, blank=True,
            help_text='Usually 1 or -1.')
    include_base_amount = models.BooleanField('included in base amount', default=False,
            help_text='Indicates if the amout of tax must be included in the abase amount for the computation of the next taxes.')
    price_include = models.BooleanField('tax included in price', default=False,
            help_text='Check this if the price you use on the product and invoices includes this tax.')
    type_tax_use = models.CharField(max_length=8, choices=TYPE_TAX_USES, default='all')

    class Meta:
        ordering = ['sequence']

    def __unicode__(self):
        return self.name


class Journal(models.Model):
    TYPES = (
        ('sale', 'Sale'),
        ('sale_refund', 'Sale refund'),
        ('purchase', 'Purchase'),
        ('purchase_refund', 'Purchase refund'),
        ('cash', 'Cash'),
        ('bank', 'Bank and checks'),
        ('general', 'General'),
        ('situation', 'Opening/Closing situation')
    )

    with_last_closing_balance = models.BooleanField('Opening with last closing balance', default=False)
    name = models.CharField('journal name', max_length=64, unique=True)
    code = models.CharField(max_length=5, unique=True,
            help_text='The code will be displayed on reports.')
    type = models.CharField(max_length=32, choices=TYPES,
            help_text="""Select 'Sale' for customer invoices journals.<br />
            Select 'Purchase' for supplier invoices journals.<br />
            Select 'Cash' or 'Bank' for journals that are used in customer or supplier payments.<br />
            Select 'General' for miscellaneious operations journals.<br />
            Select 'Opening/Closing Situation' for entries generated for new fiscal years.""")
    account_type = models.ManyToManyField(AccountType, verbose_name='type controls')
    account_control = models.ManyToManyField(Account, verbose_name='account', related_name='journal_control',
            limit_choices_to={'type__in': ['other', 'receivable', 'payable', 'liquidity', 'consolidation']})
    default_credit_account = models.ForeignKey(Account, related_name='journal_default_credit',
            help_text='It acts as a default account for credit amount.',
            limit_choices_to={'type__in': ['other', 'receivable', 'payable', 'liquidity', 'consolidation', 'closed']})
    default_debit_account = models.ForeignKey(Account, related_name='journal_default_debit',
            help_text='It acts as a default account for debit amount.',
            limit_choices_to={'type__in': ['other', 'receivable', 'payable', 'liquidity', 'consolidation', 'closed']})
    centralization = models.BooleanField('centralized counterpart',
            help_text="Check this box to determine that each entry of this journal won't create a new counterpart but will share the same counterpart. This is used in fiscal year closing.")
    update_posted = models.BooleanField('allow cancelling entries',
            help_text='Check this box if you want to allow the cancellation the entries related to this journal or of the invoice related to this journal.')
    group_invoice_lines = models.BooleanField(help_text='If this box is checked, the system will try to group the accounting lines when generating them from invoices.')
    sequence = models.ForeignKey(Sequence, verbose_name='entry sequence',
            help_text='This field contains the information related to the numbering of the journal entries of this journal.')
    user = models.ForeignKey(User, help_text='The user responsible for this journal.')
    groups = models.ManyToManyField(Group)
    currency = models.ForeignKey(Currency, help_text='The currency used to enter statement.')
    entry_posted = models.BooleanField('autopost created moves', help_text='Check this box to automatically post entries of this journal. Note that legally, some entries may be automatically posted when the source document is validated (Invoices), whatever the status of this field.')
    allow_date = models.BooleanField('check date in period', help_text='If set to True then do not accept the entry if the entry date is not into the period dates.')
    profit_account = models.ForeignKey(Account, related_name='journal_profit')
    loss_account = models.ForeignKey(Account, related_name='journal_loss')
    internal_account = models.ForeignKey(Account, verbose_name='internal transfers account', related_name='journal_internal')
    cash_control = models.BooleanField(default=False, help_text='If you want the journal should be control at opening/closing, check this option.')

    class Meta:
        ordering = ['-code']

    def __unicode__(self):
        return self.name
