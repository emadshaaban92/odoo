# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    repair_order_ids = fields.One2many(comodel_name='repair.order', inverse_name='sale_order_id', string='Repair Order')
    repair_count = fields.Integer("Repair Order(s)", compute='_compute_repair_order_ids')

    @api.depends('repair_order_ids')
    def _compute_repair_order_ids(self):
        for order in self:
            order.repair_count = len(order.repair_order_ids)

    def _action_confirm(self):
        res = super()._action_confirm()

        for order in self:
            for _ in filter(lambda line: line._is_create_repair_order_line(), order.order_line):# one Per SO_line, DO NOT use qty
                order.repair_order_ids.create({
                    'state' : 'confirmed',
                    'partner_id' : order.partner_id.id,
                    'sale_order_id' : order.id,
                })

        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    repair_move_line_id = fields.One2many(comodel_name='stock.move', inverse_name='sale_line_id', string='Repair Operation')

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        lines_without_repair_move = self.filtered(lambda line: line.move_ids and not line.move_ids.repair_id)
        if lines_without_repair_move:
            return super(SaleOrderLine, lines_without_repair_move)._action_launch_stock_rule()

    def _is_create_repair_order_line(self):
        self.ensure_one()
        return self.product_template_id.create_repair
