# coding=utf-8
import logging
from .odoo_repo import OdooRepo

__author__ = 'Son'
_logger = logging.getLogger('api')


class SrmProduct(OdooRepo):
    _name = 'products'
    _model = 'product.product'
    _is_formalization = True

    def create_srm_product(self, data={}):
        """
        get list of srm_product
        :return: list[SrmProduct]
        """
        return self.create(data)
