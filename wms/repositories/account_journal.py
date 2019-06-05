import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountJournal(OdooRepo):
    _name = 'account_journal'
    _model = 'account.journal'
