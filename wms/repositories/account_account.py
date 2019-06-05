import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountAccount(OdooRepo):
    _name = 'account_account'
    _model = 'account.account'
