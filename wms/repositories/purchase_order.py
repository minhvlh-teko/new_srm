import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PurchaseOrder(OdooRepo):
    _name = 'purchase_orders'
    _model = 'purchase.order'
    _mapping = {
        'create': 'api_create_from_srm',
        'update': 'api_update_from_srm',
        'delete': 'api_delete_from_msg',
    }
