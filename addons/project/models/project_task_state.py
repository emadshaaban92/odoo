# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProjectTaskState(models.Model):
    _name = 'project.task.state'
    _description = 'Task State'


    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=50)
    name = fields.Char(required=True, translate=True)
    approval_mode = fields.Boolean(default=False)
    user_trigger_possible = fields.Boolean(default=True)
    
