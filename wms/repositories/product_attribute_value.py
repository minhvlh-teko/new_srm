import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductAttributeValue(OdooRepo):
    _name = 'product_attribute_value'
    _model = 'product.attribute.value'
