import logging

# from django.db import connections
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class StockTransferStatus(OdooRepo):
    _name = 'stock_transfer_status'

    """def _parse_payload(self, request):
        super()._parse_payload(request)

        if self._api_method == 'list':
            request_codes = request.query_params.get('requestCodes')
            if not request_codes:
                raise ValidationError('Param `requestCodes` is required')

            self._payload['request_codes'] = request_codes.split(',')

    def _call_api(self):
        request_codes = self._payload['request_codes']

        cursor = connections['wms'].cursor()
        cursor.execute("SELECT name, state, write_date, id FROM stock_transfer WHERE name IN %s;",
                       [tuple(request_codes)])

        data = {record[0]: {
            'id': record[3],
            'status': record[1],
            'last_update_date': record[2].__str__(),
        } for record in cursor}

        return {
            'code': 0,
            'message': 'OK',
            'data': data,
        }

    def _handle(self, request, *args, **kwargs):
        try:
            self._parse_payload(request)

            response = self._call_api()

            return Response(response)

        except Exception as e:
            _logger.exception('[%s@%s] FAILED' % (self._name, self._api_method))
            return Response(repr(e), status=500)
            """
