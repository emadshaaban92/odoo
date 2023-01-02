# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import format_amount
from odoo.addons.account.controllers.portal import PortalAccount
from odoo import fields

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
        domain = [
            ('state', 'in', ['opening_control', 'opened']),
            ('user_id', '=', request.session.uid),
            ('rescue', '=', False),
            ('config_id', '=', int(pos_id)),
        ]
        pos_session = request.env['pos.session'].sudo().search(domain).read(['id','name', 'login_number'])[0]
        context = {
            'pos_id': pos_id,
            'table_number': table_number,
            'pos_name' : pos_details_sudo.get('name'),
            'currency' : pos_details_sudo.get('currency_id')[1],
            # 'login_number': pos_session['login_number'],
            # 'pos_session_id': pos_session['id'],
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
    

    # this is the route that the POS Self Order App uses to SEND THE ORDER
    @http.route('/pos-self-order/send-order/<int:pos_id>/<int:table_number>/', auth='public', type="json", website=True)
    def pos_self_order_send_order(self, cart, pos_id, table_number):
        # TODO: we need to check if the order is valid -- the values of cart have to be integers, for ex
        print("items in cart ",cart)
        # We create the lines of the order from the cart variable
        lines = []
        for item in cart:
            # from the frontend we only get the id of the product and the quantity
            # we need to get the other details of the product from the database
            # this is done for security reasons
            product_info_sudo =  request.env['product.product'].sudo().search([('available_in_pos', '=', True), ('id', '=', item.get("id"))]).read(['list_price', 'name'])[0]
            # We want to check if the session_id of the last order is the same as the current session_id
            # If it is the same, we will look at what the last order_id was and add 1 to it
            # If it is not the same, we will start from 1
            sequence_number =  request.env['pos.order'].sudo().search([('config_id', '=', int(pos_id))]).read(["sequence_number"])[0].get("sequence_number") + 1
            # last_order =  request.env['pos.order'].sudo().search([('config_id', '=', int(pos_id))]).read(['session_id', ])[0]
            # import pdb; pdb.set_trace()
            # TODO: I don't know yet how to code should actually work:
            #  ex: if the last code is 00007-001-0002 and the next order done on this POS session is 
            # done by a different user, the code should be 00007-002-0001 or 00007-002-0003?
            print(item.get("quantity"))
            lines.append([0, 0, {
                'product_id': item.get('id'),
                'quantity': item.get('quantity'),
                'price_unit': product_info_sudo.get("list_price"),
                'price_subtotal': product_info_sudo.get("list_price") * item.get('quantity'),
                'price_subtotal_incl': product_info_sudo.get("list_price") * item.get('quantity'),
                # TODO: figure out how to get the discount
                'discount': 0,
                # TODO: figure out how to get the taxes
                'tax_ids': [[6, False, []]],
                'id': 1,
                'pack_lot_ids': [],
                'description': '',
                'full_product_name': product_info_sudo.get("name"),
                'price_extra': 0,
                'customer_note': '',
                'price_manually_set': False,
                'note': '',
            }])

        # We get the POS Session details from the database 
        domain = [
            ('state', 'in', ['opening_control', 'opened']),
            ('user_id', '=', request.session.uid),
            ('rescue', '=', False),
            ('config_id', '=', int(pos_id)),
        ]
        pos_session = request.env['pos.session'].sudo().search(domain).read(['id','name', 'login_number'])[0]
        total_amount = sum(orderline[2].get("price_subtotal") for orderline in lines)
        order_id = self.generate_unique_id(pos_session["id"], pos_session["login_number"], sequence_number)
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print("date")
        print(str(fields.Datetime.now()).replace(" ", "T"))
        order = {'id': order_id,
                 'data': 
                    {
                        'name': f"Order {order_id}", 
                        'amount_paid': 0, 
                        'amount_total': total_amount, 
                        'amount_tax': 0, 
                        'amount_return': 0, 
                        'lines': lines, 
                        'statement_ids': [[0, 0, {'name': '2023-01-02 08:20:07', 'payment_method_id': 1, 'amount': total_amount, 'payment_status': '', 'ticket': '', 'card_type': '', 'cardholder_name': '', 'transaction_id': ''}]], 
                        'pos_session_id': pos_session.get("id"), 
                        'pricelist_id': 1, 
                        'partner_id': False, 
                        'user_id': request.session.uid, 
                        'uid': order_id, 
                        'sequence_number': sequence_number, 
                        'creation_date': str(fields.Datetime.now()).replace(" ", "T"), 
                        # 'creation_date': fields.Datetime.now(), 
                        'fiscal_position_id': False, 
                        # 'server_id': False, 
                        'to_invoice': False, 
                        'to_ship': False, 
                        'is_tipped': False, 
                        'tip_amount': 0, 
                        'access_token': '756581b3-bd49-4cf6-8037-011336780d03', 
                        'customer_count': 1
                    }, 
                    'to_invoice': False,
                    'session_id': pos_session.get("id")}
        resp = request.env['pos.order'].sudo().create_from_ui([order])
        print(resp) 
        return True
    # this function resembles the one with the same name in the models.js file
    def generate_unique_id(self, id, login_number, sequence_number):
        # // Generates a public identification number for the order.
        # // The generated number must be unique and sequential. They are made 12 digit long
        # // to fit into EAN-13 barcodes, should it be needed
        # here we use a trick with f-strings
        # ex: f"{id:0>5}" will return a string with 5 digits
        # if the id is 1, the result will be 00001
        return f"{id:0>5}-{login_number:0>3}-{sequence_number:0>4}"