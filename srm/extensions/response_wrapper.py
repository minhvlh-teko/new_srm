# coding=utf-8
import logging

__author__ = 'ThucNC'
_logger = logging.getLogger('api')


def wrap_response(data=None, message="", http_code=200):
    """
    Return general HTTP response
    :param data:
    :param str message: detail info
    :param int http_code:
    :return:
    """
    res = {
        'code': http_code.__str__(),
        # 'success': http_code // 100 == 2,
        'message': message,
        # 'data': data
    }

    if http_code == 200:
        res['result'] = data
    else:
        res['extra'] = data

    return res, http_code
