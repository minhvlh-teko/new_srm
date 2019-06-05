import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ResPartnerBank(OdooRepo):
    _name = 'res_partner_bank'
    _model = 'res.partner.bank'
