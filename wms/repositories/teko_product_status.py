import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class TekoProductStatus(OdooRepo):
    _name = 'product_status'
    _model = 'teko.product.status'
