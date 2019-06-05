import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class AccountInvoice(OdooRepo):
    _name = 'invoices'
    _model = 'teko.account.invoice.status'
    _mapping = {
        'update': 'api_update_status_invoice',
    }
