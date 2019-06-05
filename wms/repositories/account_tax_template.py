import logging

from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')


class AccountTaxTemplate(OdooRepo):
    _name = 'account_tax_template'
    _model = 'account.tax.template'
