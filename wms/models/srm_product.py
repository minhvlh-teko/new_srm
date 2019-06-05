# coding=utf-8

import logging

from flask_restplus import fields

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class SrmProductSchema:
    srm_product = {
        # 'fe_id': fields.Integer(required=True, description='Product id generated at seller_center'),
        'defaultCode': fields.String(required=True, description='Default code'),
        'name': fields.String(required=True, description='Name'),
        'shortName': fields.String(required=False, description='Feature name'),
        'partNumber': fields.String(required=False, description='Part Number'),
        'attributeValueCode': fields.String(required=False, description='Property (color)'),
        'type': fields.String(required=True, description='Product type:\
- consu: Product does not manage inventory (Allow to sell negative)\
- product: Product with inventory management and storage', enum=['consu','product']),

        'barcode': fields.String(required=True, description='Barcode'),
        'productBrandCode': fields.String(required=True, description='Brand code'),
        'categCode': fields.String(required=True, description='Category'),
        'uomName': fields.String(required=True, description='Unit'),
        'uomPoName': fields.String(required=True, description='Purchase unit of measurement'),
        'salePoint': fields.Float(required=False, description='Product points'),
        'warrantyPeriod': fields.Float(required=False, description='Warranty period'),
        'warrantyNote': fields.String(required=False, description='Warranty notes'),
        'exchangePeriod': fields.Integer(required=False, description='1-1 Exchange period (day)'),
        'warrantyStampQty': fields.Integer(required=False, description='Number of warranty stamps'),
        'saleOnlineOnly': fields.Boolean(required=True, description='Sale online only', default=False),
        'supportDelivery': fields.Boolean(required=True, description='Support delivery', default=False),
        'productStatus': fields.Integer(required=False, description='Status'),
        'costPriceCalc': fields.Boolean(required=True, description='Calculate cost price', default=False),
        'tracking': fields.String(required=True, description='tracking', default=None),
        'note': fields.String(required=False, description='Note'),
        'isUncounted': fields.Boolean(required=True, description='No tally', default=False),
        'isService': fields.Boolean(required=True, description='Product service', default=False),
    }

    srm_product_req = srm_product.copy()
    srm_product_res = {
        'code': fields.Integer(required=True, description='Code'),
        'message': fields.String(required=True, description='Message'),
        'success': fields.String(description='Success message'),
        'data': fields.Raw(description='Data')
    }


class SrmProductModel:
    pass
