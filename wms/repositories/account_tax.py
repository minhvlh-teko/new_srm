import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountTax(OdooRepo):
    _name = 'account_tax'
    _model = 'account.tax'
