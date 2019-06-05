import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductAttribute(OdooRepo):
    _name = 'product_attribute'
    _model = 'product.attribute'
