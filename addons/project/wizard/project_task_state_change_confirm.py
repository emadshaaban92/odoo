
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from ast import literal_eval


class WizardConfirmation(models.TransientModel):
    _name = "project.wizard.confirmation"
    _description = 'Confirmation wizard'

    depend_on_task_string = fields.Char(default='',readonly=True)

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        result['depend_on_task_string'] = ', '.join(self.env.context['blocking_task_list'])
        #if not result.get('access_mode'):
        #    result.update(
        #        access_mode='read',
        #        display_access_mode=True,
        #    )
        return result

    def confirm(self):
        future_state = self.env['project.task.state'].search([('key', '=', self.env.context['future_state_key'])])
        self.env['project.task'].search([('id','=',self.env.context['active_id'])]).write({'state_id': future_state,'state_forced': True})
        return