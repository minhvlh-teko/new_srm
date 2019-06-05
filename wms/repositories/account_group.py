import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountGroup(OdooRepo):
    _name = 'account_group'
    _model = 'account.group'
