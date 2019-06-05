# coding=utf-8

import logging

from flask_restplus import fields, Model
from .base import ResponseModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class BranchSchema:
    branch = {
        'code': fields.String(required=True, description='branch code'),
        'name': fields.String(required=False, description='branch name'),
    }

    branch_res = branch.copy()
    branch_req = {}


class BranchMappingSchema:
    branch_mapping_res = {
        'code_1': fields.String(required=False, description='branch name'),
        'code_2': fields.String(required=False, description='branch name'),
        'code_n': fields.String(required=False, description='branch name')
    }


class BranchModel:
    branch = Model('branch', {
        'code': fields.String(required=True, description='branch code'),
        'name': fields.String(required=True, description='branch name'),
    })

    branch_success = ResponseModel.success_response.clone('branch_success', {
        'result': fields.List(fields.Nested(branch))
    })

    branch_error = ResponseModel.error_response.clone('branch_error')

    branch_mapping = Model('branch_mapping')

    branch_mapping_success = ResponseModel.success_response.clone('branch_mapping_success', {
        'result': fields.Raw(description="'branch_code':'branch_name'")
    })
