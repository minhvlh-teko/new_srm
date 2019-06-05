import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PoType(OdooRepo):
    _name = 'po_types'
    _model = 'teko.po.type'
