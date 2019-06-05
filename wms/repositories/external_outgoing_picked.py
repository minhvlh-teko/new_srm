from .odoo_repo import OdooRepo


class ExternalOutgoingPicked(OdooRepo):
    _name = 'ex_out_picked'
    _model = 'stock.picking'
    _mapping = {
        'create': 'api_external_outgoing_picked',
    }
    _is_formalization = True
    _faker_data = {
        'req': {
            '_id': True,
            'items': True
        },
        'res': {'code': '200', 'message': 'OK'}
    }
