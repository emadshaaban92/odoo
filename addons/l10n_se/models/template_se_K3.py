# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_se_K3_template_data(self, template_code):
        return {
            'parent_id': 'l10nse_chart_template_K2',
            'bank_account_code_prefix': '193',
            'cash_account_code_prefix': '191',
            'transfer_account_code_prefix': '194',
            'code_digits': '4',
        }

    def _get_se_K3_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.se',
            },
        }

    def _get_se_K3_account_tax(self, template_code):
        return {
        }
