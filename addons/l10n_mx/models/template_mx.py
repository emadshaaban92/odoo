# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_mx_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_mx_fiscal_position(template_code),
        }

    def _get_mx_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '102.01.0',
            'cash_account_code_prefix': '101.01.0',
            'transfer_account_code_prefix': '102.01.01',
            'code_digits': '3',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'cuenta105_01',
            'property_account_payable_id': 'cuenta201_01',
            'property_account_expense_categ_id': 'cuenta601_84',
            'property_account_income_categ_id': 'cuenta401_01',
            'property_stock_account_input_categ_id': 'cuenta205_06_01',
            'property_stock_account_output_categ_id': 'cuenta107_05_01',
            'property_stock_valuation_account_id': 'cuenta115_01',
            'property_cash_basis_base_account_id': 'cuenta801_01_99',
        }

    def _get_mx_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.mx',
                'account_default_pos_receivable_account_id': 'cuenta105_02',
                'income_currency_exchange_account_id': 'cuenta702_01',
                'expense_currency_exchange_account_id': 'cuenta701_01',
                'account_journal_early_pay_discount_loss_account_id': 'cuenta9993',
                'account_journal_early_pay_discount_gain_account_id': 'cuenta9994',
            },
        }

    def _get_mx_account_tax(self, template_code):
        return {
            'tax9': {
                'sequence': 10,
                'name': 'VAT(0%) sales',
                'description': 'VAT(0%)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_0',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta209_01',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta208_01',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_iva',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta208_01',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_iva',
                            ]),
                        ],
                    }),
                ],
            },
            'tax12': {
                'sequence': 1,
                'name': 'VAT(16%) sales',
                'description': 'VAT(16%)',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_16',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta209_01',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta208_01',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_iva',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta208_01',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_iva',
                            ]),
                        ],
                    }),
                ],
            },
            'tax1': {
                'sequence': 10,
                'name': 'VAT withholding 4%',
                'description': 'VAT withholding(-4%)',
                'amount': -4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_ret_4',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta216_10',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
            },
            'tax2': {
                'sequence': 10,
                'name': 'VAT withholding lease 10%',
                'description': 'VAT withholding(-10%)',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_ret_10',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta216_10',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
            },
            'tax3': {
                'sequence': 10,
                'name': 'Withholding of lease income tax 10%',
                'description': 'Withholding income(-10%)',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_isr_ret_10',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_03',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_03',
                    }),
                ],
            },
            'tax5': {
                'sequence': 10,
                'name': 'Withholding of income tax on salaries 10%',
                'description': 'Withholding income salaries (-10%)',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_isr_ret_10',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_04',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_04',
                    }),
                ],
            },
            'tax7': {
                'sequence': 10,
                'name': 'Vat withholding tax on leasing 10.67%',
                'description': 'Vat withholding(-10.67%)',
                'amount': -10.67,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_ret_1067',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta216_10',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
            },
            'tax8': {
                'sequence': 10,
                'name': 'Vat withholding fees 10.67%',
                'description': 'Vat withholding(-10.67%)',
                'amount': -10.67,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_ret_1067',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta216_10',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_ret',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta216_10_20',
                    }),
                ],
            },
            'tax13': {
                'sequence': 10,
                'name': 'VAT(0%) purchases',
                'description': 'VAT(0%)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_0',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta119_01',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_0',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta118_01',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_0',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta118_01',
                    }),
                ],
            },
            'tax14': {
                'sequence': 1,
                'name': 'VAT(16%) purchases',
                'description': 'VAT(16%)',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_16',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta119_01',
                'l10n_mx_tax_type': 'Tasa',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_16',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta118_01',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_16',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta118_01',
                    }),
                ],
            },
            'tax16': {
                'name': 'VAT(8%) purchases',
                'description': 'VAT(8%)',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_8',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta119_01',
                'l10n_mx_tax_type': 'Tasa',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_8',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta118_01',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_diot_8',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'cuenta118_01',
                    }),
                ],
            },
            'tax17': {
                'name': 'VAT(8%) sales',
                'description': 'VAT(8%)',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_8',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'cuenta209_01',
                'l10n_mx_tax_type': 'Tasa',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_iva',
                            ]),
                        ],
                        'account_id': 'cuenta208_01',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_mx.tag_iva',
                            ]),
                        ],
                        'account_id': 'cuenta208_01',
                    }),
                ],
            },
        }

    def _get_mx_fiscal_position(self, template_code):
        return {
            'account_fiscal_position_foreign': {
                'name': 'Foreign Customer',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax14',
                        'tax_dest_id': 'tax13',
                    }),
                    Command.create({
                        'tax_src_id': 'tax12',
                        'tax_dest_id': 'tax9',
                    }),
                ],
            },
        }
