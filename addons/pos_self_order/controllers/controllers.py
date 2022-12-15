# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import format_amount
from odoo.addons.account.controllers.portal import PortalAccount


class PosSelfOrder(http.Controller):
    # this is the main controller for the POS Self Order App
    # The user gets this route from the QR code that they scan at the table
    @http.route('/pos-self-order/start/<int:pos_id>/<int:table_number>/', auth='public', website=True)
    def pos_self_order_start(self, table_number, pos_id):
        # We know the id of the POS from the QR code
        # We get some details about this POS from the model "pos.config"
        # We need:
        # 1. The name of the POS - to display it on the POS Self Order App - this name is the name that the user gave to the POS when they created it
        # 2. The currency of the POS - to display the prices in the correct currency
        pos_details = http.request.env['pos.config'].sudo().search_read([('id', '=', pos_id)], ['name', 'currency_id'])[0]
        context = {
            'pos_id': pos_id,
            'table_number': table_number,
            'pos_name' : pos_details.get('name'),
            'currency' : pos_details.get('currency_id')[1],
        }
        # and pass it to the template
        # pos_details = http.request.env['pos.config'].sudo().search_read([('id', '=', pos_id)], ['name', 'company_id'])[0]
        response = request.render('pos_self_order.pos_self_order_index', context)
        # response.headers['Cache-Control'] = 'no-store'
        return response
    # this is the route that the POS Self Order App uses to GET THE MENU
    @http.route('/pos-self-order/get-menu', auth='public',type="json", website=True)
    def pos_self_order_get_menu(self,config_id = False):
        # response.headers['Cache-Control'] = 'no-store'
        # Let me break this down:
        # 0. We request the product.product model
        # 1. We are using the sudo() method to bypass the access rights
        # 2. We are using the search() method to get the products that are available in the POS
        # 3. We are using the read() method to get the name and price of the product
        # 4. We are using the type="json" argument in the function call to return the response as JSON
        response = http.request.env['product.product'].sudo().search([('available_in_pos', '=', True)]).read(['id', 'name', 'list_price', 'description_sale'])
        return response
    @http.route('/pos-self-order/get-comp/<int:pos_id>', auth='public', type="json", website=True)
    def pos_self_order_get_comp(self,pos_id):
        # pos_details = http.request.env['pos.config'].sudo().browse(pos_id).read([])[0]
        pos_details = http.request.env['pos.config'].sudo().search_read([('id', '=', pos_id)], [])[0]
        # company_name = http.request.env['res.company'].sudo().search_read([('id' '=', pos_details.get('company_id')[0])], ['name'])[0]
        # import pdb; pdb.set_trace()

        return pos_details
    # this is the route that the POS Self Order App uses to GET THE PRODUCT IMAGES
    @http.route('/pos-self-order/get-images/<int:product_id>', methods=['GET'], type='http', auth='public')
    def pos_self_order_get_images(self, product_id, **kwargs):
        # We get the product with the specific id from the database
        product = request.env['product.product'].sudo().browse(product_id)
        # We return the image of the product in binary format
        # 'image_1920' is the name of the field that contains the image
        # If the product does not have an image, the function _get_image_stream_from will return the default image
        return request.env['ir.binary']._get_image_stream_from(product, field_name='image_1920').get_response()