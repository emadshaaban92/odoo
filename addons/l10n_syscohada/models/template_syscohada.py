# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_syscohada_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'pcg_4111',
            'property_account_payable_id': 'pcg_4011',
            'property_account_expense_categ_id': 'pcg_6011',
            'property_account_income_categ_id': 'pcg_7011',
            'bank_account_code_prefix': '52',
            'cash_account_code_prefix': '51',
            'transfer_account_code_prefix': '588',
            'code_digits': '6',
        }

    def _get_syscohada_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_default_pos_receivable_account_id': 'pcg_4113',
                'income_currency_exchange_account_id': 'pcg_776',
                'expense_currency_exchange_account_id': 'pcg_676',
                'account_journal_early_pay_discount_loss_account_id': 'pcg_6019',
                'account_journal_early_pay_discount_gain_account_id': 'pcg_7019',
            },
        }

    def _get_syscohada_account_tax(self, template_code):
        return {
            'tva_sale_18': {
                'name': 'VAT 18% (sale)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_18',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4449',
                    }),
                ],
            },
            'tva_purchase_18': {
                'name': 'VAT 18% (purchase)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_18',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4449',
                    }),
                ],
            },
            'tva_exonere': {
                'name': 'Exempt from VAT (sale)',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_achat_exonere': {
                'name': 'Exempt from VAT (purchase)',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }
