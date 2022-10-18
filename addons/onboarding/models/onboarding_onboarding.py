# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, Command, fields, models
from odoo.addons.onboarding.models.onboarding_progress import ONBOARDING_PROGRESS_STATES
from odoo.exceptions import ValidationError


class Onboarding(models.Model):
    _name = 'onboarding.onboarding'
    _description = 'Onboarding'
    _order = 'sequence asc, id desc'

    name = fields.Char('Name of the onboarding', translate=True)
    # One word identifier used to define the onboarding panel's route: `/onboarding/{route_name}`.
    route_name = fields.Char('One word name', required=True)
    step_ids = fields.Many2many('onboarding.onboarding.step', string='Onboarding steps')

    text_completed = fields.Char(
        'Congratulations on completed', default='Nice work! Your configuration is done.',
        help='Text shown on onboarding when completed')

    is_per_company = fields.Boolean('Should be done per company?', default=True)

    panel_background_color = fields.Selection(
        [('orange', 'Orange'), ('blue', 'Blue'), ('violet', 'Violet'), ('none', 'None')],
        string="Panel's Background color", default='orange',
        help="Color gradient added to the panel's background.")
    panel_background_image = fields.Binary("Panel's background image")
    panel_close_action_name = fields.Char(
        'Closing action', help='Name of the onboarding model action to execute when closing the panel.')

    current_progress_id = fields.Many2one(
        'onboarding.progress', 'Onboarding Progress', compute='_compute_current_progress',
        help='Onboarding Progress for the current context (company).')
    current_onboarding_state = fields.Selection(
        ONBOARDING_PROGRESS_STATES, string='Completion State', compute='_compute_current_progress', readonly=True)
    is_onboarding_closed = fields.Boolean(string='Was panel closed?', compute='_compute_current_progress')

    progress_ids = fields.One2many(
        'onboarding.progress', 'onboarding_id', string='Onboarding Progress Records', readonly=True,
        help='All Onboarding Progress Records (across companies).')

    sequence = fields.Integer(default=10)
    _sql_constraints = [
        ('route_name_uniq', 'UNIQUE (route_name)', 'Onboarding alias must be unique.'),
    ]

    @api.constrains('is_per_company', 'step_ids')
    def check_is_per_company_consistency(self):
        for onboarding in self:
            if any(is_step_per_company != onboarding.is_per_company
                   for is_step_per_company in onboarding.step_ids.mapped('is_per_company')):
                raise ValidationError(_('Onboarding and step `is_per_company` must be equal.'))

    @api.depends_context('company')
    @api.depends('progress_ids', 'progress_ids.is_onboarding_closed', 'progress_ids.onboarding_state')
    def _compute_current_progress(self):
        for onboarding in self:
            current_progress_id = onboarding.progress_ids.filtered(
                lambda progress: progress.company_id.id in {False, self.env.company.id})
            if current_progress_id:
                onboarding.current_onboarding_state = current_progress_id.onboarding_state
                onboarding.current_progress_id = current_progress_id
                onboarding.is_onboarding_closed = current_progress_id.is_onboarding_closed
            else:
                onboarding.current_onboarding_state = 'not_done'
                onboarding.current_progress_id = False
                onboarding.is_onboarding_closed = False

    def action_close(self):
        """Close the onboarding panel."""
        self.current_progress_id.action_close()

    @api.model
    def action_safe_close(self, xmlid):
        """Close the onboarding panel identified by its `xmlid`. If not found,
        quietly do nothing."""
        onboarding = self.env.ref(xmlid, raise_if_not_found=False)
        if onboarding:
            onboarding.action_close()

    def action_toggle_visibility(self):
        self.current_progress_id.action_toggle_visibility()

    def write(self, values):
        onboardings_per_company_update = self
        if 'is_per_company' in values:
            onboardings_per_company_update = onboardings_per_company_update.filtered(
                lambda onboarding: onboarding.is_per_company != values['is_per_company'])
            if onboardings_per_company_update.step_ids:
                raise ValidationError(
                    _('To change "is_per_company" for onboardings with associated steps, '
                      'use the dedicated toggle button (action) of the onboarding.'))

        res = super().write(values)

        if 'is_per_company' in values:
            # When changing this parameter, all progress must be reset.
            onboardings_per_company_update.progress_ids.unlink()
        return res

    def _search_or_create_progress(self):
        """Create Progress record(s) as necessary for the context.
        """
        onboardings_without_progress = self.filtered(lambda onboarding: not onboarding.current_progress_id)
        onboardings_without_progress._create_progress()
        return self.current_progress_id

    def _create_progress(self):
        return self.env['onboarding.progress'].create([
            {
                'company_id': self.env.company.id if onboarding.is_per_company else False,
                'onboarding_id': onboarding.id
            } for onboarding in self
        ])

    def _prepare_rendering_values(self):
        self.ensure_one()
        values = {
            'bg_image': f'/web/image/onboarding.onboarding/{self.id}/panel_background_image',
            'classes': f'o_onboarding_{self.panel_background_color}'
                       if self.panel_background_color not in {False, 'none'} else '',
            'close_method': self.panel_close_action_name,
            'close_model': 'onboarding.onboarding',
            'steps': self.step_ids.sorted('sequence'),
            'state': self.current_progress_id._get_and_update_onboarding_state(),
            'text_completed': self.text_completed,
        }

        return values

    def action_toggle_is_per_company(self):
        """ Toggle onboarding and steps `is_per_company`, discarding existing
        progress. This action is allowed when the steps included in 'self'
        onboardings are not used in other onboardings.
        """

        onboardings_were_per_company = self.filtered(lambda o: o.is_per_company)
        onboardings_were_not_per_company = self - onboardings_were_per_company

        onboarding_steps_were_per_company = onboardings_were_per_company.step_ids
        onboarding_steps_were_not_per_company = onboardings_were_not_per_company.step_ids

        # check that steps to update are not used in other onboardings.
        if (onboarding_steps_were_per_company.onboarding_ids > onboardings_were_per_company
                or onboarding_steps_were_not_per_company.onboarding_ids > onboardings_were_not_per_company):
            raise ValidationError(
                _('Impossible to toggle is_per_company for onboardings with steps used in other onboardings.'))

        self.step_ids.progress_ids.unlink()

        onboardings_to_steps = {onboarding: onboarding.step_ids for onboarding in self if onboarding.step_ids}

        self.step_ids = False
        self.flush_recordset(['step_ids'])

        onboardings_were_per_company.is_per_company = False
        onboarding_steps_were_per_company.is_per_company = False

        onboardings_were_not_per_company.is_per_company = True
        onboarding_steps_were_not_per_company.is_per_company = True

        for onboarding, steps in onboardings_to_steps.items():
            onboarding.step_ids = [Command.set(steps.ids)]
