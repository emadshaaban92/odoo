# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import format_amount
from odoo.addons.account.controllers.portal import PortalAccount


class PosSelfOrder(http.Controller):
    """
    # this is the controller for the POS Self Order App
    # The user gets this route from the QR code that they scan at the table
    # This START ROUTE will render the LANDIN PAGE of the POS Self Order App
    # And it will pass some generic variabiles to the template: pos_id, table_number, pos_name, currency
    """
    @http.route('/pos-self-order/start/<int:pos_id>/<int:table_number>/', auth='public', website=True)
    def pos_self_order_start(self, table_number, pos_id):
        """
        # We know the id of the POS from the QR code
        # We get some details about this POS from the model "pos.config"
        # We need:
        # 1. The name of the POS - to display it on the POS Self Order App - this name is the name that the user gave to the POS when they created it
        # 2. The currency of the POS - to display the prices in the correct currency
        """
        pos_details_sudo = http.request.env['pos.config'].sudo().search_read([('id', '=', pos_id)], ['name', 'currency_id'])[0]
        context = {
            'pos_id': pos_id,
            'table_number': table_number,
            'pos_name' : pos_details_sudo.get('name'),
            'currency' : pos_details_sudo.get('currency_id')[1],
        }
        # We pass the context to the template
        response = request.render('pos_self_order.pos_self_order_index', context)
        # response.headers['Cache-Control'] = 'no-store'
        return response
    # this is the route that the POS Self Order App uses to GET THE MENU
    @http.route('/pos-self-order/get-menu', auth='public',type="json", website=True)
    def pos_self_order_get_menu(self,config_id = False):
        response_sudo = http.request.env['product.product'].sudo().search([('available_in_pos', '=', True)]).read(['id', 'name', 'list_price', 'description_sale'])
        return response_sudo
    # this is the route that the POS Self Order App uses to GET THE PRODUCT IMAGES
    @http.route('/pos-self-order/get-images/<int:product_id>', methods=['GET'], type='http', auth='public')
    def pos_self_order_get_images(self, product_id):
        # We get the product with the specific id from the database
        product_sudo = request.env['product.product'].sudo().browse(product_id)
        # We return the image of the product in binary format
        # 'image_1920' is the name of the field that contains the image
        # If the product does not have an image, the function _get_image_stream_from will return the default image
        return request.env['ir.binary']._get_image_stream_from(product_sudo, field_name='image_1920').get_response()
    @http.route('/pos-self-order/send-order', auth='public', type="json", website=True)
    def pos_self_order_send_order(self, cart):
        # TODO: we need to check if the order is valid -- the values of cart have to be integers, for ex
        print(cart)
        # We create the lines of the order from the cart variable
        lines = []
        for item in cart:
            product_info_sudo =  request.env['product.product'].sudo().search([('available_in_pos', '=', True)]).read(['list_price', 'description_sale'])
            
            lines.append([0, 0, {
                'product_id': item.get('id'),
                'qty': item.get('qty'),
                'price_unit': product_info_sudo.get("list_price"),
                'price_subtotal': product_info_sudo.get("list_price") * item.get('qty'),
                'price_subtotal_incl': product_info_sudo.get("list_price") * item.get('qty'),
                # TODO: figure out how to get the discount
                'discount': 0,
                # TODO: figure out how to get the taxes
                'tax_ids': [[6, False, []]],
                'id': 1,
                'pack_lot_ids': [],
                'description': '',
                'full_product_name': product_info_sudo.get("description_sale"),
                'price_extra': 0,
                'customer_note': '',
                'price_manually_set': False,
                'note': '',
            }])

            

        order = {'id': '00010-001-0004',
                 'data': 
                    {'name': 'Order 00010-001-0004', 
                    'amount_paid': 0, 
                    'amount_total': 840, 
                    'amount_tax': 0, 
                    'amount_return': 0, 
                    'lines': lines, 
                    'statement_ids': [[0, 0, {'name': '2023-01-02 08:20:07', 'payment_method_id': 1, 'amount': 840, 'payment_status': '', 'ticket': '', 'card_type': '', 'cardholder_name': '', 'transaction_id': ''}]], 
                    'pos_session_id': 10, 
                    'pricelist_id': 1, 
                    'partner_id': False, 
                    'user_id': 2, 
                    'uid': '00010-001-0003', 
                    'sequence_number': 1, 
                    'creation_date': '2023-01-02T08:20:07.456Z', 
                    'fiscal_position_id': False, 
                    'server_id': False, 
                    'to_invoice': False, 
                    'to_ship': False, 
                    'is_tipped': False, 
                    'tip_amount': 0, 
                    'access_token': '756581b3-bd49-4cf6-8037-011336780d03', 
                    'customer_count': 1}, 
                    'to_invoice': False,
                    'session_id': 10}
        request.env['pos.order'].sudo().create_from_ui([order])
        return True