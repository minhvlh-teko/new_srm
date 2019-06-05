import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductCategory(OdooRepo):
    _name = 'categories'
    _model = 'product.category'
