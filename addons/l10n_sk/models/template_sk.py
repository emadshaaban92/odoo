# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_sk_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_sk_fiscal_position(template_code),
        }

    def _get_sk_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '221',
            'cash_account_code_prefix': '211',
            'transfer_account_code_prefix': '261',
            'use_storno_accounting': True,
            'property_account_receivable_id': 'chart_sk_311000',
            'property_account_payable_id': 'chart_sk_321000',
            'property_account_expense_categ_id': 'chart_sk_504000',
            'property_account_income_categ_id': 'chart_sk_604000',
            'property_account_expense_id': 'chart_sk_504000',
            'property_account_income_id': 'chart_sk_604000',
            'property_stock_account_input_categ_id': 'chart_sk_131000',
            'property_stock_account_output_categ_id': 'chart_sk_504000',
            'property_stock_valuation_account_id': 'chart_sk_132000',
        }

    def _get_sk_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.sk',
                'income_currency_exchange_account_id': 'chart_sk_663000',
                'expense_currency_exchange_account_id': 'chart_sk_563000',
                'account_journal_suspense_account_id': 'chart_sk_261000',
                'account_journal_early_pay_discount_loss_account_id': 'chart_sk_546000',
                'account_journal_early_pay_discount_gain_account_id': 'chart_sk_646000',
                'default_cash_difference_income_account_id': 'chart_sk_668000',
                'default_cash_difference_expense_account_id': 'chart_sk_568000',
            },
        }

    def _get_sk_account_tax(self, template_code):
        return {
            'vy_tuz_20': {
                'name': 'DPH na výstupe 20%',
                'description': '20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'sequence': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343220',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343220',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_20',
            },
            'vy_tuz_10': {
                'name': 'DPH na výstupe 10%',
                'description': '10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'sequence': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343210',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343210',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_10',
            },
            'vy_tuz_0': {
                'name': 'DPH na výstupe 0%',
                'description': '0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
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
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_tuz_20': {
                'name': 'DPH na vstupe 20%',
                'description': '20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343120',
                    }),
                ],
            },
            'vs_tuz_10': {
                'name': 'DPH na vstupe 10%',
                'description': '10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343110',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343110',
                    }),
                ],
            },
            'vy_dod_eu': {
                'name': 'Dodanie do EU',
                'description': '0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
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
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_nad_eu': {
                'name': 'Nadobudnutie z EU',
                'description': '20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343120',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343220',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343120',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_sk_343220',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_20',
            },
        }

    def _get_sk_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'sequence': 1,
                'name': 'Obchody v SK',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.sk',
            },
            'fp_intra_private': {
                'sequence': 2,
                'name': 'Obchody s EU konzument',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_2': {
                'sequence': 3,
                'name': 'Obchody s EU',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'vy_tuz_20',
                        'tax_dest_id': 'vy_dod_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vy_tuz_10',
                        'tax_dest_id': 'vy_dod_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vy_tuz_0',
                        'tax_dest_id': 'vy_dod_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_tuz_20',
                        'tax_dest_id': 'vs_nad_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_tuz_10',
                        'tax_dest_id': 'vs_nad_eu',
                    }),
                ],
            },
        }
