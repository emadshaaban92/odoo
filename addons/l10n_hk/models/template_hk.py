# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_hk_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_hk_1240',
            'property_account_payable_id': 'l10n_hk_2211',
            'property_account_income_categ_id': 'l10n_hk_41',
            'property_account_expense_categ_id': 'l10n_hk_51',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '1200',
            'cash_account_code_prefix': '1210',
            'transfer_account_code_prefix': '111220',
            'code_digits': '6',
        }

    def _get_hk_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.hk',
                'account_default_pos_receivable_account_id': 'l10n_hk_1243',
                'income_currency_exchange_account_id': 'l10n_hk_4240',
                'expense_currency_exchange_account_id': 'l10n_hk_5240',
                'account_journal_early_pay_discount_loss_account_id': 'l10n_hk_5250',
                'account_journal_early_pay_discount_gain_account_id': 'l10n_hk_4250',
            },
        }

    def _get_hk_account_tax(self, template_code):
        return {
        }
