# coding=utf-8
import logging
from .odoo_repo import OdooRepo

__author__ = 'Son'
_logger = logging.getLogger('api')


class Warehouse(OdooRepo):
    _name = 'warehouses'
    _model = 'stock.warehouse'
    _mapping = {
        'list': 'api_get_list_detail',
    }
    _is_formalization = True
    _faker_data = {
        'req': {},
        'res': 'not OK'
    }

    def get_warehouses(self, data={}):
        """
        get list of warehouse
        :return: list[Warehouse]
        """
        return self.list(data)


class WarehouseMapping(OdooRepo):
    _name = 'warehouse_mapping'
    _model = 'stock.warehouse'
    _mapping = {
        'list': 'api_get_list_mapping',
    }
    _is_formalization = True
    _faker_data = {
        'req': {},
        'res': 'not OK'
    }

    def get_warehouse_mapping(self, data={}):
        """
        get list of warehouse
        :return: list[Warehouse]
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
