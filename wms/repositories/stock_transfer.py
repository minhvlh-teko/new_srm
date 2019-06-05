import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class StockTransfer(OdooRepo):
    _name = 'stock_transfers'
    _model = 'stock.transfer'
    _mapping = {
        'create': 'api_create_from_srm',
    }
