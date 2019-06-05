# coding=utf-8
import logging
from .odoo_repo import OdooRepo

__author__ = 'Son'
_logger = logging.getLogger('api')


class Branch(OdooRepo):
    _name = 'branches'
    _model = 'teko.branch'
    _mapping = {
        'list': 'api_get_list_detail',
    }
    _is_formalization = True
    _faker_data = {
        'req': {},
        'res': "not OK"
    }

    def get_branches(self, data={}):
        """
        get list of branch
        :return: list[Branch]
        """
        return self.list(data)


class BranchMapping(OdooRepo):
    _name = 'branch_mapping'
    _model = 'teko.branch'
    _mapping = {
        'list': 'api_get_list_mapping',
    }
    _is_formalization = True
    _faker_data = {
        'req': {},
        'res': 'not OK'
    }

    def get_branch_mapping(self, data={}):
        """
        get list of branch
        :return: list[Branch]
        """
        return self.list(data)

    # def _formalize(self, response):
    #     """
    #     Override parent method
    #     :param response:
    #     :return:
    #     """
    #     response = super()._formalize(response)
    #     new_list = []
    #     for key in response:
    #         new_list.append({
    #             'code': key,
    #             'name': response[key]
    #         })
    #     return new_list
