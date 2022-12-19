# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.tools import groupby
from re import search
from functools import partial

import pytz

from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    note = fields.Char('Internal Note added by the waiter.')
    uuid = fields.Char(string='Uuid', readonly=True, copy=False)
    mp_skip = fields.Boolean('Skip line when sending ticket to kitchen printers.')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    table_id = fields.Many2one('restaurant.table', string='Table', help='The table where this order was served', index='btree_not_null', readonly=True)
    customer_count = fields.Integer(string='Guests', help='The amount of customers that have been served by this order.', readonly=True)
    multiprint_resume = fields.Char(string='Multiprint Resume', help="Last printed state of the order")

    def _get_fields_for_order_line(self):
        fields = super(PosOrder, self)._get_fields_for_order_line()
        fields.extend([
            'note',
            'uuid',
            'mp_skip',
        ])
        return fields

    def _get_fields_for_draft_order(self):
        fields = super()._get_fields_for_draft_order()
        fields.extend([
            'table_id',
            'customer_count',
            'multiprint_resume'
        ])
        return fields

    @api.model
    def get_table_draft_orders(self, table_ids):
        """Generate an object of all draft orders for the given table.

        Generate and return an JSON object with all draft orders for the given table, to send to the
        front end application.

        :param table_id: Id of the selected table.
        :type table_id: int.
        :returns: list -- list of dict representing the table orders
        """
        table_orders = self.search_read(
                domain=[('state', '=', 'draft'), ('table_id', 'in', table_ids)],
                fields=self._get_fields_for_draft_order())

        self._get_order_lines(table_orders)
        self._get_payment_lines(table_orders)

        timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
        for order in table_orders:
            order['pos_session_id'] = order['session_id'][0]
            order['uid'] = search(r"\d{5,}-\d{3,}-\d{4,}", order['pos_reference']).group(0)
            order['name'] = order['pos_reference']
            order['creation_date'] = order['create_date'].astimezone(timezone)
            order['server_id'] = order['id']
            if order['fiscal_position_id']:
                order['fiscal_position_id'] = order['fiscal_position_id'][0]
            if order['pricelist_id']:
                order['pricelist_id'] = order['pricelist_id'][0]
            if order['partner_id']:
                order['partner_id'] = order['partner_id'][0]
            if order['table_id']:
                order['table_id'] = order['table_id'][0]

            if not 'lines' in order:
                order['lines'] = []
            if not 'statement_ids' in order:
                order['statement_ids'] = []

            del order['id']
            del order['session_id']
            del order['pos_reference']
            del order['create_date']

        return table_orders

    def set_tip(self, tip_line_vals):
        """Set tip to `self` based on values in `tip_line_vals`."""

        self.ensure_one()
        PosOrderLine = self.env['pos.order.line']
        process_line = partial(PosOrderLine._order_line_fields, session_id=self.session_id.id)

        # 1. add/modify tip orderline
        processed_tip_line_vals = process_line([0, 0, tip_line_vals])[2]
        processed_tip_line_vals.update({ "order_id": self.id })
        tip_line = self.lines.filtered(lambda line: line.product_id == self.session_id.config_id.tip_product_id)
        if not tip_line:
            tip_line = PosOrderLine.create(processed_tip_line_vals)
        else:
            tip_line.write(processed_tip_line_vals)

        # 2. modify payment
        payment_line = self.payment_ids.filtered(lambda line: not line.is_change)[0]
        # TODO it would be better to throw error if there are multiple payment lines
        # then ask the user to select which payment to update, no?
        payment_line._update_payment_line_for_tip(tip_line.price_subtotal_incl)

        # 3. flag order as tipped and update order fields
        self.write({
            "is_tipped": True,
            "tip_amount": tip_line.price_subtotal_incl,
            "amount_total": self.amount_total + tip_line.price_subtotal_incl,
            "amount_paid": self.amount_paid + tip_line.price_subtotal_incl,
        })

    def set_no_tip(self):
        """Override this method to introduce action when setting no tip."""
        self.ensure_one()
        self.write({
            "is_tipped": True,
            "tip_amount": 0,
        })

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['table_id'] = ui_order.get('table_id', False)
        order_fields['customer_count'] = ui_order.get('customer_count', 0)
        order_fields['multiprint_resume'] = ui_order.get('multiprint_resume', False)
        return order_fields

    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result['table_id'] = order.table_id.id
        return result
