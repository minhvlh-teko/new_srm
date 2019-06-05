# coding=utf-8
import logging

import pytest
from ..models import db, OdooAccount
from ..admin.models import User, Role
from werkzeug.security import generate_password_hash
from ..extensions import exceptions
import xmlrpc.client as xc

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


@pytest.fixture
def app_class(request, app):

    if request.cls is not None:
        request.cls.app = app




@pytest.fixture()
def odoo_account_test_server():
    print("Create instance odoo test account")
    test_account = OdooAccount(
        user='admin',
        password='1234',
        client_ip='127.0.0.1',
        url='123.31.32.200',
        uid=1,
        dbs='wms_test',
        port=8069,
        secret_key='test_secret_key'
    )
    db.session.add(test_account)
    db.session.commit()
    return test_account


@pytest.fixture()
def odoo_account_local_server():
    test_account = OdooAccount(
        user='admin',
        password='1234',
        client_ip='127.0.0.1',
        url='test.srm.phongvu.vn',
        uid=1,
        dbs='wms_test',
        port=8069,
    )
    db.session.add(test_account)
    db.session.commit()
    return test_account


@pytest.fixture()
def create_admin_user():
    role = Role(name='admin', description='Admin role')
    user = User(username='admin', password=generate_password_hash('admin'), roles=[role])
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def create_test_user():
    role = Role(name='test', description='Test role')
    user = User(username='test', password=generate_password_hash('test'), roles=[role])
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def odoo_account_not_ip_not_allow():
    test_account = OdooAccount(
        user='admin',
        password='1234',
        client_ip='192.168.123.123',
        url='test.srm.phongvu.vn',
        uid=1,
        dbs='wms_test',
        port=8069,
    )
    db.session.add(test_account)
    db.session.commit()
    return test_account


@pytest.fixture()
def mocker_patch_odoo_send_request(mocker):

    def get_faker_data(self, req_data=None, res_data=None):
        if res_data:
            self.set_faker_data(res_data=res_data)

        # Check if all keys is valid
        if req_data:
            invalid_key = None
            for key in req_data:
                if key not in self._faker_data[self._api_method]['req']:
                    invalid_key = key
                    break
            if invalid_key:
                # Invalid input key
                raise exceptions.BadRequestException('Key ({0}) is invalid'.format(invalid_key))
            # Check if required fields dont exist

            if self._faker_data[self._api_method]['req']:
                for key in self._faker_data[self._api_method]['req']:
                    if key not in req_data and self._faker_data[self._api_method]['req'][key]:
                        invalid_key = key
                        break
            if invalid_key:
                # Missing key required
                raise exceptions.BadRequestException('Key ({0}) is required'.format(invalid_key))
        return self._faker_data[self._api_method]['res']

    def fake_send_request(self, account=None, faker=None):
        _logger.info("Using fake_send_request to get data...................")
        print("\nUsing fake_send_request to get data...................")
        response = get_faker_data(self, self._payload, faker)
        # should cache response or not
        _logger.info("Use cache for faker: {0}, api_method= {1}".format(self._used_cache, self._api_method))
        if self._used_cache and (self._api_method == 'list' or self._api_method == 'retrieve'):
            self._set_cache_data(req_data=self._payload, res_data=response)
            _logger.info("Saved data to cached.....")

        return response

    mocker.patch("srm.repositories.odoo_repo.OdooRepo._send_request", fake_send_request)


@pytest.fixture()
def mocker_odoo_response_with_data(mocker):
    def with_data(data):
        def fake_execute_kw(self, dbs, uid, password, model, method, payload):
            return data
        mocker.patch("xmlrpc.client.ServerProxy.execute_kw", fake_execute_kw, create=True)

    return with_data


@pytest.fixture()
def mocker_odoo_response_with_xc_exception(mocker):
    def with_data(data):
        def fake_execute_kw(self, dbs, uid, password, model, method, payload):
            raise xc.Fault(data['faultCode'], data['faultString'])
        mocker.patch("xmlrpc.client.ServerProxy.execute_kw", fake_execute_kw, create=True)

    return with_data


@pytest.fixture()
def mocker_odoo_response_with_cache(mocker):
    def with_data(data, cache):
        def fake_execute_kw(self, dbs, uid, password, model, method, payload):
            raise xc.Fault(data['faultCode'], data['faultString'])

        def fake_get_cache_data(self, req_data=None):
            return cache

        mocker.patch("xmlrpc.client.ServerProxy.execute_kw", fake_execute_kw, create=True)
        mocker.patch("srm.repositories.odoo_repo.OdooRepo._get_cache_data", fake_get_cache_data)

    return with_data


@pytest.fixture()
def mocker_odoo_response_check_payload(mocker):
    def with_data(fields):
        def fake_execute_kw(self, dbs, uid, password, model, method, payloads):
            # Check if payload has extra fields
            for field in payloads[0]:
                if field not in fields:
                    _logger.debug('Payload has extra field ({0})'.format(field))
                    return 'Payload has extra field'

            # Check required fields
            for field in fields:
                if field not in payloads[0] and fields[field]:
                    _logger.debug('Payload missing required field ({0})'.format(field))
                    return 'Payload is missing required field'

            return {'code': 0, 'message': 'Payload is valid'}

        mocker.patch("xmlrpc.client.ServerProxy.execute_kw", fake_execute_kw, create=True)

    return with_data
