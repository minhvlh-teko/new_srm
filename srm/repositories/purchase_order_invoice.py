import logging
from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')

class PurchaseOrderInvoice(OdooRepo):
    _name = 'po_invoices'
    _model = 'purchase.order'
    _mapping = {
        'update': 'api_on_po_invoice_updated',
    }
