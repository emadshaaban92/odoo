# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Onboarding(models.Model):
    _inherit = 'onboarding.onboarding'

    # Sale Quotation Onboarding
    @api.model
    def action_close_sale_quotation_onboarding(self):
        self.action_safe_close('sale.sale_quotation_onboarding')
