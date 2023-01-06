# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_es_common_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_es_common_fiscal_position(template_code),
        }

    def _get_es_common_template_data(self, template_code):
        return {
            'visible': 0,
            'cash_account_code_prefix': '570',
            'bank_account_code_prefix': '572',
            'transfer_account_code_prefix': '57299',
            'property_account_receivable_id': 'account_common_4300',
            'property_account_payable_id': 'account_common_4100',
            'property_account_expense_categ_id': 'account_common_600',
            'property_account_income_categ_id': 'account_common_7000',
        }

    def _get_es_common_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.es',
                'account_default_pos_receivable_account_id': 'account_common_4301',
                'income_currency_exchange_account_id': 'account_common_768',
                'expense_currency_exchange_account_id': 'account_common_668',
                'account_journal_suspense_account_id': 'account_common_572998',
                'account_journal_early_pay_discount_loss_account_id': 'account_common_6060',
                'account_journal_early_pay_discount_gain_account_id': 'account_common_7060',
                'account_journal_payment_debit_account_id': 'account_common_4312',
                'account_journal_payment_credit_account_id': 'account_common_411',
                'default_cash_difference_income_account_id': 'account_common_778',
                'default_cash_difference_expense_account_id': 'account_common_678',
            },
        }

    def _get_es_common_account_tax(self, template_code):
        return {
            'account_tax_template_s_iva21b': {
                'sequence': 0,
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 21% (Bienes)',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_07',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_iva21s': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 21% (Servicios)',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_07',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_iva21isp': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 21% (ISP)',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_07',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_bc': {
                'sequence': 0,
                'description': None,
                'type_tax_use': 'purchase',
                'name': '21% IVA soportado (bienes corrientes)',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_sc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '21% IVA soportado (servicios corrientes)',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva21_sp_in': {
                'name': 'IVA 21% Adquisición de servicios intracomunitarios',
                'description': None,
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 21.0,
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_10',
                                'l10n_es.mod_303_36',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_37',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_purchase',
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_ic_bc': {
                'description': None,
                'amount_type': 'percent',
                'amount': 21.0,
                'type_tax_use': 'purchase',
                'name': 'IVA 21% Adquisición Intracomunitaria. Bienes corrientes',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_36',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_37',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_ic_bi': {
                'name': 'IVA 21% Adquisición Intracomunitaria. Bienes de inversión',
                'description': None,
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 21.0,
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_10',
                                'l10n_es.mod_303_38',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_39',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_ibc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA 21% Importaciones bienes corrientes',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_32',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_33',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva21_ibi': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA 21% Importaciones bienes de inversión',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_34',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_35',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_irpf21td': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF (Trabajadores) dinerarios',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_03',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_03',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva4_sp_ex': {
                'amount': 4.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 4% Adquisición de servicios extracomunitarios',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_12',
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_purchase',
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva10_sp_ex': {
                'amount': 10.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 10% Adquisición de servicios extracomunitarios',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_sp_ex': {
                'name': 'IVA 21% Adquisición de servicios extracomunitarios',
                'description': None,
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva4_ic_bc': {
                'amount': 4.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 4% Adquisición Intracomunitario. Bienes corrientes',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_36',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_37',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva4_ic_bi': {
                'amount': 4.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 4% Adquisición Intracomunitario. Bienes de inversión',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_38',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_39',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva10_ic_bc': {
                'amount': 10.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 10% Adquisición Intracomunitario. Bienes corrientes',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_36',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_37',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva10_ic_bi': {
                'amount': 10.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 10% Adquisición Intracomunitario. Bienes de inversión',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_38',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_39',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_iva0_sp_i': {
                'description': 'Intracomunitario exento (Servicios)',
                'type_tax_use': 'sale',
                'name': 'IVA 0% Prestación de servicios intracomunitario',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_59',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_59',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_s_iva_ns': {
                'description': 'No sujeto (Servicios)',
                'type_tax_use': 'sale',
                'name': 'No sujeto Repercutido (Servicios)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_120',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_120',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_oss_s_iva_ns': {
                'description': 'No sujeto y acogidas a la OSS (Servicios)',
                'type_tax_use': 'sale',
                'name': 'No sujeto y acogidas a la OSS (Servicios)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_123',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_123',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_s_iva_ns_b': {
                'description': 'No sujeto (Bienes)',
                'type_tax_use': 'sale',
                'name': 'No sujeto Repercutido (Bienes)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_120',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_120',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_oss_s_iva_ns_b': {
                'description': 'No sujeto y acogidas a la OSS (Bienes)',
                'type_tax_use': 'sale',
                'name': 'No sujeto y acogidas a la OSS (Bienes)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_123',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_123',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_s_iva_e': {
                'description': 'Extracomunitario (Servicios)',
                'type_tax_use': 'sale',
                'name': 'IVA 0% Prestación de servicios extracomunitaria',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_122',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_122',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_p_iva4_ibc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA 4% Importaciones bienes corrientes',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_32',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_33',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva4_ibi': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA 4% Importaciones bienes de inversión',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_34',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_35',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva10_ibc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA 10% Importaciones bienes corrientes',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_32',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_33',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva10_ibi': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA 10% Importaciones bienes de inversión',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_34',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_35',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva4_bi': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '4% IVA Soportado (bienes de inversión)',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_30',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_31',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva4_sc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '4% IVA soportado (servicios corrientes)',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva5_sc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '5% IVA soportado',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva10_bi': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '10% IVA Soportado (bienes de inversión)',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_30',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_31',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva21_bi': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '21% IVA Soportado (bienes de inversión)',
                'amount': 21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_30',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_31',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva10_bc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '10% IVA soportado (bienes corrientes)',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva4_bc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '4% IVA soportado (bienes corrientes)',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_p_iva10_sc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '10% IVA soportado (servicios corrientes)',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_iva0': {
                'description': 'IVA Exento',
                'type_tax_use': 'sale',
                'name': 'IVA Exento Repercutido Sujeto',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                    }),
                ],
            },
            'account_tax_template_s_iva0_ns': {
                'description': 'IVA Exento No Sujeto',
                'type_tax_use': 'sale',
                'name': 'IVA Exento Repercutido No Sujeto',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
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
            'account_tax_template_s_req05': {
                'description': '0.50% Rec. Eq.',
                'type_tax_use': 'sale',
                'name': '0.50% Recargo Equivalencia Ventas',
                'amount': 0.5,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_recargo_0-5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_16',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_18',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_25',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_26',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
            },
            'account_tax_template_s_iva4b': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 4% (Bienes)',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_01',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_03',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
            },
            'account_tax_template_s_iva10b': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 10% (Bienes)',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_04',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_06',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva0_nd': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '21% IVA Soportado no deducible',
                'amount': 21.0,
                'amount_type': 'percent',
                'analytic': True,
                'tax_group_id': 'tax_group_iva_nd',
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
            'account_tax_template_p_iva10_nd': {
                'type_tax_use': 'purchase',
                'name': '10% IVA Soportado no deducible',
                'amount': 10.0,
                'amount_type': 'percent',
                'analytic': True,
                'tax_group_id': 'tax_group_iva_nd',
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
            'account_tax_template_p_iva4_nd': {
                'type_tax_use': 'purchase',
                'name': '4% IVA Soportado no deducible',
                'amount': 4.0,
                'amount_type': 'percent',
                'analytic': True,
                'tax_group_id': 'tax_group_iva_nd',
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
            'account_tax_template_s_iva4s': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 4% (Servicios)',
                'amount': 4.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_01',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_03',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
            },
            'account_tax_template_s_iva5s': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_01',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_03',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                        'account_id': 'account_common_477',
                    }),
                ],
            },
            'account_tax_template_s_iva10s': {
                'description': None,
                'type_tax_use': 'sale',
                'name': 'IVA 10% (Servicios)',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_04',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_06',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_14_sale',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_req014': {
                'description': '1.4% Rec. Eq.',
                'type_tax_use': 'sale',
                'name': '1.4% Recargo Equivalencia Ventas',
                'amount': 1.4,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_recargo_1-4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_19',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_21',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_25',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_26',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_req52': {
                'description': '5.2% Rec. Eq.',
                'type_tax_use': 'sale',
                'name': '5.2% Recargo Equivalencia Ventas',
                'amount': 5.2,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_recargo_5-2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_22',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_24',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_25',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_26',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva0_bc': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA Soportado exento (operaciones corrientes)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
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
            'account_tax_template_p_iva0_ns': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA Soportado no sujeto (Servicios)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
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
            'account_tax_template_p_iva0_ns_b': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'IVA Soportado no sujeto (Bienes)',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
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
            'account_tax_template_s_irpf9': {
                'description': 'Retención 9%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 9%',
                'amount': -9.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf18': {
                'description': 'Retención 18%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 18%',
                'amount': -18.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_18',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf19': {
                'description': 'Retención 19%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 19%',
                'amount': -19.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf19a': {
                'description': 'Retención 19% (Arrend.)',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta 19% (Arrendamientos)',
                'amount': -19.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf195a': {
                'description': 'Retención 19,5% (Arrend.)',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta 19,5% (Arrendamientos)',
                'amount': -19.5,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19-5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_p_irpf19': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 19%',
                'amount': -19.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf20a': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones 20% (Arrendamientos)',
                'amount': -20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf18': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 18%',
                'amount': -18.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_18',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf19a': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones 19% (Arrendamientos)',
                'amount': -19.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf195a': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones 19,5% (Arrendamientos)',
                'amount': -19.5,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19-5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf7': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 7%',
                'amount': -7.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf9': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 9%',
                'amount': -9.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf24': {
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 24%',
                'amount': -24.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_24',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_irpf20': {
                'description': 'Retención 20%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 20%',
                'amount': -20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf20a': {
                'description': 'Retención 20% (Arrend.)',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta 20% (Arrendamientos)',
                'amount': -20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf24': {
                'description': 'Retención 24%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 24%',
                'amount': -24.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_24',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_p_iva12_agr': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '12% IVA Soportado régimen agricultura',
                'amount': 12.0,
                'amount_type': 'percent',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_42',
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
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_42',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva105_gan': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '10,5% IVA Soportado régimen ganadero o pesca',
                'amount': 10.5,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_10-5',
                'include_base_amount': 1,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_42',
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
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_42',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_iva0_e': {
                'description': 'Exportación (Bienes)',
                'type_tax_use': 'sale',
                'name': 'IVA 0% Exportaciones',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_60',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_60',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_s_iva0_ic': {
                'description': 'Intracomunitario exento (Bienes)',
                'type_tax_use': 'sale',
                'name': 'IVA 0% Entregas Intracomunitarias exentas',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_59',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_59',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_p_req014': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '1.4% Recargo Equivalencia Compras',
                'amount': 1.4,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_recargo_1-4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_req05': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '0.50% Recargo Equivalencia Compras',
                'amount': 0.5,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_recargo_0-5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_req52': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': '5.2% Recargo Equivalencia Compras',
                'amount': 5.2,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_recargo_5-2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_irpf1': {
                'description': 'Retención 1%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 1%',
                'amount': -1.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf2': {
                'description': 'Retención 2%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 2%',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf21': {
                'description': 'Retención 21%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 21%',
                'amount': -21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf21a': {
                'description': 'Retención  21% (Arrend.)',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta 21% (Arrendamientos)',
                'amount': -21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf7': {
                'description': 'Retención 7%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 7%',
                'amount': -7.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_s_irpf15': {
                'description': 'Retención 15%',
                'type_tax_use': 'sale',
                'name': 'Retenciones a cuenta IRPF 15%',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_473',
                    }),
                ],
            },
            'account_tax_template_p_irpf1': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 1%',
                'amount': -1.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf15': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 15%',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf21t': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF (Trabajadores)',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_03',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_03',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva10_sp_in': {
                'amount': 10.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 10% Adquisición de servicios intracomunitarios',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_36',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_37',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva4_sp_in': {
                'amount': 4.0,
                'description': None,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'name': 'IVA 4% Adquisición de servicios intracomunitarios',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_36',
                                'l10n_es.mod_303_10',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_37',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                        'account_id': 'account_common_472',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf21te': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF (Trabajadores) en especie',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_05',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_06',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_05',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_06',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf15e': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 15% en especie',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_11',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_12',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_11',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_12',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf7e': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 7% en especie',
                'amount': -7.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_11',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_12',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_11',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_12',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf20': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 20%',
                'amount': -20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf21a': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones 21% (Arrendamientos)',
                'amount': -21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_02',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_115_03',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf21p': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 21%',
                'amount': -21.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_irpf2': {
                'description': None,
                'type_tax_use': 'purchase',
                'name': 'Retenciones IRPF 2%',
                'amount': -2.0,
                'sequence': 2,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_08',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_111_09',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_s_iva0_isp': {
                'description': 'IVA 0% ISP',
                'name': 'IVA 0% Venta con Inversión del Sujeto Pasivo',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_122',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_122',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_template_p_iva4_isp': {
                'description': None,
                'name': 'IVA 4% Compra con Inversión del Sujeto Pasivo Nacional',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 4.0,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva10_isp': {
                'description': None,
                'name': 'IVA 10% Compra con Inversión del Sujeto Pasivo Nacional',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_isp': {
                'description': None,
                'name': 'IVA 21% Compra con Inversión del Sujeto Pasivo Nacional',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 21.0,
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_28',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_29',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva4_isp_bi': {
                'name': 'IVA 4% ISP (bienes de inversión)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 4.0,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_30',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_31',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva10_isp_bi': {
                'name': 'IVA 10% ISP (bienes de inversión)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_30',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_31',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_iva21_isp_bi': {
                'name': 'IVA 21% ISP (bienes de inversión)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 21.0,
                'tax_group_id': 'tax_group_iva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_30',
                                'l10n_es.mod_303_12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_31',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_40',
                                'l10n_es.mod_303_14_purchase',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_472',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_41',
                            ]),
                        ],
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_common_477',
                        'tag_ids': [
                            Command.set([
                                'l10n_es.mod_303_15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_template_p_rp19': {
                'type_tax_use': 'purchase',
                'description': None,
                'name': 'Retenciones 19% (préstamos)',
                'amount': -19.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                    }),
                ],
            },
            'account_tax_template_p_rrD19': {
                'type_tax_use': 'purchase',
                'description': None,
                'name': 'Retenciones 19% (reparto de dividendos)',
                'amount': -19.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_retenciones_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_common_4751',
                    }),
                ],
            },
        }

    def _get_es_common_fiscal_position(self, template_code):
        return {
            'fp_nacional': {
                'sequence': 1,
                'name': 'Régimen Nacional',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.es',
            },
            'fp_intra_private': {
                'sequence': 2,
                'name': 'EU privado',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fp_intra': {
                'sequence': 3,
                'name': 'Régimen Intracomunitario',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_ic_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sp_in',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_iva4_ic_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_ic_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sp_in',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_iva10_ic_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_ic_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sp_in',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_iva21_ic_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva0_ic',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva0_sp_i',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva0_ic',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva0_sp_i',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva0_ic',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva0_sp_i',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva0_ic',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_common_7000',
                        'account_dest_id': 'account_common_7001',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7010',
                        'account_dest_id': 'account_common_7011',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7020',
                        'account_dest_id': 'account_common_7021',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7030',
                        'account_dest_id': 'account_common_7031',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7040',
                        'account_dest_id': 'account_common_7041',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7050',
                        'account_dest_id': 'account_common_7051',
                    }),
                ],
            },
            'fp_extra': {
                'sequence': 4,
                'name': 'Régimen Extracomunitario',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_ibc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sp_ex',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_iva4_ibi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_ibc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sp_ex',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_iva10_ibi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_ibc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sp_ex',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_iva21_ibi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva0_e',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva_e',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva0_e',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva_e',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva0_e',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva_e',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva0_e',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_common_7000',
                        'account_dest_id': 'account_common_7002',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7010',
                        'account_dest_id': 'account_common_7012',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7020',
                        'account_dest_id': 'account_common_7022',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7030',
                        'account_dest_id': 'account_common_7032',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7040',
                        'account_dest_id': 'account_common_7042',
                    }),
                    Command.create({
                        'account_src_id': 'account_common_7050',
                        'account_dest_id': 'account_common_7052',
                    }),
                ],
            },
            'fp_not_subject_tai': {
                'name': 'Régimen No sujeto por reglas de localización (TAI - Canarias, Ceuta, Melilla...)',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva_ns_b',
                    }),
                ],
            },
            'fp_recargo': {
                'name': 'Recargo de Equivalencia',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_iva4_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_iva10_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_iva21_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_req52',
                    }),
                ],
            },
            'fp_recargo_isp': {
                'name': 'Recargo de Equivalencia Revendedor con ISP',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_iva4_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_req05',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_iva10_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_req014',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_req52',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_iva21_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_req52',
                    }),
                ],
            },
            'fp_irpf1': {
                'name': 'Retención IRPF 1%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf1',
                    }),
                ],
            },
            'fp_irpf2': {
                'name': 'Retención IRPF 2%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                ],
            },
            'fp_irpf7': {
                'name': 'Retención IRPF 7%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf7',
                    }),
                ],
            },
            'fp_irpf9': {
                'name': 'Retención IRPF 9%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf9',
                    }),
                ],
            },
            'fp_irpf15': {
                'name': 'Retención IRPF 15%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf15',
                    }),
                ],
            },
            'fp_irpf18': {
                'name': 'Retención IRPF 18%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf18',
                    }),
                ],
            },
            'fp_irpf19': {
                'name': 'Retención IRPF 19%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf19',
                    }),
                ],
            },
            'fp_irpf19a': {
                'name': 'Retención 19% arrendamientos',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf19a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf19a',
                    }),
                ],
            },
            'fp_irpf195a': {
                'name': 'Retención 19,5% arrendamientos',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf195a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf195a',
                    }),
                ],
            },
            'fp_irpf20': {
                'name': 'Retención IRPF 20%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf20',
                    }),
                ],
            },
            'fp_irpf24': {
                'name': 'Retención IRPF 24%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf24',
                    }),
                ],
            },
            'fp_irpf20a': {
                'name': 'Retención 20% arrendamientos',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf20a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf20a',
                    }),
                ],
            },
            'fp_irpf21': {
                'name': 'Retención IRPF 21%',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0_ns',
                        'tax_dest_id': 'account_tax_template_s_irpf21',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns_b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns_b',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_iva0_ns',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_ns',
                        'tax_dest_id': 'account_tax_template_p_irpf21p',
                    }),
                ],
            },
            'fp_irpf21a': {
                'name': 'Retención 21% arrendamientos',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva21b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva21isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva21s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva10b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva10s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva4b',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva4s',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_sc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_iva0',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva0',
                        'tax_dest_id': 'account_tax_template_s_irpf21a',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_iva0_bc',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva0_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf21a',
                    }),
                ],
            },
            'fp_ispn': {
                'name': 'Inversion del Sujeto Pasivo Nacional',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva4_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_sc',
                        'tax_dest_id': 'account_tax_template_p_iva4_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bi',
                        'tax_dest_id': 'account_tax_template_p_iva4_isp_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bc',
                        'tax_dest_id': 'account_tax_template_p_iva10_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_sc',
                        'tax_dest_id': 'account_tax_template_p_iva10_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva10_bi',
                        'tax_dest_id': 'account_tax_template_p_iva10_isp_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bc',
                        'tax_dest_id': 'account_tax_template_p_iva21_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_sc',
                        'tax_dest_id': 'account_tax_template_p_iva21_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva21_bi',
                        'tax_dest_id': 'account_tax_template_p_iva21_isp_bi',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4b',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva4s',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10b',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva10s',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21b',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21s',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                ],
            },
            'fp_rnrisp': {
                'name': 'Régimen Nacional Revendedor con Inversión del sujeto pasivo',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_s_iva21isp',
                        'tax_dest_id': 'account_tax_template_s_iva0_isp',
                    }),
                ],
            },
            'fp_reagyp_a': {
                'name': 'REAGYP - Agricultura',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva12_agr',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                ],
            },
            'fp_reagyp_gp': {
                'name': 'REAGYP - Ganadería y pesca',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_iva105_gan',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_p_iva4_bc',
                        'tax_dest_id': 'account_tax_template_p_irpf2',
                    }),
                ],
            },
        }
