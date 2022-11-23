# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class OnboardingStep(models.Model):
    _inherit = "onboarding.onboarding.step"

    @api.model
    def action_save_payment_onboarding_payment_provider_step(self):
        return self.action_safe_set_just_done('payment.payment_onboarding_payment_provider_step')
