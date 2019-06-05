import logging
from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')


class StockTransfer(OdooRepo):
    _name = 'stock_transfers'
    _model = 'stock.transfer'
    _mapping = {
        'update': 'api_update_status_from_wms',
    }
