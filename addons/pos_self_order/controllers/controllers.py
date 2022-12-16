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
        # and pass it to the template
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
    # def pos_self_order_send_order(self,cart):
    def pos_self_order_send_order(self):
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        print('vlad')
        # pos_details = http.request.env['pos.order'].sudo().search([('id', '=', 7)])
        order = {
            'name': 'resto1/0001-test-vlad',
            'user_id': 2,
            'amount_tax': 2,
            'amount_total': 10,
            'amount_paid': 10,
            'amount_return': 0,
            'lines': [
                (0, 0, {
                    'product_id': 1,
                    'qty': 1,
                    'price_unit': 10,
                    'discount': 0,
                    'price_subtotal': 10,
                    'price_subtotal_incl': 10,
                })
            ],
            'company_id': 1,
            'partner_id': 1,

            'session_id': 8,
            'config_id': 2,
            'currency_id': 2,
            'state': 'paid',

        }

        # old_orders = request.env['pos.order'].sudo().search([]).read(['name'])
        old_orders = request.env['pos.order'].sudo().search([])
        import pdb; pdb.set_trace()
        request.env['pos.order'].sudo().create([order])

        return True

    # name = fields.Char(string='Order Ref', required=True, readonly=True, copy=False, default='/')
    # date_order = fields.Datetime(string='Date', readonly=True, index=True, default=fields.Datetime.now)
    # user_id = fields.Many2one(
    #     comodel_name='res.users', string='Responsible',
    #     help="Person who uses the cash register. It can be a reliever, a student or an interim employee.",
    #     default=lambda self: self.env.uid,
    #     states={'done': [('readonly', True)], 'invoiced': [('readonly', True)]},
    # )
    # amount_tax = fields.Float(string='Taxes', digits=0, readonly=True, required=True)
    # amount_total = fields.Float(string='Total', digits=0, readonly=True, required=True)
    # amount_paid = fields.Float(string='Paid', states={'draft': [('readonly', False)]},
    #     readonly=True, digits=0, required=True)
    # amount_return = fields.Float(string='Returned', digits=0, required=True, readonly=True)
    # margin = fields.Monetary(string="Margin", compute='_compute_margin')
    # margin_percent = fields.Float(string="Margin (%)", compute='_compute_margin', digits=(12, 4))
    # is_total_cost_computed = fields.Boolean(compute='_compute_is_total_cost_computed',
    #     help="Allows to know if all the total cost of the order lines have already been computed")
    # lines = fields.One2many('pos.order.line', 'order_id', string='Order Lines', states={'draft': [('readonly', False)]}, readonly=True, copy=True)
    # company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True)
    # pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, states={
    #                                'draft': [('readonly', False)]}, readonly=True)
    # partner_id = fields.Many2one('res.partner', string='Customer', change_default=True, index='btree_not_null', states={'draft': [('readonly', False)], 'paid': [('readonly', False)]})
    # sequence_number = fields.Integer(string='Sequence Number', help='A session-unique sequence number for the order', default=1)

    # session_id = fields.Many2one(
    #     'pos.session', string='Session', required=True, index=True,
    #     domain="[('state', '=', 'opened')]", states={'draft': [('readonly', False)]},
    #     readonly=True)
    # config_id = fields.Many2one('pos.config', related='session_id.config_id', string="Point of Sale", readonly=False)
    # currency_id = fields.Many2one('res.currency', related='config_id.currency_id', string="Currency")
    # currency_rate = fields.Float("Currency Rate", compute='_compute_currency_rate', compute_sudo=True, store=True, digits=0, readonly=True,
    #     help='The rate of the currency to the currency of rate applicable at the date of the order')

    # state = fields.Selection(
    #     [('draft', 'New'), ('cancel', 'Cancelled'), ('paid', 'Paid'), ('done', 'Posted'), ('invoiced', 'Invoiced')],
    #     'Status', readonly=True, copy=False, default='draft')

    # account_move = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False, index="btree_not_null")
    # picking_ids = fields.One2many('stock.picking', 'pos_order_id')
    # picking_count = fields.Integer(compute='_compute_picking_count')
    # failed_pickings = fields.Boolean(compute='_compute_picking_count')
    # picking_type_id = fields.Many2one('stock.picking.type', related='session_id.config_id.picking_type_id', string="Operation Type", readonly=False)
    # procurement_group_id = fields.Many2one('procurement.group', 'Procurement Group', copy=False)

    # note = fields.Text(string='Internal Notes')
    # nb_print = fields.Integer(string='Number of Print', readonly=True, copy=False, default=0)
    # pos_reference = fields.Char(string='Receipt Number', readonly=True, copy=False)
    # sale_journal = fields.Many2one('account.journal', related='session_id.config_id.journal_id', string='Sales Journal', store=True, readonly=True, ondelete='restrict')
    # fiscal_position_id = fields.Many2one(
    #     comodel_name='account.fiscal.position', string='Fiscal Position',
    #     readonly=True,
    #     states={'draft': [('readonly', False)]},
    # )
    # payment_ids = fields.One2many('pos.payment', 'pos_order_id', string='Payments', readonly=True)
    # session_move_id = fields.Many2one('account.move', string='Session Journal Entry', related='session_id.move_id', readonly=True, copy=False)
    # to_invoice = fields.Boolean('To invoice', copy=False)
    # to_ship = fields.Boolean('To ship')
    # is_invoiced = fields.Boolean('Is Invoiced', compute='_compute_is_invoiced')
    # is_tipped = fields.Boolean('Is this already tipped?', readonly=True)
    # tip_amount = fields.Float(string='Tip Amount', digits=0, readonly=True)
    # refund_orders_count = fields.Integer('Number of Refund Orders', compute='_compute_refund_related_fields')
    # is_refunded = fields.Boolean(compute='_compute_refund_related_fields')
    # refunded_order_ids = fields.Many2many('pos.order', compute='_compute_refund_related_fields')
    # has_refundable_lines = fields.Boolean('Has Refundable Lines', compute='_compute_has_refundable_lines')
    # refunded_orders_count = fields.Integer(compute='_compute_refund_related_fields')