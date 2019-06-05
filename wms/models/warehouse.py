# coding=utf-8

import logging

from flask_restplus import fields, Model
from .base import ResponseModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class WarehouseSchema:
    warehouse = {
        'code': fields.String(required=True, description='warehouse code'),
        'name': fields.String(required=False, description='warehouse name'),
        'branchCode': fields.String(required=False, description='warehouse branch code'),
    }

    warehouse_res = warehouse.copy()
    warehouse_req = {}


class WarehouseMappingSchema:
    warehouse_mapping_res = {
        'code': fields.String(required=True, description='warehouse code'),
        'name': fields.String(required=False, description='warehouse name'),
    }


class WarehouseModel:
    warehouse = Model('warehouse', {
        'code': fields.String(required=True, description='warehouse code'),
        'name': fields.String(required=False, description='warehouse name'),
        'branchCode': fields.String(required=False, description='warehouse branch code'),
    })

    warehouse_success = ResponseModel.success_response.clone('warehouse_success', {
        'result': fields.List(fields.Nested(warehouse))
    })

    warehouse_mapping_success = ResponseModel.success_response.clone('warehouse_mapping_success', {
        'result': fields.Raw(description="'warehouse_code':'warehouse_name'")
    })
