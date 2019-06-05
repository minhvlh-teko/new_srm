import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class ProductSaleBranch(OdooRepo):
    _name = 'sale_branches'
    _model = 'product.sale_branch'
