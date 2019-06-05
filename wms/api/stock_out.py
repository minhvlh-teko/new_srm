# coding=utf-8
import logging
import json

import flask_restplus as _fr
from flask import request

from wms.helpers import request_helper
from .. import models
from ..services import odoo_service
from ..models.base import ResponseModel
from ..extensions import Namespace

__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('Stock Out', description='StockOut operations')

# Define Schemas for Request and Response API decorator here
_stock_out_request_req = ns.model('stock_out_request_req', models.StockOutSchema.stock_out_request_req)
_stock_out_confirm_req = ns.model('stock_out_confirm_req', models.StockOutSchema.stock_out_confirm_req)

_stock_out_result = ns.model('stock_out_result', {
    'requestCode': _fr.fields.String()
})

_success_res = ns.clone('stock_out_success', ResponseModel.success_response, {
    'result': _fr.fields.Nested(_stock_out_result)
})
_error_res = ns.clone('stock_out_error', ResponseModel.error_response)


@ns.route('/', methods=['POST', 'PUT'], )
class StockOut(_fr.Resource):
    @ns.expect(_stock_out_request_req, validate=True)
    @ns.response(403, 'Order canceled', _error_res)
    @ns.marshal_with(_success_res, description='Confirm order request', code=200)
    def post(self):
        """
        Request to pick up product
        """
        data = request.json
        data.update(request_helper.get_special_params())
        _logger.debug("Request to pick up product: %s" % data)
        return odoo_service.call_odoo_repo('StockOutRequest', 'create', data=data, module_name='stock_out')

    @ns.expect(_stock_out_confirm_req, validate=True)
    @ns.marshal_with(_success_res, description='Confirm order request', code=200)
    @ns.response(403, 'Underselling', _error_res)
    def put(self):
        """
        Confirm pick up product
        """
        data = request.json
        data.update(request_helper.get_special_params())
        _logger.debug("Request to pick up product: %s" % data)
        return odoo_service.call_odoo_repo('StockOutConfirm', 'create', data=data, module_name='stock_out')
