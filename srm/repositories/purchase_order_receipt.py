import logging
from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')


class PurchaseOrderReceipt(OdooRepo):
    _name = 'po_receipts'
    _model = 'purchase.order'
    _mapping = {
        'create': 'api_on_po_receipt_created',
        'update': 'api_on_po_receipt_updated',
    }
