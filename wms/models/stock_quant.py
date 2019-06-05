# coding=utf-8

import logging

from flask_restplus import fields, Model
from .base import ResponseModel

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class StockQuantSchema:
    stock_quant_req = {
        'products': fields.String(required=True, description='List sku'),
        'branches': fields.String(required=False, description='Branches'),
        'warehouses': fields.String(required=False, description='Warehouses code'),
        'locations': fields.String(required=False, description='Locations'),
        'regions': fields.Integer(required=False, description='Regions'),
    }

    stock_quant_item = {
        # 'sku': fields.String(required=True, description='product sku'),
        'branch': fields.String(required=False, description='Branch code'),
        'location': fields.String(required=False, description='Location code'),
        'warehouse': fields.String(required=False, description='Warehouse code'),
        'reserved': fields.Float(required=False, description='Stock held quantity'),
        'incoming': fields.Integer(required=False, description='Quantity about to enter stock'),
        'storeCode': fields.String(required=False, description='Asia region type'),
        'outgoing': fields.Integer(required=False, description='Stock outgoing quantity'),
        'available': fields.Float(required=False,
                                  description='Available quantity = Actual inventory number - stock held = onHand- reserved',
                                  ),
        'forecast': fields.Float(required=False, description='Forecast = Physical Stock + Incoming - Outgoing'),
        'onHand': fields.Float(required=False, description='Actual quantity in stock'),
        'productBizType': fields.String(required=False, description='Type of product business'),

    }
    # Remove some fields for stock_quant_item_min
    stock_quant_item_min = stock_quant_item.copy()
    stock_quant_item_min.pop('incoming')
    stock_quant_item_min.pop('forecast')
    stock_quant_item_min.pop('outgoing')
    stock_quant_item_min['branchName']= fields.String(required=False, description='Branch name')
    stock_quant_item_min['locationName']= fields.String(required=False, description='Location name')
    stock_quant_item_min['warehouseName']= fields.String(required=False, description='Warehouse name')
    stock_quant_item_min['serial']= fields.String(required=False, description='Serial of Product')


class StockQuantModel:
    stock_quant = Model('stock_quant', {
        # 'sku': fields.String(required=True, description='product sku'),
        'branch': fields.String(required=False, description='Branch code'),
        'location': fields.String(required=False, description='Location code'),
        'warehouse': fields.String(required=False, description='Warehouse code'),
        'reserved': fields.Float(required=False, description='Stock held quantity'),
        'incoming': fields.Integer(required=False, description='Quantity about to enter stock'),
        'storeCode': fields.String(required=False, description='Asia region type'),
        'outgoing': fields.Integer(required=False, description='Stock outgoing quantity'),
        'available': fields.Float(required=False,
            description='Available quantity = Actual inventory number - stock held = onHand- reserved'),
        'forecast': fields.Float(required=False, description='Forecast = Physical Stock + Incoming - Outgoing'),
        'onHand': fields.Float(required=False, description='Actual quantity in stock'),
        'productBizType': fields.String(required=False, description='Type of product business'),
    })

    stock_quant_response = Model('stock_quant_response', {
        'sku': fields.String(required=True, description='Product sku'),
        'items': fields.Nested(stock_quant, allow_null=True, as_list=True, skip_none=True)
    })

    stock_quant_min = Model('stock_quant_min', {
        # 'sku': fields.String(required=True, description='product sku'),
        'branch': fields.String(required=False, description='Branch code'),
        'branchName': fields.String(required=False, description='Branch name'),
        'location': fields.String(required=False, description='Location code'),
        'locationName': fields.String(required=False, description='Location name'),
        'warehouse': fields.String(required=False, description='Warehouse name'),
        'warehouseName': fields.String(required=False, description='Warehouse code'),
        'timestamp': fields.Float(required=False, description='Time Stamp'),
        'reserved': fields.Float(required=False, description='Stock held quantity'),
        'storeCode': fields.String(required=False, description='Asia region type'),
        'available': fields.Float(required=False,
            description='Available quantity = Actual inventory number - stock held = onHand- reserved'),
        'onHand': fields.Float(required=False, description='Actual quantity in stock'),
        'productBizType': fields.String(required=False, description='Type of product business'),
    })

    stock_quant_min_response = Model('stock_quant_min_response', {
        'sku': fields.String(required=True, description='Product sku'),
        'items': fields.Nested(stock_quant_min, allow_null=True, as_list=True, skip_none=True)
    })

    stock_quant_success = ResponseModel.success_response.clone('stock_quant_success', {
        'result': fields.Nested(stock_quant_response, as_list=True)
    })

    stock_quant_min_success = ResponseModel.success_response.clone('stock_quant_min_success', {
        'result': fields.Nested(stock_quant_min_response, as_list=True)
    })
