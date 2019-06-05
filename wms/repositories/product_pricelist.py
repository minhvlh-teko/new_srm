import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductPricelist(OdooRepo):
    _name = 'pricelists'
    _model = 'product.pricelist'
