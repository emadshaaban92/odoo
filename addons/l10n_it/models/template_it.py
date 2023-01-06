# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_it_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_it_fiscal_position(template_code),
        }

    def _get_it_template_data(self, template_code):
        return {
            'property_account_receivable_id': '1501',
            'property_account_payable_id': '2501',
            'property_account_expense_categ_id': '4101',
            'property_account_income_categ_id': '3101',
            'property_tax_payable_account_id': '2605',
            'property_tax_receivable_account_id': '2605',
            'cash_account_code_prefix': '180',
            'bank_account_code_prefix': '182',
            'transfer_account_code_prefix': '183',
        }

    def _get_it_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.it',
                'account_default_pos_receivable_account_id': '1508',
                'income_currency_exchange_account_id': '3220',
                'expense_currency_exchange_account_id': '4920',
                'account_journal_early_pay_discount_loss_account_id': '4111',
                'account_journal_early_pay_discount_gain_account_id': '3111',
            },
        }

    def _get_it_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            '22v': {
                'description': '22%',
                'name': '22%',
                'sequence': 1,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('+4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '10v': {
                'description': '10%',
                'name': '10%',
                'sequence': 2,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('+4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '5v': {
                'description': '5%',
                'name': '5%',
                'active': False,
                'sequence': 3,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('+4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '4v': {
                'description': '4%',
                'name': '4%',
                'sequence': 4,
                'active': False,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('+4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '00v': {
                'description': '0%',
                'name': '0%',
                'sequence': 5,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
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
            '22am': {
                'description': '22%',
                'name': '22% G',
                'sequence': 6,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '10am': {
                'description': '10%',
                'name': '10% G',
                'sequence': 7,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '5am': {
                'description': '5%',
                'name': '5% G',
                'sequence': 8,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '4am': {
                'description': '4%',
                'name': '4% G',
                'sequence': 9,
                'active': False,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '00am': {
                'description': '0%',
                'name': '0% G',
                'sequence': 10,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
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
            '22as': {
                'description': '22%',
                'name': '22% S',
                'sequence': 11,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '10as': {
                'description': '10%',
                'name': '10% S',
                'sequence': 12,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '5as': {
                'description': '5%',
                'name': '5% S',
                'sequence': 13,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '4as': {
                'description': '4%',
                'name': '4% S',
                'sequence': 14,
                'active': False,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                ],
            },
            '00as': {
                'description': '0%',
                'name': '0% S',
                'sequence': 15,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
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
            '00eu': {
                'description': '0%',
                'name': '0% EU',
                'sequence': 16,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
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
            '00art15v': {
                'description': '0%',
                'name': '0% Art.15',
                'sequence': 17,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_imp_esc_art_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
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
            '00art15a': {
                'description': '00art15a',
                'name': '0% Art.15',
                'sequence': 18,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'tax_group_imp_esc_art_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
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
            '22rcs': {
                'description': '22%',
                'name': '22% S RC',
                'sequence': 19,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '10rcs': {
                'description': '10%',
                'name': '10% S RC',
                'sequence': 20,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '5rcs': {
                'description': '5%',
                'name': '5% S RC',
                'sequence': 21,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '4rcs': {
                'description': '4%',
                'name': '4% S RC',
                'sequence': 22,
                'active': False,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '00rcs': {
                'description': '0%',
                'name': '0% S RC',
                'sequence': 23,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '22rcm': {
                'description': '22%',
                'name': '22% G RC',
                'sequence': 24,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '10rcm': {
                'description': '10%',
                'name': '10% G RC',
                'sequence': 25,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '5rcm': {
                'description': '5%',
                'name': '5% G RC',
                'sequence': 26,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '4rcm': {
                'description': '4%',
                'name': '4% G RC',
                'sequence': 27,
                'active': False,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '00rcm': {
                'description': '0%',
                'name': '0% G RC',
                'sequence': 28,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj9'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '22rcd': {
                'description': '22%',
                'name': '22% G Deposit',
                'sequence': 29,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '10rcd': {
                'description': '10%',
                'name': '10% G Deposit',
                'sequence': 30,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '5rcd': {
                'description': '5%',
                'name': '5% G Deposit',
                'sequence': 31,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '4rcd': {
                'description': '4%',
                'name': '4% G Deposit',
                'sequence': 32,
                'active': False,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'price_include': False,
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
            '00rcd': {
                'description': '0%',
                'name': '0% G Deposit',
                'sequence': 33,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'price_include': False,
                'tax_group_id': 'tax_group_fuori',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03', '+vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                        'tag_ids': tags('+5v'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                        'tag_ids': tags('-4v'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03', '-vj3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '1601',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2601',
                    }),
                ],
            },
        }

    def _get_it_fiscal_position(self, template_code):
        return {
            'it': {
                'name': 'Domestic',
                'sequence': 1,
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.it',
            },
            'extra': {
                'name': 'Extra-EU',
                'sequence': 4,
                'auto_apply': 1,
            },
            'intra_private': {
                'name': 'Extra-EU (Private)',
                'sequence': 2,
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'intra': {
                'name': 'Intra-EU',
                'sequence': 3,
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': '22v',
                        'tax_dest_id': '00eu',
                    }),
                    Command.create({
                        'tax_src_id': '10v',
                        'tax_dest_id': '00eu',
                    }),
                    Command.create({
                        'tax_src_id': '5v',
                        'tax_dest_id': '00eu',
                    }),
                    Command.create({
                        'tax_src_id': '4v',
                        'tax_dest_id': '00eu',
                    }),
                    Command.create({
                        'tax_src_id': '00v',
                        'tax_dest_id': '00eu',
                    }),
                    Command.create({
                        'tax_src_id': '22am',
                        'tax_dest_id': '22rcm',
                    }),
                    Command.create({
                        'tax_src_id': '10am',
                        'tax_dest_id': '10rcm',
                    }),
                    Command.create({
                        'tax_src_id': '5am',
                        'tax_dest_id': '5rcm',
                    }),
                    Command.create({
                        'tax_src_id': '4am',
                        'tax_dest_id': '4rcm',
                    }),
                    Command.create({
                        'tax_src_id': '00am',
                        'tax_dest_id': '00rcm',
                    }),
                    Command.create({
                        'tax_src_id': '22as',
                        'tax_dest_id': '22rcs',
                    }),
                    Command.create({
                        'tax_src_id': '10as',
                        'tax_dest_id': '10rcs',
                    }),
                    Command.create({
                        'tax_src_id': '5as',
                        'tax_dest_id': '5rcs',
                    }),
                    Command.create({
                        'tax_src_id': '4as',
                        'tax_dest_id': '4rcs',
                    }),
                    Command.create({
                        'tax_src_id': '00as',
                        'tax_dest_id': '00rcs',
                    }),
                ],
            },
        }
