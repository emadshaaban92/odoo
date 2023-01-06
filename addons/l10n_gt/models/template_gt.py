# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_gt_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '1.0.01.0',
            'cash_account_code_prefix': '1.0.02.0',
            'transfer_account_code_prefix': '1.0.03.01',
            'code_digits': '9',
            'property_account_receivable_id': 'cta110201',
            'property_account_payable_id': 'cta210101',
            'property_account_income_categ_id': 'cta410101',
            'property_account_expense_categ_id': 'cta510101',
        }

    def _get_gt_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.gt',
                'account_default_pos_receivable_account_id': 'cta110205',
                'income_currency_exchange_account_id': 'cta410103',
                'expense_currency_exchange_account_id': 'cta710101',
            },
        }

    def _get_gt_account_tax(self, template_code):
        return {
            'impuestos_plantilla_iva_por_cobrar': {
                'name': 'IVA por Cobrar',
                'description': 'IVA por Cobrar',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'tax_group_iva_12',
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
            'impuestos_plantilla_iva_por_pagar': {
                'name': 'IVA por Pagar',
                'description': 'IVA por Pagar',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': True,
                'tax_group_id': 'tax_group_iva_12',
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
