import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountAccountTag(OdooRepo):
    _name = 'account_account_tag'
    _model = 'account.account.tag'
