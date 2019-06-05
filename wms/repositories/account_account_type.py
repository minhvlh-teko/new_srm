import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountAccountType(OdooRepo):
    _name = 'account_account_type'
    _model = 'account.account.type'
