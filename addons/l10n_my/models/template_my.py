# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_my_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_my_1240',
            'property_account_payable_id': 'l10n_my_2211',
            'property_account_income_categ_id': 'l10n_my_41',
            'property_account_expense_categ_id': 'l10n_my_51',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '1200',
            'cash_account_code_prefix': '1210',
            'transfer_account_code_prefix': '111220',
            'code_digits': '6',
        }

    def _get_my_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.my',
                'account_default_pos_receivable_account_id': 'l10n_my_1243',
                'income_currency_exchange_account_id': 'l10n_my_4240',
                'expense_currency_exchange_account_id': 'l10n_my_5240',
            },
        }

    def _get_my_account_tax(self, template_code):
        return {
            'l10n_my_tax_sale_5': {
                'name': 'SST 5%',
                'sequence': 1,
                'description': '5%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_scope': 'consu',
                'amount': 5.0,
                'price_include': False,
                'tax_group_id': 'tax_group_sst',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_my_2213',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_my_2213',
                    }),
                ],
            },
            'l10n_my_tax_sale_6': {
                'name': 'SST 6%',
                'sequence': 1,
                'description': '6%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_scope': 'service',
                'amount': 6.0,
                'price_include': False,
                'tax_group_id': 'tax_group_sst',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_my_2213',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_my_2213',
                    }),
                ],
            },
            'l10n_my_tax_sale_10': {
                'name': 'SST 10%',
                'sequence': 1,
                'description': '10%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_scope': 'consu',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_sst',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_my_2213',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_my_2213',
                    }),
                ],
            },
        }
