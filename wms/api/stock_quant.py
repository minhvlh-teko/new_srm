# coding=utf-8
import logging
import flask_restplus as _fr
from ..services import odoo_service
from ..extensions import Namespace
from ..models import StockQuantModel
from ..helpers import request_helper



__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('Stock Quantities', description='StockQuant operations', validate=True)

# Register Schemas for Request and Response API decorator here
ns.models[StockQuantModel.stock_quant.name] = StockQuantModel.stock_quant
ns.models[StockQuantModel.stock_quant_response.name] = StockQuantModel.stock_quant_response
ns.models[StockQuantModel.stock_quant_min.name] = StockQuantModel.stock_quant_min
ns.models[StockQuantModel.stock_quant_min_response.name] = StockQuantModel.stock_quant_min_response
ns.models[StockQuantModel.stock_quant_success.name] = StockQuantModel.stock_quant_success
ns.models[StockQuantModel.stock_quant_min_success.name] = StockQuantModel.stock_quant_min_success

# add multi params
_stock_quant_req = ns.parser()
_stock_quant_req.add_argument('products', type=int, location='args', help='List sku', required=True, action='append')
_stock_quant_req.add_argument('regions', type=int, location='args', help='Regions', action='append')
_stock_quant_req.add_argument('branches', type=str, location='args', help='Branches', action='append')
_stock_quant_req.add_argument('warehouses', type=str, location='args', help='Warehouses code', action='append')
_stock_quant_req.add_argument('locations', type=str, location='args', help='Locations', action='append')


@ns.route('/', methods=['GET'])
class StockQuants(_fr.Resource):
    @ns.expect(_stock_quant_req, validate=True)
    @ns.marshal_with(StockQuantModel.stock_quant_success, description="Successful Return")
    def get(self):
        """
        Get list all stock quants
        :return: list[StockQuant] - list all stock quants
        """

        data = dict(_stock_quant_req.parse_args())
        # TODO: get special params such as faker data
        data.update(request_helper.get_special_params())

        return odoo_service.call_odoo_repo('StockQuant', 'list', data)


@ns.route('/get_min', methods=['GET'])
class StockQuantsMin(_fr.Resource):
    @ns.expect(_stock_quant_req, validate=True)
    @ns.marshal_with(StockQuantModel.stock_quant_min_success, description="Successful Return")
    def get(self):
        """
        Get list all stock quants but for minimize properties
        :return: list[StockQuant] - list all stock quants
        """

        data = dict(_stock_quant_req.parse_args())
        # TODO: get special params such as faker data
        data.update(request_helper.get_special_params())

        return odoo_service.call_odoo_repo('StockQuant', 'list', data)
