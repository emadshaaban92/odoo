# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models


class OnboardingStep(models.Model):
    _inherit = 'onboarding.onboarding.step'

    # COMMON STEPS
    @api.model
    def action_open_account_common_onboarding_company(self):
        """ Onboarding step for company basic information. """
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_open_account_common_onboarding_company")
        action['res_id'] = self.env.company.id
        return action

    @api.model
    def action_save_account_common_onboarding_company_step(self):
        return self.action_safe_set_just_done('account.account_common_onboarding_company_step')

    @api.model
    def action_open_account_common_onboarding_layout(self, action_ref=None):
        if not action_ref:
            view_id = self.env.ref('web.view_base_document_layout').id
            return {
                'name': _('Configure your document layout'),
                'type': 'ir.actions.act_window',
                'res_model': 'base.document.layout',
                'target': 'new',
                'view_mode': 'form',
                'views': [(view_id, "form")],
            }
        res = self.env["ir.actions.actions"]._for_xml_id(action_ref)
        self.env[res["res_model"]].check_access_rights('write')
        return res

    @api.model
    def action_save_account_common_onboarding_layout_step(self):
        """ Set the onboarding(s) step as done only if layout is set. """
        step = self.env.ref('account.account_common_onboarding_layout_step', raise_if_not_found=False)
        if not step or not self.env.company.external_report_layout_id:
            return False
        return bool(step.action_set_just_done())

    # INVOICE ONBOARDING
    @api.model
    def action_setting_init_bank_account(self):
        return self.env.company.setting_init_bank_account_action()

    @api.model
    def action_save_account_invoice_onboarding_bank_account_step(self):
        return self.action_safe_set_just_done('account.account_invoice_onboarding_bank_account_step')

    @api.model
    def action_open_account_onboarding_create_invoice(self):
        return self.env["ir.actions.actions"]._for_xml_id("account.action_open_account_onboarding_create_invoice")
