# coding=utf-8

import logging

from flask_restplus import fields, Model
from .base import ResponseModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class LocationSchema:
    location = {
        'code': fields.String(required=True, description='location code'),
        'name': fields.String(required=False, description='location name'),
        'parentCode': fields.String(required=True, description='location parent code'),
    }

    location_res = location.copy()
    location_req = {}


class LocationMappingSchema:
    location_mapping_res = {
        'code': fields.String(required=True, description='location code'),
        'name': fields.String(required=False, description='location name'),
    }


class LocationModel:
    location = Model('location', {
        'code': fields.String(required=True, description='location code'),
        'name': fields.String(required=False, description='location name'),
        'parentCode': fields.String(required=True, description='location parent code'),
    })

    location_success = ResponseModel.success_response.clone('location_success', {
        'result': fields.List(fields.Nested(location))
    })

    location_mapping_success = ResponseModel.success_response.clone('location_mapping_success', {
        'result': fields.Raw(description="'location_code':'location_name'")
    })
