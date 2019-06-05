# coding=utf-8
import logging
from flask_restplus import fields
# from ..extensions.exceptions import BadRequestException
# from .. import repositories

from importlib import import_module

__author__ = 'Son'
_logger = logging.getLogger('api')


def call_odoo_repo(repo_name, method_name, data={}, module_name=None):
    """
    Load repositories to get class and call method API with data
    :param str repo_name: name of class of Repo, with CamelCase name
    :param str method_name: enum(create, list, retrieve, update, destroy)
    :param dict data:  request params
    :param str module_name:  module name (filename) of a repo
    :return: dict: return data
    """
    module_name = fields.camel_to_dash(repo_name) if not module_name else module_name
    repo_module = import_module('.' + module_name, 'wms.repositories')
    repo_class = getattr(repo_module, repo_name)
    return getattr(repo_class(), method_name)(data)
