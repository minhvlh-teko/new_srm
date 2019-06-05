import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductTemplate(OdooRepo):
    _name = 'product_templates'
    _model = 'product.template'
