# coding=utf-8
import logging

from wms.helpers import request_helper
from ..extensions import Namespace
from flask_restplus import Resource
from ..models import EtonApiModel
from ..services import odoo_service
from flask import request

__author__ = 'Huu'
_logger = logging.getLogger('api')

ns = Namespace('External', description='External APIs')

# Register Schemas for Request and Response API decorator here
ns.models[EtonApiModel.eton_product.name] = EtonApiModel.eton_product
ns.models[EtonApiModel.eton_po_req.name] = EtonApiModel.eton_po_req
ns.models[EtonApiModel.eton_so_req.name] = EtonApiModel.eton_so_req
ns.models[EtonApiModel.eton_so_returned_req.name] = EtonApiModel.eton_so_returned_req
ns.models[EtonApiModel.eton_success_res.name] = EtonApiModel.eton_success_res


@ns.route('/po/<int:id>', methods=['PUT'])
@ns.doc(params={'id': 'The IN coupon ID of stock.picking needs to handle WMS'})
class ExternalPO(Resource):
    @ns.expect(EtonApiModel.eton_po_req, validate=True)
    @ns.marshal_with(EtonApiModel.eton_success_res, description='Operation succeed', code=200)
    def put(self, id):
        """
        Update PO status
        """
        data = request.get_json()
        data['_id'] = id
        data.update(request_helper.get_special_params())
        repo_name = 'ExternalIncomingReceived'
        return odoo_service.call_odoo_repo(repo_name, 'create', data=data)


@ns.route('/so/<int:id>', methods=['PUT'])
@ns.doc(params={'id': 'The Pick coupon ID of stock.picking needs to handle WMS'})
class ExternalSO(Resource):
    @ns.expect(EtonApiModel.eton_so_req, validate=True)
    @ns.marshal_with(EtonApiModel.eton_success_res, description='Successful updating', code=200)
    def put(self, id):
        """
        Update SO status by type (picked, packed, delivered)
        """
        data = request.get_json()
        data['_id'] = id
        data.update(request_helper.get_special_params())
        repo_name = None
        if data['eventType'] == 'picked':
            repo_name = 'ExternalOutgoingPicked'
        if data['eventType'] == 'packed':
            repo_name = 'ExternalOutgoingPacked'
        if data['eventType'] == 'delivered':
            repo_name = 'ExternalOutgoingDelivered'

        data.pop('eventType')

        return odoo_service.call_odoo_repo(repo_name, 'create', data=data)


@ns.route('/so/<int:id>/returned', methods=['PUT'])
@ns.doc(params={'id': 'The Pick coupon ID of stock.picking needs to handle WMS'})
class ExternalSOReturn(Resource):
    @ns.expect(EtonApiModel.eton_so_returned_req, validate=True)
    @ns.marshal_with(EtonApiModel.eton_success_res, description='Successful updating', code=200)
    def put(self, id):
        """
        Update SO status by type (returned)
        """
        data = request.get_json()
        data['_id'] = id
        data.update(request_helper.get_special_params())
        repo_name = 'ExternalOutgoingReturned'
        return odoo_service.call_odoo_repo(repo_name, 'create', data=data)