# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_id_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_id_11210010',
            'property_account_payable_id': 'l10n_id_21100010',
            'property_account_expense_categ_id': 'l10n_id_51000010',
            'property_account_income_categ_id': 'l10n_id_41000010',
            'property_stock_account_input_categ_id': 'l10n_id_29000000',
            'property_stock_account_output_categ_id': 'l10n_id_29000000',
            'property_stock_valuation_account_id': 'l10n_id_11300180',
            'use_anglo_saxon': 1,
            'bank_account_code_prefix': '1112',
            'cash_account_code_prefix': '1111',
            'transfer_account_code_prefix': '1999999',
            'code_digits': '8',
        }

    def _get_id_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.id',
                'account_default_pos_receivable_account_id': 'l10n_id_11210011',
                'income_currency_exchange_account_id': 'l10n_id_81100010',
                'expense_currency_exchange_account_id': 'l10n_id_91100010',
                'account_journal_early_pay_discount_loss_account_id': 'l10n_id_99900003',
                'account_journal_early_pay_discount_gain_account_id': 'l10n_id_99900004',
            },
        }

    def _get_id_account_tax(self, template_code):
        return {
            'tax_ST1': {
                'description': 'ST1',
                'type_tax_use': 'sale',
                'name': '11%',
                'amount_type': 'percent',
                'amount': 11.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.link('l10n_id.ppn_tag'),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221020',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.link('l10n_id.ppn_tag'),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221020',
                    }),
                ],
            },
            'tax_PT1': {
                'description': 'PT1',
                'type_tax_use': 'purchase',
                'name': '11%',
                'amount_type': 'percent',
                'amount': 11.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.link('l10n_id.ppn_tag'),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221010',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.link('l10n_id.ppn_tag'),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221010',
                    }),
                ],
            },
            'tax_ST0': {
                'description': 'ST0',
                'type_tax_use': 'sale',
                'name': '0%',
                'amount_type': 'percent',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221020',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221020',
                    }),
                ],
            },
            'tax_ST2': {
                'description': 'ST2',
                'type_tax_use': 'sale',
                'name': 'Exempt',
                'amount_type': 'percent',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221020',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221020',
                    }),
                ],
            },
            'tax_PT2': {
                'description': 'PT2',
                'type_tax_use': 'purchase',
                'name': 'Exempt',
                'amount_type': 'percent',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221010',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221010',
                    }),
                ],
            },
            'tax_PT0': {
                'description': 'PT0',
                'type_tax_use': 'purchase',
                'name': '0%',
                'amount_type': 'percent',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221010',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_id_21221010',
                    }),
                ],
            },
        }
