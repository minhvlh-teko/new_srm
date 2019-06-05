import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PoTypeDetail(OdooRepo):
    _name = 'po_type_details'
    _model = 'teko.po.type.detail'
