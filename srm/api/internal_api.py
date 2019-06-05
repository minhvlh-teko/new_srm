# coding=utf-8
import logging


from ..extensions import Namespace

from .odoo_common import OdooCommon


__author__ = 'MinhVlh'
_logger = logging.getLogger('api')

ns = Namespace('Internal', description='Internal API operations')


@ns.route('/stockTransfer/<int:id>/', methods=['PUT'], doc=False)
class StockTransferPUT(OdooCommon):
    _repo_name = 'StockTransfer'



@ns.route('/purchaseOrderReceipt/', methods=['POST'], doc=False)
class PurchaseOrderReceiptPOST(OdooCommon):
    _repo_name = 'PurchaseOrderReceipt'


@ns.route('/purchaseOrderReceipt/<int:id>/', methods=['PUT'], doc=False)
class PurchaseOrderReceiptPUT(OdooCommon):
    _repo_name = 'PurchaseOrderReceipt'



@ns.route('/purchaseOrderInvoice/<int:id>/', methods=['PUT'], doc=False)
class PurchaseOrderInvoicePUT(OdooCommon):
    _repo_name = 'PurchaseOrderInvoice'




@ns.route('/accountInvoice/', methods=['POST'], doc=False)
class AccountInvoicePOST(OdooCommon):
    _repo_name = 'AccountInvoice'



@ns.route('/stockPickingType/', methods=['POST'], doc=False)
class StockPickingTypePOST(OdooCommon):
    _repo_name = 'StockPickingType'


@ns.route('/stockPickingType/<int:id>/', methods=['PUT','DELETE'], doc=False)
class StockPickingTypePUT(OdooCommon):
    _repo_name = 'StockPickingType'



