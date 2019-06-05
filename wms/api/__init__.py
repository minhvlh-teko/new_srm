# coding=utf-8
import logging

from flask import Blueprint
# from flask_restplus import Api
from ..extensions.custom_api import CustomApi
from ..extensions.exceptions import global_error_handler

# Import all necesary API NameSpace here
# from .user import ns as user_ns
from .branch import ns as branch_ns
from .location import ns as location_ns
from .warehouse import ns as warehouse_ns
from .srm_product import ns as srm_product_ns
from .stock_quant import ns as stock_quant_ns
from .stock_out import ns as stock_out_ns
from .internal_api import ns as internal_api_ns
from .eton_api import ns as eton_api_ns

__author__ = 'ThucNC'
_logger = logging.getLogger('api')

api_wms = Blueprint('api', __name__, url_prefix='/api/v2')

custom_definition = {
    'info': {
        'x-logo': {
            'url': 'https://teko-vn.github.io/api-docs/Teko-Logo-01.svg'
        }
    },
}

api = CustomApi(
    app=api_wms,
    version='1.0',
    title='Teko WMS API Specification',
    validate=False,
    description='This documentation describes APIs used in/exposed from Teko micro-services ecosystem \
    # Introduction\
    These specifications are following\
    [OpenAPI 3.0.0 format](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md).',
    license='Apache 2.0',
    license_url='http://www.apache.org/licenses/LICENSE-2.0.html',
    contact_email='son.lp@teko.vn'
    # doc='' # disable Swagger UI
)

# add custom definition
api.add_custom_definition(custom_definition)


def init_app(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    # Add all necesary namespace here
    # api.add_namespace(user_ns)
    api.add_namespace(branch_ns, tag_group_name='WMS', path='/branches')
    api.add_namespace(warehouse_ns, tag_group_name='WMS', path='/warehouses')
    api.add_namespace(location_ns, tag_group_name='WMS', path='/locations')
    api.add_namespace(stock_quant_ns, tag_group_name='WMS', path='/stock_quants')
    api.add_namespace(stock_out_ns, tag_group_name='WMS', path='/stock_out')

    api.add_namespace(srm_product_ns, tag_group_name='SRM', path='/srm_products')
    api.add_namespace(internal_api_ns, tag_group_name='WMS', path='/internals')

    api.add_namespace(eton_api_ns, tag_group_name='WMS', path='/external')

    app.register_blueprint(api_wms)
    api.error_handlers[Exception] = global_error_handler
