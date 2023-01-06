# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_cn_template_data(self, template_code):
        return {
            'code_digits': 6,
            'cash_account_code_prefix': '1001',
            'bank_account_code_prefix': '1002',
            'transfer_account_code_prefix': '1012',
            'use_storno_accounting': True,
            'property_account_receivable_id': 'l10n_cn_1122',
            'property_account_payable_id': 'l10n_cn_2202',
            'property_account_expense_categ_id': 'l10n_cn_6401',
            'property_account_income_categ_id': 'l10n_cn_6001',
        }

    def _get_cn_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.cn',
                'account_default_pos_receivable_account_id': 'l10n_cn_1124',
                'income_currency_exchange_account_id': 'l10n_cn_6051',
                'expense_currency_exchange_account_id': 'l10n_cn_6711',
            },
        }

    def _get_cn_account_tax(self, template_code):
        return {
            'l10n_cn_sales_included_13': {
                'name': '税收13％（含)',
                'description': '税收13％',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': True,
                'tax_group_id': 'l10n_cn_tax_group_vat_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_sales_included_9': {
                'name': '税收9％（含)',
                'description': '税收9％',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': True,
                'tax_group_id': 'l10n_cn_tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_sales_included_6': {
                'name': '税收6％（含)',
                'description': '税收6％',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': True,
                'tax_group_id': 'l10n_cn_tax_group_vat_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_sales_excluded_13': {
                'name': '税收13%',
                'description': '税收13%',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'l10n_cn_tax_group_vat_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_sales_excluded_9': {
                'name': '税收9%',
                'description': '税收9%',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'l10n_cn_tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_sales_excluded_6': {
                'name': '税收6%',
                'description': '税收6％',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'l10n_cn_tax_group_vat_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_purchase_excluded_13': {
                'name': '税收13%',
                'description': '税收13%',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'l10n_cn_tax_group_vat_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_purchase_excluded_9': {
                'name': '税收9%',
                'description': '税收9%',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'l10n_cn_tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
            'l10n_cn_purchase_excluded_6': {
                'name': '税收6%',
                'description': '税收6％',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'l10n_cn_tax_group_vat_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_cn_2221',
                    }),
                ],
            },
        }
