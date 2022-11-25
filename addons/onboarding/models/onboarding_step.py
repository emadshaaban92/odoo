# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.addons.onboarding.models.onboarding_progress import ONBOARDING_PROGRESS_STATES
from odoo.exceptions import ValidationError


class OnboardingStep(models.Model):
    _name = 'onboarding.onboarding.step'
    _description = 'Onboarding Step'
    _order = 'sequence asc, id asc'
    _rec_name = 'title'

    onboarding_ids = fields.Many2many('onboarding.onboarding', string='Onboardings')

    title = fields.Char('Title', translate=True)
    description = fields.Char('Description', translate=True)
    button_text = fields.Char(
        'Button text', required=True, default=_("Let's do it"), translate=True,
        help="Text on the panel's button to start this step")
    done_icon = fields.Char('Font Awesome Icon when completed', default='fa-star')
    done_text = fields.Char(
        'Text to show when step is completed', default=_('Step Completed! - Click to review'), translate=True)
    panel_step_open_action_name = fields.Char(
        string='Opening action', required=False,
        help='Name of the onboarding step model action to execute when opening the step, '
             'e.g. action_open_onboarding_1_step_1')

    current_progress_step_id = fields.Many2one(
        'onboarding.progress.step', string='Step Progress',
        compute='_compute_current_progress', help='Onboarding Progress Step for the current context (company).')
    current_step_state = fields.Selection(
        ONBOARDING_PROGRESS_STATES, string='Completion State', compute='_compute_current_progress')
    progress_ids = fields.One2many(
        'onboarding.progress.step', 'step_id', string='Onboarding Progress Step Records', readonly=True,
        help='All related Onboarding Progress Step Records (across companies)')

    is_per_company = fields.Boolean('Is per company', default=True)
    sequence = fields.Integer(default=10)

    @api.depends_context('company')
    @api.depends('progress_ids', 'progress_ids.step_state', 'is_per_company')
    def _compute_current_progress(self):
        existing_progress_steps = self.progress_ids.filtered_domain([
            ('step_id', 'in', self.ids),
            ('company_id', 'in', [False, self.env.company.id]),
        ])
        for step in self:
            if step in existing_progress_steps.step_id:
                current_progress_step_id = existing_progress_steps.filtered(
                    lambda progress_step: progress_step.step_id == step)
                step.current_progress_step_id = current_progress_step_id
                step.current_step_state = current_progress_step_id.step_state
            else:
                step.current_progress_step_id = False
                step.current_step_state = 'not_done'

    @api.constrains('is_per_company', 'onboarding_ids')
    def check_is_per_company_consistency(self):
        for step in self:
            if any(is_step_per_company != step.is_per_company
                   for is_step_per_company in self.onboarding_ids.mapped('is_per_company')):
                raise ValidationError(_('Onboarding and step `is_per_company` must be equal.'))

    @api.constrains('onboarding_ids')
    def check_step_on_onboarding_has_action(self):
        for step in self:
            if step.onboarding_ids and not step.panel_step_open_action_name:
                raise ValidationError(_('An action name to open is required for steps linked to an onboarding panel.'))

    def write(self, vals):
        all_per_company_before = set(self.mapped('is_per_company'))
        res = super().write(vals)
        if 'is_per_company' in vals and all_per_company_before - {vals['is_per_company']}:
            if self.onboarding_ids:
                raise ValidationError(
                    _('To change "is_per_company" for onboarding steps used in an onboarding panel, '
                      'use the dedicated toggle button (action) of the onboarding.'))
            # Resetting progress
            self.progress_ids.unlink()
        return res

    def action_set_just_done(self):
        # Make sure progress records exist for the current context (company)
        steps_without_progress = self.filtered(lambda step: not step.current_progress_step_id)
        steps_without_progress._create_progress_steps()
        return self.current_progress_step_id.action_set_just_done()

    def _create_progress_steps(self):
        """Create progress step records only for (current company if `is_per_company`) and
        * If no onboarding panel is linked, or
        * for existing `onboarding.progress` records."""
        onboarding_progress_records = self.env['onboarding.progress'].search([
            ('onboarding_id', 'in', self.onboarding_ids.ids),
            ('company_id', 'in', [False, self.env.company.id])
        ])
        progress_step_values = [
            {
                'step_id': step_id.id,
                'progress_ids': [
                    (4, onboarding_progress_record.id)
                    for onboarding_progress_record
                    in onboarding_progress_records.filtered(lambda p: step_id in p.onboarding_id.step_ids)],
                'company_id': self.env.company.id if step_id.is_per_company else False,
            } for step_id in self
        ]
        return self.env['onboarding.progress.step'].create(progress_step_values)
