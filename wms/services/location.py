# coding=utf-8
import logging

from ..repositories import location

# from ..extensions.exceptions import BadRequestException

__author__ = 'Son'
_logger = logging.getLogger('api')


def get_locations(request):
    """
    Handle/verify data and business logic for location
    :return:
    """
    # call repository location
    return location.Location().get_locations(request)


def get_location_mapping(request={}):
    """
    Handle/verify data and business logic for location mapping
    :return:
    """
    # call repository location
    return location.LocationMapping().get_location_mapping(request)
