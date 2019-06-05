import logging

from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')


class PorPrices(OdooRepo):
    _name = 'por_prices'
    _model = 'product.product'
    _mapping = {
        'list': 'api_get_por_price',
        'create': 'api_get_por_price',  # support POST method for long list of products
    }
