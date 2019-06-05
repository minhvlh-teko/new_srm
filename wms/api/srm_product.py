# coding=utf-8
import logging
# import json

import flask_restplus as _fr
from flask import request

from .. import models
from ..services import odoo_service
from ..extensions import Namespace
from ..models.base import ResponseModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('SRM Products', description='SRM product operations')

# Define Schemas for Request and Response API decorator here
_srm_product_res = ns.model('srm_product_res', models.SrmProductSchema.srm_product_res)
_srm_product_req = ns.model('srm_product_item_req', models.SrmProductSchema.srm_product_req)

_srm_product_result = ns.model('srm_product_result', {
    'feId': _fr.fields.String(description='ID of record, empty if not exist')
})

_success_res = ns.clone('srm_product_success', ResponseModel.success_response, {
    'result': _fr.fields.Nested(_srm_product_result)
})
_error_res = ns.clone('srm_product_error', ResponseModel.error_response)


@ns.route('/', methods=['POST'])
class SrmProductLists(_fr.Resource):
    @ns.expect(_srm_product_req, validate=True)
    @ns.marshal_with(_success_res, as_list=False, description="Successful Creation", code=200)
    @ns.response(400, 'Category does not exist', _error_res)
    @ns.response(403, 'Insufficient permissions', _error_res)
    def post(self):
        """
        Create a product
        """
        data = request.args or request.json
        # rs = services.srm_product.create_srm_product(data)
        return odoo_service.call_odoo_repo('SrmProduct', 'create', data)


@ns.route('/<int:id>', methods=['PUT', 'DELETE'])
class SrmProductItem(_fr.Resource):
    @ns.expect(_srm_product_req, validate=True)
    @ns.marshal_with(_success_res, as_list=False, description="Successful Update")
    @ns.response(403, 'Insufficient permissions', _error_res)
    def put(self, id):
        """
        Update a product
        """
        data = request.args or request.json
        data['feId'] = id
        odoo_service.call_odoo_repo('SrmProduct', 'update', data)

    @ns.marshal_with(_success_res, as_list=False, description="Successful Delete")
    @ns.response(403, 'Insufficient permissions', _error_res)
    def delete(self, id):
        """
        Delete a product
        """
        return odoo_service.call_odoo_repo('SrmProduct', 'destroy', {'id': id})
