import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductProduct(OdooRepo):
    _name = 'products'
    _model = 'product.product'
