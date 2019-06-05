import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountTaxGroup(OdooRepo):
    _name = 'account_tax_group'
    _model = 'account.tax.group'
