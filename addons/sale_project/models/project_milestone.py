# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProjectMilestone(models.Model):
    _name = 'project.milestone'
    _inherit = 'project.milestone'

    def _default_sale_line_id(self):
        project_id = self._context.get('default_project_id')
        if project_id:
            return self.env['project.project'].browse(project_id).sale_line_id.filtered(lambda sol: sol.qty_delivered_method == 'milestones')

    allow_billable = fields.Boolean(related='project_id.allow_billable')
    project_partner_id = fields.Many2one(related='project_id.partner_id')

    sale_line_id = fields.Many2one('sale.order.line', 'Sales Order Item', default=_default_sale_line_id, help='Sales Order Item that will be updated once the milestone is reached.',
        domain="[('order_partner_id', '=?', project_partner_id), ('qty_delivered_method', '=', 'milestones')]")
    sale_line_name = fields.Text(compute="_compute_sale_line_id_name")
    quantity_percentage = fields.Float('Quantity Percentage', compute="_compute_quantity_percentage", store=True, help='Percentage of the ordered quantity that will automatically be delivered once the milestone is reached.')
    product_uom_qty = fields.Float(related="sale_line_id.product_uom_qty")
    product_uom = fields.Many2one(related="sale_line_id.product_uom")
    total_qty = fields.Float("Total Quantity", compute="_compute_total_qty", inverse="_inverse_total_qty")
    remaining_percentage = fields.Float("Remaining Percentage", compute="_compute_remaining_quantity")

    @api.depends('sale_line_id.name')
    def _compute_sale_line_id_name(self):
        for rec in self:
            rec.sale_line_name = rec.sale_line_id.display_name

    @api.depends('product_uom_qty', 'total_qty')
    def _compute_quantity_percentage(self):
        for milestone in self:
            milestone.quantity_percentage = milestone.product_uom_qty and milestone.total_qty / milestone.product_uom_qty

    @api.depends('quantity_percentage', 'product_uom_qty')
    def _compute_total_qty(self):
        for milestone in self:
            milestone.total_qty = milestone.quantity_percentage * milestone.product_uom_qty

    @api.onchange('product_uom_qty', 'total_qty')
    def _inverse_total_qty(self):
        for milestone in self:
            milestone.quantity_percentage = milestone.product_uom_qty and milestone.total_qty / milestone.product_uom_qty

    @api.depends('quantity_percentage', 'total_qty')
    def _compute_remaining_quantity(self):
        for milestone in self:
            milestone.remaining_percentage = milestone.product_uom_qty and (milestone.product_uom_qty - milestone.total_qty) / milestone.product_uom_qty

    @api.model
    def _get_fields_to_export(self):
        return super()._get_fields_to_export() + ['allow_billable', 'quantity_percentage', 'sale_line_name']

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Order'),
            'res_model': 'sale.order',
            'res_id': self.sale_line_id.order_id.id,
            'view_mode': 'form',
        }
