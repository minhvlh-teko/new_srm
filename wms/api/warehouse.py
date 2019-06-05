# coding=utf-8
import logging
import json

import flask_restplus as _fr
from flask import request

from .. import services, models
from ..extensions import Namespace
from ..models import WarehouseModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('Warehouses', description='Warehouse operations')

# Register Schemas for Request and Response API decorator here
ns.models[WarehouseModel.warehouse.name] = WarehouseModel.warehouse
ns.models[WarehouseModel.warehouse_success.name] = WarehouseModel.warehouse_success
ns.models[WarehouseModel.warehouse_mapping_success.name] = WarehouseModel.warehouse_mapping_success


@ns.route('/', methods=['GET'])
class Warehouses(_fr.Resource):
    @ns.marshal_with(WarehouseModel.warehouse_success, description="Successful Return")
    def get(self):
        """
        Get list all warehouses
        :return: list[Warehouse]
        """
        data = request.args
        warehouse_list = services.warehouse.get_warehouses(data)
        return warehouse_list


@ns.route('/mapping', methods=['GET'], doc=False)
class WarehouseMapping(_fr.Resource):
    @ns.marshal_with(WarehouseModel.warehouse_mapping_success)
    def get(self):
        """
        Get list all warehouses mapping
        :return: list[Warehouse]
        """
        data = request.args
        warehouse_mapping_list = services.warehouse.get_warehouse_mapping(data)
        return warehouse_mapping_list
