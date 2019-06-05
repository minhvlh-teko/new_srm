import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ResPartnerIndustry(OdooRepo):
    _name = 'res_partner_industry'
    _model = 'res.partner.industry'
