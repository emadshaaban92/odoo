# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_il_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_il_fiscal_position(template_code),
        }

    def _get_il_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'il_account_101200',
            'property_account_payable_id': 'il_account_111100',
            'property_account_expense_categ_id': 'il_account_212200',
            'property_account_income_categ_id': 'il_account_200000',
            'property_stock_account_input_categ_id': 'il_account_101120',
            'property_stock_account_output_categ_id': 'il_account_101130',
            'property_stock_valuation_account_id': 'il_account_101110',
            'bank_account_code_prefix': '1014',
            'cash_account_code_prefix': '1015',
            'transfer_account_code_prefix': '1017',
            'code_digits': '6',
        }

    def _get_il_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.il',
                'account_default_pos_receivable_account_id': 'il_account_101201',
                'income_currency_exchange_account_id': 'il_account_201000',
                'expense_currency_exchange_account_id': 'il_account_202100',
            },
        }

    def _get_il_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'il_vat_sales_17': {
                'sequence': 1,
                'description': '17%',
                'name': 'VAT Sales',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+VAT SALES (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                        'tag_ids': tags('+VAT Sales'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-VAT SALES (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                        'tag_ids': tags('-VAT Sales'),
                    }),
                ],
            },
            'il_vat_pa_sales_17': {
                'sequence': 8,
                'description': '17%',
                'name': 'VAT PA Sales',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+VAT SALES (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111120',
                        'tag_ids': tags('+VAT PA Sales'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-VAT SALES (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111120',
                        'tag_ids': tags('-VAT PA Sales'),
                    }),
                ],
            },
            'il_vat_sales_exempt': {
                'sequence': 9,
                'description': '0%',
                'name': 'VAT exempt sales',
                'price_include': True,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+VAT Exempt Sales (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-VAT Exempt Sales (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                    }),
                ],
            },
            'il_vat_self_inv_purchase': {
                'sequence': 10,
                'description': '17%',
                'name': 'Self Invoice',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+VAT SALES (BASE)'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('+VAT Inputs 17%'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                        'tag_ids': tags('-VAT Sales'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-VAT SALES (BASE)'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('-VAT Inputs 17%'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                        'tag_ids': tags('+VAT Sales'),
                    }),
                ],
            },
            'il_vat_inputs_17': {
                'sequence': 2,
                'description': '17%',
                'name': 'VAT inputs',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('+VAT Inputs 17%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('-VAT Inputs 17%'),
                    }),
                ],
            },
            'il_vat_pa_purchase_16': {
                'sequence': 3,
                'description': '16%',
                'name': 'VAT 16% (PA)',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101340',
                        'tag_ids': tags('+VAT Inputs PA 16%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101340',
                        'tag_ids': tags('-VAT Inputs PA 16%'),
                    }),
                ],
            },
            'il_vat_inputs_2_3_17': {
                'sequence': 4,
                'description': '17%',
                'name': 'VAT Inputs 2/3',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 66.67,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('+VAT Inputs 2/3'),
                    }),
                    Command.create({
                        'factor_percent': 33.33,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 66.67,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('-VAT Inputs 2/3'),
                    }),
                    Command.create({
                        'factor_percent': 33.33,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'il_vat_inputs_1_4_17': {
                'sequence': 5,
                'description': '17%',
                'name': 'VAT Inputs 1/4',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 75,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('+VAT Inputs 1/4'),
                    }),
                    Command.create({
                        'factor_percent': 25,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 75,
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                        'tag_ids': tags('-VAT Inputs 1/4'),
                    }),
                    Command.create({
                        'factor_percent': 25,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'il_vat_inputs_fa_17': {
                'sequence': 6,
                'description': '17%',
                'name': 'VAT inputs for fixed assets',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101320',
                        'tag_ids': tags('+VAT INPUTS (fixed assets)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101320',
                        'tag_ids': tags('-VAT INPUTS (fixed assets)'),
                    }),
                ],
            },
            'il_vat_purchase_exempt': {
                'sequence': 7,
                'description': '0%',
                'name': 'VAT exempt purchase',
                'amount': 0.0,
                'price_include': True,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_exempt_purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                    }),
                ],
            },
            'il_vat_only_purchase': {
                'sequence': 17,
                'description': 'VAT Import Line',
                'name': 'VAT Import Line',
                'amount': 100.0,
                'amount_type': 'division',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_17',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101840',
                        'tag_ids': tags('+VAT Inputs 17%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101840',
                        'tag_ids': tags('-VAT Inputs 17%'),
                    }),
                ],
            },
            'il_vat_purchase_zero': {
                'sequence': 7,
                'description': '0%',
                'name': 'VAT Zero',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_exempt_purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_101310',
                    }),
                ],
            },
            'il_vat_sales_zero': {
                'sequence': 9,
                'description': '0%',
                'name': 'VAT Zero',
                'price_include': True,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+VAT Exempt Sales (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-VAT Exempt Sales (BASE)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'il_account_111110',
                    }),
                ],
            },
        }

    def _get_il_fiscal_position(self, template_code):
        return {
            'account_fiscal_position_israel': {
                'name': 'Israel',
                'country_id': 'base.il',
                'auto_apply': 1,
            },
            'account_fiscal_position_palestinian_authority': {
                'name': 'Palestinian Authority (PA)',
                'auto_apply': 1,
                'country_id': 'base.ps',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'il_vat_sales_17',
                        'tax_dest_id': 'il_vat_pa_sales_17',
                    }),
                    Command.create({
                        'tax_src_id': 'il_vat_inputs_17',
                        'tax_dest_id': 'il_vat_pa_purchase_16',
                    }),
                ],
            },
            'account_fiscal_position_import_export': {
                'name': 'Import / Export',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'il_vat_sales_17',
                        'tax_dest_id': 'il_vat_sales_exempt',
                    }),
                    Command.create({
                        'tax_src_id': 'il_vat_inputs_17',
                    }),
                ],
            },
            'account_fiscal_position_eilat': {
                'name': 'Eilat',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'il_vat_sales_17',
                        'tax_dest_id': 'il_vat_sales_exempt',
                    }),
                    Command.create({
                        'tax_src_id': 'il_vat_inputs_17',
                        'tax_dest_id': 'il_vat_purchase_exempt',
                    }),
                ],
            },
            'account_fiscal_position_vat_zero': {
                'name': 'Vat Zero',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'il_vat_sales_17',
                        'tax_dest_id': 'il_vat_sales_zero',
                    }),
                    Command.create({
                        'tax_src_id': 'il_vat_inputs_17',
                        'tax_dest_id': 'il_vat_purchase_zero',
                    }),
                ],
            },
            'account_fiscal_position_self_invoice': {
                'name': 'Self Invoice',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'il_vat_inputs_17',
                        'tax_dest_id': 'il_vat_self_inv_purchase',
                    }),
                ],
            },
        }
