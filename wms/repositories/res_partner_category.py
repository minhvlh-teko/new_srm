import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ResPartnerCategory(OdooRepo):
    _name = 'res_partner_category'
    _model = 'res.partner.category'
