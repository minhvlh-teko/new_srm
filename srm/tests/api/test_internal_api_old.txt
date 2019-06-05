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


class TestInternalApi(APITestCase):
    def url(self):
        return '/api/v2/internals/product_uom/1'

    def method(self):
        return 'PUT'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                "/api/v2/internals/product_uom/1/",
                {
                    "payload": "{\"id\": 84, \"__origin_id\": 84, \"__seq_num\": 3, \"name\": \"TEST-ETON\", \"__vals\": {\"name\": \"TEST-ETON\"}, \"__ts\": \"2019-04-02 06:51:19.812446\", \"__lang\": \"vi_VN\", \"__login\": \"admin\", \"__origin_model\": \"product.uom\", \"__sign\": \"dadeeb67a09ec84bc9fcaf7af96171f501241301\"}"
                },
                {'code': 0, 'message': 'OK'}
        )
    ])
    def test_update_product_uom_when_send_odoo_success_then_return_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                "/api/v2/internals/product_uom/1/?use_faker=true&no_cache=true",
                {
                    "payload": "{\"id\": 84, \"__origin_id\": 84, \"__seq_num\": 3, \"name\": \"TEST-ETON\", \"__vals\": {\"name\": \"TEST-ETON\"}, \"__ts\": \"2019-04-02 06:51:19.812446\", \"__lang\": \"vi_VN\", \"__login\": \"admin\", \"__origin_model\": \"product.uom\", \"__sign\": \"dadeeb67a09ec84bc9fcaf7af96171f501241301\"}"
                },
                {'code': 0, 'message': 'OK'}
        )
    ])
    def test_update_product_uom_use_faker_data_with_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    # test product brands
    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
            "/api/v2/internals/brands/",
            {
                "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
            },
            {
                "code": 5,
                "data": None,
                "message": "ProductBrand #424 already exists."
            }
        )
    ])
    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_post_brands_when_send_odoo_then_return_bad_request_response(self, url, payload, expected):
        rv = self.send_request(url=url, data=payload, method='post')
        assert rv.status_code == 400
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                "/api/v2/internals/brands/",
                {
                    "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
                },
                {
                    "code": 0,
                    "message": "OK"
                }
        )
    ])
    @pytest.mark.usefixtures('odoo_account_local_server')
    @pytest.mark.usefixtures('mocker_patch_odoo_send_request')
    def test_post_brands_use_mocker_then_return_success_response(self, url, payload, expected):
        rv = self.send_request(url=url, data=payload, method='post')
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_response_of_api_create_brands_use_new_mocker_fixture(self, mocker_odoo_response_with_data):
        fake_odoo_response_data = {
            "code": 10,
            "message": "OK"
        }
        payload = {
            "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
        }
        expected = {
            "code": 10,
            "message": "OK"
        }
        mocker_odoo_response_with_data(fake_odoo_response_data)
        res = self.send_request(url='/api/v2/internals/brands/', data=payload, method='post')
        res_data = json.loads(res.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_response_of_api_create_brands_use_new_mocker_fixture_mapping(self, mocker_odoo_response_with_xc_exception):
        fake_odoo_response_data = {
            "faultCode": 2,
            "faultString": "message abc"
        }
        payload = {
            "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
        }
        expected = {
            "code": 2,
            "message": "message abc",
            "data": None
        }
        mocker_odoo_response_with_xc_exception(fake_odoo_response_data)
        res = self.send_request(url='/api/v2/internals/brands/', data=payload, method='post')
        assert res.status_code == 200
        res_data = json.loads(res.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_payload_format_of_api_create_brands_missing_required_field(self, mocker_odoo_response_check_payload):
        fields = {
            "__seq_num": True,
            "__ts": True,
            "__data": True,
            "__origin_model": True,
            "__lang": True,
            "__origin_id": True,
            "__sign": True,
            "test": True,
        }
        payload = {
            "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
        }
        expected = {
            'code': '400',
            'message': '400 Bad Request: Payload is missing required field',
            'extra': None
        }
        mocker_odoo_response_check_payload(fields)
        res = self.send_request(url='/api/v2/internals/brands/', data=payload, method='post')
        assert res.status_code == 400
        res_data = json.loads(res.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_payload_format_of_api_create_brands_not_allow_extra_field(self, mocker_odoo_response_check_payload):
        fields = {
            "__seq_num": True,
            "__ts": True,
            "__data": True,
            "__origin_model": True,
            "__lang": True,
            "__origin_id": True,
        }
        payload = {
            "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
        }
        expected = {
            'code': '400',
            'message': '400 Bad Request: Payload has extra field',
            'extra': None
        }
        mocker_odoo_response_check_payload(fields)
        res = self.send_request(url='/api/v2/internals/brands/', data=payload, method='post')
        assert res.status_code == 400
        res_data = json.loads(res.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)
