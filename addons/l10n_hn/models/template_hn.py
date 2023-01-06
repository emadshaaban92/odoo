# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_hn_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'cta110201',
            'property_account_payable_id': 'cta210101',
            'property_account_income_categ_id': 'cta410101',
            'property_account_expense_categ_id': 'cta510101',
            'bank_account_code_prefix': '1.1.01.',
            'cash_account_code_prefix': '1.1.01.',
            'transfer_account_code_prefix': '1.1.01.00',
            'code_digits': '9',
        }

    def _get_hn_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.hn',
                'account_default_pos_receivable_account_id': 'cta110205',
                'income_currency_exchange_account_id': 'cta410103',
                'expense_currency_exchange_account_id': 'cta710101',
                'account_journal_early_pay_discount_loss_account_id': 'cta620202',
                'account_journal_early_pay_discount_gain_account_id': 'cta420102',
            },
        }

    def _get_hn_account_tax(self, template_code):
        return {
            'impuestos_plantilla_isv_por_cobrar': {
                'name': 'ISV por Cobrar',
                'description': 'ISV por Cobrar',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'tax_group_iva_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cta110301',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cta110301',
                    }),
                ],
            },
            'impuestos_plantilla_isv_por_pagar': {
                'name': 'ISV por Pagar',
                'description': 'ISV por Pagar',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': True,
                'tax_group_id': 'tax_group_iva_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cta210201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cta210201',
                    }),
                ],
            },
        }
