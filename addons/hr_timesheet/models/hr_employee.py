# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def name_get(self):
        res = super().name_get()
        if len(self.env.context.get('allowed_company_ids', [])) <= 1:
            return res
        name_mapping = dict(res)
        employee_read_group = self.env['hr.employee'].sudo()._read_group(
            [('user_id', 'in', self.user_id.ids)],
            ['user_id'],
            ['user_id'],
        )
        employees_count_per_user = {res['user_id'][0]: res['user_id_count'] for res in employee_read_group}
        for employee in self:
            if employees_count_per_user.get(employee.user_id.id, 0) > 1:
                name_mapping[employee.id] = f'{name_mapping[employee.id]} - {employee.company_id.name}'
        return list(name_mapping.items())

    def action_unlink_wizard(self):
        wizard = self.env['hr.employee.delete.wizard'].create({
            'employee_ids': self.ids,
        })
        if not self.user_has_groups('hr_timesheet.group_hr_timesheet_approver') and wizard.has_timesheet and not wizard.has_active_employee:
            raise UserError(_('You cannot delete employees who have timesheets.'))

        return {
            'name': _('Confirmation'),
            'view_mode': 'form',
            'res_model': 'hr.employee.delete.wizard',
            'views': [(self.env.ref('hr_timesheet.hr_employee_delete_wizard_form').id, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': wizard.id,
            'target': 'new',
            'context': self.env.context,
        }
