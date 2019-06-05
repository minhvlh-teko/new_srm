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


class TestExternalPO(APITestCase):
    def url(self):
        return '/api/v2/external/po/123'

    def method(self):
        return 'PUT'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                None,
                {
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {
                    "extra": None,
                    "code": '400',
                    "message": "400 Bad Request: ValidationError('Picking #123 at state <cancel> cannot be validated', None)"
                }
        )
    ])
    def test_post_external_po_by_request_odoo_return_bad_request_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 400
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                '/api/v2/external/po/123?use_faker=true&no_cache=true',
                {
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {'code': '200', 'message': '', 'result': {}}
        )
    ])
    def test_put_external_po_use_faker_data_return_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)


class TestExternalSO(APITestCase):
    def url(self):
        return '/api/v2/external/so/123'

    def method(self):
        return 'PUT'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                None,
                {
                    "eventType": "picked",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {
                    "code": "400",
                    "extra": None,
                    "message": "400 Bad Request: UserError('Only PICK Picking of ST/SO are allowed.', '')"
                }
        ),
        (
                None,
                {
                    "eventType": "packed",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {
                    "code": "400",
                    "extra": None,
                    "message": "400 Bad Request: UserError('Only PACK Picking of ST/SO are allowed.', '')"
                }
        ),
        (
                None,
                {
                    "eventType": "delivered",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {
                    "code": "400",
                    "extra": None,
                    "message": "400 Bad Request: UserError('Only OUT Picking of ST/SO or PO Return are allowed.', '')"
                }
        )
    ])
    def test_post_external_so_by_request_odoo_return_bad_request_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 400
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                '/api/v2/external/so/123?use_faker=true&no_cache=true',
                {
                    "eventType": "picked",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "1806143",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {'code': '200', 'message': '', 'result': {}}
        ),
        (
                '/api/v2/external/so/123?use_faker=true&no_cache=true',
                {
                    "eventType": "packed",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "1806143",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {'code': '200', 'message': '', 'result': {}}
        ),
        (
                '/api/v2/external/so/123?use_faker=true&no_cache=true',
                {
                    "eventType": "delivered",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "1806143",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {'code': '200', 'message': '', 'result': {}}
        )
    ])
    def test_put_external_so_use_faker_data_return_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)


class TestExternalSOReturn(APITestCase):
    def url(self):
        return '/api/v2/external/so/123456789/returned'

    def method(self):
        return 'PUT'

    @pytest.mark.skipif(os.environ.get("ENV_MODE", 'dev') != 'dev',
                        reason="Can only test on local, when connecting directly to Odoo")
    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                None,
                {
                    "type": "string",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {
                    "extra": None,
                    "code": '400',
                    "message": "400 Bad Request: ValidationError('Picking #123456789 not found', None)"
                }
        )
    ])
    def test_post_external_so_return_by_request_odoo_return_bad_request_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        res_data = json.loads(rv.data.decode("utf-8"))
        assert rv.status_code == 400
        assert_that(res_data).is_equal_to(expected)

    @pytest.mark.parametrize(('url', 'payload', 'expected'), [
        (
                '/api/v2/external/so/123/returned?use_faker=true&no_cache=true',
                {
                    "type": "string",
                    "items": [
                        {
                            "qty": 0,
                            "sku": "string",
                            "serials": [
                                "string"
                            ]
                        }
                    ]
                },
                {'code': '200', 'message': '', 'result': {}}
        )
    ])
    def test_put_external_so_return_use_faker_data_return_success_response(self, odoo_account_local_server, url, payload, expected):
        rv = self.send_request(url=url, data=payload)
        assert rv.status_code == 200
        res_data = json.loads(rv.data.decode("utf-8"))
        assert_that(res_data).is_equal_to(expected)
