import logging
from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')


class AccountInvoice(OdooRepo):
    _name = 'account_invoices'
    _model = 'account.invoice'
    _mapping = {
        'create': 'api_on_wms_invoice_created',
    }
