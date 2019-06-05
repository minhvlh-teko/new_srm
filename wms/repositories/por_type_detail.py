import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PorTypeDetail(OdooRepo):
    _name = 'por_type_details'
    _model = 'teko.por.type.detail'
