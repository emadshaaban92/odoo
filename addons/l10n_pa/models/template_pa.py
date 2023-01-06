# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_pa_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '111.',
            'cash_account_code_prefix': '113.',
            'transfer_account_code_prefix': '112.',
            'code_digits': '7',
            'property_account_receivable_id': '121',
            'property_account_payable_id': '211',
            'property_account_expense_categ_id': '62_01',
            'property_account_income_categ_id': '411_01',
        }

    def _get_pa_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.pa',
                'account_default_pos_receivable_account_id': '121_01',
                'income_currency_exchange_account_id': 'gain81_01',
                'expense_currency_exchange_account_id': 'loss81_01',
            },
        }

    def _get_pa_account_tax(self, template_code):
        return {
            'ITAX_19': {
                'name': 'ITBMS 7% Venta',
                'description': 'ITBMS 7% Venta',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                    }),
                ],
            },
            'OTAX_19': {
                'name': 'ITBMS 7% Compra',
                'description': 'ITBMS 7% Compra',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                    }),
                ],
            },
        }
