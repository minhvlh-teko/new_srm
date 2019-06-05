import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductPricelistItem(OdooRepo):
    _name = 'pricelist_items'
    _model = 'product.pricelist.item'
