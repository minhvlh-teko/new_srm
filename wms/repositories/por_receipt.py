import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PorReceipt(OdooRepo):
    _name = 'por_receipts'
    _model = 'purchase.order'
    _mapping = {
        'create': 'api_create_por_stock_picking',
    }
