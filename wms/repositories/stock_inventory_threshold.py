import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class StockInventoryThreshold(OdooRepo):
    _name = 'stock_inventory_threshold'
    _model = 'stock.inventory.threshold'
