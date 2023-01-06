# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_za_template_data(self, template_code):
        return {
            'property_account_receivable_id': '110010',
            'property_account_payable_id': '220010',
            'property_account_expense_categ_id': '600010',
            'property_account_income_categ_id': '500010',
            'property_stock_account_input_categ_id': '200010',
            'property_stock_account_output_categ_id': '100050',
            'property_stock_valuation_account_id': '100020',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '1200',
            'cash_account_code_prefix': '1250',
            'transfer_account_code_prefix': '1010',
            'code_digits': '6',
        }

    def _get_za_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.za',
                'account_default_pos_receivable_account_id': '110030',
                'income_currency_exchange_account_id': '610440',
                'expense_currency_exchange_account_id': '610440',
            },
        }

    def _get_za_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'ST1': {
                'description': '15%',
                'type_tax_use': 'sale',
                'name': 'Standard Rate',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[1] Standard Rate (Excluding Capital goods and/or services and accomodation)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('+[1] Standard Rate (Excluding Capital goods and/or services and accomodation)', '+[4] x 15/ (100 + 15)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[1] Standard Rate (Excluding Capital goods and/or services and accomodation)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('-[1] Standard Rate (Excluding Capital goods and/or services and accomodation)', '-[4] x 15/ (100 + 15)'),
                    }),
                ],
            },
            'ST1A': {
                'description': '15%',
                'type_tax_use': 'sale',
                'name': 'Standard Rate (Capital Goods)',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[1A] Standard Rate (Only Capital goods and/or services)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('+[1A] Standard Rate (Only Capital goods and/or services)', '+[4A] x 15/ (100 + 15)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[1A] Standard Rate (Only Capital goods and/or services)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('-[1A] Standard Rate (Only Capital goods and/or services)', '-[4A] x 15/ (100 + 15)'),
                    }),
                ],
            },
            'ST2': {
                'description': '0%',
                'type_tax_use': 'sale',
                'name': 'Zero Rate',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[2] Zero Rate (excluding goods exported)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[2] Zero Rate (excluding goods exported)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'ST2A': {
                'description': '0%',
                'type_tax_use': 'sale',
                'name': 'Zero Rate Exports',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[2A] Zero Rate (Only goods exported)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[2A] Zero Rate (Only goods exported)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'ST3': {
                'description': '0%',
                'type_tax_use': 'sale',
                'name': 'Exempt and Non-Supplies',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[3] Exempt and Non supplies'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[3] Exempt and Non supplies'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'ST5': {
                'description': '15%',
                'type_tax_use': 'sale',
                'name': 'Accommodation (28+ days)',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[5] Accomodation exceeding 28 days'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('+VAT on Accomodation exceeding 28 days'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[5] Accomodation exceeding 28 days'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('-VAT on Accomodation exceeding 28 days'),
                    }),
                ],
            },
            'ST7': {
                'description': '15%',
                'type_tax_use': 'sale',
                'name': 'Accommodation (Under 28 days)',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[7] Accomodation under 28 days'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('+VAT on Accomodation under 28 days'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[7] Accomodation under 28 days'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('-VAT on Accomodation under 28 days'),
                    }),
                ],
            },
            'ST10': {
                'description': '15%',
                'type_tax_use': 'sale',
                'name': 'Export of Second-hand Goods/ Change in Use',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+[10] Change in use and export of second-hand goods'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('+[11] x 15 / (100 + 15)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-[10] Change in use and export of second-hand goods'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('-[11] x 15 / (100 + 15)'),
                    }),
                ],
            },
            'ST12': {
                'description': '15%',
                'type_tax_use': 'sale',
                'name': 'VAT Adjustments and Manual VAT',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('+[12] Other and imported services'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '200060',
                        'tag_ids': tags('-[12] Other and imported services'),
                    }),
                ],
            },
            'PT15': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Standard Rate',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[15] Other goods and/or services supplied to you (not Capital Goods)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[15] Other goods and/or services supplied to you (not Capital Goods)'),
                    }),
                ],
            },
            'PT14': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Standard Rate (Capital Goods)',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[14] Capital Goods and/or services supplied to you'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[14] Capital Goods and/or services supplied to you'),
                    }),
                ],
            },
            'PT14A': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Capital Goods Imported',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[14A] Capital Goods imported by you'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[14A] Capital Goods imported by you'),
                    }),
                ],
            },
            'PT15A': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Goods and Services Imported',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[15A] Other goods imported by you (not Capital Goods)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[15A] Other goods imported by you (not Capital Goods)'),
                    }),
                ],
            },
            'PT16': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Change in Use',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[16] Change in Use'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[16] Change in Use'),
                    }),
                ],
            },
            'PT17': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Bad Debts',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[17] Bad Debts'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[17] Bad Debts'),
                    }),
                ],
            },
            'PT18': {
                'description': '15%',
                'type_tax_use': 'purchase',
                'name': 'Other Adjustments',
                'amount_type': 'percent',
                'amount': 15.0,
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('+[18] Other'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '100060',
                        'tag_ids': tags('-[18] Other'),
                    }),
                ],
            },
        }
