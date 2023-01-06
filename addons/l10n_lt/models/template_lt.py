# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_lt_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_lt_fiscal_position(template_code),
        }

    def _get_lt_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'account_account_template_2410',
            'property_account_payable_id': 'account_account_template_4430',
            'property_account_expense_categ_id': 'account_account_template_6000',
            'property_account_income_categ_id': 'account_account_template_5000',
            'property_stock_account_input_categ_id': 'account_account_template_2045',
            'property_stock_account_output_categ_id': 'account_account_template_2045',
            'property_stock_valuation_account_id': 'account_account_template_2040',
            'code_digits': '1',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '271',
            'cash_account_code_prefix': '272',
            'transfer_account_code_prefix': '273',
        }

    def _get_lt_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.lt',
                'account_default_pos_receivable_account_id': 'account_account_template_2411',
                'income_currency_exchange_account_id': 'account_account_template_5803',
                'expense_currency_exchange_account_id': 'account_account_template_6803',
                'account_journal_early_pay_discount_loss_account_id': 'account_account_template_509',
                'account_journal_early_pay_discount_gain_account_id': 'account_account_template_6209',
            },
        }

    def _get_lt_account_tax(self, template_code):
        return {
            'account_tax_template_sales_0_vat5': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Sale 0% (VAT5) Tax Exempt in LT',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_sales_0_vat12': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Sale 0% (VAT12) export',
                'description': '0% VAT',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_sales_0_vat13': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Sale 0% (VAT13)',
                'description': '0% VAT',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_sales_0_vat15': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Sale 0% (VAT15) Service not in EU',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_sales_5': {
                'tax_group_id': 'tax_group_vat_5',
                'name': 'Sale 5% (VAT3)',
                'description': '5% VAT',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_sales_21': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Sale 21% (VAT1)',
                'description': '21% VAT',
                'type_tax_use': 'sale',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 1,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_sales_reversed_21': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Reversed Sale 21% (VAT25)',
                'description': '21% VAT',
                'type_tax_use': 'sale',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_purchase_0_vat5': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Purchase 0% (VAT5) Tax Exempt LT',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_0_vat14': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Purchase 0% (VAT14) export, transportation',
                'description': '0% VAT',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_0': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Purchase 0% (VAT15)',
                'description': '0% VAT',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_0_vat42': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Purchase 0% (VAT42)',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_0_vat100': {
                'tax_group_id': 'tax_group_vat_0',
                'name': 'Purchase 0% (VAT100) other cases',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_5': {
                'tax_group_id': 'tax_group_vat_5',
                'name': 'Purchase 5% (VAT3)',
                'description': '5% VAT',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_not_deductible_9': {
                'tax_group_id': 'tax_group_vat_9',
                'name': 'Purchase 9% (VAT2) not deductible',
                'description': '9% VAT',
                'type_tax_use': 'purchase',
                'amount': 9.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_63081',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_63081',
                    }),
                ],
            },
            'account_tax_template_purchase_9': {
                'tax_group_id': 'tax_group_vat_9',
                'name': 'Purchase 9% (VAT2)',
                'description': '9% VAT',
                'type_tax_use': 'purchase',
                'amount': 9.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_not_deductible_21': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Purchase 21% (VAT1) not deductible',
                'description': '21% VAT',
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 10,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_63081',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_63081',
                    }),
                ],
            },
            'account_tax_template_purchase_21': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Purchase 21% (VAT1)',
                'description': '21% VAT',
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 1,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                ],
            },
            'account_tax_template_purchase_reversed_21': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Reversed Purchase 21% (VAT25)',
                'description': '21% VAT',
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 90,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_purchase_assumed_21_vat16': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Assumed Purchase 21% (VAT16) from EU',
                'description': 'Assumed 21% VAT',
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 100,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_purchase_assumed_21_vat20': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Assumed Purchase 21% (VAT20)',
                'description': 'Assumed 21% VAT',
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 110,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
            'account_tax_template_purchase_assumed_21': {
                'tax_group_id': 'tax_group_vat_21',
                'name': 'Assumed Purchase 21% (VAT21) Goods/Services',
                'description': 'Assumed 21% VAT',
                'type_tax_use': 'purchase',
                'amount': 21.0,
                'amount_type': 'percent',
                'sequence': 120,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_2441',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_account_template_4492',
                    }),
                ],
            },
        }

    def _get_lt_fiscal_position(self, template_code):
        return {
            'account_fiscal_position_template_lt': {
                'name': 'LT',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.lt',
                'sequence': 10,
            },
            'account_fiscal_position_template_eu': {
                'name': 'EU',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'sequence': 20,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_21',
                        'tax_dest_id': 'account_tax_template_sales_0_vat13',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_purchase_21',
                        'tax_dest_id': 'account_tax_template_purchase_assumed_21',
                    }),
                ],
            },
            'account_fiscal_position_template_b2c_eu': {
                'name': 'B2C EU',
                'auto_apply': 1,
                'vat_required': 0,
                'country_group_id': 'base.europe',
                'sequence': 25,
            },
            'account_fiscal_position_template_out_eu': {
                'name': 'Not EU',
                'auto_apply': 1,
                'sequence': 30,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_21',
                        'tax_dest_id': 'account_tax_template_sales_0_vat12',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_purchase_21',
                        'tax_dest_id': 'account_tax_template_purchase_0',
                    }),
                ],
            },
        }
