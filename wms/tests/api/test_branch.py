# coding=utf-8
import json
import logging
import os
# from parameterized import parameterized, param
import pytest
import pytest_flask
from assertpy import assert_that

# from .. import models as m
from . import APITestCase

__author__ = 'Huu'
_logger = logging.getLogger(__name__)


class TestBranch(APITestCase):
    def url(self):
        return '/api/v2/branches/'

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
    def test_get_branches_by_request_odoo_with_return_success_response(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 200
        assert res_data['code'] == expected['code']
        assert isinstance(res_data['result'], list)
        assert len(res_data['result']) != 0
        assert res_data['message'] == expected['message']

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/branches/?use_faker=true&no_cache=true",
                {'code': '400', 'message': '400 Bad Request: not OK', 'extra': None}
        )
    ])
    def test_get_branches_use_faker_data_with_wrong_response_format(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        assert rv.status_code == 400
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'expected'), [
        (
                '/api/v2/branches/mapping',
                {'code': '200', 'result': {}, 'message': ''}
        )
    ])
    def test_get_branches_mapping_by_request_odoo_return_success_response(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 200
        assert res_data['code'] == expected['code']
        assert isinstance(res_data['result'], dict)
        assert len(res_data['result']) != 0
        assert res_data['message'] == expected['message']

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/branches/mapping?use_faker=true&no_cache=true",
                {'code': '400', 'message': '400 Bad Request: not OK', 'extra': None}
        )
    ])
    def test_get_branches_mapping_use_faker_data_with_wrong_response_format(self, odoo_account_local_server, url, expected):
        rv = self.send_request(url=url)
        assert rv.status_code == 400
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/branches/?use_faker=true&no_cache=true",
                {'code': '401', 'message': '401 Unauthorized: Client IP not authenticate!', 'extra': None}
        )
    ])
    def test_get_branches_with_client_ip_not_allow_then_return_error(self, odoo_account_not_ip_not_allow, url, expected):
        rv = self.send_request(url=url)
        assert rv.status_code == 401
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'expected'), [
        (
                "/api/v2/branches/?use_faker=true&no_cache=true",
                {'code': '401', 'message': '401 Unauthorized: Client IP not authenticate!', 'extra': None}
        )
    ])
    def test_get_branches_response_header_content_type_application_json(self, odoo_account_not_ip_not_allow, url, expected):
        rv = self.send_request(url=url)
        assert isinstance(rv, pytest_flask.plugin.JSONResponse)
        assert rv.status_code == 401
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_response_of_api_get_branches_use_new_mocker_fixture_cache(self, mocker, mocker_odoo_response_with_cache):
        mocker.patch("wms.repositories.branch.Branch._used_cache", True)
        mocker.patch("wms.repositories.branch.Branch._is_formalization", False)
        fake_odoo_response_data = {
            "code": '10',
            "message": "OK"
        }
        fake_cache_data = {
            "code": '1010',
            "message": "OK"
        }
        expected = {
            "code": '1010',
            'result': None,
            "message": "OK"
        }
        mocker_odoo_response_with_cache(fake_odoo_response_data, fake_cache_data)
        res = self.send_request(url='/api/v2/branches/', data=None, method='get')
        res_data = json.loads(res.data.decode("utf-8"))
        print(res_data)
        assert_that(res_data).is_equal_to(expected)
