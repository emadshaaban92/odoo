# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_cz_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_cz_fiscal_position(template_code),
        }

    def _get_cz_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '221',
            'cash_account_code_prefix': '211',
            'transfer_account_code_prefix': '261',
            'use_storno_accounting': True,
            'property_account_receivable_id': 'chart_cz_311000',
            'property_account_payable_id': 'chart_cz_321000',
            'property_account_expense_categ_id': 'chart_cz_504000',
            'property_account_income_categ_id': 'chart_cz_604000',
            'property_account_expense_id': 'chart_cz_504000',
            'property_account_income_id': 'chart_cz_604000',
            'property_stock_account_input_categ_id': 'chart_cz_131000',
            'property_stock_account_output_categ_id': 'chart_cz_504000',
            'property_stock_valuation_account_id': 'chart_cz_132000',
        }

    def _get_cz_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.cz',
                'income_currency_exchange_account_id': 'chart_cz_663000',
                'expense_currency_exchange_account_id': 'chart_cz_563000',
                'account_journal_suspense_account_id': 'chart_cz_261000',
                'default_cash_difference_income_account_id': 'chart_cz_668000',
                'default_cash_difference_expense_account_id': 'chart_cz_568000',
            },
        }

    def _get_cz_account_tax(self, template_code):
        return {
            'vyc_tuz_21': {
                'name': 'DPH na výstupu 21%',
                'description': '21%',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'sequence': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343221',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_21',
            },
            'vyc_tuz_15': {
                'name': 'DPH na výstupu 15%',
                'description': '15%',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'sequence': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343215',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343215',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_15',
            },
            'vyc_tuz_0': {
                'name': 'DPH na výstupu 0%',
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
            'vsc_tuz_21': {
                'name': 'DPH na vstupu 21%',
                'description': '21%',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343121',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343121',
                    }),
                ],
            },
            'vsc_tuz_15': {
                'name': 'DPH na vstupu 15%',
                'description': '15%',
                'amount': 15.0,
                'amount_type': 'percent',
                'sequence': 0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343115',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343115',
                    }),
                ],
            },
            'vyc_dod_eu': {
                'name': 'Dodání do EU',
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
            'vsc_nad_eu': {
                'name': 'Pořízení z EU',
                'description': '21%',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343121',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343121',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_cz_343221',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_21',
            },
        }

    def _get_cz_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'sequence': 1,
                'name': 'Obchody v CZ',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.cz',
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
                        'tax_src_id': 'vyc_tuz_21',
                        'tax_dest_id': 'vyc_dod_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vyc_tuz_15',
                        'tax_dest_id': 'vyc_dod_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vyc_tuz_0',
                        'tax_dest_id': 'vyc_dod_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vsc_tuz_21',
                        'tax_dest_id': 'vsc_nad_eu',
                    }),
                    Command.create({
                        'tax_src_id': 'vsc_tuz_15',
                        'tax_dest_id': 'vsc_nad_eu',
                    }),
                ],
            },
        }
