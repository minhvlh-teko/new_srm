# coding=utf-8
import json
import logging

from ..general_test import GeneralTestCase
import pytest

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('client_class')
@pytest.mark.usefixtures('app_class')
class APITestCase(GeneralTestCase):
    def url(self):
        """

        :return:
        """
        raise NotImplementedError("Cần khai báo url API")

    def method(self):
        """

        :return:
        """
        raise NotImplementedError("Cần khai báo method của API")

    def send_request(self, data=None, content_type=None, method=None, url=None):
        """
        Tự động send request theo method và url
        :param data:
        :param content_type:
        :param method:
        :param url:
        :return:
        """
        content_type = content_type or 'application/json'

        if content_type == 'application/json' and data:
            data = json.dumps(data)

        method = method or self.method()
        method_func = getattr(self.client, method.lower())
        url = url or self.url()
        res = method_func(url, data=data, content_type=content_type)
        return res
