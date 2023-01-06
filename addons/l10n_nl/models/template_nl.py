# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_nl_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_nl_fiscal_position(template_code),
        }

    def _get_nl_template_data(self, template_code):
        return {
            'code_digits': '6',
            'property_account_receivable_id': 'recv',
            'property_account_payable_id': 'pay',
            'property_account_expense_categ_id': '7001',
            'property_account_income_categ_id': '8001',
            'property_stock_account_input_categ_id': '0120',
            'property_stock_account_output_categ_id': '0129',
            'property_stock_valuation_account_id': '4830',
            'cash_account_code_prefix': '101',
            'bank_account_code_prefix': '103',
            'transfer_account_code_prefix': '1060',
            'use_anglo_saxon': True,
        }

    def _get_nl_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.nl',
                'account_default_pos_receivable_account_id': 'recv_pos',
                'income_currency_exchange_account_id': '8920',
                'expense_currency_exchange_account_id': '4920',
                'account_journal_early_pay_discount_loss_account_id': '7065',
                'account_journal_early_pay_discount_gain_account_id': '8065',
            },
        }

    def _get_nl_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'btw_0': {
                'sequence': 10,
                'name': 'Verkopen/omzet onbelast (nul-tarief)',
                'description': '0% BTW',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1e (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1e (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_6': {
                'sequence': 10,
                'name': 'Verkopen/omzet laag 6%',
                'description': '6% BTW',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l',
                        'tag_ids': tags('+1b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l',
                        'tag_ids': tags('-1b (BTW)'),
                    }),
                ],
            },
            'btw_9': {
                'sequence': 10,
                'name': 'Verkopen/omzet laag 9%',
                'description': '9% BTW',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l',
                        'tag_ids': tags('+1b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l',
                        'tag_ids': tags('-1b (BTW)'),
                    }),
                ],
            },
            'btw_21': {
                'sequence': 5,
                'name': 'Verkopen/omzet hoog',
                'description': '21% BTW',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h',
                        'tag_ids': tags('+1a (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h',
                        'tag_ids': tags('-1a (BTW)'),
                    }),
                ],
            },
            'btw_overig': {
                'sequence': 15,
                'name': 'Verkopen/omzet overig',
                'description': 'variabel BTW',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h',
                        'tag_ids': tags('+1a (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1c (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h',
                        'tag_ids': tags('-1c (BTW)'),
                    }),
                ],
            },
            'btw_0_d': {
                'sequence': 10,
                'name': 'Verkopen/omzet onbelast (nul-tarief) diensten',
                'description': '0% BTW diensten',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1e (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1e (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_6_d': {
                'sequence': 10,
                'name': 'Verkopen/omzet laag diensten 6%',
                'description': '6% BTW diensten',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d',
                        'tag_ids': tags('+1b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d',
                        'tag_ids': tags('-1b (BTW)'),
                    }),
                ],
            },
            'btw_9_d': {
                'sequence': 10,
                'name': 'Verkopen/omzet laag diensten 9%',
                'description': '9% BTW diensten',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d',
                        'tag_ids': tags('+1b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d',
                        'tag_ids': tags('-1b (BTW)'),
                    }),
                ],
            },
            'btw_21_d': {
                'sequence': 6,
                'name': 'Verkopen/omzet hoog diensten',
                'description': '21% BTW diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d',
                        'tag_ids': tags('+1a (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d',
                        'tag_ids': tags('-1a (BTW)'),
                    }),
                ],
            },
            'btw_overig_d': {
                'sequence': 15,
                'name': 'Verkopen/omzet overig diensten',
                'description': 'variabel BTW diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d',
                        'tag_ids': tags('+1a (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1c (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d',
                        'tag_ids': tags('-1c (BTW)'),
                    }),
                ],
            },
            'btw_6_buy': {
                'sequence': 10,
                'name': 'BTW te vorderen laag (inkopen) 6%',
                'description': '6% BTW',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_9_buy': {
                'sequence': 10,
                'name': 'BTW te vorderen laag (inkopen) 9%',
                'description': '9% BTW',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_6_buy_incl': {
                'sequence': 10,
                'name': 'BTW te vorderen laag (inkopen incl. BTW) 6%',
                'description': '6% BTW Incl.',
                'amount': 6.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_9_buy_incl': {
                'sequence': 10,
                'name': 'BTW te vorderen laag (inkopen incl. BTW) 9%',
                'description': '9% BTW Incl.',
                'amount': 9.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_21_buy': {
                'sequence': 5,
                'name': 'BTW te vorderen hoog (inkopen)',
                'description': '21% BTW',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_21_buy_incl': {
                'sequence': 7,
                'name': 'BTW te vorderen hoog (inkopen incl. BTW)',
                'description': '21% BTW Incl.',
                'amount': 21.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_overig_buy': {
                'sequence': 15,
                'name': 'BTW te vorderen overig (inkopen)',
                'description': 'variabel BTW',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_6_buy_d': {
                'sequence': 10,
                'name': 'BTW te vorderen laag (inkopen) diensten 6%',
                'description': '6% BTW diensten',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_9_buy_d': {
                'sequence': 10,
                'name': 'BTW te vorderen laag (inkopen) diensten 9%',
                'description': '9% BTW diensten',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_21_buy_d': {
                'sequence': 6,
                'name': 'BTW te vorderen hoog (inkopen) diensten',
                'description': '21% BTW diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_overig_buy_d': {
                'sequence': 15,
                'name': 'BTW te vorderen overig (inkopen) diensten',
                'description': 'variabel BTW diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_verk_0': {
                'sequence': 15,
                'name': 'BTW af te dragen verlegd (verkopen)',
                'description': '0% BTW verlegd',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1e (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1e (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_ink_0': {
                'sequence': 15,
                'name': 'BTW af te dragen verlegd (inkopen)',
                'description': '21% BTW verlegd',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+2a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_v',
                        'tag_ids': tags('+2a (BTW)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_v',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-2a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_v',
                        'tag_ids': tags('-2a (BTW)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_v',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
            },
            'btw_I_6': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU laag 6%',
                'description': '6% BTW import binnen EU',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_eu',
                        'tag_ids': tags('-4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_eu',
                        'tag_ids': tags('+4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_I_9': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU laag 9%',
                'description': '9% BTW import binnen EU',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_eu',
                        'tag_ids': tags('-4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_eu',
                        'tag_ids': tags('+4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_I_21': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU hoog',
                'description': '21% BTW import binnen EU',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_eu',
                        'tag_ids': tags('-4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_eu',
                        'tag_ids': tags('+4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_I_overig': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU overig',
                'description': '0% BTW import binnen EU',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_X0_producten': {
                'sequence': 20,
                'name': 'Verkopen export binnen EU (producten)',
                'description': 'BTW export binnen EU (producten)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_X0_diensten': {
                'sequence': 20,
                'name': 'Verkopen export binnen EU (diensten)',
                'description': 'BTW export binnen EU (diensten)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_X2': {
                'sequence': 20,
                'name': 'Installatie/afstandsverkopen binnen EU',
                'description': 'Inst./afst.verkopen binnen EU',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3c (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3c (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_I_6_d': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU laag diensten 6%',
                'description': '6% BTW import binnen EU diensten',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_eu',
                        'tag_ids': tags('-4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_eu',
                        'tag_ids': tags('+4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_I_9_d': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU laag diensten 9%',
                'description': '9% BTW import binnen EU diensten',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_eu',
                        'tag_ids': tags('-4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_eu',
                        'tag_ids': tags('+4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_I_21_d': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU hoog diensten',
                'description': '21% BTW import binnen EU diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d_eu',
                        'tag_ids': tags('-4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d_eu',
                        'tag_ids': tags('+4b (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_I_overig_d': {
                'sequence': 20,
                'name': 'Inkopen import binnen EU overig diensten',
                'description': '0% BTW import binnen EU diensten',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4b (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_E1': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU laag 6%',
                'description': 'BTW import buiten EU laag inkopen',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_E1_9': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU laag 9%',
                'description': 'BTW import buiten EU laag inkopen',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_E2': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU hoog',
                'description': 'BTW import buiten EU hoog inkopen',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_E_overig': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU overig',
                'description': 'BTW import buiten EU overig inkopen',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_X1': {
                'sequence': 20,
                'name': 'Verkopen export buiten EU',
                'description': 'BTW export buiten EU',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_X3': {
                'sequence': 21,
                'name': 'Installatie/afstandsverkopen buiten EU',
                'description': 'Inst./afst.verkopen buiten EU',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3a (omzet)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'btw_E1_d': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU laag diensten 6%',
                'description': 'BTW import buiten EU laag inkopen diensten',
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_E1_d_9': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU laag diensten 9%',
                'description': 'BTW import buiten EU laag inkopen diensten',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_l_d_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_l_d_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_E2_d': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU hoog diensten',
                'description': 'BTW import buiten EU hoog inkopen diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
            'btw_E_overig_d': {
                'sequence': 20,
                'name': 'Inkopen import buiten EU overig diensten',
                'description': 'BTW import buiten EU overig inkopen diensten',
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d_non_eu',
                        'tag_ids': tags('-4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d_non_eu',
                        'tag_ids': tags('+5b (BTW)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4a (omzet)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'vat_payable_h_d_non_eu',
                        'tag_ids': tags('+4a (BTW)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'vat_refund_h_d_non_eu',
                        'tag_ids': tags('-5b (BTW)'),
                    }),
                ],
            },
        }

    def _get_nl_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_national': {
                'sequence': 1,
                'name': 'Binnenland',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.nl',
            },
            'fiscal_position_template_transferred': {
                'name': 'BTW verlegd',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'btw_21_buy',
                        'tax_dest_id': 'btw_ink_0',
                    }),
                ],
            },
            'fiscal_position_template_eu_private': {
                'sequence': 2,
                'name': 'EU landen privaat',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_eu': {
                'sequence': 3,
                'name': 'EU landen',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'btw_0',
                        'tax_dest_id': 'btw_X0_producten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6',
                        'tax_dest_id': 'btw_X0_producten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9',
                        'tax_dest_id': 'btw_X0_producten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21',
                        'tax_dest_id': 'btw_X0_producten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig',
                        'tax_dest_id': 'btw_X0_producten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_0_d',
                        'tax_dest_id': 'btw_X0_diensten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6_d',
                        'tax_dest_id': 'btw_X0_diensten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9_d',
                        'tax_dest_id': 'btw_X0_diensten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_d',
                        'tax_dest_id': 'btw_X0_diensten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_d',
                        'tax_dest_id': 'btw_X0_diensten',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6_buy',
                        'tax_dest_id': 'btw_I_6',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9_buy',
                        'tax_dest_id': 'btw_I_9',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_buy',
                        'tax_dest_id': 'btw_I_21',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_buy',
                        'tax_dest_id': 'btw_I_overig',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6_buy_d',
                        'tax_dest_id': 'btw_I_6_d',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9_buy_d',
                        'tax_dest_id': 'btw_I_9_d',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_buy_d',
                        'tax_dest_id': 'btw_I_21_d',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_buy_d',
                        'tax_dest_id': 'btw_I_overig_d',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': '7001',
                        'account_dest_id': '7002',
                    }),
                    Command.create({
                        'account_src_id': '7005',
                        'account_dest_id': '7006',
                    }),
                    Command.create({
                        'account_src_id': '7009',
                        'account_dest_id': '7010',
                    }),
                    Command.create({
                        'account_src_id': '8001',
                        'account_dest_id': '8002',
                    }),
                    Command.create({
                        'account_src_id': '8011',
                        'account_dest_id': '8012',
                    }),
                    Command.create({
                        'account_src_id': '8021',
                        'account_dest_id': '8022',
                    }),
                ],
            },
            'fiscal_position_template_non_eu': {
                'sequence': 4,
                'name': 'Niet-EU landen',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'btw_0',
                        'tax_dest_id': 'btw_X1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6_buy',
                        'tax_dest_id': 'btw_E1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9_buy',
                        'tax_dest_id': 'btw_E1_9',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21',
                        'tax_dest_id': 'btw_X1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig',
                        'tax_dest_id': 'btw_X1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_0_d',
                        'tax_dest_id': 'btw_X1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6_buy_d',
                        'tax_dest_id': 'btw_E1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9_buy_d',
                        'tax_dest_id': 'btw_E1_9',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_d',
                        'tax_dest_id': 'btw_X1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_d',
                        'tax_dest_id': 'btw_X1',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_buy',
                        'tax_dest_id': 'btw_E2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_buy',
                        'tax_dest_id': 'btw_E_overig',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_buy_d',
                        'tax_dest_id': 'btw_E2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_buy_d',
                        'tax_dest_id': 'btw_E_overig_d',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': '7001',
                        'account_dest_id': '7003',
                    }),
                    Command.create({
                        'account_src_id': '7005',
                        'account_dest_id': '7007',
                    }),
                    Command.create({
                        'account_src_id': '7009',
                        'account_dest_id': '7011',
                    }),
                    Command.create({
                        'account_src_id': '8001',
                        'account_dest_id': '8003',
                    }),
                    Command.create({
                        'account_src_id': '8011',
                        'account_dest_id': '8013',
                    }),
                    Command.create({
                        'account_src_id': '8021',
                        'account_dest_id': '8023',
                    }),
                ],
            },
            'fiscal_position_template_eu_no_taxes_report': {
                'name': 'Installatie en Afstandsverkopen',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'btw_0',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_verk_0',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_0_d',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_6_d',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_9_d',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_21_d',
                        'tax_dest_id': 'btw_X2',
                    }),
                    Command.create({
                        'tax_src_id': 'btw_overig_d',
                        'tax_dest_id': 'btw_X2',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': '8001',
                        'account_dest_id': '8110',
                    }),
                    Command.create({
                        'account_src_id': '8011',
                        'account_dest_id': '8120',
                    }),
                    Command.create({
                        'account_src_id': '8021',
                        'account_dest_id': '8130',
                    }),
                ],
            },
        }
