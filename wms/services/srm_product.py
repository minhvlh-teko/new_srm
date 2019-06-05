# coding=utf-8
import logging

from ..repositories import srm_product

# from ..extensions.exceptions import BadRequestException

__author__ = 'Son'
_logger = logging.getLogger('api')


# def get_srm_products(request):
#     """
#     Handle/verify data and business logic for srm_product
#     :return:
#     """
#     # call repository srm_product
#     return srm_product.SrmProduct().get_srm_products(request)


def create_srm_product(request={}):
    """
    Handle/verify data and business logic for srm_product mapping
    :return:
    """
    # call repository srm_product
    return srm_product.SrmProduct().create_srm_product(request)
