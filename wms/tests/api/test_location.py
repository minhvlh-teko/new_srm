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


class TestLocation(APITestCase):
    def url(self):
        return '/api/v2/locations/'

    def method(self):
        return 'GET'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'expected'), [
        (
                None,
                {'code': '200', 'result': {}, 'message': ''}
        )
    ])
    def test_get_locations_by_request_odoo_with_return_success_response(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 200
        assert res_data['code'] == expected['code']
        assert isinstance(res_data['result'], list)
        assert len(res_data['result']) != 0
        assert res_data['message'] == expected['message']

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/locations/?use_faker=true&no_cache=true",
                {'code': '400', 'message': '400 Bad Request: not OK', 'extra': None}
        )
    ])
    def test_get_locations_use_faker_data_with_wrong_response_format(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        assert rv.status_code == 400
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'expected'), [
        (
                '/api/v2/locations/mapping',
                {'code': '200', 'result': {}, 'message': ''}
        )
    ])
    def test_get_locations_mapping_by_request_odoo_with_return_success_response(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 200
        assert res_data['code'] == expected['code']
        assert isinstance(res_data['result'], dict)
        assert len(res_data['result']) != 0
        assert res_data['message'] == expected['message']

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/locations/mapping?use_faker=true&no_cache=true",
                {'code': '400', 'message': '400 Bad Request: not OK', 'extra': None}
        )
    ])
    def test_get_locations_mapping_use_faker_data_with_wrong_response_format(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        assert rv.status_code == 400
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

