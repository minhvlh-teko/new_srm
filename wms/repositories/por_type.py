import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class PorType(OdooRepo):
    _name = 'por_types'
    _model = 'teko.por.type'
