import logging

# import coreapi
# import coreschema
# from django.db import connections
# from rest_framework.exceptions import ValidationError
# from rest_framework.schemas import ManualSchema

from .odoo_repo import OdooRepo

_logger = logging.getLogger('api')
#
# manual_schema = ManualSchema(fields=[
#     coreapi.Field(
#         "products",
#         required=True,
#         location="path",
#         schema=coreschema.String(description='Product Codes, separated by comma')
#     ),
#     coreapi.Field(
#         "regions",
#         required=False,
#         location="path",
#         schema=coreschema.String(description="Regions Codes, separated by comma")
#     ),
#
#     coreapi.Field(
#         "branches",
#         required=False,
#         location="path",
#         schema=coreschema.String(description="Branch Codes, separated by comma")
#     ),
#
#     coreapi.Field(
#         "warehouses",
#         required=False,
#         location="path",
#         schema=coreschema.String(description="Warehouses Codes, separated by comma")
#     ),
#
#     coreapi.Field(
#         "locations",
#         required=False,
#         location="path",
#         schema=coreschema.String(description="Locations Codes, separated by comma")
#     ),
# ])


class StockQuantWms(OdooRepo):
    _name = 'stock_quants'
    _model = 'product.product'
    _mapping = {
        'list': 'api_get_available_stock',
    }
    """schema = manual_schema

    def _parse_payload(self, request):

        super()._parse_payload(request)

        if self._api_method == 'list':

            product_codes = request.query_params.get('products')
            _logger.info('Product codes: %s', product_codes)

            if not product_codes:
                raise ValidationError('Param `products` is required')
            product_codes = product_codes.split(',')

            region_codes = request.query_params.get('regions')
            _logger.info('Region codes: %s', region_codes)
            branch_codes = request.query_params.get('branches')
            warehouse_codes = request.query_params.get('warehouses')
            location_codes = request.query_params.get('locations')

            region_codes = region_codes.split(',') if region_codes else []
            branch_codes = branch_codes.split(',') if branch_codes else []
            warehouse_codes = warehouse_codes.split(',') if warehouse_codes else []
            location_codes = location_codes.split(',') if location_codes else []

            self._payload['product_codes'] = product_codes
            self._payload['region_codes'] = region_codes
            self._payload['branch_codes'] = branch_codes
            self._payload['warehouse_codes'] = warehouse_codes
            self._payload['location_codes'] = location_codes

            # product_codes la bat buoc
            # location_codes or region_codes or branch_codes or warehouse_codes
            # tom lai chi co 5TH xay ra

            # chi co product_codes
            # co product_codes & location_codes
            # co product_codes & warehouse_codes
            # co product_codes & branch_codes
            # co product_codes & region_codes

    def get_warehouse_id(self, location_id):
        cursor = connections['wms'].cursor()

        cursor.execute(
            "select sw.code from stock_warehouse sw INNER JOIN stock_location sl ON sw.view_location_id = sl.id where sl.parent_left <= (select parent_left from stock_location where id='" + str(
                location_id) + "') and sl.parent_right >= (select parent_left from stock_location where id='" + str(
                location_id) + "') limit 1")

        warehouse_code = ''

        for rep in cursor.fetchall():
            _logger.info('Rep in WH code.............................: %s', rep)
            warehouse_code = rep[0]

        return warehouse_code

    def _call_api(self):

        raise Exception("Not implemented yet !!!")

        cursor = connections['wms'].cursor()

        product_codes_list = "'" + "','".join([str(x) for x in self._payload['product_codes']]) + "'"
        region_codes_list = "'" + "','".join([str(x) for x in self._payload['region_codes']]) + "'"
        branch_codes_list = "'" + "','".join([str(x) for x in self._payload['branch_codes']]) + "'"
        warehouse_codes_list = "'" + "','".join([str(x) for x in self._payload['warehouse_codes']]) + "'"
        location_codes_list = "'" + "','".join([str(x) for x in self._payload['location_codes']]) + "'"

        product_ids_list = []
        cursor.execute("SELECT id FROM product_product WHERE default_code IN ('" + "','".join(
            [str(x) for x in self._payload['product_codes']]) + "')")
        for row in cursor.fetchall():
            product_ids_list.append(row[0])
        product_ids_list = "'" + "','".join([str(x) for x in product_ids_list]) + "'"

        if self._payload['location_codes']:
            location_ids = []
            cursor.execute("SELECT id FROM stock_location WHERE code IN (" + location_codes_list + ")")
            cursor.execute(
                "SELECT sw.code as sw_code,l.id as sl_id,l.code as sl_code FROM stock_location as l INNER JOIN stock_warehouse as sw ON sw.view_location_id = l.location_id WHERE l.code IN (" + location_codes_list + ")")

            location_codes_ids_list = {}

            for row in cursor.fetchall():
                location_codes_ids_list[row[1]] = row[2]
                location_ids.append(row[1])

            cursor.execute(
                "SELECT sum(reserved_quantity) as reserved_quantity, sum(quantity) as qty, product_id, location_id FROM stock_quant WHERE product_id IN (" + product_ids_list + ") AND location_id IN ('" + "','".join(
                    [str(x) for x in location_ids]) + "') GROUP BY product_id,location_id")

            res = {}
            for rep in cursor.fetchall():
                res[rep[2]] = []
                res[rep[2]].append({
                    'warehouse': self.get_warehouse_id(rep[3]),
                    'location': location_codes_ids_list[rep[3]],
                    'available': rep[1] - rep[0]
                })

            return {
                'code': 0,
                'message': 'OK',
                'data': res,
            }

        else:
            location_ids = []
            location_codes_ids_list = {}
            warehouse_ids = []
            warehouse_codes_ids_list = {}
            location_ids_warehouse_codes_lists = {}
            if self._payload['warehouse_codes']:
                cursor.execute(
                    "SELECT sw.id,sw.code as warehouse_code,sw.lot_stock_id,sl.code as location_code FROM stock_warehouse sw INNER JOIN stock_location sl ON sw.lot_stock_id = sl.id WHERE sw.code IN (" + warehouse_codes_list + ")")

            elif self._payload['branch_codes']:
                cursor.execute(
                    "select sw.id,sw.code as warehouse_code,sw.lot_stock_id,sl.code as location_code from stock_warehouse sw INNER JOIN teko_branch tb on sw.tk_branch_id = tb.id INNER JOIN stock_location sl on sw.lot_stock_id = sl.id where tb.code in (" + branch_codes_list + ")")

            elif self._payload['region_codes']:
                cursor.execute(
                    "select sw.id,sw.code as warehouse_code,sw.lot_stock_id,sl.code as location_code from stock_warehouse sw INNER JOIN stock_location sl ON sw.lot_stock_id = sl.id INNER JOIN res_partner ON sw.partner_id = res_partner.id INNER JOIN teko_province on res_partner.tk_province_id = teko_province.id INNER JOIN teko_region tr on teko_province.region_id = tr.id where tr.code in (" + region_codes_list + ")")

            # Case have only product_codes_list
            else:
                cursor.execute(
                    "SELECT sum(reserved_quantity) as reserved_quantity,sum(quantity) as qty,product_id,sq.location_id,sl.code as location_code FROM stock_quant sq INNER JOIN stock_location sl on sq.location_id = sl.id WHERE product_id IN (" + product_ids_list + ") GROUP BY sq.product_id, sq.location_id, sl.code"
                )

                res = {}
                for rep in cursor.fetchall():
                    _logger.info('REP...................................................: %s', rep[3])
                    res[rep[2]] = []
                    res[rep[2]].append({
                        'warehouse': self.get_warehouse_id(rep[3]),
                        'location': rep[4],
                        'available': rep[1] - rep[0]
                    })

                return {
                    'code': 0,
                    'message': 'OK',
                    'data': res,
                }

            # Processed in the case warehouse_codes, branch_codes, region_codes
            for row in cursor.fetchall():
                warehouse_codes_ids_list[row[0]] = row[1]
                warehouse_ids.append(row[0])
                location_ids_warehouse_codes_lists[row[2]] = row[1]
                location_codes_ids_list[row[2]] = row[3]
                location_ids.append(row[2])

            cursor.execute(
                "SELECT sum(reserved_quantity) as reserved_quantity, sum(quantity) as qty, product_id, location_id FROM stock_quant WHERE product_id IN (" + product_ids_list + ") AND location_id IN ('" + "','".join(
                    [str(x) for x in location_ids]) + "') GROUP BY product_id,location_id")

            res = {}
            for rep in cursor.fetchall():
                res[rep[2]] = []
                res[rep[2]].append({
                    'warehouse': location_ids_warehouse_codes_lists[rep[3]],
                    'location': location_codes_ids_list[rep[3]],
                    'available': rep[1] - rep[0]
                })

            return {
                'code': 0,
                'message': 'OK',
                'data': res,
            }"""