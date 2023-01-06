# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ke_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ke_fiscal_position(template_code),
        }

    def _get_ke_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'ke1100',
            'property_account_payable_id': 'ke2100',
            'property_account_expense_categ_id': 'ke5001',
            'property_account_income_categ_id': 'ke4001',
            'property_tax_receivable_account_id': 'ke1110',
            'property_tax_payable_account_id': 'ke2200',
            'property_stock_valuation_account_id': 'ke1001',
            'property_stock_account_output_categ_id': 'ke100120',
            'property_stock_account_input_categ_id': 'ke100110',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '12000',
            'cash_account_code_prefix': '12500',
            'transfer_account_code_prefix': '12100',
            'code_digits': '6',
        }

    def _get_ke_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ke',
                'account_default_pos_receivable_account_id': 'ke110010',
                'income_currency_exchange_account_id': 'ke5144',
                'expense_currency_exchange_account_id': 'ke5144',
                'account_journal_early_pay_discount_loss_account_id': 'ke5147',
                'account_journal_early_pay_discount_gain_account_id': 'ke400710',
                'default_cash_difference_income_account_id': 'ke5146',
                'default_cash_difference_expense_account_id': 'ke5146',
            },
        }

    def _get_ke_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'ST16': {
                'description': 'Sales VAT (16%)',
                'type_tax_use': 'sale',
                'name': 'Sales VAT (16%)',
                'amount_type': 'percent',
                'amount': 16.0,
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+16% Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke2200',
                        'tag_ids': tags('+16% Sales Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-16% Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke2200',
                        'tag_ids': tags('-16% Sales Tax'),
                    }),
                ],
            },
            'ST8': {
                'description': 'Sales VAT (8%)',
                'type_tax_use': 'sale',
                'name': 'Sales VAT (8%)',
                'amount_type': 'percent',
                'amount': 8.0,
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+8% Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke2200',
                        'tag_ids': tags('+8% Sales Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-8% Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke2200',
                        'tag_ids': tags('-8% Sales Tax'),
                    }),
                ],
            },
            'ST0': {
                'description': 'Sales VAT Zero Rated',
                'type_tax_use': 'sale',
                'name': 'Sales VAT Zero Rated (0%)',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Zero Rated Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Zero Rated Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'STEX': {
                'description': 'Sales VAT Exempt',
                'type_tax_use': 'sale',
                'name': 'Sales VAT Exempt',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Exempt Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Exempt Sales Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'SWT3': {
                'name': '3% WHT',
                'description': '3%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -3.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT5': {
                'name': '5% WHT',
                'description': '5%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -5.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT10': {
                'name': '10% WHT',
                'description': '10%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -10.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT12': {
                'name': '12% WHT',
                'description': '12%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -12.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT15': {
                'name': '15% WHT',
                'description': '15%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -15.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT20': {
                'name': '20% WHT',
                'description': '20%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -20.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT25': {
                'name': '25% WHT',
                'description': '25%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -25.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'SWT30': {
                'name': '30% WHT',
                'description': '30%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': -30.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke1120',
                    }),
                ],
            },
            'PT16': {
                'description': 'Purchases VAT (16%)',
                'type_tax_use': 'purchase',
                'name': 'Purchases VAT (16%)',
                'amount_type': 'percent',
                'amount': 16.0,
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+16% Purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke1110',
                        'tag_ids': tags('+16% Purchases Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-16% Purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke1110',
                        'tag_ids': tags('-16% Purchases Tax'),
                    }),
                ],
            },
            'PT8': {
                'description': 'Purchases VAT (8%)',
                'type_tax_use': 'purchase',
                'name': 'Purchases VAT (8%)',
                'amount_type': 'percent',
                'amount': 8.0,
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+8% purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke1110',
                        'tag_ids': tags('+8% Purchases Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-8% purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'ke1110',
                        'tag_ids': tags('-8% Purchases Tax'),
                    }),
                ],
            },
            'PT0': {
                'description': 'Purchases VAT Zero rated',
                'type_tax_use': 'purchase',
                'name': 'Purchases VAT Zero rated (0%)',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Zero Rated Purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Zero Rated Purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'PTEX': {
                'description': 'Purchase VAT Exempt',
                'type_tax_use': 'purchase',
                'name': 'Purchase VAT Exempt',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Exempt Purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Exempt Purchases Base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'PWT3': {
                'name': '3% WHT',
                'description': '3%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -3.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT5': {
                'name': '5% WHT',
                'description': '5%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -5.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT10': {
                'name': '10% WHT',
                'description': '10%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -10.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT12': {
                'name': '12% WHT',
                'description': '12%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -12.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT15': {
                'name': '15% WHT',
                'description': '15%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -15.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT20': {
                'name': '20% WHT',
                'description': '20%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -20.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT25': {
                'name': '25% WHT',
                'description': '25%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -25.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
            'PWT30': {
                'name': '30% WHT',
                'description': '30%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': -30.0,
                'tax_group_id': 'tax_group_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ke2203',
                    }),
                ],
            },
        }

    def _get_ke_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_national': {
                'sequence': 1,
                'name': 'National',
                'auto_apply': 1,
                'country_id': 'base.ke',
            },
            'fiscal_position_template_non_kenyan': {
                'sequence': 2,
                'name': 'International',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'ST16',
                        'tax_dest_id': 'ST0',
                    }),
                    Command.create({
                        'tax_src_id': 'ST8',
                        'tax_dest_id': 'ST0',
                    }),
                    Command.create({
                        'tax_src_id': 'PT16',
                        'tax_dest_id': 'PT0',
                    }),
                    Command.create({
                        'tax_src_id': 'PT8',
                        'tax_dest_id': 'PT0',
                    }),
                ],
            },
        }
