# coding=utf-8
import logging

__author__ = 'Kien'
_logger = logging.getLogger('api')

# Import all necesary services here
from . import branch
from . import warehouse
from . import location
from . import srm_product
from . import odoo_service
