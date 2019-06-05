# coding=utf-8
import logging
from .odoo_repo import OdooRepo
from werkzeug.datastructures import ImmutableMultiDict

__author__ = 'Son'
_logger = logging.getLogger('api')


class StockOutRequest(OdooRepo):
    _name = 'stock_out_request'
    _model = 'stock.picking'
    _mapping = {
        'create': 'api_stock_out_request',
    }
    _is_formalization = True
    _faker_data = {
        'req': {
            'orderID': True,
            'requestType': True,
            'createdAt': True,
            'requestCode': True,
        },
        'res': {'code': 0, 'message': 'OK', 'requestCode': 'T1207982'}
    }

    def _formalize_payload(self):
        # Don't need to formalize payload
        pass

    def _formalize(self, response):
        """
        Override parent method
        :param dict response:
        :return: dict
        """
        _logger.info(response)
        response['data'] = {'requestCode': response.pop('requestCode', '')}
        _logger.debug(response)
        return super()._formalize(response)


class StockOutConfirm(OdooRepo):
    _name = 'stock_out_confirm'
    _model = 'stock.picking'
    _mapping = {
        'create': 'api_stock_out_confirm',
    }
    _is_formalization = True
    _faker_data = {
        'req': {
            'orderID': True,
            'staff_id': True,
            'createdAt': True,
            'requestCode': True,
        },
        'res': {'code': 0, 'message': 'OK', 'requestCode': 'T1207075'}
    }

    def _formalize_payload(self):
        self._payload['staff_id'] = self._payload.pop('staffId', "")

    def _formalize(self, response):
        """
        Override parent method
        :param dict response:
        :return: dict
        """
        _logger.info(response)
        response['data'] = {'requestCode': response.pop('requestCode', '')}
        _logger.debug(response)
        return super()._formalize(response)
