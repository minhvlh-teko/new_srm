# Created by sonlp on 10-05-2019

import logging
import time
import pytest, json
from assertpy import assert_that

from wms.extensions.exceptions import BadRequestException, NotFoundException
from wms.services import odoo_service
from wms.repositories.stock_quant import StockQuant
from ..general_test import GeneralTestCase
import os

_logger = logging.getLogger(__name__)

res_faker_data = {
    "message": "OK",

    "data": {

        "1200109": [{

            "warehouse": "CH0000",

            "location": "000001",

            "available": 6

        },

            {

                "warehouse": "CP01",

                "location": "0101",

                "available": 1

            }]

    }

}


class TestOdooServiceTest(GeneralTestCase):

    @pytest.fixture(scope='class')
    def stock_quant_repo(self):
        return StockQuant()

    @pytest.mark.parametrize(('repo_name', 'method_name', 'data', 'module_name'), [
        ('StockQuant', 'update', {}, None),
        ('StockQuant', 'destroy', {}, None)

    ])
    def test_odoo_service_when_send_wrong_method_then_raise_exception(self, repo_name, method_name, data, module_name):
        with pytest.raises(BadRequestException):
            assert odoo_service.call_odoo_repo(repo_name, method_name, data, module_name)

    @pytest.mark.parametrize(('ip', 'data', 'is_ok'), [
        ('127.0.0.1', {'use_faker': True,
                       'no_cache': False,
                       'products': [132311]}, True),
        ('127.0.0.1', {'use_faker': False,
                       # 'no_cache': False,
                       'products': [132311]}, True),
        ('127.0.0.1', {'use_faker': False,
                       'no_cache': True,
                       'products': [177732311]}, False),

    ])
    def test_odoo_service_using_cache_get_stock_quant_then_ok(self, stock_quant_repo, odoo_account_test_server, ip,
                                                              data, is_ok):
        stock_quant_repo._client_ip = ip
        # print("Use faker: {}; no_cache: {}".format(data['use_faker'], data.get('no_cache')))

        # print(rv_data)
        # print("_________________+++++++_______")

        if is_ok:
            rv_data, code = stock_quant_repo.list(data)
            assert_that(code).is_equal_to(200)
        else:
            # only run on dev mode
            if os.environ.get("ENV_MODE", 'dev') == 'dev':
                rv_data, code = stock_quant_repo.list(data)
                assert_that(code).is_equal_to(200)
                assert_that(rv_data['result']).is_empty()

    @pytest.mark.parametrize(('ip', 'data'), [
        ('127.0.0.1', {'use_faker': True,
                       'no_cache': False,
                       'products': [1362311]})
    ])
    def test_odoo_service_using_cache_get_stock_quant_with_time_limited_then_ok(self, odoo_account_test_server, ip,
                                                                                data):
        limited_time = 2
        stock_quant_repo = StockQuant(cache_life_time=limited_time)
        stock_quant_repo._client_ip = ip
        # Cache time limit should be updated
        assert_that(stock_quant_repo._cached_time_limited).is_equal_to(limited_time)
        # print("Use faker: {}; no_cache: {}".format(data['use_faker'], data.get('no_cache')))

        # print(rv_data)
        # print("_________________+++++++_______")
        rv_data, code = stock_quant_repo.list(data)
        assert_that(code).is_equal_to(200)
        result = rv_data['result']
        assert_that(result).is_instance_of(list)
        assert_that(len(result)).is_equal_to(2)
        # Now check if it still uses cache or not
        time.sleep(limited_time + 1)
        # change default faker data
        stock_quant_repo.set_faker_data(res_data=res_faker_data)

        rv_data, code = stock_quant_repo.list(data)
        assert_that(code).is_equal_to(200)
        result = rv_data['result']
        assert_that(result).is_instance_of(list)
        assert_that(len(result)).is_equal_to(1)


def test_if_redis_cache_is_activating(app):
    assert_that(app.config['REDIS_PROVIDER']).is_not_none()
