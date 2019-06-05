# coding=utf-8

import logging

from flask_restplus import fields

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class StockOutSchema:
    stock_out_request_req = {
        'requestCode': fields.String(required=True, description='CKNB receipt code, stock out receipt code'),
        'requestType': fields.String(required=True, description='Export type'),
        'orderID': fields.String(required=True, description='Order code (if in other export type, orderID = 0)'),
        'createdAt': fields.DateTime(required=True, description='Request time'),
    }

    stock_out_confirm_req = {
        'requestCode': fields.String(required=True, description='CKNB receipt code, stock out receipt code'),
        'staffId': fields.String(required=False, description='Receive goods staff ID'),
        'orderID': fields.String(required=True, description='Order ID'),
        'createdAt': fields.DateTime(required=True, description='Confirmation time'),
    }


class StockOutModel:
    pass
