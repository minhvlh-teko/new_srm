import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountPaymentTermLine(OdooRepo):
    _name = 'account_payment_term_line'
    _model = 'account.payment.term.line'
