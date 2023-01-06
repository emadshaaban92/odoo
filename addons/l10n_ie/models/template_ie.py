# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ie_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_ie_a9999',
            'property_account_payable_id': 'l10n_ie_a9998',
            'property_account_expense_categ_id': 'l10n_ie_a9995',
            'property_account_income_categ_id': 'l10n_ie_a9996',
            'use_anglo_saxon': False,
            'bank_account_code_prefix': '1200',
            'cash_account_code_prefix': '1210',
            'transfer_account_code_prefix': '1220',
            'code_digits': '6',
        }

    def _get_ie_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ie',
                'account_default_pos_receivable_account_id': 'l10n_ie_a9990',
                'income_currency_exchange_account_id': 'l10n_ie_a7700',
                'expense_currency_exchange_account_id': 'l10n_ie_a7700',
            },
        }

    def _get_ie_account_tax(self, template_code):
        return {
            'l10n_ie_tax_st0': {
                'description': 'ST0',
                'type_tax_use': 'sale',
                'name': 'Zero rated sales (IE)',
                'amount_type': 'percent',
                'amount': 0.0,
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
            'l10n_ie_tax_st1': {
                'description': 'ST1',
                'type_tax_use': 'sale',
                'name': 'Standard rate sales (13.5%) (IE)',
                'amount_type': 'percent',
                'amount': 13.5,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2200',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2200',
                    }),
                ],
            },
            'l10n_ie_tax_st2': {
                'description': 'ST2',
                'type_tax_use': 'sale',
                'name': 'Exempt sales (IE)',
                'amount_type': 'percent',
                'amount': 0.0,
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
            'l10n_ie_tax_pt0': {
                'description': 'PT0',
                'type_tax_use': 'purchase',
                'name': 'Zero rated purchases (IE)',
                'amount_type': 'percent',
                'amount': 0.0,
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
            'l10n_ie_tax_pt1': {
                'description': 'PT1',
                'type_tax_use': 'purchase',
                'name': 'Standard rate purchases (13.5%) (IE)',
                'amount_type': 'percent',
                'amount': 13.5,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
            },
            'l10n_ie_tax_pt2': {
                'description': 'PT2',
                'type_tax_use': 'purchase',
                'name': 'Exempt purchases (IE)',
                'amount_type': 'percent',
                'amount': 0.0,
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
            'l10n_ie_tax_pt8': {
                'description': 'PT8',
                'type_tax_use': 'purchase',
                'name': 'Standard rated purchases from EU (IE)',
                'amount_type': 'percent',
                'amount': 17.5,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
            },
            'l10n_ie_tax_pt9': {
                'description': 'PT9',
                'type_tax_use': 'purchase',
                'name': 'Lower rate purchases (9%) (IE)',
                'amount_type': 'percent',
                'amount': 9.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
            },
            'l10n_ie_tax_st4': {
                'description': 'ST4',
                'type_tax_use': 'sale',
                'name': 'Sales to customers in EU (IE)',
                'amount_type': 'percent',
                'amount': 0.0,
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
            'l10n_ie_tax_pt7': {
                'description': 'PT7',
                'type_tax_use': 'purchase',
                'name': 'Zero rated purchases from EU (IE)',
                'amount_type': 'percent',
                'amount': 0.0,
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
            'l10n_ie_tax_st11': {
                'description': 'ST11',
                'type_tax_use': 'sale',
                'name': 'Standard rate sales (23%) (IE)',
                'amount_type': 'percent',
                'amount': 23.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2200',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2200',
                    }),
                ],
            },
            'l10n_ie_tax_pt11': {
                'description': 'PT11',
                'type_tax_use': 'purchase',
                'name': 'Standard rate purchases (23%) (IE)',
                'amount_type': 'percent',
                'amount': 23.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
            },
            'l10n_ie_tax_st9': {
                'description': 'ST9',
                'type_tax_use': 'sale',
                'name': 'Lower rate sale (9%) (IE)',
                'amount_type': 'percent',
                'amount': 9.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2202',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2202',
                    }),
                ],
            },
            'l10n_ie_tax_pt6': {
                'description': 'PT6',
                'type_tax_use': 'purchase',
                'name': 'Lower rate purchases (4.8%) (IE)',
                'amount_type': 'percent',
                'amount': 4.8,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
            },
            'l10n_ie_tax_st6': {
                'description': 'ST6',
                'type_tax_use': 'sale',
                'name': 'Lower rate sale (4.8%) (IE)',
                'amount_type': 'percent',
                'amount': 4.8,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ie_a2201',
                    }),
                ],
            },
        }
