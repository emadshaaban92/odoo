# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Onboarding(models.Model):
    _inherit = 'onboarding.onboarding'

    # Invoice Onboarding
    @api.model
    def action_close_account_invoice_onboarding(self):
        self.action_safe_close('account.account_invoice_onboarding')

    def _prepare_rendering_values(self):
        """ Compute existence of invoices for company. """
        if self == self.env.ref('account.account_invoice_onboarding', raise_if_not_found=False):
            create_invoice_step = self.env.ref('account.account_invoice_onboarding_create_invoice_step',
                                               raise_if_not_found=False)
            if create_invoice_step and create_invoice_step.current_step_state == 'not_done':
                if self.env['account.move'].search([('company_id', '=', self.env.company.id),
                                                    ('move_type', '=', 'out_invoice')], limit=1):
                    create_invoice_step.action_set_just_done()
        return super()._prepare_rendering_values()
