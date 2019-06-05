# coding=utf-8
import logging

from .odoo_common import OdooCommon

from ..extensions import Namespace

from flask import request

# from flask_restplus import fields

__author__ = 'SonLp'
_logger = logging.getLogger('api')

ns = Namespace('Internal', description='Internal API operations')

# request_model = ns.model('request_model', {
#     'payload': fields.String(required=True)
# })


@ns.route('/account_account/', methods=['POST'], doc=False)
class AccountAccount(OdooCommon):
    _repo_name = 'AccountAccount'


@ns.route('/account_account/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountAccountSingle(OdooCommon):
    _repo_name = 'AccountAccount'


@ns.route('/account_tag/', methods=['POST'], doc=False)
class AccountAccountTag(OdooCommon):
    _repo_name = 'AccountAccountTag'


@ns.route('/account_tag/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountAccountTagSingle(OdooCommon):
    _repo_name = 'AccountAccountTag'


@ns.route('/account_template/', methods=['POST'], doc=False)
class AccountTemplate(OdooCommon):
    _repo_name = 'AccountAccountTemplate'


@ns.route('/account_template/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountTemplateSingle(OdooCommon):
    _repo_name = 'AccountAccountTemplate'


@ns.route('/account_type/', methods=['POST'], doc=False)
class AccountAccountType(OdooCommon):
    _repo_name = 'AccountAccountType'


@ns.route('/account_type/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountAccountTypeSingle(OdooCommon):
    _repo_name = 'AccountAccountType'


@ns.route('/account_group/', methods=['POST'], doc=False)
class AccountGroup(OdooCommon):
    _repo_name = 'AccountGroup'


@ns.route('/account_group/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountGroupSingle(OdooCommon):
    _repo_name = 'AccountGroup'


# router.register(r'invoices', AccountInvoiceViewSet, 'invoices')
@ns.route('/invoices/<int:id>/', methods=['PUT'], doc=False)
class AccountInvoiceSingle(OdooCommon):
    _repo_name = 'AccountInvoice'


@ns.route('/account_journal/', methods=['POST'], doc=False)
class AccountJournal(OdooCommon):
    _repo_name = 'AccountJournal'


@ns.route('/account_journal/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountJournalSingle(OdooCommon):
    _repo_name = 'AccountJournal'


@ns.route('/account_payment_term/', methods=['POST'], doc=False)
class AccountPaymentTerm(OdooCommon):
    _repo_name = 'AccountPaymentTerm'


@ns.route('/account_payment_term/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountPaymentTermSingle(OdooCommon):
    _repo_name = 'AccountPaymentTerm'


@ns.route('/account_payment_term_line/', methods=['POST'], doc=False)
class AccountPaymentTermLine(OdooCommon):
    _repo_name = 'AccountPaymentTermLine'


@ns.route('/account_payment_term_line/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountPaymentTermLineSingle(OdooCommon):
    _repo_name = 'AccountPaymentTermLine'


@ns.route('/account_tax/', methods=['POST'], doc=False)
class AccountTax(OdooCommon):
    _repo_name = 'AccountTax'


@ns.route('/account_tax/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountTaxSingle(OdooCommon):
    _repo_name = 'AccountTax'


@ns.route('/account_tax_group/', methods=['POST'], doc=False)
class AccountTaxGroup(OdooCommon):
    _repo_name = 'AccountTaxGroup'


@ns.route('/account_tax_group/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountTaxGroupSingle(OdooCommon):
    _repo_name = 'AccountTaxGroup'


@ns.route('/account_tax_template/', methods=['POST'], doc=False)
class AccountTaxTemplate(OdooCommon):
    _repo_name = 'AccountTaxTemplate'


@ns.route('/account_tax_template/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class AccountTaxTemplateSingle(OdooCommon):
    _repo_name = 'AccountTaxTemplate'


@ns.route('/lo_bl_delivered/', methods=['POST'], doc=False)
class LoBlDelivered(OdooCommon):
    _repo_name = 'LoBlDelivered'


@ns.route('/lo_bl_returning/', methods=['POST'], doc=False)
class LoBlReturning(OdooCommon):
    _repo_name = 'LoBlReturning'


@ns.route('/mrp_bom/', methods=['POST'], doc=False)
class MrpBom(OdooCommon):
    _repo_name = 'MrpBom'


@ns.route('/mrp_bom/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class MrpBomSingle(OdooCommon):
    _repo_name = 'MrpBom'


@ns.route('/po_lines/', methods=['POST'], doc=False)
class PoLine(OdooCommon):
    _repo_name = 'PoLine'


@ns.route('/po_lines/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class PoLineSingle(OdooCommon):
    _repo_name = 'PoLine'


@ns.route('/po_receipts/', methods=['POST'], doc=False)
class PoReceipt(OdooCommon):
    _repo_name = 'PoReceipt'


@ns.route('/po_types/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class PoTypeSingle(OdooCommon):
    _repo_name = 'PoType'


@ns.route('/po_type_details/', methods=['POST'], doc=False)
class PoTypeDetail(OdooCommon):
    _repo_name = 'PoTypeDetail'


@ns.route('/po_type_details/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class PoTypeDetailSingle(OdooCommon):
    _repo_name = 'PoTypeDetail'


# list, create
@ns.route('/por_prices/', methods=['GET', 'POST'], doc=False)
class PorPrices(OdooCommon):
    _repo_name = 'PorPrices'

    def get(self, id=None):
        data = request.args
        product_codes = data.get('products')
        partner_id = data.get('partner')

        message = None
        if not product_codes:
            message = 'Param `products` is required'
        if not partner_id:
            message = 'Param `partner` is required'

        if message:
            return {
                'code': -1,
                'data': None,
                'message': message
            }, 400

        product_codes = product_codes.split(',')
        data = {
            'products': product_codes,
            'partner': partner_id
        }
        _logger.info(data)

        method = 'list' if id is None else 'retrieve'

        return self.call_odoo_repo(method, data)


@ns.route('/por_receipts/', methods=['POST'], doc=False)
class PorReceipt(OdooCommon):
    _repo_name = 'PorReceipt'


@ns.route('/por_types/', methods=['POST'], doc=False)
class PorType(OdooCommon):
    _repo_name = 'PorType'


@ns.route('/por_types/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class PorTypeSingle(OdooCommon):
    _repo_name = 'PorType'


@ns.route('/por_type_details/', methods=['POST'], doc=False)
class PorTypeDetail(OdooCommon):
    _repo_name = 'PorTypeDetail'


@ns.route('/por_type_details/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class PorTypeDetailSingle(OdooCommon):
    _repo_name = 'PorTypeDetail'


@ns.route('/product_attribute/', methods=['POST'], doc=False)
class ProductAttribute(OdooCommon):
    _repo_name = 'ProductAttribute'


@ns.route('/product_attribute/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductAttributeSingle(OdooCommon):
    _repo_name = 'ProductAttribute'


@ns.route('/product_attribute_value/', methods=['POST'], doc=False)
class ProductAttributeValue(OdooCommon):
    _repo_name = 'ProductAttributeValue'


@ns.route('/product_attribute_value/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductAttributeValueSingle(OdooCommon):
    _repo_name = 'ProductAttributeValue'


# router.register(r'brands', ProductBrandViewSet, 'brands')
@ns.route('/brands/', methods=['POST'], doc=False)
class ProductBrand(OdooCommon):
    _repo_name = 'ProductBrand'


@ns.route('/brands/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductBrandSingle(OdooCommon):
    _repo_name = 'ProductBrand'


# router.register(r'categories', ProductCategoryViewSet, 'categories')
@ns.route('/categories/', methods=['POST'], doc=False)
class ProductCategory(OdooCommon):
    _repo_name = 'ProductCategory'


@ns.route('/categories/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductCategorySingle(OdooCommon):
    _repo_name = 'ProductCategory'


# router.register(r'pricelists', ProductPricelistViewSet, 'pricelists')
@ns.route('/pricelists/', methods=['POST'], doc=False)
class ProductPricelist(OdooCommon):
    _repo_name = 'ProductPricelist'


@ns.route('/pricelists/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductPricelistSingle(OdooCommon):
    _repo_name = 'ProductPricelist'


# router.register(r'pricelist_items', ProductPricelistItemViewSet, 'pricelist_items')
@ns.route('/pricelist_items/', methods=['POST'], doc=False)
class ProductPriceListItems(OdooCommon):
    _repo_name = 'ProductPricelistItem'


@ns.route('/pricelist_items/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductPriceListItemsSingle(OdooCommon):
    _repo_name = 'ProductPricelistItem'


@ns.route('/products/', methods=['POST'], doc=False)
class ProductProduct(OdooCommon):
    _repo_name = 'ProductProduct'


@ns.route('/products/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductProductSingle(OdooCommon):
    _repo_name = 'ProductProduct'


# router.register(r'sale_branches', ProductSaleBranchViewSet, 'sale_branches')
@ns.route('/sale_branches/', methods=['POST'], doc=False)
class ProductSaleBranch(OdooCommon):
    _repo_name = 'ProductSaleBranch'


@ns.route('/sale_branches/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductSaleBranchSingle(OdooCommon):
    _repo_name = 'ProductSaleBranch'


# router.register(r'supplierinfos', ProductSupplierInfoViewSet, 'supplierinfos')
@ns.route('/supplierinfos/', methods=['POST'], doc=False)
class ProductSupplierInfo(OdooCommon):
    _repo_name = 'ProductSupplierInfo'


@ns.route('/supplierinfos/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductSupplierInfoSingle(OdooCommon):
    _repo_name = 'ProductSupplierInfo'


@ns.route('/product_templates/', methods=['POST'], doc=False)
class ProductTemplate(OdooCommon):
    _repo_name = 'ProductTemplate'


@ns.route('/product_templates/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductTemplateSingle(OdooCommon):
    _repo_name = 'ProductTemplate'


@ns.route('/product_uom/', methods=['POST'], doc=False)
class ProductUom(OdooCommon):
    _repo_name = 'ProductUom'


@ns.route('/product_uom/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductUomSingle(OdooCommon):
    _repo_name = 'ProductUom'


@ns.route('/product_uom_categ/', methods=['POST'], doc=False)
class ProductUomCateg(OdooCommon):
    _repo_name = 'ProductUomCateg'


@ns.route('/product_uom_categ/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ProductUomCategSingle(OdooCommon):
    _repo_name = 'ProductUomCateg'


@ns.route('/purchase_orders/', methods=['POST'], doc=False)
class PurchaseOrder(OdooCommon):
    _repo_name = 'PurchaseOrder'


@ns.route('/purchase_orders/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class PurchaseOrderSingle(OdooCommon):
    _repo_name = 'PurchaseOrder'


@ns.route('/res_partner_bank/', methods=['POST'], doc=False)
class ResPartnerBank(OdooCommon):
    _repo_name = 'ResPartnerBank'


@ns.route('/res_partner_bank/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ResPartnerBankSingle(OdooCommon):
    _repo_name = 'ResPartnerBank'


@ns.route('/res_partner_category/', methods=['POST'], doc=False)
class ResPartnerCategory(OdooCommon):
    _repo_name = 'ResPartnerCategory'


@ns.route('/res_partner_category/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ResPartnerCategorySingle(OdooCommon):
    _repo_name = 'ResPartnerCategory'


@ns.route('/res_partner_industry/', methods=['POST'], doc=False)
class ResPartnerCategory(OdooCommon):
    _repo_name = 'ResPartnerCategory'


@ns.route('/res_partner_industry/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class ResPartnerCategorySingle(OdooCommon):
    _repo_name = 'ResPartnerCategory'


@ns.route('/sale_orders/', methods=['POST'], doc=False)
class SaleOrder(OdooCommon):
    _repo_name = 'SaleOrder'


@ns.route('/sale_orders/<int:id>/', methods=['PUT'], doc=False)
class SaleOrderSingle(OdooCommon):
    _repo_name = 'SaleOrder'


@ns.route('/stock_inventory_threshold/', methods=['POST'], doc=False)
class StockInventoryThreshold(OdooCommon):
    _repo_name = 'StockInventoryThreshold'


@ns.route('/stock_inventory_threshold/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class StockInventoryThresholdSingle(OdooCommon):
    _repo_name = 'StockInventoryThreshold'


@ns.route('/stock_transfers/', methods=['POST'], doc=False)
class StockTransfer(OdooCommon):
    _repo_name = 'StockTransfer'


@ns.route('/supplier/', methods=['POST'], doc=False)
class Supplier(OdooCommon):
    _repo_name = 'Supplier'


@ns.route('/supplier/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class SupplierSingle(OdooCommon):
    _repo_name = 'Supplier'


@ns.route('/teko_product_biz_type/', methods=['POST'], doc=False)
class TekoProductBizType(OdooCommon):
    _repo_name = 'TekoProductBizType'


@ns.route('/teko_product_biz_type/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
class TekoProductBizTypeSingle(OdooCommon):
    _repo_name = 'TekoProductBizType'


# Not found in list api (https://test.api-wms.phongvu.vn/)
# @ns.route('/tekoProductStatus/', methods=['POST'], doc=False)
# class TekoProductStatus(OdooCommon):
#     _repo_name = 'TekoProductStatus'

# # new api
# @ns.route('/teko_biz_type_location_detail/', methods=['GET'], doc=False)
# class TekoBizTypeLocationDetail(OdooCommon):
#     def get(self, id=None):
#         return '???'


# # APIs bellow are connect direct to Odoo dbs !!
#
# # router.register(r'mq_incomings', VerifyReceiptViewSet, 'verify_receipt')
# @ns.route('/mq_incomings/', methods=['POST'], doc=False)
# class VerifyReceipt(OdooCommon):
#     _repo_name = 'VerifyReceipt'
#
#
# @ns.route('/mq_incomings/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
# class VerifyReceiptSingle(OdooCommon):
#     _repo_name = 'VerifyReceipt'
#
#
# @ns.route('/wms_sale_order_status/', methods=['POST'], doc=False)
# class WmsSaleOrderStatus(OdooCommon):
#     _repo_name = 'WmsSaleOrderStatus'
#
#
# @ns.route('/wms_sale_order_status/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
# class WmsSaleOrderStatusSingle(OdooCommon):
#     _repo_name = 'WmsSaleOrderStatus'
#
#
# @ns.route('/stock_transfer_status/', methods=['POST'], doc=False)
# class StockTransferStatus(OdooCommon):
#     _repo_name = 'StockTransferStatus'
#
#
# @ns.route('/stock_transfer_status/<int:id>/', methods=['PUT', 'DELETE'], doc=False)
# class StockTransferStatusSingle(OdooCommon):
#     _repo_name = 'StockTransferStatus'
