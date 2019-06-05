# coding=utf-8
import logging

from ..repositories import warehouse

# from ..extensions.exceptions import BadRequestException

__author__ = 'Son'
_logger = logging.getLogger('api')


def get_warehouses(request):
    """
    Handle/verify data and business logic for warehouse
    :return:
    """
    # call repository warehouse
    return warehouse.Warehouse().get_warehouses(request)


def get_warehouse_mapping(request={}):
    """
    Handle/verify data and business logic for warehouse mapping
    :return:
    """
    # call repository warehouse
    return warehouse.WarehouseMapping().get_warehouse_mapping(request)
