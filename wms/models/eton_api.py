# coding=utf-8

import logging
from .base import ResponseModel

from flask_restplus import fields, Model

__author__ = 'Huu'
_logger = logging.getLogger('api')


class EtonApiModel:
    eton_product = Model('eton_product', {
        'sku': fields.String(required=True, description='Product code'),
        'qty': fields.Integer(required=True, description='Quantity'),
        'serials': fields.List(fields.String, required=True, description='Serial list')
    })

    eton_po_req = Model('eton_po_req', {
        'items': fields.List(
            fields.Nested(eton_product, required=True, description='List of product information to be processed'))
    })

    eton_so_req = eton_po_req.clone('eton_so_req', {
        'eventType': fields.String(
            description='update SO by type',
            enum=['picked', 'packed', 'delivered']
        )
    })

    eton_so_returned_req = eton_po_req.clone('eton_so_returned_req', {
        'type': fields.String(
            description='Return type'
        )
    })

    eton_error_res = ResponseModel.error_response.clone('eton_error_res')

    eton_success_res = ResponseModel.success_response.clone('eton_success_res')
