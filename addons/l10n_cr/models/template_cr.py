# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_cr_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '0.1112',
            'cash_account_code_prefix': '0.1111',
            'transfer_account_code_prefix': '0.1114',
            'property_account_receivable_id': 'account_account_template_0_112001',
            'property_account_payable_id': 'account_account_template_0_211001',
            'property_account_income_categ_id': 'account_account_template_0_410001',
            'property_account_expense_categ_id': 'account_account_template_0_511301',
        }

    def _get_cr_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.cr',
                'account_default_pos_receivable_account_id': 'account_account_template_0_112011',
                'income_currency_exchange_account_id': 'account_account_template_0_450001',
                'expense_currency_exchange_account_id': 'account_account_template_0_530004',
            },
        }

    def _get_cr_account_tax(self, template_code):
        return {
            'account_tax_template_IV_0': {
                'name': 'Sales Tax',
                'description': 'IV',
                'sequence': 10,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_0_212101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_0_212101',
                    }),
                ],
            },
            'account_tax_template_IV_1': {
                'name': 'Purchase Tax',
                'description': 'IV',
                'sequence': 10,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_0_212101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_0_212101',
                    }),
                ],
            },
        }
