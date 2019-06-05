# coding=utf-8
import logging
from .odoo_repo import OdooRepo

__author__ = 'Son'
_logger = logging.getLogger(__name__)


class StockQuant(OdooRepo):
    _name = 'stock_quants'
    _model = 'product.product'
    _mapping = {
        'list': 'api_get_available_stock',
        'create': 'api_get_available_stock',  # support POST method for long list of products
    }
    _is_formalization = True
    ''' Set enable to get data from cache instead of get data directly from odoo'''
    _used_cache = True
    _faker_data = {
        'req': {
            'products': True,
            'regions': False,
            'branches': False,
            'warehouses': False,
            'locations': False,
        },
        'res': {
            "message": "OK",

            "data": {

                "1200109": [{

                    "warehouse": "CH0000",

                    "location": "000001",

                    "available": 6

                },

                    {

                        "warehouse": "CP01",

                        "location": "0101",

                        "available": 1

                    }],

                "1805119": [{

                    "warehouse": "CP04",

                    "location": "0402",

                    "available": 10

                }]

            }

        }
    }

    def _formalize(self, response):
        """
        Override parent method
        :param dict response:
        :return: dict
        """
        response = super()._formalize(response)
        # print(response)
        new_list = []
        for key in response[0]['result']:
            obj = {
                'sku': key,
                'items': []
            }
            for item in response[0]['result'][key]:
                obj['items'].append(item)
            new_list.append(obj)

        response[0]['result'] = new_list
        return response
