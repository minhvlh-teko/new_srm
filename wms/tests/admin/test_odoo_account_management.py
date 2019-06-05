import logging
import pytest
from ..general_test import GeneralTestCase

_logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('client_class')
@pytest.mark.usefixtures('app_class')
@pytest.mark.usefixtures('create_admin_user')
@pytest.mark.usefixtures('create_test_user')
class TestOdooAccountManagement(GeneralTestCase):

    _content_type = 'application/x-www-form-urlencoded'

    def login(self, username, password):
        data = dict(username=username, password=password)
        res = self.client.post('/admin/login/', content_type=self._content_type, data=data)
        assert res.status_code == 302

    def login_admin(self):
        self.login('admin', 'admin')

    def login_test(self):
        self.login('test', 'test')

    def test_access_odoo_account_list_with_user_admin_and_success(self):
        self.login_admin()
        res = self.client.get('/admin/odooaccount/')
        assert res.status_code == 200

    def test_access_odoo_account_list_with_user_test_and_fail(self):
        self.login_test()
        res = self.client.get('/admin/odooaccount/')
        assert res.status_code == 403

    def test_create_odoo_account_and_success(self):
        self.login_admin()
        url = '/admin/odooaccount/new/?url=%2Fadmin%2Fodooaccount%2F'
        res = self.client.get(url)
        assert res.status_code == 200
        data = dict(
            name='Test create',
            user='test_create',
            password='test_create',
            url='test.example.com',
            port=8069,
            dbs='wms_dev',
            uid=122,
            client_ip='10.0.2.2',
            status='y',
            secret_key='test',
            api_list=None,
            cors_allow=None,
        )
        res = self.client.post(url, content_type=self._content_type, data=data)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert 'Record was successfully created.' in res.data.decode('utf-8')

    def test_create_odoo_account_without_username_and_fail(self):
        self.login_admin()
        url = '/admin/odooaccount/new/?url=%2Fadmin%2Fodooaccount%2F'
        res = self.client.get(url)
        assert res.status_code == 200
        data = dict(
            name='Test create',
            user=None,
            password='test_create',
            url='test.example.com',
            port=8069,
            dbs='wms_dev',
            uid=122,
            client_ip='10.0.2.2',
            status='y',
            secret_key='test',
            api_list=None,
            cors_allow=None,
        )
        res = self.client.post(url, content_type=self._content_type, data=data)
        assert res.status_code == 200
        assert 'This field is required.' in res.data.decode('utf-8')

    def test_view_detail_exist_odoo_account_and_success(self):
        self.test_create_odoo_account_and_success()
        res = self.client.get('/admin/odooaccount/details/?id=1')
        assert res.status_code == 200

    def test_view_detail_not_exist_odoo_account_and_alert_record_not_exist(self):
        self.login_admin()
        res = self.client.get('/admin/odooaccount/details/?id=1')
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert 'Record does not exist.' in res.data.decode('utf-8')

    def test_edit_odoo_account_and_alert_record_saved(self):
        self.test_create_odoo_account_and_success()
        url = '/admin/odooaccount/edit/?id=1&url=%2Fadmin%2Fodooaccount%2F'
        res = self.client.get(url)
        assert res.status_code == 200
        data = dict(
            name='Test edit',
            user='test_edit',
            password='test_edit',
            url='test.example.com',
            port=8069,
            dbs='wms_dev',
            uid=122,
            client_ip='10.0.2.2',
            status='y',
            secret_key='test',
            api_list=None,
            cors_allow=None,
        )
        res = self.client.post(url, content_type=self._content_type, data=data)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert 'Record was successfully saved.' in res.data.decode('utf-8')
        res = self.client.get('/admin/odooaccount/details/?id=1')
        assert 'Test edit' in res.data.decode('utf-8')

    def test_edit_not_exist_odoo_account_and_alert_record_not_exist(self):
        self.login_admin()
        url = '/admin/odooaccount/edit/?id=1&url=%2Fadmin%2Fodooaccount%2F'
        res = self.client.get(url)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert 'Record does not exist.' in res.data.decode('utf-8')

    def test_delete_single_odoo_account_and_alert_record_deleted(self):
        self.test_create_odoo_account_and_success()
        data = dict(id=1)
        res = self.client.post('admin/odooaccount/delete/', content_type=self._content_type, data=data)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert 'Record was successfully deleted.' in res.data.decode('utf-8')

    def test_delete_not_exist_single_odoo_account_and_alert_record_not_exist(self):
        self.login_admin()
        data = dict(id=1)
        res = self.client.post('/admin/odooaccount/delete/', content_type=self._content_type, data=data)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert 'Record does not exist.' in res.data.decode('utf-8')

    def test_delete_multiple_odoo_account_with_2_id_exist_then_alert_2_records_were_deleted(self):
        self.test_create_odoo_account_and_success()
        self.test_create_odoo_account_and_success()
        data = dict(action='delete', rowid=[1, 2])
        res = self.client.post('/admin/odooaccount/action/', content_type=self._content_type, data=data)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert '2 records were successfully deleted.' in res.data.decode('utf-8')

    def test_delete_multiple_odoo_account_with_2_id_not_exist_then_alert_0_records_were_deleted(self):
        self.login_admin()
        data = dict(action='delete', rowid=[1, 2])
        res = self.client.post('/admin/odooaccount/action/', content_type=self._content_type, data=data)
        assert res.status_code == 302
        res = self.client.get('/admin/odooaccount/')
        assert '0 records were successfully deleted.' in res.data.decode('utf-8')
