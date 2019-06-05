# coding=utf-8
import logging

from . import db, TimestampMixin

__author__ = 'Sonlp'
_logger = logging.getLogger('api')


class OdooAccount(db.Model, TimestampMixin):
    """
    Contains information of Odoo Acounts table
    """
    __tablename__ = 'odoo_accounts'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=True, default='None')
    user = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=8069)
    dbs = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.Integer, nullable=True, default=None)
    client_ip = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    # Add secret key for the case using public API
    secret_key = db.Column(db.String(256), nullable=True, default='')
    # List of public API restriction for secret key
    api_list = db.Column(db.String(256), nullable=True, default='')
    # CORS allow access control origin
    cors_allow = db.Column(db.String(250), nullable=True, default='')
