# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    task_id = fields.Many2one('project.task', string='Task')
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _compute_analytic_distribution(self):
        super()._compute_analytic_distribution()
        for line in self:
            if line._context.get('project_id'):
                line.analytic_distribution = {line.env['project.project'].browse(line._context['project_id']).analytic_account_id.id: 100}
            if line._context.get('task_id'):
                line.analytic_distribution = {line.env['project.task'].browse(line._context['task_id']).analytic_account_id.id: 100}
