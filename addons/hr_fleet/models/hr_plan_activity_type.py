# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class HrPlanActivityType(models.Model):
    _inherit = 'hr.plan.activity.type'

    responsible = fields.Selection(selection_add=[('fleet_manager', "Fleet Manager"), ('employee', 'Employee')], ondelete={'fleet_manager': 'set default'})

    def get_responsible_id(self, employee):
        if self.responsible == 'fleet_manager':
            warning = False
            responsible = self.env['hr.employee'].browse(employee._origin.id).car_ids.manager_id
            if not responsible:
                warning = _('Fleet manager of employee %s is not set.', employee.name)
            return {
                'responsible': responsible,
                'warning': warning,
        }
        return super().get_responsible_id(employee)
