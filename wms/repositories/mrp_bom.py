import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class MrpBom(OdooRepo):
    _name = 'mrp_bom'
    _model = 'mrp.bom'
