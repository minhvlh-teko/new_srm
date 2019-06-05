import time

from .odoo_repo import OdooRepo


LO_BL_DELIVERED_MAPPING = {
    'id': 'BL/orderId',
    'requestType': 'BL/requestType',
}


class LoBlDelivered(OdooRepo):
    _name = 'lo_bl_delivered'
    _model = 'sale.order'
    _mapping = {
        'create': 'api_cancel_ort_by_lo_delivered',
    }

    def _parse_payload(self, request):
        super()._parse_payload(request)
        self._payload = self._parse_by_template(self._payload, LO_BL_DELIVERED_MAPPING)
