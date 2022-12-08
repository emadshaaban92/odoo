# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _



class Project(models.Model):
    _inherit = "project.task"

    purchase_orders_count = fields.Integer('# Purchase Orders', compute='_compute_purchase_orders_count', groups='purchase.group_purchase_user')

    def _compute_purchase_orders_count(self):
        purchase_orders_data = self.env['purchase.order'].read_group([
            ('task_id', 'in', self.ids),
        ], ['task_id'], ['task_id'])
        purchase_orders_per_task = {}
        for purchase_order in purchase_orders_data:
            purchase_orders_per_task[purchase_order['task_id'][0]] = purchase_order['task_id_count']
        for task in self:
            task.purchase_orders_count = purchase_orders_per_task.get(task.id, 0)

    # ----------------------------
    #  Actions
    # ----------------------------

    def action_open_task_purchase_orders(self):
        self.ensure_one()
        query = self.env['purchase.order.line']._search([])
        query_string, query_param = query.select('order_id')
        self._cr.execute(query_string, query_param)
        purchase_order_ids = [pol.get('order_id') for pol in self._cr.dictfetchall()]
        action_window = {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'views': [[False, 'tree'], [False, 'form']],
            'context':{'task_id': self.id},
            'domain': [('task_id', '=', self.id)],
        }
        if len(purchase_order_ids) == 1:
            action_window['views'] = [[False, 'form']]
            action_window['res_id'] = purchase_order_ids
        return action_window

    @api.model
    def action_create_purchase_order_from_task(self):
        self.ensure_one()
        res = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': _('Purchase order successfully created.'),
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

        tasks = self.filtered(lambda task: task.partner_id)
        if not tasks:
            res['params'].update({
                'type': 'warning',
                'message': _("Some required fields are missing so you can't create an purchase order.")
            })
            return res

        else:
            self.env['purchase.order'].create({'partner_id': self.partner_id.id, 'task_id': self.id})
        return res
