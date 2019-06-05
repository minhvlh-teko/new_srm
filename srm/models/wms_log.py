# coding=utf-8
import logging

from . import db, TimestampMixin

__author__ = 'Sonlp'
_logger = logging.getLogger('api')


class WmsLog(db.Model, TimestampMixin):
    """
    Contains information of WMS LOG table
    """
    __tablename__ = 'wms_logs'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_ip = db.Column(db.String(191), nullable=True)
    payload = db.Column(db.Text(), nullable=True)
