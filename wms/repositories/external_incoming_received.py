from .odoo_repo import OdooRepo


class ExternalIncomingReceived(OdooRepo):
    _name = 'ex_in_received'
    _model = 'stock.picking'
    _mapping = {
        'create': 'api_external_incoming_received',
    }
    _is_formalization = True
    _faker_data = {
        'req': {
            '_id': True,
            'items': True,
        },
        'res': {'code': 0, 'message': 'OK'}
    }
