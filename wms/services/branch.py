# coding=utf-8
import logging

from ..repositories import branch

# from ..extensions.exceptions import BadRequestException

__author__ = 'Son'
_logger = logging.getLogger('api')


def get_branches(request):
    """
    Handle/verify data and business logic for branch
    :return:
    """
    # call repository branch
    return branch.Branch().get_branches(request)


def get_branch_mapping(request={}):
    """
    Handle/verify data and business logic for branch mapping
    :return:
    """
    # call repository branch
    return branch.BranchMapping().get_branch_mapping(request)
