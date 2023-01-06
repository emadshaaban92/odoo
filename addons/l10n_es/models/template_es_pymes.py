# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_es_pymes_template_data(self, template_code):
        return {
            'cash_account_code_prefix': '570',
            'bank_account_code_prefix': '572',
            'transfer_account_code_prefix': '57299',
            'parent_id': 'account_chart_template_common',
        }

    def _get_es_pymes_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.es',
            },
        }

    def _get_es_pymes_account_tax(self, template_code):
        return {
        }
