# coding=utf-8
import logging
import re
import json
import ast

import odoorpc
import xmlrpc.client as xc
from ..models import OdooAccount
from ..extensions import exceptions
from werkzeug.datastructures import ImmutableMultiDict
from dictsearch.search import iterate_dictionary

from ..extensions.response_wrapper import wrap_response

from flask import request, current_app

__author__ = 'Son'
_logger = logging.getLogger('api')

"""
Constant code errors response from Odoo
"""
RPC_FAULT_CODE_APPLICATION_ERROR = 1
RPC_FAULT_CODE_WARNING = 2
RPC_FAULT_CODE_ACCESS_DENIED = 3
RPC_FAULT_CODE_ACCESS_ERROR = 4
RPC_FAULT_CODE_CLIENT_ERROR = 5

ODOO_REPO_CACHE_TIME_LIMIT = 300


class OdooRepo:
    """
    This Repo is the port to connect and get api from Odoo
    """
    # Const values
    _CACHE_KEY_PREFIX = '_redis_odoo__'

    # properties values
    _api_method = None
    _client_ip = None
    _cors_allow = ''
    _name = 'odoo_repo'
    _odoo = None
    _model = None
    _mapping = {
        'create': 'api_create_from_msg',
        'update': 'api_update_from_msg',
        'delete': 'api_delete_from_msg',
    }
    ''' if this param is set to true, all requests and responses param will be standardlized'''
    _is_formalization = False
    ''' by default is sending to odoo, for the case testing sample data, set to faker, or cache: set to cache'''
    _target = 'odoo'
    ''' Set enable to get data from cache instead of get data directly from odoo'''
    _used_cache = False
    ''' Life time limited for caching, default 300 seconds, 0 mean unlimited'''
    _cached_time_limited = ODOO_REPO_CACHE_TIME_LIMIT
    ''' Unique cache key'''
    _cache_key = None
    ''' Cache provider'''
    _cache_provider = None

    '''
    Faker data for testing
    - For instance:
        _faker_data = {
            'req': {
                'id': True,
                'name': False
            },
            'res': {
            
            }
        }
      It means field 'id' is required, 'name' is not required  
    '''
    _faker_data = {
        'req': None,
        'res': None
    }
    '''If payload has these key, then update properties and pop'''
    _special_params = {
        'no_cache': None,
        'use_faker': False,
        'debug_mode': False,
    }

    def __init__(self, target='odoo', used_cache=None, cache_life_time=ODOO_REPO_CACHE_TIME_LIMIT):
        """
        Construct method
        :param str target: target server to get data, enum('odoo', 'cache', 'faker')
        :param boolean used_cache: enable cache or not
        :param int cache_life_time: life time for cache storage
        """
        self._target = target
        self._used_cache = used_cache if used_cache else self._used_cache
        self._cached_time_limited = cache_life_time

    def _get_account(self, client_ip):
        """
        GEt odoo account to loggin and get data from api
        :param str client_ip:  ip
        :return: [OdooAccount] account info
        """
        account = OdooAccount.query.filter(
            OdooAccount.client_ip.ilike('%{0}%'.format(client_ip))
        ).first()
        if account:
            return account
        raise exceptions.UnAuthorizedException('Client IP not authenticate!')

    def _get_account_by_secret(self):
        """
        Use for public API to access if secret key is exist and not null
        :param secret_key:
        :return: account info
        """

        if not self._is_using_secret_key():
            raise exceptions.ForbiddenException('Cannot access function _get_account_by_secret when secret key is null')

        # account = OdooAccount.objects.filter(secret_key=self._secret_key).filter(api_list__contains=self._name)
        account = OdooAccount.query.filter(OdooAccount.secret_key == self._secret_key).filter(
            OdooAccount.api_list.contains(self._name)).all()

        if account:
            return account[0]
        raise exceptions.UnAuthorizedException('Secret Key is invalid!')

    def _is_using_secret_key(self):
        """
        Check if this API using Secret Key for Public API or not
        :return: True if this API use secret key
        """
        if self._secret_key is not None and self._secret_key:
            return True
        else:
            return False

    def _update_secret_key_info(self):
        """
        If params of request have secret_key value then update to the system
        :return: None
        """
        params = self._payload
        secret_key = params.get('secret_key')
        if secret_key is None or not secret_key:
            self._secret_key = None
        else:
            self._secret_key = secret_key

    def _get_client_ip(self):
        if self._client_ip is None:
            x_forwarded_for = request.headers.getlist('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                self._client_ip = x_forwarded_for.split(',')[0]
            else:
                self._client_ip = request.remote_addr

        return self._client_ip

    def _get_odoo_client(self):
        if self._odoo is None:
            self._odoo = self._connect()
        return self._odoo

    def _handle(self, rq_data, *args, **kwargs):
        """
        Manage all all request handle here
        :param rq_data:
        :param args:
        :param kwargs:
        :return:
        """
        _logger.info('[%s@%s] Called by <%s>...' % (self._name, self._api_method, self._get_client_ip()))
        # get data params
        self._parse_payload(rq_data)
        # make all data to underscope style
        self._formalize_payload()

        _logger.debug('[%s@%s] Payload:\n%s' % (self._name, self._api_method, self._payload))

        try:

            if not (self._model and self._mapping and self._mapping.get(self._api_method)):
                raise exceptions.BadRequestException("Endpoint is not defined.")

            _logger.info('Payload %s', self._payload)

            response = self._call_api()

            _logger.info('[%s@%s] Completed.' % (self._name, self._api_method))
            # _logger.info('response: %s', response)
            rs_data = self._formalize(response)
            # _logger.info('response formalized: %s', rs_data)
            return rs_data

            # Set response header CORS for public API
            # if self._cors_allow:
            #     header = {
            #         "Access-Control-Allow-Origin": self._cors_allow
            #     }
            #     return Response(response, None, None, header)
            # else:
            #     return Response(response)

        except Exception as e:
            _logger.exception('[%s@%s] FAILED' % (self._name, self._api_method))
            # raise exceptions.global_error_handler(e)
            raise e

    def _validate(self, response):
        """
        Validate data response, formalization and wrap response
        :param response: dict data return from Odoo
        :return: Dict, necessary data to return
        """

        if isinstance(response, dict):
            if self._is_formalization:
                data = self._apply_camelcase_to_dict(response.get("data")) if response.get("data") else {}
                return wrap_response(data)
            else:
                return response
        else:
            msg = "There is a problem with response format"
            _logger.debug(msg)
            if isinstance(response, str):
                msg = response
            raise exceptions.HTTPException(message=msg)

    def _call_api(self):
        """
        Call API to Odoo
        :return: dict[Response data]
        """

        # Update secret key if available, should add to init functions
        self._update_secret_key_info()
        # Check whether using Secret Key  or Using IP to get API account
        if self._is_using_secret_key():
            account = self._get_account_by_secret()
            # Only set response header when using Public API
            self._cors_allow = account.cors_allow
        else:
            client_ip = self._get_client_ip()
            account = self._get_account(client_ip)

        return self._send_request(account)

    def _send_request(self, account=None, faker=None):
        """
        Send request by payload to _target
        :param obj account:
        :param dict|list faker: faker data from target response, using for unit test
        :return: dict response
        """
        # Check if should get data from cache first or not, only apply for get method
        if self._used_cache and (self._api_method == 'list' or self._api_method == 'retrieve'):
            response = self._get_cache_data(self._payload)
            if response:
                _logger.info("Cached data exists, return data.....")
                return response

        if self._target == 'odoo':
            try:
                if account.port != 443:
                    url = 'http://{0}:{1}'.format(account.url, account.port)
                else:
                    url = 'https://{0}'.format(account.url)
                if not account.uid:
                    common = xc.ServerProxy('{}/xmlrpc/2/common'.format(url))
                    account.uid = common.authenticate(account.dbs, account.user, account.password, {})
                    account.save()
                _logger.info("Prepare to send to Odoo, url:%s...", '{}/xmlrpc/2/object'.format(url))
                models = xc.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                response = models.execute_kw(account.dbs, account.uid, account.password,
                                             self._model, self._mapping.get(self._api_method),
                                             [self._payload])

                # Clear cache if user send param with no_cache = False
                if self._special_params['no_cache'] is not None and not self._used_cache:
                    _logger.info('Should clear cache because use pass param no_cache = true')
                    self._delete_cache_data(self._payload)
                # should cache response or not
                _logger.info("Use cache: {0}, api_method= {1}".format(self._used_cache, self._api_method))
                if self._used_cache and (self._api_method == 'list' or self._api_method == 'retrieve'):
                    self._set_cache_data(req_data=self._payload, res_data=response)
                    _logger.info("Saved data to cached.....")
                return response
            except xc.Fault as e:

                error_msg = e.faultString
                error_data = None

                try:
                    error = ast.literal_eval(e.faultString)
                except:
                    error = None
                if isinstance(error, tuple) and len(error) == 2:
                    error_msg, error_data = error
                    try:
                        error_data = json.loads(error_data)
                    except:
                        pass
                _logger.error("[%s@%s] RPC FAULT <%s> %s", self._name, self._api_method, e.faultCode, e.faultString)

                errors = None
                if not self._is_formalization:
                    errors = {
                        'internal_response': {
                            'code': e.faultCode,
                            'data': error_data,
                            'message': error_msg
                        }
                    }

                if e.faultCode == RPC_FAULT_CODE_CLIENT_ERROR:
                    # status_code = 400
                    raise exceptions.BadRequestException(error_msg, errors)
                elif e.faultCode == RPC_FAULT_CODE_ACCESS_ERROR:
                    # status_code = 401
                    raise exceptions.UnAuthorizedException(error_msg, errors)
                elif e.faultCode == RPC_FAULT_CODE_ACCESS_DENIED:
                    # status_code = 403
                    raise exceptions.ForbiddenException(error_msg, errors)
                elif e.faultCode == RPC_FAULT_CODE_WARNING:
                    # Still return success with status code
                    # status_code = 200
                    if self._is_formalization:
                        return {
                            'code': 200,
                            'message': error_msg,
                            'result': None
                        }
                    else:
                        return errors['internal_response']
                else:
                    # status_code = 500
                    raise exceptions.HTTPException(code=500, message=error_msg)

            except Exception as e:
                _logger.exception('[%s@%s] RPC Unknown Exception', self._name, self._api_method)
                raise exceptions.HTTPException(code=500, message=str(e))
        elif self._target == 'faker':
            # TODO: Using fake data from Odoo
            _logger.info("Using Faker data...................")
            response = self.get_faker_data(self._payload, faker)
            # should cache response or not
            _logger.info("Use cache for faker: {0}, api_method= {1}".format(self._used_cache, self._api_method))
            if self._used_cache and (self._api_method == 'list' or self._api_method == 'retrieve'):
                self._set_cache_data(req_data=self._payload, res_data=response)
                _logger.info("Saved data to cached.....")

            return response
        else:
            raise exceptions.HTTPException(message='Invalid TARGET provider.')

    def _connect(self):
        try:
            client_ip = self._get_client_ip()
            account = self._get_account(client_ip)
            odoo = odoorpc.ODOO(account.url, port=account.port)
            odoo.login(account.dbs, account.user, account.password)
            _logger.info('Success authentication user %s', odoo.env.user.name)
            return odoo
        except Exception as e:
            _logger.info('Failed to authenticate error= %s', repr(e))
            raise exceptions.UnAuthorizedException('Can not authentication! Client IP: %s' % client_ip)

    def create(self, rq_data, *args, **kwargs):
        """
        Apply for Post method
        :param dict|list rq_data:
        :param args:
        :param kwargs:
        :return:
        """
        self._api_method = 'create'
        return self._handle(rq_data, *args, **kwargs)

    def retrieve(self, rq_data, *args, **kwargs):
        """
        Apply for GET one item method
        :param dict|list rq_data:
        :param args:
        :param kwargs:
        :return:
        """
        self._api_method = 'retrieve'
        return self._handle(rq_data, *args, **kwargs)

    def list(self, rq_data, *args, **kwargs):
        """
        Apply for GET a list of item Method
        :param dict|list rq_data:
        :param args:
        :param kwargs:
        :return:
        """
        self._api_method = 'list'
        return self._handle(rq_data, *args, **kwargs)

    def update(self, rq_data, *args, **kwargs):
        """
        Apply for PUT method
        :param dict|list rq_data:
        :param args:
        :param kwargs:
        :return:
        """
        self._api_method = 'update'
        return self._handle(rq_data, *args, **kwargs)

    def destroy(self, rq_data, *args, **kwargs):
        """
        Apply DELETE method
        :param dict|list rq_data:
        :param args:
        :param kwargs:
        :return:
        """
        self._api_method = 'delete'
        return self._handle(rq_data, *args, **kwargs)

    def _parse_payload(self, rq_data):
        """
        Parse payload from data input
        :param rq_data:
        :return:
        """
        payload = rq_data
        if isinstance(payload, ImmutableMultiDict):
            payload = payload.to_dict(flat=False)

        if payload:
            self._payload = payload if not isinstance(payload, str) else json.loads(payload)
            self._parse_special_params(self._payload)  # pop special keys
        else:
            self._payload = {}

    def _formalize_payload(self):
        """make all data to underscore style"""
        if self._is_formalization:
            self._apply_underscore_to_dict(self._payload)

    def _to_underscore(self, name):
        """
        Convert ( Lower) Camelcase to underscore
        :param  str name: string to be converted
        :return:
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _to_camel_case(self, snake_str):
        """
        Convert underscore to camel case
        :param str snake_str: string to be converted
        :return:
        """
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return components[0] + ''.join(x.title() for x in components[1:])

    def _apply_underscore_to_dict(self, dict_item):
        """
        under score for all key of a dict (using reference variable)
        :param dict|list dict_item: dictionary or list object to be converted
        :return: dict
        """
        if isinstance(dict_item, dict):
            for key in dict_item:
                item = dict_item.pop(key)
                dict_item[self._to_underscore(key)] = item
                if isinstance(item, dict) or isinstance(item, list):
                    self._apply_underscore_to_dict(item)

        if isinstance(dict_item, list):
            for item in dict_item:
                if isinstance(item, dict) or isinstance(item, list):
                    self._apply_underscore_to_dict(item)

    def _apply_camelcase_to_dict(self, dict_item):
        """
        under score for all key of a dict (using reference variable)
        :param dict|list dict_item: dictionary or list object to be converted
        :return: dict|list
        """
        if isinstance(dict_item, dict):
            for key in dict_item:
                item = dict_item.pop(key)
                dict_item[self._to_camel_case(key)] = item
                if isinstance(item, dict) or isinstance(item, list):
                    self._apply_camelcase_to_dict(item)

        if isinstance(dict_item, list):
            for item in dict_item:
                if isinstance(item, dict) or isinstance(item, list):
                    self._apply_camelcase_to_dict(item)
        return dict_item

    def _formalize(self, response):
        """
        Abstract method to reformat response following good rule
        :param dict response: odoo response data
        :return: dict
        """
        return self._validate(response)

    def _parse_by_template(self, content, mapping):
        """
        Define emplate and add content to payload
        :param content:
        :param mapping:
        :return:
        """
        response = {}

        for key, val in mapping.items():
            response[key] = iterate_dictionary(content, val)
            # Because all return list as value so we must get real value
            if response[key] is not None and len(response[key]) == 1 and not isinstance(response[key][0], dict):
                response[key] = response[key][0]

        return response

    def _get_req_data_fields(self, req_data):
        """
        Convert request data params to string
        :param dict|list req_data:
        :return: serialized string
        """
        # //Should order req_data fields
        return json.dumps(req_data)

    def _generate_cache_key(self, req_data=None):
        """
        Generate unique cache key for the request
        :param list|dict req_data:
        :return: str key
        """
        # using prefix plus class name of this instance
        prefix = self._CACHE_KEY_PREFIX + self.__class__.__name__ + '__'
        return prefix + (self._get_req_data_fields(req_data) if req_data else '')

    def _get_cache_key(self, req_data=None):
        """
        Get cache key
        :param dict|list req_data:
        :return: str key
        """
        if not self._cache_key:
            self._cache_key = self._generate_cache_key(req_data)
        return self._cache_key

    def get_cache_provider(self):
        """
        Get cache provider
        :return: Redis provider
        """
        if not self._cache_provider:
            # _logger.info(current_app.config)
            self._cache_provider = current_app.config['REDIS_PROVIDER']
        return self._cache_provider

    def _get_cache_data(self, req_data=None):
        """
        Get cache data, using lazy load
        :param dict|list req_data: request data
        :return:
        """
        key = self._get_cache_key(req_data)
        cache_provider = self.get_cache_provider()
        _logger.info("Get data from cached..... with ke={0}".format(key))
        _logger.info("Data: {0}".format(cache_provider.get(key)))
        if cache_provider:
            data = cache_provider.get(key)
            if data:
                _logger.info("Successfully get cache data object...")
                return json.loads(data.decode("utf-8"))

        return None

    def _delete_cache_data(self, req_data=None):
        """
        Get cache data, using lazy load
        :param dict|list req_data: request data
        :return:
        """
        key = self._get_cache_key(req_data)
        cache_provider = self.get_cache_provider()
        _logger.info("Delete data from cached..... with ke={0}".format(key))
        if cache_provider:
            data = cache_provider.delete(key)
            if data:
                _logger.info("Successfully deleted cache data object...")

        return None

    def _set_cache_data(self, req_data=None, res_data=None):
        """
        Set cache data, using lazy load
        :param req_data:
        :param str res_data:
        :return:
        """
        key = self._get_cache_key(req_data)
        cache_provider = self.get_cache_provider()
        if cache_provider:
            _logger.info("Store response to cache....")

            return cache_provider.set(key, json.dumps(res_data), ex=self._cached_time_limited)
        else:
            _logger.info("Store response to cache fail, provider is null...")
            return None

    def get_faker_data(self, req_data=None, res_data=None):
        """
        Get Faker data, using for unit test
        :param req_data:
        :param res_data:
        :return: dict
        """
        if res_data:
            self.set_faker_data(res_data=res_data)

        # Check if all keys is valid
        if req_data:
            invalid_key = None
            for key in req_data:
                if key not in self._faker_data['req']:
                    invalid_key = key
                    break
            if invalid_key:
                # Invalid input key
                raise exceptions.BadRequestException('Key ({0}) is invalid'.format(invalid_key))
            # Check if required fields dont exist

            if self._faker_data['req']:
                for key in self._faker_data['req']:
                    if key not in req_data and self._faker_data['req'][key]:
                        invalid_key = key
                        break
            if invalid_key:
                # Missing key required
                raise exceptions.BadRequestException('Key ({0}) is required'.format(invalid_key))
        return self._faker_data['res']

    def set_faker_data(self, req_data=None, res_data=None):
        """
        Set faker data format for unit test
        :param dict|list req_data:
        :param dic|list res_data:
        :return:
        """
        if req_data:
            self._faker_data['req'] = req_data
        if res_data:
            self._faker_data['res'] = res_data

    def _parse_special_params(self, payload):
        """
        Pop payload item for those keys which are in _special_params
        :param dict payload:
        :return:
        """
        if payload:
            # _logger.info("Parsing special query params: use_faker, no_cache......")
            # _logger.info("before: {}".format(payload))
            for key in self._special_params:
                if key in payload:
                    self._special_params[key] = payload.pop(key)
                    if key == 'use_faker':
                        self._target = 'faker' if self._special_params[key] else 'odoo'
                    if key == 'no_cache':
                        self._used_cache = False if self._special_params[key] else True
            # _logger.info("After: {}. With use_fake:{}. used cache:{}".format(payload, self._target, self._used_cache))
        return payload
