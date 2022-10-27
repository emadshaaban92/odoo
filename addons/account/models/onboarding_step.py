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

    # DASHBOARD ONBOARDING
    @api.model
    def action_open_account_dashboard_onboarding_fiscal_year(self):
        company = self.env.company
        company.create_op_move_if_non_existant()
        new_wizard = self.env['account.financial.year.op'].create({'company_id': company.id})
        view_id = self.env.ref('account.setup_financial_year_opening_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Accounting Periods'),
            'view_mode': 'form',
            'res_model': 'account.financial.year.op',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    @api.model
    def action_open_account_dashboard_onboarding_taxes(self):
        """ Called by the 'Taxes' button of the setup bar."""
        self.action_safe_set_just_done('account.account_dashboard_onboarding_taxes_step')

        view_id_list = self.env.ref('account.view_onboarding_tax_tree').id
        view_id_form = self.env.ref('account.view_tax_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Taxes'),
            'res_model': 'account.tax',
            'target': 'current',
            'views': [[view_id_list, 'list'], [view_id_form, 'form']],
            'context': {'search_default_sale': True, 'search_default_purchase': True, 'active_test': False},
        }

    @api.model
    def action_open_account_dashboard_onboarding_chart_of_accounts(self):
        """ Called by the 'Chart of Accounts' button of the dashboard onboarding panel."""
        company = self.env.company
        self.action_safe_set_just_done('account.account_dashboard_onboarding_chart_of_accounts_step')

        # If an opening move has already been posted, we open the tree view showing all the accounts
        if company.opening_move_posted():
            return 'account.action_account_form'

        # Otherwise, we create the opening move
        company.create_op_move_if_non_existant()

        # Then, we open will open a custom tree view allowing to edit opening balances of the account
        view_id = self.env.ref('account.init_accounts_tree').id
        # Hide the current year earnings account as it is automatically computed
        domain = [('account_type', '!=', 'equity_unaffected'), ('company_id', '=', company.id)]
        return {
            'type': 'ir.actions.act_window',
            'name': _('Chart of Accounts'),
            'res_model': 'account.account',
            'view_mode': 'tree',
            'limit': 99999999,
            'search_view_id': [self.env.ref('account.view_account_search').id],
            'views': [[view_id, 'list']],
            'domain': domain,
        }

    # STEPS WITHOUT PANEL
    @api.model
    def action_save_account_onboarding_setup_bill_step(self):
        return self.action_safe_set_just_done('account.account_dashboard_setup_bill_step')

    @api.model
    def action_open_account_onboarding_sale_tax(self):
        view_id = self.env.ref('account.account_onboarding_sale_tax_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales tax'),
            'res_id': self.env.company.id,
            'res_model': 'res.company',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']],
        }

    @api.model
    def action_save_account_onboarding_sale_tax_step(self):
        return self.action_safe_set_just_done('account.account_onboarding_sale_tax_step')
