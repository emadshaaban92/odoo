# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ua_psbo_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'ua_psbp_361',
            'property_account_payable_id': 'ua_psbp_631',
            'property_account_expense_categ_id': 'ua_psbp_901',
            'property_account_income_categ_id': 'ua_psbp_701',
            'use_anglo_saxon': True,
            'property_stock_account_input_categ_id': 'ua_psbp_2812',
            'property_stock_account_output_categ_id': 'ua_psbp_2811',
            'property_stock_valuation_account_id': 'ua_psbp_281',
            'cash_account_code_prefix': '301',
            'bank_account_code_prefix': '311',
            'transfer_account_code_prefix': '333',
            'code_digits': '6',
            'use_storno_accounting': True,
        }

    def _get_ua_psbo_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ua',
                'account_default_pos_receivable_account_id': 'ua_psbp_366',
                'income_currency_exchange_account_id': 'ua_psbp_711',
                'expense_currency_exchange_account_id': 'ua_psbp_942',
            },
        }

    def _get_ua_psbo_account_tax(self, template_code):
        return {
            'sale_tax_template_vat20_psbo': {
                'sequence': 9,
                'name': 'Реалізація ПДВ 20%',
                'description': '+ ПДВ 20%',
                'amount': 20.0,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'tax_group_id': 'tax_group_vat20',
            },
            'sale_tax_template_vat20incl_psbo': {
                'sequence': 9,
                'name': 'Реалізація в т. ч. ПДВ 20%',
                'description': 'в т. ч. ПДВ 20%',
                'amount': 20.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'tax_group_id': 'tax_group_vat20',
            },
            'sale_tax_template_vat14_psbo': {
                'sequence': 10,
                'name': 'Реалізація ПДВ 14%',
                'description': '+ ПДВ 14%',
                'amount': 14.0,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'tax_group_id': 'tax_group_vat14',
            },
            'sale_tax_template_vat14incl_psbo': {
                'sequence': 10,
                'name': 'Реалізація в т. ч. ПДВ 14%',
                'description': 'в т. ч. ПДВ 14%',
                'amount': 14.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'tax_group_id': 'tax_group_vat14',
            },
            'sale_tax_template_vat7_psbo': {
                'sequence': 11,
                'name': 'Реалізація ПДВ 7%',
                'description': '+ ПДВ 7%',
                'amount': 7.0,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'tax_group_id': 'tax_group_vat7',
            },
            'sale_tax_template_vat7incl_psbo': {
                'sequence': 11,
                'name': 'Реалізація в т. ч. ПДВ 7%',
                'description': 'в т .ч. ПДВ 7%',
                'amount': 7.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6431',
                    }),
                ],
                'tax_group_id': 'tax_group_vat7',
            },
            'sale_tax_template_vat0_psbo': {
                'sequence': 12,
                'name': 'Реалізація ПДВ 0%',
                'description': 'ПДВ 0%',
                'amount': 0.0,
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
            },
            'sale_tax_template_vat_free_psbo': {
                'sequence': 13,
                'name': 'Реалізація звільнена від  ПДВ',
                'description': 'Звільнено від ПДВ',
                'amount': 0.0,
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
            },
            'sale_tax_template_vat_not_psbo': {
                'sequence': 14,
                'name': "Реалізація Не є об'єктом ПДВ",
                'description': "Не є об'єктом ПДВ",
                'amount': 0.0,
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
            },
            'purchase_tax_template_vat20_psbo': {
                'sequence': 19,
                'name': 'Придбання ПДВ 20%',
                'description': '+ ПДВ 20%',
                'amount': 20.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'tax_group_id': 'tax_group_vat20',
            },
            'purchase_tax_template_vat20incl_psbo': {
                'sequence': 19,
                'name': 'Придбання в т. ч. ПДВ 20%',
                'description': 'в т. ч. ПДВ 20%',
                'amount': 20.0,
                'type_tax_use': 'purchase',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'tax_group_id': 'tax_group_vat20',
            },
            'purchase_tax_template_vat14_psbo': {
                'sequence': 20,
                'name': 'Придбання ПДВ 14%',
                'description': '+ ПДВ 14%',
                'amount': 14.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'tax_group_id': 'tax_group_vat14',
            },
            'purchase_tax_template_vat14incl_psbo': {
                'sequence': 20,
                'name': 'Придбання в т. ч. ПДВ 14%',
                'description': 'в т. ч. ПДВ 14%',
                'amount': 14.0,
                'type_tax_use': 'purchase',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'tax_group_id': 'tax_group_vat14',
            },
            'purchase_tax_template_vat7_psbo': {
                'sequence': 21,
                'name': 'Придбання ПДВ 7%',
                'description': '+ ПДВ 7%',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'tax_group_id': 'tax_group_vat7',
            },
            'purchase_tax_template_vat7incl_psbo': {
                'sequence': 21,
                'name': 'Придбання в т. ч. ПДВ 7%',
                'description': 'в т. ч. ПДВ 7%',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ua_psbp_6441',
                    }),
                ],
                'tax_group_id': 'tax_group_vat7',
            },
            'purchase_tax_template_vat0_psbo': {
                'sequence': 22,
                'name': 'Придбання ПДВ 0%',
                'description': 'ПДВ 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
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
            'purchase_tax_template_vat_free_psbo': {
                'sequence': 23,
                'name': 'Придбання звільнене від  ПДВ',
                'description': 'Звільнено від ПДВ',
                'amount': 0.0,
                'type_tax_use': 'purchase',
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
            'purchase_tax_template_vat_not_psbo': {
                'sequence': 24,
                'name': "Придбання Не є об'єктом ПДВ",
                'description': "Не є об'єктом ПДВ",
                'amount': 0.0,
                'type_tax_use': 'purchase',
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
            'simple_tax_sale_product_psbo': {
                'sequence': 30,
                'name': 'Дохід від продажу  товарів',
                'description': 'Дохід від продажу товарів',
                'amount': 0.0,
                'type_tax_use': 'sale',
            },
            'simple_tax_sale_gift_psbo': {
                'sequence': 31,
                'name': 'Дохід від безоплатно отриманих  товарів',
                'description': 'Дохід від безоплатно отриманих товарів',
                'amount': 0.0,
                'type_tax_use': 'sale',
            },
            'simple_tax_sale_old_psbo': {
                'sequence': 32,
                'name': 'Дохід від заборгованності за якою минув строк позивної давності',
                'description': 'Дохід від заборгованності, за якою минув строк позивної давності',
                'amount': 0.0,
                'type_tax_use': 'sale',
            },
            'simple_tax_sale_15_psbo': {
                'sequence': 33,
                'name': 'Дохід, за ставкою 15%',
                'description': 'Дохід за ставкою 15%',
                'amount': 0.0,
                'type_tax_use': 'sale',
            },
            'simple_tax_purchase_product_psbo': {
                'sequence': 40,
                'name': 'Витрати від продажу  товарів',
                'description': 'Витрати від продажу товарів',
                'amount': 0.0,
                'type_tax_use': 'purchase',
            },
            'simple_tax_purchase_salary_psbo': {
                'sequence': 41,
                'name': 'Витрати на оплату праці',
                'description': 'Витрати на оплату праці найманих працівників',
                'amount': 0.0,
                'type_tax_use': 'purchase',
            },
            'simple_tax_purchase_esv_psbo': {
                'sequence': 42,
                'name': 'Витрати ЄСВ',
                'description': 'Витрати на ЄСВ',
                'amount': 0.0,
                'type_tax_use': 'purchase',
            },
            'simple_tax_purchase_other_psbo': {
                'sequence': 43,
                'name': 'Витрати  інші',
                'description': 'Витрати інші',
                'amount': 0.0,
                'type_tax_use': 'purchase',
            },
        }
