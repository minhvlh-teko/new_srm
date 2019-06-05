# coding=utf-8
import json
import logging
import os
# from parameterized import parameterized, param
import pytest
from assertpy import assert_that

# from .. import models as m
from . import APITestCase

__author__ = 'Huu'
_logger = logging.getLogger(__name__)


class TestStockOutRequest(APITestCase):
    def url(self):
        return '/api/v2/stock_out/'

    def method(self):
        return 'POST'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                None,
                {
                    'orderID': '0',
                    'createdAt': '2019-05-14T10:08:03.583Z',
                    'requestType': 'string',
                    'requestCode': 'T1207075'
                },
                {'code': '400', 'extra': None, 'message': '400 Bad Request: Incorrect picking state.'}
        )
    ])
    def test_put_stock_out_request_by_request_odoo_return_bad_request_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 400
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                '/api/v2/stock_out/?use_faker=true&no_cache=true',
                {
                    'orderID': '0',
                    'createdAt': '2019-05-14T10:08:03.583Z',
                    'requestType': 'string',
                    'requestCode': 'T1207982'
                },
                {'code': '200', 'message': '', 'result': {'requestCode': 'T1207982'}}
        )
    ])
    def test_put_stock_out_request_use_faker_data_return_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)


class TestStockOutConfirm(APITestCase):
    def url(self):
        return '/api/v2/stock_out/'

    def method(self):
        return 'PUT'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                None,
                {
                    'orderID': '0',
                    'staffId': '1',
                    'createdAt': '2019-05-14T09:35:37.717Z',
                    'requestCode': 'T0100132'
                },
                {'code': '400', 'extra': None, 'message': '400 Bad Request: Already confirmed by #123'}
        )
    ])
    def test_put_stock_out_confirm_by_request_odoo_return_bad_request_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 400
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                '/api/v2/stock_out/?use_faker=true&no_cache=true',
                {
                    'orderID': '0',
                    'staffId': '1',
                    'createdAt': '2019-05-14T09:35:37.717Z',
                    'requestCode': 'T1207075'
                },
                {'code': '200', 'message': '', 'result': {'requestCode': 'T1207075'}}
        )
    ])
    def test_put_stock_out_confirm_use_faker_data_return_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)