# coding=utf-8
import logging

from ..extensions import reqparse
from flask import request

__author__ = 'ThucNC'
_logger = logging.getLogger('api')

_SPECIAL_PARAMS = [
    'no_cache',
    'use_faker',
    'debug'
]


def get_special_params():
    """
    Get special params from requests
    :return: dict: Params
    """
    data = request.args or request.json
    params = {}

    for param in _SPECIAL_PARAMS:
        if param in data:
            params[param] = data[param]
    return params


class RequestHelper:
    pagination_params = reqparse.RequestParser(bundle_errors=True)
    pagination_params.add_argument(
        'page',
        type=int,
        help='Page number, starting from 1',
        required=False,
        default=1,
        location='args'
    )

    pagination_params.add_argument(
        'pageSize',
        type=int,
        help='Page size',
        required=False,
        default=10,
        location='args'
    )
