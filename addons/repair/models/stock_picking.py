# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import _, api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    code = fields.Selection(selection_add=[
        ('repair_operation', 'Repair')
    ], ondelete={'repair_operation': 'cascade'})

    count_repair_ready = fields.Integer(string="Number of Repair Orders to Process",
        compute='_compute_count_repair')
    count_repair_waiting = fields.Integer(string="Number of Repair Orders Waiting",
        compute='_compute_count_repair')
    count_repair_late = fields.Integer(string="Number of Repair Orders Late",
        compute='_compute_count_repair')

    is_repairable = fields.Boolean(
        'Create Repair Orders from Returns',
        compute='_compute_is_repairable', store=True, readonly=False,
        help="If ticked, you will be able to directly create repair orders from a return.")
    return_type_of_ids = fields.One2many('stock.picking.type', 'return_picking_type_id')

    @api.depends('return_type_of_ids', 'code')
    def _compute_is_repairable(self):
        for picking_type in self:
            if not(picking_type.code == 'incoming' and picking_type.return_type_of_ids):
                picking_type.is_repairable = False

    def _compute_count_repair(self):
        repair_picking_types = self.filtered(lambda picking: picking.code == 'repair_operation')

        #By default, set count_repair_xxx to False
        self.count_repair_ready = False
        self.count_repair_waiting = False
        self.count_repair_late = False

        #if there's no repair picking_type, that's all
        if not repair_picking_types:
            return

        #else, define the domain for each count_repair_xxx, and assign the result of search_count to repair picking_types
        domains = {
            'count_repair_ready': [('state', '=', 'assigned')],
            'count_repair_waiting': [('state', 'in', ('confirmed', 'waiting'))],
            'count_repair_late': [('state', 'in', ('assigned', 'waiting', 'confirmed')), ('scheduled_date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT))],
        }

        for field, domain in domains.items():
            for record in repair_picking_types:
                record[field] = self.env['stock.picking'].search_count(domain +
                [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', repair_picking_types.ids)])

class Picking(models.Model):
    _inherit = 'stock.picking'

    is_repairable = fields.Boolean(related='picking_type_id.is_repairable')
    repair_ids = fields.One2many('repair.order', 'picking_id')
    nbr_repairs = fields.Integer('Number of repairs linked to this picking', compute='_compute_nbr_repairs')

    @api.depends('repair_ids')
    def _compute_nbr_repairs(self):
        for picking in self:
            picking.nbr_repairs = len(picking.repair_ids)

    def action_repair_return(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({
            'default_location_id': self.location_dest_id.id,
            'default_picking_id': self.id,
            'default_partner_id': self.partner_id and self.partner_id.id or False,
        })
        return {
            'name': _('Create Repair'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'repair.order',
            'view_id': self.env.ref('repair.view_repair_order_form').id,
            'context': ctx,
        }

    def action_view_repairs(self):
        if self.repair_ids:
            action = {
                'res_model': 'repair.order',
                'type': 'ir.actions.act_window',
            }
            if len(self.repair_ids) == 1:
                action.update({
                    'view_mode': 'form',
                    'res_id': self.repair_ids[0].id,
                })
            else:
                action.update({
                    'name': _('Repair Orders'),
                    'view_mode': 'tree,form',
                    'domain': [('id', 'in', self.repair_ids.ids)],
                })
            return action
