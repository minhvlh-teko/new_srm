import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductUomCateg(OdooRepo):
    _name = 'product_uom_categ'
    _model = 'product.uom.categ'
