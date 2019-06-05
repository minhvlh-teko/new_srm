# coding=utf-8
import json
import logging
import os
# from parameterized import parameterized, param
import pytest
from assertpy import assert_that

# from .. import models as m
from . import APITestCase

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


class TestStockQuantApi(APITestCase):
    def url(self):
        return '/api/v2/stock_quants/'

    def method(self):
        return 'GET'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/stock_quants/?products=18120233",
                {
                    'url': '',
                    'skus': 1,
                    'first_sku': '18120233',
                    'first_sku_item_length_greater_than': 1
                }
        ),
        (
                '/api/v2/stock_quants/?products=1200109&products=18120233',
                {
                    'skus': 2,
                    'first_sku': '1200109',
                    'first_sku_item_length_greater_than': 3
                }
        )
    ])
    def test_get_stock_quants_when_send_odoo_success_then_return_stock_quants_response_with_data(self,
                                                                                                 odoo_account_test_server,
                                                                                                 url, expected):
        rv = self.send_request(url=url)
        assert rv.status_code == 200
        rv_data = json.loads(rv.data.decode("utf-8"))

        assert 'code' in rv_data
        assert 'message' in rv_data
        assert 'result' in rv_data

        res_data = rv_data['result']
        # number items should be greater than 0
        assert len(res_data) >= expected['skus']

        assert res_data[0]['sku'], 'Sku must not be empty'
        assert len(res_data[0]['items']) >= expected['first_sku_item_length_greater_than']
        if expected['first_sku_item_length_greater_than']:
            assert res_data[0]['items'][0]['warehouse'] is not '', 'Warehouse should not be empty'

    @pytest.mark.parametrize(('url'), [
        (None),
        ('/api/v2/stock_quants/?products=18120233,1200109')
    ])
    def test_get_stock_quants_when_invalid_query_params_then_return_400_code(self, url):
        bad_request = 400
        rv = self.send_request(url=url)
        assert rv.status_code == bad_request

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/stock_quants/?products=18120233&use_faker=true&no_cache=true",
                [
                 {'sku': '1200109', 'items': [{'location': '000001', 'available': 6.0, 'warehouse': 'CH0000'},
                                              {'location': '0101', 'available': 1.0, 'warehouse': 'CP01'}]},
                {'sku': '1805119', 'items': [{'location': '0402', 'available': 10.0, 'warehouse': 'CP04'}]}]
        ),
        (
                '/api/v2/stock_quants/?products=1200109&products=18120233&use_faker=true&no_cache=true',
                [
                 {'sku': '1200109', 'items': [{'location': '000001', 'available': 6.0, 'warehouse': 'CH0000'},
                                              {'location': '0101', 'available': 1.0, 'warehouse': 'CP01'}]},
                {'sku': '1805119', 'items': [{'location': '0402', 'available': 10.0, 'warehouse': 'CP04'}]}]
        )
    ])
    def test_get_stock_quants_from_faker_with_correct_api_and_no_cache_response_200(self, odoo_account_test_server, url,
                                                                                    expected):
        ok_status = 200
        rv = self.send_request(url=url)

        assert rv.status_code == ok_status
        rv_data = json.loads(rv.data.decode("utf-8"))
        assert 'code' in rv_data
        assert 'message' in rv_data
        assert 'result' in rv_data
        res_data = rv_data['result']
        # print(res_data)
        assert len(res_data) == 2

        assert res_data[0]['sku'], 'Sku must not be empty'
        assert len(res_data[0]['items']) >= 1
        assert res_data[0]['items'][0]['warehouse'] is not '', 'Warehouse should not be empty'
