import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductSupplierInfo(OdooRepo):
    _name = 'supplierinfos'
    _model = 'product.supplierinfo'
