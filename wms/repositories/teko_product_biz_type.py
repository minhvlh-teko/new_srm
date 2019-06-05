import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class TekoProductBizType(OdooRepo):
    _name = 'teko_product_biz_type'
    _model = 'teko.product.biz.type'
