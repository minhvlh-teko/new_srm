# coding=utf-8
import logging
import json

import flask_restplus as _fr
from flask import request

from ..services import odoo_service
from ..helpers import request_helper

__author__ = 'SonLp'
_logger = logging.getLogger('api')


class OdooCommon(_fr.Resource):
    _repo_name = ''
    _module_name = ''

    def parse_data(self):
        data = request.json['payload'] if request.json is not None and 'payload' in request.json else request.json
        if isinstance(data, str):
            data = json.loads(data)
        data.update(request_helper.get_special_params())
        _logger.info('data with special params: %s' % data)
        return data

    def post(self):
        data = self.parse_data()
        _logger.info("%s - %s" % (type(data), data))

        return self.call_odoo_repo('create', data)

    def put(self, id):
        data = self.parse_data()
        _logger.info(data)

        return self.call_odoo_repo('update', data)

    def get(self, id=None):
        data = request.args or request.json
        data.update(request_helper.get_special_params())
        _logger.info(data)

        method = 'list' if id is None else 'retrieve'

        return self.call_odoo_repo(method, data)

    def delete(self, id):
        data = self.parse_data()
        _logger.info(data)

        return self.call_odoo_repo('destroy', data)

    def call_odoo_repo(self, method, data):
        if self._module_name:
            return odoo_service.call_odoo_repo(self._repo_name, method, data=data, module_name=self._module_name)
        else:
            return odoo_service.call_odoo_repo(self._repo_name, method, data=data)
