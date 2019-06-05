# coding=utf-8
import logging

__author__ = 'Kien'
_logger = logging.getLogger('api')

# Import all necesary repositories here
from . import branch
from . import warehouse
from . import location
from . import srm_product
