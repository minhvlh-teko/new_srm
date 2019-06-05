import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class Supplier(OdooRepo):
    _name = 'res_partners'
    _model = 'res.partner'

