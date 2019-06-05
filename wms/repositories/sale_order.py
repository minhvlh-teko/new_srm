import logging

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')

OM_SALE_ORDER_MAPPING = {
    # customer
    'customer_id': "customer/asiaCrmId",  # "customer/id",
    'customer_name': "customer/name",
    'customer_phone': "customer/phone",
    'customer_address': "customer/address",
    'customer_email': "customer/email",

    # billing
    'customer_billing_phone': "addresses/billing/telephone",
    'customer_billing_address': "addresses/billing/address",
    'customer_billing_name': "addresses/billing/name",
    'customer_billing_email': "addresses/billing/email",
    'customer_billing_tax': "addresses/billing/taxCode",
    'customer_billing_type': "addresses/billing/billingType",  # string
    'customer_billing_print_after': "addresses/billing/printAfter",  # int : xuat hoa don sau N ngay
    'customer_billing_print_pretax_price': "addresses/billing/printPretaxPrice",  # boolean : in giá trước thuế

    # shipping
    'customer_shipping_phone': "addresses/shipping/telephone",
    'customer_shipping_street': "addresses/shipping/street",
    'customer_shipping_name': "addresses/shipping/name",
    'customer_shipping_address_code': "addresses/shipping/addressCode",
    'customer_shipping_email': "addresses/shipping/email",

    # warehouse and branch
    'inventory_code': "inventoryCode",  # "CP01"
    'store_code': "storeId",  # "1234"
    'store_name': "storeName",  # "PHONGVU"
    'salesman_id': "salesmanId",  # "1234"
    'source_channel': "channel",  # "ONLINE" => int 1 (OM Change)
    # order
    'client_order_ref': "code",  # "43809SX"
    'tk_om_order_id': "id",  # "43809SX"
    'note': "note",
    'ship_date': "shipDate",  # 1526973085
    'date_order': "createdAt",  # 1526973085  thời điểm xác nhận đơn (UNIX timestamp)

    # amount
    # @formatter:off
    'tk_discount_amount': "totalDiscount",  # int	Giảm giá đơn hàng
    'tk_grand_total': "grandTotal",         # int = ∑items.rowTotal=paidAmount+COD+otherAmount+totalDiscount
    'tk_paid_amount': "paidAmount",         # int = ∑payments.amount (trong đó: các payments.amount của các phương thức có method từ 1->5)
    'tk_cod_amount': "COD",                 # int = payments.amount của phương thức có method =6
    'tk_other_amount': "otherAmount",       # int = ∑payments.amount (trong đó, các payments.amount của các phương thức có method từ 7->10)
    'tk_residual': "residual",              # float Số dư
    # @formatter:on

    # product
    'items': "items",

    # # payment
    'payments': "payments",

    # addition fields
    'tk_install': "install",  # boolean	Lắp đặt tại phòng máy (từ app agent chuyển sang)
    'tk_delivery': "delivery",  # boolean	Giao hàng tận nơi
    'tk_technical_support': "technicalSupport",  # boolean	Hỗ trợ kỹ thuật

    'payment_duration': 'paymentDuration',
    'price_table': 'priceTable',
    'tk_deposit': 'deposit',  # boolean Đơn hàng có đặt cọc, ghi nhận từ OM
    'tk_installment': 'installment',  # boolean Đơn hàng trả góp, ghi nhận từ OM

    # !!! NOTE: we don't want this field passed into _parse_by_template()
    # therefore we disabled this here, and will map after _parse_by_template() called
    # 'tk_confirmer': 'confirmer',

    'should_ignore': 'isDifferentStorage',
}

OM_SALE_ORDER_LINE_MAPPING = {
    'default_code': "sku",  # "1603607"
    'product_uom_qty': "quantity",  # 2,
    'tk_discount_amount': "discountAmount",  # 1000
    'tk_discount_note': "discountReason",
    'tk_init_price_unit': "unitPrice",  # 12790000
    'price_unit': "price",  # 22790000
    'price_unit_untaxed': "unitPriceUntax",  # ten field OM sida, ke no di nha !!
    'tax_amount': "vat",  # 10,
    'tk_row_total': "rowTotal",  # 12790000
    'tk_row_total_untaxed': "priceUntax",  # ten field OM sida, ke no di nha !!
    'product_biz_type': 'productType',
}

OM_SALE_ORDER_PAYMENT_MAPPING = {
    'ops_id': "opsId",  # "1234" # string id của người xử lý đơn.
    'payment_id': "paymentId",  # 55345
    'payment_method': "paymentMethod",  # 1
    'bank_account': "bankAccount",  # "1122222000"
    'amount': "amount",  # 25580000
    'ref': "ref",  # "2034424"
    'time_transfer': "timeTransfer",  # 1526886679
    'debtor_id': "debtorId",  # string	ID của người nhận nợ (nếu payment_method = 7,9)
    'asia_username': "asiaUsername",
    'auto_code': "autoCode",
}

OM_SALE_ORDER_CANCEL_MAPPING = {
    # order
    'client_order_ref': "code",  # "43809SX"
}


class SaleOrder(OdooRepo):
    _name = 'sale_orders'
    _model = 'sale.order'
    _mapping = {
        'create': 'api_create_from_om_message',
        'update': 'api_cancel_from_om_message'
    }

    def _get_lines(self):
        return [self._parse_by_template(item, OM_SALE_ORDER_LINE_MAPPING) for item in self._payload['items']]

    def _get_payments(self):
        _payments = self._payload.get('payments') or []
        return [self._parse_by_template(item, OM_SALE_ORDER_PAYMENT_MAPPING) for item in _payments]

    def _convert_lines(self):
        for item in self._payload.get('items'):
            item['price_unit'] = float(item.get('price_unit'))
            item['tk_init_price_unit'] = float(item.get('tk_init_price_unit'))
            item['price_unit_untaxed'] = float(item.get('price_unit_untaxed'))
            item['tk_row_total_untaxed'] = float(item.get('tk_row_total_untaxed'))
            item['tk_row_total'] = float(item.get('tk_row_total'))

    def _convert_payments(self):
        for payment in self._payload.get('payments'):
            if payment.get('amount'):
                payment['amount'] = str(payment.get('amount'))

    def _parse_payload(self, request):
        super()._parse_payload(request)

        if self._api_method == 'create':
            # !!!
            confirmer = self._payload.get('confirmer')

            self._payload = self._parse_by_template(self._payload, OM_SALE_ORDER_MAPPING)
            self._payload['items'] = self._get_lines()
            self._payload['payments'] = self._get_payments()
            self._payload['tk_src'] = 1

            # !!!
            self._payload['tk_confirmer'] = confirmer

            ## !!! IMPORTANT: convert below fields to string because fields may have big value
            ## grandTotal, otherAmount, otherAmount, paidAmount, residual, payments.amount
            ## items[price, unitPrice, unitPriceUntax, priceUntax, rowTotal]

            self._convert_lines()
            self._convert_payments()
            self._payload['tk_grand_total'] = str(self._payload.get('tk_grand_total'))
            self._payload['tk_other_amount'] = str(self._payload.get('tk_other_amount'))
            self._payload['tk_paid_amount'] = float(self._payload.get('tk_paid_amount'))
            self._payload['tk_residual'] = float(self._payload.get('tk_residual'))
