import time

from .odoo_repo import OdooRepo


LO_BL_RETURN_MAPPING = {
    'id': 'BL/orderId',
    'cancelledAt': 'transport/endTime',
    'requestType': 'BL/requestType',
}


class LoBlReturning(OdooRepo):
    _name = 'lo_bl_returning'
    _model = 'sale.order'
    _mapping = {
        'create': 'api_cancel_from_om_message',
    }

    def _parse_payload(self, request):
        super()._parse_payload(request)
        self._payload = self._parse_by_template(self._payload, LO_BL_RETURN_MAPPING)

        if not self._payload['cancelledAt']:
            self._payload['cancelledAt'] = time.time()

        self._payload.update(
            {
                "action": "full",
                "reason": "LO 3rd party - Hủy toàn bộ",
            })
