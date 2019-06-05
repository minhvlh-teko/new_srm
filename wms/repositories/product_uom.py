import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductUom(OdooRepo):
    _name = 'product_uom'
    _model = 'product.uom'
    _faker_data = {
        # 'post': {
        #     'req': {
        #         '__data': True,
        #         '__lang': False,
        #         '__ts': False,
        #         '__origin_model': False,
        #         '__seq_num': False,
        #         '__origin_id': False,
        #         '__sign': False,
        #     },
        #     'res': {'result': {'message': 'OK', 'code': 0}, 'message': '', 'code': 200}
        # },
        # 'put': {
        'req': {
            'id': True,
            '__vals': True,
            '__lang': False,
            '__ts': False,
            '__origin_model': False,
            '__seq_num': False,
            '__origin_id': False,
            '__sign': False,
            '__login': False,
            'name': False,
        },
        'res': {'message': 'OK', 'code': 0}
        # },
        # 'delete': {
        #     'req': {
        #         'id': True,
        #         '__ts': False,
        #         '__seq_num': False,
        #         '__origin_model': False,
        #         '__origin_id': False,
        #         '__sign': False,
        #     },
        #     'res': {'result': {'message': 'OK', 'code': 0}, 'message': '', 'code': 200}
        # },
    }
