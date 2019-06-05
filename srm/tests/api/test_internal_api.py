# coding=utf-8
import json

from assertpy import assert_that

from . import APITestCase
import logging

import pytest



__author__ = 'MinhVlh'
_logger = logging.getLogger(__name__)

post_url=[
    "/api/v2/internals/purchaseOrderReceipt/",
    "/api/v2/internals/accountInvoice/",
    "/api/v2/internals/stockPickingType/",
]

put_url=[
    "/api/v2/internals/purchaseOrderInvoice/1/",
    "/api/v2/internals/purchaseOrderReceipt/1/",
    "/api/v2/internals/stockPickingType/1/",
    "/api/v2/internals/stockTransfer/1/",
]
delete_url=[
    "/api/v2/internals/stockPickingType/1/",
]
class TestInternalApi(APITestCase):

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_api_recieved_payload_fields_from_client_correctly_then_return_200(self, mocker_odoo_response_check_payload):
        fields = {
            "__seq_num": True,
            "__ts": True,
            "__data": True,
            "__origin_model": True,
            "__lang": True,
            "__origin_id": True,
            "__sign": True,
        }
        payload = {
            "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
        }
        expected = {
            'code': 0, 'message': 'Payload is valid'
        }
        mocker_odoo_response_check_payload(fields)
        for url in post_url:
            res = self.send_request(url=url,data=payload, method='post')
            assert res.status_code == 200
            res_data = json.loads(res.data.decode("utf-8"))
            assert_that(res_data).is_equal_to(expected)
        for url in put_url:
            res = self.send_request(url=url,data=payload, method='put')
            assert res.status_code == 200
            res_data = json.loads(res.data.decode("utf-8"))
            assert_that(res_data).is_equal_to(expected)

    @pytest.mark.usefixtures('odoo_account_local_server')
    def test_odoo_response_when_success_then_return_the_same_data(self, mocker_odoo_response_with_data,):
        """
        """
        fake_odoo_response_data = {
            "code": '0',
            "message": "Minh",
            "data": [
                {
                    'warehouse_code': '77', 'product_biz_type_code': '88', 'location_code': '99'
                }
            ],
        }
        payload = {
            "payload": "{\"__seq_num\": 1, \"__ts\": \"2019-04-23 03:58:01.058769\", \"__data\": [{\"name\": \"Quang Test 1\", \"description\": false, \"__login\": \"admin\", \"partner_id\": false, \"__last_update\": \"2019-04-23 03:58:01\", \"code\": \"TH000371\", \"active\": true, \"__id\": 424, \"display_name\": \"[TH000371] Quang Test 1\"}], \"__origin_model\": \"product.brand\", \"__lang\": \"vi_VN\", \"__origin_id\": 424, \"__sign\": \"5386e148b163dc29a696bf7819c9c79cf89c1076\"}"
        }
        expected = {
            "code": '0',
            "message": "Minh",
            "data": [
                {
                    'warehouse_code': '77', 'product_biz_type_code': '88', 'location_code': '99'
                }
            ],
        }
        mocker_odoo_response_with_data(fake_odoo_response_data)
        for url in post_url:
            res = self.send_request(url=url, data=payload, method='post')
            assert res.status_code == 200
            res_data = json.loads(res.data.decode("utf-8"))
            assert_that(res_data).is_equal_to(expected)
        for url in put_url:
            res = self.send_request(url=url, data=payload, method='put')
            assert res.status_code == 200
            res_data = json.loads(res.data.decode("utf-8"))
            assert_that(res_data).is_equal_to(expected)
        for url in delete_url:
            res = self.send_request(url=url, data=payload, method='put')
            assert res.status_code == 200
            res_data = json.loads(res.data.decode("utf-8"))
            assert_that(res_data).is_equal_to(expected)










