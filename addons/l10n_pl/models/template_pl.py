# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_pl_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_pl_fiscal_position(template_code),
        }

    def _get_pl_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'chart20000000',
            'property_account_payable_id': 'chart21000000',
            'property_account_expense_categ_id': 'chart30020000',
            'property_account_income_categ_id': 'chart73010000',
            'code_digits': '6',
            'bank_account_code_prefix': '11.000.000',
            'cash_account_code_prefix': '12.000.000',
            'transfer_account_code_prefix': '11.090.000',
            'use_storno_accounting': True,
        }

    def _get_pl_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.pl',
                'account_default_pos_receivable_account_id': 'chart20000100',
                'income_currency_exchange_account_id': 'chart75060000',
                'expense_currency_exchange_account_id': 'pl_a_pay',
            },
        }

    def _get_pl_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'vs_kraj_23': {
                'name': 'VAT-23%',
                'description': 'V23',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'sequence': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_23',
            },
            'vs_kraj_22': {
                'name': 'VAT-22%',
                'description': 'V22',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030100',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030100',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_22',
            },
            'vs_kraj_8': {
                'name': 'VAT-8%',
                'description': 'V8',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030500',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030500',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_8',
            },
            'vs_kraj_7': {
                'name': 'VAT-7%',
                'description': 'V7',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030200',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030200',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 7% lub 8%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_7',
            },
            'vs_kraj_5': {
                'name': 'VAT-5%',
                'description': 'V5',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030600',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030600',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_5',
            },
            'vs_kraj_3': {
                'name': 'VAT-3%',
                'description': 'V3',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030300',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030300',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 3% lub 5%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_3',
            },
            'vs_kraj_0': {
                'name': 'VAT-0%',
                'description': 'V0',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_kraj_zw': {
                'name': 'VAT-ZW',
                'description': 'VZW',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, zwolnione'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, zwolnione'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_kraj_usl_23': {
                'name': 'VAT usł-23%',
                'description': 'VU23',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_23',
            },
            'vs_kraj_usl_22': {
                'name': 'VAT usł-22%',
                'description': 'VU22',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030100',
                        'tag_ids': tags('+Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22030100',
                        'tag_ids': tags('-Podatek - Dostawa towarów/usług, kraj, 22% lub 23%'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_22',
            },
            'vz_kraj_23': {
                'name': 'VAT naliczony-23%',
                'description': 'Z23',
                'amount': 23.0,
                'amount_type': 'percent',
                'sequence': 0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
            },
            'vz_kraj_22': {
                'name': 'VAT naliczony-22%',
                'description': 'Z22',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020100',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020100',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
            },
            'vz_kraj_8': {
                'name': 'VAT naliczony-8%',
                'description': 'Z8',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020500',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020500',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_8',
            },
            'vz_kraj_7': {
                'name': 'VAT naliczony-7%',
                'description': 'Z7',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020200',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020200',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_7',
            },
            'vz_kraj_5': {
                'name': 'VAT naliczony-5%',
                'description': 'Z5',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020600',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020600',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_5',
            },
            'vz_kraj_3': {
                'name': 'VAT naliczony-3%',
                'description': 'Z3',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020300',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020300',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_3',
            },
            'vz_kraj_0': {
                'name': 'VAT naliczony-0%',
                'description': 'Z0',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_kraj_zw': {
                'name': 'VAT naliczony-ZW',
                'description': 'ZZW',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_kraj_usl_23': {
                'name': 'VAT usł nalicz-23%',
                'description': 'ZU23',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_23',
            },
            'vz_kraj_usl_22': {
                'name': 'VAT usł nalicz-22%',
                'description': 'ZU22',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020100',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020100',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_22',
            },
            'vp_leas_sale': {
                'name': 'VAT - leasing pojazdu(sale)',
                'description': 'VLP',
                'amount': 23.0,
                'sequence': 1,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 60,
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 40,
                        'repartition_type': 'tax',
                        'account_id': 'chart76140000',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 60,
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 40,
                        'repartition_type': 'tax',
                        'account_id': 'chart76140000',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_23',
            },
            'vp_leas_purchase': {
                'name': 'VAT - leasing pojazdu(purchase)',
                'description': 'VLP',
                'amount': 23.0,
                'sequence': 1,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 60,
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 40,
                        'repartition_type': 'tax',
                        'account_id': 'chart76140000',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 60,
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': 40,
                        'repartition_type': 'tax',
                        'account_id': 'chart76140000',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_23',
            },
            'vs_stal': {
                'name': 'Sprzedaż stali',
                'description': 'VST',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów, podatnik nabywca'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów, podatnik nabywca'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_stal': {
                'name': 'Zakup stali',
                'description': 'ZST',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych', '+Podstawa - Dostawa towarów, podatnik nabywca'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - Dostawa towarów, podatnik nabywca'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych', '-Podstawa - Dostawa towarów, podatnik nabywca'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - Dostawa towarów, podatnik nabywca'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_unia': {
                'name': 'Dost tow. unia',
                'description': 'UDT',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Wew-wspól dostawa towarów'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Wew-wspól dostawa towarów'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_unia': {
                'name': 'Nab tow unia',
                'description': 'UNT',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych', '+Podstawa - Wewn-wspól. nabycie towarów'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - Wewn-wspól. nabycie towarów'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych', '-Podstawa - Wewn-wspól. nabycie towarów'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - Wewn-wspól. nabycie towarów'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_dostu': {
                'name': 'Świad Usł',
                'description': 'UDU',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - W tym usługi art 100.1.4'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - W tym usługi art 100.1.4'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_nabu': {
                'name': 'Nab Usł',
                'description': 'UNU',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych', '+Podstawa - W tym nabycie wg art 28b'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - W tym nabycie wg art 28b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych', '-Podstawa - W tym nabycie wg art 28b'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - W tym nabycie wg art 28b'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_eksp_tow': {
                'name': 'Eksp Tow',
                'description': 'EXT',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Eksport towarów'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Eksport towarów'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_imp_tow': {
                'name': 'Imp Tow',
                'description': 'IMT',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych', '+Podstawa - Import towarów art. 33a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - Import towarów art. 33a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych', '-Podstawa - Import towarów art. 33a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - Import towarów art. 33a'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vs_ekspu': {
                'name': 'Eksp Usł',
                'description': 'EXU',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Dostawa towarów/usług, poza kraj'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Dostawa towarów/usług, poza kraj'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
            'vz_impu': {
                'name': 'Imp Usł',
                'description': 'IMU',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Podstawa - Nabycie towarów i usług pozostałych', '+Podstawa - Import usług'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('+Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('-Podatek - Import usług'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Podstawa - Nabycie towarów i usług pozostałych', '-Podstawa - Import usług'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart22020400',
                        'tag_ids': tags('-Podatek - Nabycie towarów i usług pozostałych'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart22030400',
                        'tag_ids': tags('+Podatek - Import usług'),
                    }),
                ],
                'tax_group_id': 'tax_group_vat_0',
            },
        }

    def _get_pl_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'sequence': 1,
                'name': 'Kraj',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.pl',
            },
            'fiscal_position_template_4': {
                'sequence': 2,
                'name': 'Wspólnota Prywatny',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_2': {
                'sequence': 3,
                'name': 'Wspólnota',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'vs_kraj_23',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_22',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_8',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_7',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_5',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_3',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_0',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_zw',
                        'tax_dest_id': 'vs_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_usl_23',
                        'tax_dest_id': 'vs_dostu',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_usl_22',
                        'tax_dest_id': 'vs_dostu',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_23',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_22',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_8',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_7',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_5',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_3',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_0',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_zw',
                        'tax_dest_id': 'vz_unia',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_usl_23',
                        'tax_dest_id': 'vz_nabu',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_usl_22',
                        'tax_dest_id': 'vz_nabu',
                    }),
                ],
            },
            'fiscal_position_template_3': {
                'sequence': 4,
                'name': 'Import/Eksport',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'vs_kraj_23',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_22',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_8',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_7',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_5',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_3',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_0',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_zw',
                        'tax_dest_id': 'vs_eksp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_usl_23',
                        'tax_dest_id': 'vs_ekspu',
                    }),
                    Command.create({
                        'tax_src_id': 'vs_kraj_usl_22',
                        'tax_dest_id': 'vs_ekspu',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_23',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_22',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_8',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_7',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_5',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_3',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_0',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_zw',
                        'tax_dest_id': 'vz_imp_tow',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_usl_23',
                        'tax_dest_id': 'vz_impu',
                    }),
                    Command.create({
                        'tax_src_id': 'vz_kraj_usl_22',
                        'tax_dest_id': 'vz_impu',
                    }),
                ],
            },
        }
