import logging
import pytest
from ..general_test import GeneralTestCase

_logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('client_class')
@pytest.mark.usefixtures('app_class')
@pytest.mark.usefixtures('create_admin_user')
@pytest.mark.usefixtures('create_test_user')
class TestLoginLogout(GeneralTestCase):

    def test_access_index_page(self):
        res = self.client.get('/')
        res_data = res.data.decode('utf-8')
        assert res.status_code == 200
        assert 'Go to admin!' in res_data
        assert 'Go to Swagger UI!' in res_data

    def test_access_admin_index_page_without_user_login(self):
        res = self.client.get('/admin/')
        assert res.status_code == 302  # User not login so return a redirect response

    def test_access_admin_index_page_with_user_test_logged_in(self):
        self.test_login_success_with_account_test()
        res = self.client.get('/admin/')
        res_data = res.data.decode('utf-8')
        assert res.status_code == 200
        assert 'Wms-Admin' in res_data
        assert 'Odoo Account' not in res_data

    def test_access_admin_index_page_with_user_admin_logged_in(self):
        self.test_login_success_with_account_admin()
        res = self.client.get('/admin/')
        res_data = res.data.decode('utf-8')
        assert res.status_code == 200
        assert 'Wms-Admin' in res_data
        assert 'Odoo Account' in res_data

    def test_access_admin_register_page(self):
        res = self.client.get('/admin/register/')
        res_data = res.data.decode('utf-8')
        assert res.status_code == 200
        assert 'Already have an account?' in res_data
        assert 'Click here to log in.' in res_data

    def test_register_user_success(self):
        content_type = 'application/x-www-form-urlencoded'
        data = {
            'username': 'test_register_user_success',
            'password': 'test_register_user_success',
        }
        res = self.client.post('/admin/register/', content_type=content_type, data=data)
        assert res.status_code == 302

    def test_register_user_duplicate_username(self):
        # user test/test was created in fixture create_test_user
        content_type = 'application/x-www-form-urlencoded'
        data = {
            'username': 'test',
            'password': 'test',
        }
        res = self.client.post('/admin/register/', content_type=content_type, data=data)
        assert 'Duplicate username' in res.data.decode('utf-8')

    def test_access_admin_login_page(self):
        res = self.client.get('/admin/login/')
        assert res.status_code == 200

    def test_login_invalid_user(self):
        content_type = 'application/x-www-form-urlencoded'
        data = {
            'username': 'admin1',
            'password': 'admin1',
        }
        res = self.client.post('/admin/login/', content_type=content_type, data=data)
        assert 'Invalid user' in res.data.decode("utf-8")

    def test_login_invalid_password(self):
        content_type = 'application/x-www-form-urlencoded'
        data = {
            'username': 'admin',
            'password': 'admin1',
        }
        res = self.client.post('/admin/login/', content_type=content_type, data=data)
        assert 'Invalid password' in res.data.decode("utf-8")

    def test_login_success_with_account_test(self):
        content_type = 'application/x-www-form-urlencoded'
        data = {
            'username': 'test',
            'password': 'test',
        }
        res = self.client.post('/admin/login/', content_type=content_type, data=data)
        assert res.status_code == 302  # Login success then redirect

    def test_login_success_with_account_admin(self):
        content_type = 'application/x-www-form-urlencoded'
        data = {
            'username': 'admin',
            'password': 'admin',
        }
        res = self.client.post('/admin/login/', content_type=content_type, data=data)
        assert res.status_code == 302  # Login success then redirect

    def test_logout(self):
        self.test_login_success_with_account_test()
        res = self.client.get('/admin/logout/')
        assert res.status_code == 302  # Logout success then redirect
