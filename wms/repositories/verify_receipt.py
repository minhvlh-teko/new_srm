import logging

# from django.db import connections
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response

from .odoo_repo import OdooRepo


_logger = logging.getLogger('api')


class VerifyReceipt(OdooRepo):
    _name = 'verify_receipt'

    # Mapping list from model IncomingMessage
    STATUS_LIST = {
        0: 'Received',
        1: 'Success',
        -1: 'Waiting Retry',
        -2: 'Failed',
        -3: 'Invalid',
        -4: 'Wait Prev Msg',
        10: 'Working',
        -11: 'Canceled'
    }

""" Refactor later
    def _map_status(self, status_code):
        return self.STATUS_LIST[status_code]


    def _parse_payload(self, request):
        super()._parse_payload(request)

        if self._api_method == 'list':
            routing_key = request.query_params.get('routing_key')
            if not routing_key:
                raise ValidationError('Param `routing_key` is required')

            msg_ids = request.query_params.get('msg_ids')
            if not msg_ids:
                raise ValidationError('Param `msg_ids` is required')

            msg_ids = msg_ids.split(',')

            self._payload['routing_key'] = routing_key
            self._payload['msg_ids'] = msg_ids

    def _call_api(self):
        routing_key = self._payload['routing_key']
        cursor = connections['mq'].cursor()

        cursor.execute("SELECT id "
                       "FROM in_routing_keys "
                       "WHERE routing_key = %s;", (routing_key,))

        # No routing key found, return all None
        if cursor.rowcount == 0:
            return self._get_null_response()

        data = {}
        routing_key_id = cursor.fetchone()[0]
        msg_ids = self._payload['msg_ids']

        # Check if msg_id is not a int
        for record in msg_ids:
            if not record.isdigit():
                data[record] = None
                msg_ids.remove(record)

        if len(msg_ids) == 0:
            return self._get_null_response()

        msg_id_list = "'" + "','".join([str(x) for x in msg_ids]) + "'"

        cursor.execute("SELECT src_id, status "
                       "FROM in_messages "
                       "WHERE in_routing_key_id = '%s' AND src_id IN (%s);" % (routing_key_id, msg_id_list))

        for record in cursor.fetchall():
            data[record[0]] = '%s|%s' % (record[1], self._map_status(record[1]))

        for record in msg_ids:
            if int(record) not in data:
                data[int(record)] = None

        return {
            'code': 0,
            'message': 'OK',
            'data': data
        }

    def _get_null_response(self):
        data = {}
        msg_ids = self._payload['msg_ids']

        for record in msg_ids:
            data[record] = None

        return {
            'code': 0,
            'message': 'OK',
            'data': data
        }

    def _handle(self, request, *args, **kwargs):
        try:
            self._parse_payload(request)
            response = self._call_api()

            return Response(response)

        except Exception as e:
            _logger.exception('[%s@%s] FAILED' % (self._name, self._api_method))
            return Response(repr(e), status=500)"""