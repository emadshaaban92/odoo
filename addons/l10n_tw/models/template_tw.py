# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_tw_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '1113',
            'cash_account_code_prefix': '1111',
            'transfer_account_code_prefix': '1114',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'tw_119100',
            'property_account_payable_id': 'tw_217100',
            'property_account_expense_categ_id': 'tw_511100',
            'property_account_income_categ_id': 'tw_411100',
            'property_stock_account_input_categ_id': 'tw_217150',
            'property_stock_account_output_categ_id': 'tw_123150',
            'property_stock_valuation_account_id': 'tw_123100',
        }

    def _get_tw_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.tw',
                'account_default_pos_receivable_account_id': 'tw_119150',
                'income_currency_exchange_account_id': 'tw_718100',
                'expense_currency_exchange_account_id': 'tw_718200',
                'account_journal_early_pay_discount_loss_account_id': 'tw_411400',
                'account_journal_early_pay_discount_gain_account_id': 'tw_512400',
                'default_cash_difference_income_account_id': 'tw_718500',
                'default_cash_difference_expense_account_id': 'tw_718600',
            },
        }

    def _get_tw_account_tax(self, template_code):
        return {
            'tw_tax_sale_5': {
                'name': 'Sale (5%)',
                'sequence': 1,
                'description': 'GST Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 5.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_220400',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_220400',
                    }),
                ],
            },
            'tw_tax_sale_inc_5': {
                'name': 'GST Inc Sale (5%)',
                'sequence': 2,
                'description': 'GST Inclusive Sale',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 5.0,
                'price_include': True,
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_220400',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_220400',
                    }),
                ],
            },
            'tw_tax_purchase_5': {
                'name': 'Purchase (5%)',
                'sequence': 1,
                'description': 'GST Purchase',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 5.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_126800',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_126800',
                    }),
                ],
            },
            'tw_tax_purchase_inc_5': {
                'name': 'GST Inc Purchase (5%)',
                'description': 'GST Inclusive Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 5.0,
                'price_include': True,
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_126800',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'tw_126800',
                    }),
                ],
            },
        }
