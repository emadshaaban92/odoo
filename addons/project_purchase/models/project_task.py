# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class Project(models.Model):
    _inherit = "project.task"

    purchase_orders_count = fields.Integer('# Purchase Orders', compute='_compute_purchase_orders_count', groups='purchase.group_purchase_user')

    def _compute_purchase_orders_count(self):
        if not self.analytic_account_id:
            self.purchase_orders_count = 0
            return
        purchase_orders_data = self.env['purchase.order.line'].read_group([
            ('account_analytic_id', 'in', self.analytic_account_id.ids),
            ('task_id', 'in', self.ids)
        ], ['task_id', 'order_id:count_distinct'], ['task_id'])
        purchase_orders_per_task = {}
        for purchase_order in purchase_orders_data:
            purchase_orders_per_task[purchase_order['task_id'][0]] = purchase_order['order_id']
        for task in self:
            task.purchase_orders_count = purchase_orders_per_task.get(task.id, 0)
    	   

    # ----------------------------
    #  Actions
    # ----------------------------

    def action_open_task_purchase_orders(self):
        self.ensure_one()
        purchase_orders = self.env['purchase.order'].search([
            ('task_id', '=', self.id),
        ])
        action_window = {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'views': [[False, 'tree'], [False, 'form']],
            'domain': [('id', 'in', purchase_orders.ids)],
            'context': {
                'create': False,
            }
        }
        if len(purchase_orders) == 1:
            action_window['views'] = [[False, 'form']]
            action_window['res_id'] = purchase_orders.id
        return action_window

    @api.model
    def action_create_purchase_order_from_task(self):
        self.ensure_one()
        if not self.partner_id:
            ValidationError(_("set customer to create purchase order"))
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'journal_id': self[0].journal_id.id,
            'payment_ids': [(4, payment.id, None) for payment in self],
            'payment_method_id': self[0].payment_method_id.id,
            'batch_type': self[0].payment_type,
        })

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.batch.payment",
            "views": [[False, "form"]],
            "res_id": batch.id,
        }
        