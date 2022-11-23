# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.addons.onboarding.models.onboarding_progress import ONBOARDING_PROGRESS_STATES
from odoo.exceptions import ValidationError


class OnboardingProgressStep(models.Model):
    _name = 'onboarding.progress.step'
    _description = 'Onboarding Progress Step Tracker'
    _rec_name = 'step_id'

    progress_ids = fields.Many2many(
        'onboarding.progress', 'onboarding_progress_onboarding_progress_step_rel',
        'onboarding_progress_step_id', 'onboarding_progress_id',
        string='Related Onboarding Progress Tracker', required=False)
    step_state = fields.Selection(
        ONBOARDING_PROGRESS_STATES, string='Onboarding Step Progress', default='not_done')
    company_id = fields.Many2one('res.company', string='Company', ondelete='cascade')
    step_id = fields.Many2one(
        'onboarding.onboarding.step', string='Onboarding Step', required=True, ondelete='cascade')

    @api.constrains('company_id', 'step_id')
    def check_progress_per_company(self):
        progress_data = self.read_group(
            [('company_id', 'in', [self.env.company.id, False]), ('step_id', 'in', self.step_id.ids)],
            ['step_id', 'ids:array_agg(id)'], ['step_id']
        )
        for data in progress_data:
            if len(data['ids']) > 1:
                raise ValidationError(_(
                    'There cannot be multiple records of the same onboarding step completion for the same company.'))

    def action_consolidate_just_done(self):
        was_just_done = self.filtered(lambda progress: progress.step_state == 'just_done')
        was_just_done.step_state = 'done'
        return was_just_done

    def action_set_just_done(self):
        not_done = self.filtered_domain([('step_state', '=', 'not_done')])
        not_done.step_state = 'just_done'
        return not_done
