# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tools.misc import format_duration
from odoo import _, api, fields, models


class HRLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    hr_attendance_overtime = fields.Boolean(compute='_compute_hr_attendance_overtime')
    overtime_deductible = fields.Boolean(
        "Deduct Extra Hours", default=False,
        help="Once a time off of this type is approved, extra hours in attendances will be deducted.")

    def name_get(self):
        # Exclude hours available in allocation contexts, it might be confusing otherwise
        if not self.requested_name_get() or self._context.get('request_type', 'leave') == 'allocation':
            return super().name_get()
        employee_id = False
        overtime_leaves = self.env['hr.leave.type']
        res = []
        for leave_type in self:
            if leave_type.overtime_deductible and leave_type.requires_allocation == 'no':
                if not employee_id:
                    employee_id = self.env['hr.employee'].browse(self._context.get('employee_id')).sudo()
                if employee_id.total_overtime > 0:
                    overtime_leaves |= leave_type
                    name = "%(name)s (%(count)s)" % {
                        'name': leave_type.name,
                        'count': _('%s hours available',
                            format_duration(employee_id.total_overtime)),
                    }
                    res.append((leave_type.id, name))
        res += super(HRLeaveType, self - overtime_leaves).name_get()
        return res

    def get_allocation_data(self, employee_ids, date=None):
        res = super().get_allocation_data(employee_ids)
        deductible_time_off_type_ids = self.env['hr.leave.type'].search([
            ('overtime_deductible', '=', True),
            ('requires_allocation', '=', 'no')])
        leave_type_names = deductible_time_off_type_ids.mapped('name')
        for employee in res:
            for leave_data in res[employee]:
                if leave_data[0] in leave_type_names:
                    leave_data[1]['virtual_remaining_leaves'] = employee.sudo().total_overtime
                    leave_data[1]['overtime_deductible'] = True
                else:
                    leave_data[1]['overtime_deductible'] = False
        return res

    def _get_days_request(self, date=None):
        res = super()._get_days_request(date)
        res[1]['overtime_deductible'] = self.overtime_deductible
        return res

    @api.depends('company_id.hr_attendance_overtime')
    def _compute_hr_attendance_overtime(self):
        # If no company is linked to the time off type, use the current company's setting
        for leave_type in self:
            if leave_type.company_id:
                leave_type.hr_attendance_overtime = leave_type.company_id.hr_attendance_overtime
            else:
                leave_type.hr_attendance_overtime = self.env.company.hr_attendance_overtime
