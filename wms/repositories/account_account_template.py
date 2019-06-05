import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountAccountTemplate(OdooRepo):
    _name = 'account_account_template'
    _model = 'account.account.template'
