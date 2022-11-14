# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tasks_ids = fields.Many2many('project.task', compute='_compute_tasks_ids', string='Tasks associated to this sale')
    tasks_count = fields.Integer(string='Tasks', compute='_compute_tasks_ids', groups="project.group_project_user")

    visible_project = fields.Boolean('Display project', compute='_compute_visible_project', readonly=True)
    project_id = fields.Many2one(
        'project.project', 'Project', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help='Select a non billable project on which tasks can be created.')
    project_ids = fields.Many2many('project.project', compute="_compute_project_ids", string='Projects', copy=False, groups="project.group_project_user", help="Projects used in this sales order.")
    project_count = fields.Integer(string='Number of Projects', compute='_compute_project_ids', groups='project.group_project_user')
    milestone_count = fields.Integer(compute='_compute_milestone_count')
    is_product_milestone = fields.Boolean(compute='_compute_is_product_milestone')
    show_create_project_button = fields.Boolean(compute='_compute_show_project_and_task_button')
    show_project_and_task_button = fields.Boolean(compute='_compute_show_project_and_task_button')

    def _compute_milestone_count(self):
        read_group = self.env['project.milestone']._read_group(
            [('sale_line_id', 'in', self.order_line.ids)],
            ['sale_line_id'],
            ['sale_line_id'],
        )
        line_data = {res['sale_line_id'][0]: res['sale_line_id_count'] for res in read_group}
        for order in self:
            order.milestone_count = sum(line_data.get(line.id, 0) for line in order.order_line)

    def _compute_is_product_milestone(self):
        for order in self:
            order.is_product_milestone = order.order_line.product_id.filtered(lambda p: p.service_policy == 'delivered_milestones')

    def _compute_show_project_and_task_button(self):
        user_is_manager = self.env.user.has_group('project.group_project_manager')
        user_has_access_right = user_is_manager or self.env.user.has_group('project.group_project_user')
        for order in self:
            show_project = any(sol.is_service and sol.product_id.service_policy != 'delivered_manual' for sol in order.order_line) and not order.state in ['draft', 'sent']
            order.show_project_and_task_button = show_project and user_has_access_right and order.project_count > 0
            order.show_create_project_button = show_project and user_is_manager and order.project_count == 0

    @api.depends('order_line.product_id.project_id')
    def _compute_tasks_ids(self):
        for order in self:
            order.tasks_ids = self.env['project.task'].search(['&', ('display_project_id', '!=', 'False'), '|', ('sale_line_id', 'in', order.order_line.ids), ('sale_order_id', '=', order.id)])
            order.tasks_count = len(order.tasks_ids)

    @api.depends('order_line.product_id.service_tracking')
    def _compute_visible_project(self):
        """ Users should be able to select a project_id on the SO if at least one SO line has a product with its service tracking
        configured as 'task_in_project' """
        for order in self:
            order.visible_project = any(
                service_tracking == 'task_in_project' for service_tracking in order.order_line.mapped('product_id.service_tracking')
            )

    @api.depends('order_line.product_id', 'order_line.project_id')
    def _compute_project_ids(self):
        is_project_manager = self.user_has_groups('project.group_project_manager')
        projects = self.env['project.project'].search([('sale_order_id', 'in', self.ids)])
        projects_per_so = defaultdict(lambda: self.env['project.project'])
        for project in projects:
            projects_per_so[project.sale_order_id.id] |= project
        for order in self:
            projects = order.order_line.mapped('product_id.project_id')
            projects |= order.order_line.mapped('project_id')
            projects |= order.project_id
            projects |= projects_per_so[order.id or order._origin.id]
            if not is_project_manager:
                projects = projects._filter_access_rules('read')
            order.project_ids = projects
            order.project_count = len(projects)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        """ Set the SO analytic account to the selected project's analytic account """
        if self.project_id.analytic_account_id:
            self.analytic_account_id = self.project_id.analytic_account_id

    def _action_confirm(self):
        """ On SO confirmation, some lines should generate a task or a project. """
        result = super()._action_confirm()
        if len(self.company_id) == 1:
            # All orders are in the same company
            self.order_line.sudo().with_company(self.company_id)._timesheet_service_generation()
        else:
            # Orders from different companies are confirmed together
            for order in self:
                order.order_line.sudo().with_company(order.company_id)._timesheet_service_generation()
        return result

    def action_view_task(self):
        self.ensure_one()
        if not self.order_line:
            return {'type': 'ir.actions.act_window_close'}

        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id
        kanban_view_id = self.env.ref('project.view_task_kanban_inherit_view_default_project').id

        default_line = next(sol for sol in self.order_line if sol.is_service and sol.product_id.service_policy != 'delivered_manual')

        action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")
        action['context'] = {}  # erase default context to avoid default filter
        if self.tasks_count > 1:  # cross project kanban task
            action['views'] = [[kanban_view_id, 'kanban'], [list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'calendar'], [False, 'pivot']]
        else:  # 1 or 0 tasks -> form view
            action['views'] = [(form_view_id, 'form')]
            action['res_id'] = self.tasks_ids.id
        # filter on the task of the current SO
        action.setdefault('context', {})
        # set default project
        default_project_id = default_line.project_id.id or self.project_id.id or (len(self.project_ids) > 0 and self.project_ids[0].id)

        action['context'].update({
            'search_default_sale_order_id': self.id,
            'default_sale_order_id': self.id,
            'default_sale_line_id': default_line.id,
            'default_partner_id': self.partner_id.id,
            'default_project_id': default_project_id,
            'default_user_ids': [self.env.uid],
        })
        return action

    def action_create_project(self):
        self.ensure_one()
        if not self.order_line:
            return {'type': 'ir.actions.act_window_close'}

        sorted_line = self.order_line.sorted(key=lambda sol: sol.sequence)
        default_sale_line = next(sol for sol in sorted_line if sol.is_service and sol.product_id.service_policy != 'delivered_manual')
        action = self.env["ir.actions.actions"]._for_xml_id("project.open_create_project")
        action['context'] = {
            'default_sale_order_id': self.id,
            'default_sale_line_id': default_sale_line.id,
            'default_partner_id': self.partner_id.id,
            'default_user_ids': [self.env.uid],
            'default_allow_billable': 1,
        }
        return action

    def action_view_project_ids(self):
        self.ensure_one()
        if not self.order_line:
            return {'type': 'ir.actions.act_window_close'}

        sorted_line = self.order_line.sorted(key=lambda sol: sol.sequence)
        default_sale_line = next(sol for sol in sorted_line if sol.is_service and sol.product_id.service_policy != 'delivered_manual')

        view_form_id = self.env.ref('project.edit_project').id
        view_kanban_id = self.env.ref('project.view_project_kanban').id
        domain = ['|', ('sale_order_id', '=', self.id), ('id', 'in', self.project_ids.ids)]
        action = {
            'type': 'ir.actions.act_window',
            'domain': domain,
            'view_mode': 'kanban,form',
            'name': _('Projects'),
            'res_model': 'project.project',
            'help': _("""
                <p class="o_view_nocontent_smiling_face">
                    No Projects found. Let's create one!
                </p><p>
                    Create projects to organize your tasks. Define a different workflow for each project.
                </p>
            """),
            'context': {
                **self.env.context,
                'default_partner_id': self.partner_id.id,
                'default_sale_line_id': default_sale_line.id,
                'default_allow_billable': 1,
            }
        }
        if len(self.project_ids) == 1:
            action.update({'views': [(view_form_id, 'form')], 'res_id': self.project_ids.id})
        else:
            action['views'] = [(view_kanban_id, 'kanban'), (view_form_id, 'form')]
        return action

    def action_view_milestone(self):
        self.ensure_one()
        default_project = self.project_ids and self.project_ids[0]
        default_sale_line = default_project.sale_line_id or self.order_line and self.order_line[0]
        return {
            'type': 'ir.actions.act_window',
            'name': _('Milestones'),
            'domain': [('sale_line_id', 'in', self.order_line.ids)],
            'res_model': 'project.milestone',
            'views': [(self.env.ref('sale_project.sale_project_milestone_view_tree').id, 'tree')],
            'view_mode': 'tree',
            'help': _("""
                <p class="o_view_nocontent_smiling_face">
                    No milestones found. Let's create one!
                </p><p>
                    Track major progress points that must be reached to achieve success.
                </p>
            """),
            'context': {
                **self.env.context,
                'default_project_id' : default_project.id,
                'default_sale_line_id' : default_sale_line.id,
            }
        }

    def write(self, values):
        if 'state' in values and values['state'] == 'cancel':
            self.project_id.sudo().sale_line_id = False
        return super(SaleOrder, self).write(values)
