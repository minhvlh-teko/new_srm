import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductBrand(OdooRepo):
    _name = 'brands'
    _model = 'product.brand'
    _faker_data = {
        'create': {
            'req': {
                "__seq_num": True,
                "__ts": True,
                "__data": True,
                "__origin_model": True,
                "__lang": True,
                "__origin_id": True,
                "__sign": True
            },
            'res': {
                "code": 0,
                "message": "OK"
            }
        }
    }