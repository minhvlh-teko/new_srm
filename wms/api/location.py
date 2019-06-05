# coding=utf-8
import logging
import json

import flask_restplus as _fr
from flask import request

from .. import services, models
from ..extensions import Namespace
from ..models import LocationModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('Locations', description='Location operations')

# Register Schemas for Request and Response API decorator here
ns.models[LocationModel.location.name] = LocationModel.location
ns.models[LocationModel.location_success.name] = LocationModel.location_success
ns.models[LocationModel.location_mapping_success.name] = LocationModel.location_mapping_success


@ns.route('/', methods=['GET'])
class Locations(_fr.Resource):
    @ns.marshal_with(LocationModel.location_success, description="Successful Return")
    def get(self):
        """
        Get list all locations
        :return: list[Location] - list all locations
        """
        data = request.args
        location_list = services.location.get_locations(data)
        return location_list


@ns.route('/mapping', methods=['GET'], doc=False)
class LocationMapping(_fr.Resource):
    @ns.marshal_with(LocationModel.location_mapping_success)
    def get(self):
        """
        Get list all locations mapping
        :return: list[Location] - list all locations
        """
        data = request.args
        location_mapping_list = services.location.get_location_mapping(data)
        return location_mapping_list
