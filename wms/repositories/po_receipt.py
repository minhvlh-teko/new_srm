import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PoReceipt(OdooRepo):
    _name = 'po_receipts'
    _model = 'purchase.order'
    _mapping = {
        'create': 'api_create_stock_picking',
    }
