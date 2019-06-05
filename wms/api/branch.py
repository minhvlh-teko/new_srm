# coding=utf-8
import logging
import json

import flask_restplus as _fr
from flask import request

from .. import services, models
from ..extensions import Namespace
from ..models import BranchModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('Branches', description='Branch operations')

# Register Schemas for Request and Response API decorator here
ns.models[BranchModel.branch.name] = BranchModel.branch
ns.models[BranchModel.branch_error.name] = BranchModel.branch_error
ns.models[BranchModel.branch_success.name] = BranchModel.branch_success
ns.models[BranchModel.branch_mapping_success.name] = BranchModel.branch_mapping_success


@ns.route('/', methods=['GET'])
class Branches(_fr.Resource):
    @ns.marshal_with(BranchModel.branch_success, description="Successful Return")
    def get(self):
        """
        Get list all branches
        :return: list[Branch] - list all branches
        """
        data = request.args
        response = services.branch.get_branches(data)
        return response


@ns.route('/mapping', methods=['GET'], doc=False)
class BranchMapping(_fr.Resource):
    @ns.marshal_with(BranchModel.branch_mapping_success, as_list=True)
    def get(self):
        """
        Get list all branches mapping
        :return: list[Branch] - list all branches
        """
        data = request.args
        response = services.branch.get_branch_mapping(data)
        return response
