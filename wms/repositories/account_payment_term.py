import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountPaymentTerm(OdooRepo):
    _name = 'account_payment_term'
    _model = 'account.payment.term'
