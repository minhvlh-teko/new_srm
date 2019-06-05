# Created by thanhpd on 3/13/2019
import logging
import unittest

import pytest

from wms import models as m
from wms.repositories import odoo_repo
from ...extensions import exceptions
from ...models import db, OdooAccount
from ..general_test import GeneralTestCase

_logger = logging.getLogger(__name__)


class TestOdooRepositoryTestCase(GeneralTestCase):
    odoo_1 = odoo_repo.OdooRepo()
    odoo_2 = odoo_repo.OdooRepo(target='cache', used_cache=True)

    @pytest.fixture
    def setup(self, mocker):
        mocker.patch("flask_sqlalchemy.SQLAlchemy.init_app", return_value=True)

    def test_connect_odoo_service_when_account_is_invalid_then_return_internal_error(
            self):
        pass

    def test_odoo_repo_function_name__parse_special_params(self):
        test_cases = [
            {
                'description': '',
                'input': {
                    'payload': {
                        'hello': 5,
                        'faker': 6
                    }
                },
                'expected': {
                    'payload': {
                        'hello': 5,
                        'faker': 6
                    }
                },

            },
            {
                'description': '',
                'input': {
                    'payload': {
                        'hello': 5,
                        'use_faker': True,
                        'no_cache': False,
                        'debug_mode': True
                    }
                },
                'expected': {
                    'payload': {
                        'hello': 5,
                    },

                },

            },
        ]

        # Test for the first case
        before_target = self.odoo_1._target
        before_used_cache = self.odoo_1._used_cache
        self.odoo_1._parse_special_params(test_cases[0]['input']['payload'])
        assert test_cases[0]['input']['payload'] == test_cases[0]['expected']['payload']
        assert self.odoo_1._target == before_target
        assert self.odoo_1._used_cache == before_used_cache

        # Test for the second case
        self.odoo_1._parse_special_params(test_cases[1]['input']['payload'])
        msg = "Payload should remove special value. Expect: (%s). Actual: (%s" % (
            test_cases[1]['expected']['payload'], test_cases[1]['input']['payload'])
        assert test_cases[1]['input']['payload'] == test_cases[1]['expected']['payload'], msg
        assert self.odoo_2._special_params['use_faker']
        assert self.odoo_2._special_params['debug_mode']
        assert not self.odoo_2._special_params['no_cache']

    def test_odoo_repo_function_name__to_underscore(self):
        test_cases = [
            {
                'input': 'camelCaseFunctionName',
                'expected': 'camel_case_function_name'
            },
            {
                'input': 'came1CaSeFUnctionName',
                'expected': 'came1_ca_se_f_unction_name'
            }
        ]
        for test_case in test_cases:
            output = self.odoo_1._to_underscore(test_case['input'])
            assert output == test_case['expected']

    def test_odoo_repo_function_name__to_camel_case(self):
        test_cases = [
            {
                'input': 'camel_case_function_name',
                'expected': 'camelCaseFunctionName',
            },
            {
                'input': 'came1_ca_se_f_unction_name',
                'expected': 'came1CaSeFUnctionName',
            }
        ]
        for test_case in test_cases:
            output = self.odoo_1._to_camel_case(test_case['input'])
            assert output == test_case['expected']

    def test_odoo_repo_function_name__apply_underscore_to_dict(self):
        test_cases = [
            {
                'input': {
                    'firstKey': 'firstKey value',
                    'secondKey': {
                        'firstChildKey': 'firstChildKey value',
                        'secondChildKey': [
                            'first secondChildKey value ',
                            {
                                'firstChildChildKey': 'firstChildChildKey value'
                            }
                        ]
                    }
                },
                'expected': {
                    'first_key': 'firstKey value',
                    'second_key': {
                        'first_child_key': 'firstChildKey value',
                        'second_child_key': [
                            'first secondChildKey value ',
                            {
                                'first_child_child_key': 'firstChildChildKey value'
                            }
                        ]
                    }
                }
            }
        ]

        for test_case in test_cases:
            self.odoo_1._apply_underscore_to_dict(test_case['input'])
            assert test_case['input'] == test_case['expected']

    def test_odoo_repo_function_name__apply_camelcase_to_dict(self):
        test_cases = [
            {
                'input': {
                    'first_key': 'firstKey value',
                    'second_key': {
                        'first_child_key': 'firstChildKey value',
                        'second_child_key': [
                            'first secondChildKey value ',
                            {
                                'first_child_child_key': 'firstChildChildKey value'
                            }
                        ]
                    }
                },
                'expected': {
                    'firstKey': 'firstKey value',
                    'secondKey': {
                        'firstChildKey': 'firstChildKey value',
                        'secondChildKey': [
                            'first secondChildKey value ',
                            {
                                'firstChildChildKey': 'firstChildChildKey value'
                            }
                        ]
                    }
                }
            }
        ]

        for test_case in test_cases:
            self.odoo_1._apply_camelcase_to_dict(test_case['input'])
            assert test_case['input'] == test_case['expected']

    def test_odoo_repo_function_name__get_account(self):
        test_account = OdooAccount(
            user='test_user',
            password='1234',
            client_ip='123.123.123.123',
            url='dev.wms.phongvu.vn',
            uid=123,
            dbs='wms_dev',
            port=80
        )
        db.session.add(test_account)
        db.session.commit()

        client_ip = '123.123.123.123'
        account = self.odoo_1._get_account(client_ip)
        assert account is not None

        try:
            client_ip = '123.123.123.1'
            account = self.odoo_1._get_account(client_ip)
        except Exception as e:
            assert isinstance(e, exceptions.UnAuthorizedException)

        db.session.delete(test_account)
        db.session.commit()

    def test_odoo_repo_function_name__get_account_by_secret(self):
        test_account = OdooAccount(
            user='test_user',
            password='1234',
            client_ip='123.123.123.123',
            url='dev.wms.phongvu.vn',
            uid=123,
            dbs='wms_dev',
            port=80,
            secret_key='test_secret_key',
            api_list='test'
        )
        db.session.add(test_account)
        db.session.commit()

        odoo_repo_instance = odoo_repo.OdooRepo()
        odoo_repo_instance._secret_key = 'test_secret_key'
        odoo_repo_instance._name = 'test'

        account = odoo_repo_instance._get_account_by_secret()
        assert account is not None

        try:
            odoo_repo_instance._secret_key = None
            account = odoo_repo_instance._get_account_by_secret()
        except Exception as e:
            assert isinstance(e, exceptions.ForbiddenException)

        try:
            odoo_repo_instance._secret_key = 'test_wrong_secret_key'
            account = odoo_repo_instance._get_account_by_secret()
        except Exception as e:
            assert isinstance(e, exceptions.UnAuthorizedException)

        db.session.delete(test_account)
        db.session.commit()
