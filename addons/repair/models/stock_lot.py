# -*- coding: utf-8 -*-

from collections import defaultdict
from odoo import api, fields, models, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    repair_order_ids = fields.Many2many('repair.order', string="Repair Orders", compute="_compute_repair_order_ids")
    repair_order_count = fields.Integer('Repair order count', compute="_compute_repair_order_ids")

    @api.depends('name')
    def _compute_repair_order_ids(self):
        repair_orders = defaultdict(lambda: self.env['repair.order'])
        for repair_line in self.env['stock.move'].search([('repair_id', '!=', False), ('lot_ids', 'in', self.ids), ('state', '=', 'done')]): #Now a stock.move with repair_id
            for rl_id in repair_line.lot_ids.ids:
                repair_orders[rl_id] |= repair_line.repair_id
        for lot in self:
            lot.repair_order_ids = repair_orders[lot.id]
            lot.repair_order_count = len(lot.repair_order_ids)

    def action_view_ro(self):
        self.ensure_one()

        action = {
            'res_model': 'repair.order',
            'type': 'ir.actions.act_window'
        }
        if len(self.repair_order_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.repair_order_ids[0].id
            })
        else:
            action.update({
                'name': _("Repair orders of %s", self.name),
                'domain': [('id', 'in', self.repair_order_ids.ids)],
                'view_mode': 'tree,form'
            })
        return action
