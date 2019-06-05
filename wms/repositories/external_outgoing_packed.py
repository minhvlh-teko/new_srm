from .odoo_repo import OdooRepo


class ExternalOutgoingPacked(OdooRepo):
    _name = 'ex_out_packed'
    _model = 'stock.picking'
    _mapping = {
        'create': 'api_external_outgoing_packed',
    }
    _is_formalization = True
    _faker_data = {
        'req': {
            '_id': True,
            'items': True
        },
        'res': {'code': '200', 'message': 'OK'}
    }
