import logging
from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')




class StockPickingType(OdooRepo):
    _name = 'picking_types'
    _model = 'stock.picking.type'
