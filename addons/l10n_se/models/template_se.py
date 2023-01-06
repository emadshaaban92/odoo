# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_se_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_se_fiscal_position(template_code),
        }

    def _get_se_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'a1510',
            'property_account_payable_id': 'a2440',
            'property_account_expense_categ_id': 'a4000',
            'property_account_income_categ_id': 'a3001',
            'property_stock_account_input_categ_id': 'a4960',
            'property_stock_account_output_categ_id': 'a4960',
            'property_stock_valuation_account_id': 'a1410',
            'bank_account_code_prefix': '193',
            'cash_account_code_prefix': '191',
            'transfer_account_code_prefix': '194',
            'code_digits': '4',
        }

    def _get_se_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.se',
                'account_default_pos_receivable_account_id': 'a1910',
                'income_currency_exchange_account_id': 'a3960',
                'expense_currency_exchange_account_id': 'a3960',
                'account_journal_early_pay_discount_loss_account_id': 'a9993',
                'account_journal_early_pay_discount_gain_account_id': 'a9994',
            },
        }

    def _get_se_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'sale_tax_25_goods': {
                'name': 'Utgående moms 25%',
                'description': 'ST25',
                'amount': 25.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2611',
                        'tag_ids': tags('+se_10'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2611',
                        'tag_ids': tags('-se_10'),
                    }),
                ],
            },
            'sale_tax_25_services': {
                'name': 'Utgående moms Tjänst 25%',
                'description': 'ST25',
                'amount': 25.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2611',
                        'tag_ids': tags('+se_10'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2611',
                        'tag_ids': tags('-se_10'),
                    }),
                ],
            },
            'purchase_tax_25_goods': {
                'name': 'Ingående moms 25%',
                'description': 'PT25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('-se_48'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('+se_48'),
                    }),
                ],
            },
            'purchase_tax_25_services': {
                'name': 'Ingående moms Tjänst 25%',
                'description': 'PT25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('-se_48'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('+se_48'),
                    }),
                ],
            },
            'sale_tax_12_goods': {
                'name': 'Utgående moms 12%',
                'description': 'ST12',
                'amount': 12.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2621',
                        'tag_ids': tags('+se_11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2621',
                        'tag_ids': tags('-se_11'),
                    }),
                ],
            },
            'sale_tax_12_services': {
                'name': 'Utgående moms Tjänst 12%',
                'description': 'ST12',
                'amount': 12.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2621',
                        'tag_ids': tags('+se_11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2621',
                        'tag_ids': tags('-se_11'),
                    }),
                ],
            },
            'purchase_tax_12_goods': {
                'name': 'Ingående moms 12%',
                'description': 'PT12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('-se_48'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('+se_48'),
                    }),
                ],
            },
            'purchase_tax_12_services': {
                'name': 'Ingående moms Tjänst 12%',
                'description': 'PT12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('-se_48'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('+se_48'),
                    }),
                ],
            },
            'sale_tax_6_goods': {
                'name': 'Utgående moms 6%',
                'description': 'ST6',
                'amount': 6.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2631',
                        'tag_ids': tags('+se_12'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2631',
                        'tag_ids': tags('-se_12'),
                    }),
                ],
            },
            'sale_tax_6_services': {
                'name': 'Utgående moms Tjänst 6%',
                'description': 'ST6',
                'amount': 6.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2631',
                        'tag_ids': tags('+se_12'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_05'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2631',
                        'tag_ids': tags('-se_12'),
                    }),
                ],
            },
            'purchase_tax_6_goods': {
                'name': 'Ingående moms 6%',
                'description': 'PT6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('-se_48'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('+se_48'),
                    }),
                ],
            },
            'purchase_tax_6_services': {
                'name': 'Ingående moms Tjänst 6%',
                'description': 'PT6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('-se_48'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2641',
                        'tag_ids': tags('+se_48'),
                    }),
                ],
            },
            'sale_tax_services_EC': {
                'name': 'Momsfri försäljning av tjänst EU',
                'description': 'SE0',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_39'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_39'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sale_tax_goods_EC': {
                'name': 'Momsfri Försäljning av varor EU',
                'description': 'SE0',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_35'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_35'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'purchase_goods_tax_25_EC': {
                'name': 'Inköp av varor EU moms 25%',
                'description': 'PE25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_20'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_30', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_20'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_30', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
            },
            'purchase_goods_tax_12_EC': {
                'name': 'Inköp av varor EU moms 12%',
                'description': 'PE12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_20'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_31', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_20'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_31', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
            },
            'purchase_goods_tax_6_EC': {
                'name': 'Inköp av varor EU moms 6%',
                'description': 'PE6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_20'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_32', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_20'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_32', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
            },
            'purchase_services_tax_25_EC': {
                'name': 'Inköp av tjänst EU moms 25%',
                'description': 'PE25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_30', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_30', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
            },
            'purchase_services_tax_12_EC': {
                'name': 'Inköp av tjänst EU moms 12%',
                'description': 'PE12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_31', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_31', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
            },
            'purchase_services_tax_6_EC': {
                'name': 'Inköp av tjänst EU moms 6%',
                'description': 'PE6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_32', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_32', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
            },
            'purchase_construction_services_tax_25_EC': {
                'name': 'Inköpta tjänster i Sverige, omvändskattskyldighet, 25 %',
                'description': 'PCS25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_24'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2647',
                        'tag_ids': tags('+se_30', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_24'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2647',
                        'tag_ids': tags('-se_30', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
            },
            'purchase_construction_services_tax_12_EC': {
                'name': 'Inköpta tjänster i Sverige, omvändskattskyldighet, 12 %',
                'description': 'PCS12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_24'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a4426',
                        'tag_ids': tags('+se_31', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_24'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a4426',
                        'tag_ids': tags('-se_31', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
            },
            'purchase_construction_services_tax_6_EC': {
                'name': 'Inköpta tjänster i Sverige, omvändskattskyldighet, 6 %',
                'description': 'PCS6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_24'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a4427',
                        'tag_ids': tags('+se_32', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_24'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a4427',
                        'tag_ids': tags('-se_32', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
            },
            'sale_tax_services_NEC': {
                'name': 'Momsfri försäljning av tjänst utanför EU',
                'description': 'SE0',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_39'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_39'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sale_tax_goods_NEC': {
                'name': 'Momsfri försäljning av varor utanför EU',
                'description': 'SE0',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_36'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_36'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'purchase_goods_tax_25_NEC': {
                'name': 'Beskattningsunderlag vid import 25%',
                'description': 'PN25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_50'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_60'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2615',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_50'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_60'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2615',
                    }),
                ],
            },
            'purchase_goods_tax_12_NEC': {
                'name': 'Beskattningsunderlag vid import 12%',
                'description': 'PN12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_50'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_61'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2625',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_50'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_61'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2625',
                    }),
                ],
            },
            'purchase_goods_tax_6_NEC': {
                'name': 'Beskattningsunderlag vid import 6%',
                'description': 'PN6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_50'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2635',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_50'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2635',
                    }),
                ],
            },
            'purchase_services_tax_25_NEC': {
                'name': 'Inköp av tjänster utanför EU 25%',
                'description': 'PN25',
                'amount': 25.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_22'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_30', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_22'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_30', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2614',
                    }),
                ],
            },
            'purchase_services_tax_12_NEC': {
                'name': 'Inköp av tjänster utanför EU 12%',
                'description': 'PN12',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_22'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_31', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_22'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_31', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2624',
                    }),
                ],
            },
            'purchase_services_tax_6_NEC': {
                'name': 'Inköp av tjänster utanför EU 6%',
                'description': 'PN6',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_22'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('+se_32', '-se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_22'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                        'tag_ids': tags('-se_32', '+se_48'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2634',
                    }),
                ],
            },
            'triangular_tax_25_goods': {
                'name': 'Trepartshandel - moms 25%',
                'description': 'T25',
                'amount': 25.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_37', '-se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2615',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_37', '+se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2615',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                    }),
                ],
            },
            'triangular_tax_12_goods': {
                'name': 'Trepartshandel - moms 12%',
                'description': 'T12',
                'amount': 12.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_37', '-se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2625',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_37', '+se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2625',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                    }),
                ],
            },
            'triangular_tax_6_goods': {
                'name': 'Trepartshandel - moms 6%',
                'description': 'T6',
                'amount': 6.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_37', '-se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2635',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_37', '+se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a2635',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a2645',
                    }),
                ],
            },
            'triangular_tax_0_goods': {
                'name': 'Trepartshandel - momsfrei',
                'description': 'T0',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+se_37', '-se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-se_37', '+se_38'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_se_fiscal_position(self, template_code):
        return {
            'fp_sweden': {
                'name': 'Sverige',
                'auto_apply': 1,
                'country_id': 'base.se',
                'vat_required': 1,
                'sequence': 10,
            },
            'fp_euro_b2c': {
                'name': 'Europaunionen (B2C)',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
                'sequence': 11,
            },
            'fp_euro_b2b': {
                'name': 'Europaunionen (B2B)',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'sequence': 12,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'purchase_tax_25_services',
                        'tax_dest_id': 'purchase_services_tax_25_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_25_goods',
                        'tax_dest_id': 'purchase_goods_tax_25_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_12_services',
                        'tax_dest_id': 'purchase_services_tax_12_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_12_goods',
                        'tax_dest_id': 'purchase_goods_tax_12_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_6_services',
                        'tax_dest_id': 'purchase_services_tax_6_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_6_goods',
                        'tax_dest_id': 'purchase_goods_tax_6_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_25_services',
                        'tax_dest_id': 'sale_tax_services_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_25_goods',
                        'tax_dest_id': 'sale_tax_goods_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_12_services',
                        'tax_dest_id': 'sale_tax_services_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_12_goods',
                        'tax_dest_id': 'sale_tax_goods_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_6_services',
                        'tax_dest_id': 'sale_tax_services_EC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_6_goods',
                        'tax_dest_id': 'sale_tax_goods_EC',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'a3001',
                        'account_dest_id': 'a3106',
                    }),
                    Command.create({
                        'account_src_id': 'a3002',
                        'account_dest_id': 'a3106',
                    }),
                    Command.create({
                        'account_src_id': 'a3003',
                        'account_dest_id': 'a3106',
                    }),
                    Command.create({
                        'account_src_id': 'a3004',
                        'account_dest_id': 'a3106',
                    }),
                    Command.create({
                        'account_src_id': 'a3001',
                        'account_dest_id': 'a3308',
                    }),
                    Command.create({
                        'account_src_id': 'a3002',
                        'account_dest_id': 'a3308',
                    }),
                    Command.create({
                        'account_src_id': 'a3003',
                        'account_dest_id': 'a3308',
                    }),
                    Command.create({
                        'account_src_id': 'a3004',
                        'account_dest_id': 'a3308',
                    }),
                ],
            },
            'fp_outside_euro': {
                'name': 'Utanför Europaunionen',
                'auto_apply': 1,
                'sequence': 13,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'purchase_tax_25_services',
                        'tax_dest_id': 'purchase_services_tax_25_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_25_goods',
                        'tax_dest_id': 'purchase_goods_tax_25_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_12_services',
                        'tax_dest_id': 'purchase_services_tax_12_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_12_goods',
                        'tax_dest_id': 'purchase_goods_tax_12_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_6_services',
                        'tax_dest_id': 'purchase_services_tax_6_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'purchase_tax_6_goods',
                        'tax_dest_id': 'purchase_goods_tax_6_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_25_services',
                        'tax_dest_id': 'sale_tax_services_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_25_goods',
                        'tax_dest_id': 'sale_tax_goods_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_12_services',
                        'tax_dest_id': 'sale_tax_services_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_12_goods',
                        'tax_dest_id': 'sale_tax_goods_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_6_services',
                        'tax_dest_id': 'sale_tax_services_NEC',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_6_goods',
                        'tax_dest_id': 'sale_tax_goods_NEC',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'a3001',
                        'account_dest_id': 'a3105',
                    }),
                    Command.create({
                        'account_src_id': 'a3002',
                        'account_dest_id': 'a3105',
                    }),
                    Command.create({
                        'account_src_id': 'a3003',
                        'account_dest_id': 'a3105',
                    }),
                    Command.create({
                        'account_src_id': 'a3004',
                        'account_dest_id': 'a3105',
                    }),
                    Command.create({
                        'account_src_id': 'a3001',
                        'account_dest_id': 'a3305',
                    }),
                    Command.create({
                        'account_src_id': 'a3002',
                        'account_dest_id': 'a3305',
                    }),
                    Command.create({
                        'account_src_id': 'a3003',
                        'account_dest_id': 'a3305',
                    }),
                    Command.create({
                        'account_src_id': 'a3004',
                        'account_dest_id': 'a3305',
                    }),
                ],
            },
        }
