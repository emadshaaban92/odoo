# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_si_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_si_fiscal_position(template_code),
        }

    def _get_si_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'gd_acc_120000',
            'property_account_payable_id': 'gd_acc_220000',
            'property_account_expense_categ_id': 'gd_acc_702000',
            'property_account_income_categ_id': 'gd_acc_762000',
            'bank_account_code_prefix': '110',
            'cash_account_code_prefix': '100',
            'transfer_account_code_prefix': '109',
            'code_digits': '6',
            'use_storno_accounting': True,
        }

    def _get_si_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.si',
                'account_default_pos_receivable_account_id': 'gd_acc_125000',
                'income_currency_exchange_account_id': 'gd_acc_777000',
                'expense_currency_exchange_account_id': 'gd_acc_484000',
            },
        }

    def _get_si_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'gd_taxr_3': {
                'sequence': 10,
                'name': '22% VAT',
                'description': 'VAT charged at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-21'),
                    }),
                ],
            },
            'gd_taxr_2': {
                'sequence': 20,
                'name': '9,5% VAT',
                'description': 'VAT charged at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-22'),
                    }),
                ],
            },
            'l10n_si_vat_5_sale': {
                'sequence': 30,
                'name': '5% VAT',
                'description': 'VAT charged at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+22a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-22a'),
                    }),
                ],
            },
            'l10n_si_vat_recipient_22_sale': {
                'sequence': 40,
                'name': '22% VAT recipient',
                'description': 'VAT charged by the recipient at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_si_vat_recipient_9_sale': {
                'sequence': 50,
                'name': '9,5% VAT recipient',
                'description': 'VAT charged by the recipient at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_si_vat_recipient_5_sale': {
                'sequence': 60,
                'name': '5% VAT recipient',
                'description': 'VAT charged by the recipient at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'gd_taxr_1': {
                'sequence': 70,
                'name': '0% VAT EU',
                'description': 'VAT charged from acquisitions of goods and services from other EU Member States at a rate of 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_si_vat_22_sale_distance': {
                'sequence': 80,
                'name': '22% VAT distance',
                'description': 'Distance selling goods at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-23'),
                    }),
                ],
            },
            'l10n_si_vat_9_sale_distance': {
                'sequence': 90,
                'name': '9,5% VAT distance',
                'description': 'Distance selling goods at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+24'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-24'),
                    }),
                ],
            },
            'l10n_si_vat_5_sale_distance': {
                'sequence': 100,
                'name': '5% VAT distance',
                'description': 'Distance selling goods at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+24b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-24b'),
                    }),
                ],
            },
            'l10n_si_vat_22_sale_installation_eu': {
                'sequence': 110,
                'name': '22% VAT EU installation',
                'description': 'VAT charged from assembly and installation of goods in other EU Member States at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-23'),
                    }),
                ],
            },
            'l10n_si_vat_9_sale_installation_eu': {
                'sequence': 120,
                'name': '9,5% VAT EU installation',
                'description': 'VAT charged from assembly and installation of goods in other EU Member States at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+24'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-24'),
                    }),
                ],
            },
            'l10n_si_vat_5_sale_installation_eu': {
                'sequence': 130,
                'name': '5% VAT EU installation',
                'description': 'VAT charged from assembly and installation of goods in other EU Member States at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+24b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-24b'),
                    }),
                ],
            },
            'l10n_si_vat_0_sale_no_deduction': {
                'sequence': 140,
                'name': '0% VAT without deduction',
                'description': 'VAT charged at a rate of 0% without deduction',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+15'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-15'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_si_vat_self_22_sale': {
                'sequence': 150,
                'name': '22% VAT self-assessment',
                'description': 'VAT charged on the basis of self-assessment as a recipient of goods and services at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+25'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-25'),
                    }),
                ],
            },
            'l10n_si_vat_self_9_sale': {
                'sequence': 160,
                'name': '9,5% VAT self-assessment',
                'description': 'VAT charged on the basis of self-assessment as a recipient of goods and services at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+25a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-25a'),
                    }),
                ],
            },
            'l10n_si_vat_self_5_sale': {
                'sequence': 170,
                'name': '5% VAT self-assessment',
                'description': 'VAT charged on the basis of self-assessment as a recipient of goods and services at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+25b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-25b'),
                    }),
                ],
            },
            'l10n_si_vat_self_22_sale_76a': {
                'sequence': 180,
                'name': '22% VAT 76.a',
                'description': 'VAT charged on the basis of self-assessment as a recipient of goods and services specified in Article 76.a at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+25'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-25'),
                    }),
                ],
            },
            'l10n_si_vat_self_9_sale_76a': {
                'sequence': 190,
                'name': '9,5% VAT 76.a',
                'description': 'VAT charged on the basis of self-assessment as a recipient of goods and services specified in Article 76.a at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+25a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-25a'),
                    }),
                ],
            },
            'l10n_si_vat_self_22_sale_imports': {
                'sequence': 200,
                'name': '22% VAT imports self-assessment',
                'description': 'VAT charged on the basis of self-assessment of imports at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+26'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-26'),
                    }),
                ],
            },
            'l10n_si_vat_self_9_sale_imports': {
                'sequence': 210,
                'name': '9,5% VAT imports self-assessment',
                'description': 'VAT charged on the basis of self-assessment of imports at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+26'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-26'),
                    }),
                ],
            },
            'l10n_si_vat_self_5_sale_imports': {
                'sequence': 220,
                'name': '5% VAT imports self-assessment',
                'description': 'VAT charged on the basis of self-assessment of imports at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('+26'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_260000',
                        'tag_ids': tags('-26'),
                    }),
                ],
            },
            'gd_taxp_3': {
                'sequence': 230,
                'name': '22% VAT',
                'description': 'VAT deduction at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'gd_taxp_2': {
                'sequence': 240,
                'name': '9,5% VAT',
                'description': 'VAT deduction at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase': {
                'sequence': 250,
                'name': '5% VAT',
                'description': 'VAT deduction at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42a'),
                    }),
                ],
            },
            'gd_taxp_nr_2': {
                'sequence': 260,
                'name': '22% VAT non-deductible',
                'description': 'VAT non-deductible at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': tags('+31'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': tags('-31'),
                    }),
                ],
            },
            'gd_taxp_nr_1': {
                'sequence': 270,
                'name': '9,5% VAT non-deductible',
                'description': 'VAT non-deductible at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': tags('+31'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': tags('-31'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_non_deductible': {
                'sequence': 280,
                'name': '5% VAT non-deductible',
                'description': 'VAT non-deductible at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': tags('+31'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'tag_ids': tags('-31'),
                    }),
                ],
            },
            'gd_taxp_st_2': {
                'sequence': 290,
                'name': '22% VAT EU goods',
                'description': 'VAT deduction on acquisitions of goods from other EU Member States at the rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+23', '+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-23', '-41'),
                    }),
                ],
            },
            'gd_taxp_st_1': {
                'sequence': 300,
                'name': '9,5% VAT EU goods',
                'description': 'VAT deduction on acquisitions of goods from other EU Member States at the rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+24', '+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-24', '-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_goods_eu': {
                'sequence': 310,
                'name': '5% VAT EU goods',
                'description': 'VAT deduction on acquisitions of goods from other EU Member States at the rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+24b', '+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-24b', '-42a'),
                    }),
                ],
            },
            'l10n_si_vat_22_purchase_services_eu': {
                'sequence': 320,
                'name': '22% VAT EU services',
                'description': 'VAT deduction on acquisitions of services from other EU Member States at the rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+23a', '+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-23a', '-41'),
                    }),
                ],
            },
            'l10n_si_vat_9_purchase_services_eu': {
                'sequence': 330,
                'name': '9,5% VAT EU services',
                'description': 'VAT deduction on acquisitions of services from other EU Member States at the rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+24a', '+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-24a', '-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_services_eu': {
                'sequence': 340,
                'name': '5% VAT EU services',
                'description': 'VAT deduction on acquisitions of services from other EU Member States at the rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+24c', '+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32a'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-24c', '-42a'),
                    }),
                ],
            },
            'gd_taxp_1': {
                'sequence': 350,
                'name': '0% VAT',
                'description': 'VAT deduction from purchases of goods and services, acquisition of goods and services received from other EU Member States and from imports at a rate of 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+33'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-33'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_si_vat_22_purchase_estate': {
                'sequence': 360,
                'name': '22% VAT real estate',
                'description': 'VAT deduction from the purchase of real estate at the rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31', '+34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31', '-34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'l10n_si_vat_9_purchase_estate': {
                'sequence': 370,
                'name': '9,5% VAT real estate',
                'description': 'VAT deduction from the purchase of real estate at the rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31', '+34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31', '-34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_estate': {
                'sequence': 380,
                'name': '5% VAT real estate',
                'description': 'VAT deduction from the purchase of real estate at the rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31', '+34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31', '-34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42a'),
                    }),
                ],
            },
            'l10n_si_vat_22_purchase_estate_76a': {
                'sequence': 390,
                'name': '22% VAT 76.a',
                'description': 'VAT deduction from the purchase of real estate specified in Article 76.a at a rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31a', '+34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31a', '-34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'l10n_si_vat_9_purchase_estate_76a': {
                'sequence': 400,
                'name': '9,5% VAT 76.a',
                'description': 'VAT deduction from the purchase of real estate specified in Article 76.a at a rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31a', '+34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31a', '-34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_estate_76a': {
                'sequence': 410,
                'name': '5% VAT 76.a',
                'description': 'VAT deduction from the purchase of real estate specified in Article 76.a at a rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31a', '+34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31a', '-34'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42a'),
                    }),
                ],
            },
            'l10n_si_vat_22_purchase_fixed': {
                'sequence': 420,
                'name': '22% VAT fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets at the rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'l10n_si_vat_9_purchase_fixed': {
                'sequence': 430,
                'name': '9,5% VAT fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets at the rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_fixed': {
                'sequence': 440,
                'name': '5% VAT fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets at the rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-31', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42a'),
                    }),
                ],
            },
            'l10n_si_vat_0_purchase_fixed': {
                'sequence': 450,
                'name': '0% VAT fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets at the rate of 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+33', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-33', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_si_vat_22_purchase_fixed_eu': {
                'sequence': 460,
                'name': '22% VAT EU fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets from other EU Member States at the rate of 22%',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+41'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'l10n_si_vat_9_purchase_fixed_eu': {
                'sequence': 470,
                'name': '9,5% VAT EU fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets from other EU Member States at the rate of 9,5%',
                'amount': 9.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_95',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42'),
                    }),
                ],
            },
            'l10n_si_vat_5_purchase_fixed_eu': {
                'sequence': 480,
                'name': '5% VAT EU fixed assets',
                'description': 'VAT deduction from the purchase of other fixed assets from other EU Member States at the rate of 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32', '+35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('+42a'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-32', '-35'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'gd_acc_160000',
                        'tag_ids': tags('-42a'),
                    }),
                ],
            },
        }

    def _get_si_fiscal_position(self, template_code):
        return {
            'gd_fp_exempt': {
                'name': 'Exempt taxpayer',
            },
            'gd_fp_do': {
                'name': 'Domestic',
                'sequence': 10,
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.si',
            },
            'gd_fp_do1': {
                'name': 'EU partner private',
                'sequence': 20,
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'gd_fp_eu': {
                'name': 'EU partner',
                'sequence': 30,
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gd_taxr_3',
                        'tax_dest_id': 'gd_taxr_1',
                    }),
                    Command.create({
                        'tax_src_id': 'gd_taxr_2',
                        'tax_dest_id': 'gd_taxr_1',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_si_vat_5_sale',
                        'tax_dest_id': 'gd_taxr_1',
                    }),
                    Command.create({
                        'tax_src_id': 'gd_taxp_3',
                        'tax_dest_id': 'gd_taxp_st_2',
                    }),
                    Command.create({
                        'tax_src_id': 'gd_taxp_2',
                        'tax_dest_id': 'gd_taxp_st_1',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_si_vat_5_purchase',
                        'tax_dest_id': 'l10n_si_vat_5_purchase_goods_eu',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'gd_acc_120000',
                        'account_dest_id': 'gd_acc_121000',
                    }),
                    Command.create({
                        'account_src_id': 'gd_acc_220000',
                        'account_dest_id': 'gd_acc_221000',
                    }),
                    Command.create({
                        'account_src_id': 'gd_acc_760000',
                        'account_dest_id': 'gd_acc_761000',
                    }),
                    Command.create({
                        'account_src_id': 'gd_acc_762000',
                        'account_dest_id': 'gd_acc_763000',
                    }),
                ],
            },
            'gd_fp_ne': {
                'name': 'Partner outside the EU',
                'sequence': 40,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gd_taxp_3',
                        'tax_dest_id': 'gd_taxp_1',
                    }),
                    Command.create({
                        'tax_src_id': 'gd_taxp_2',
                        'tax_dest_id': 'gd_taxp_1',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_si_vat_5_purchase',
                        'tax_dest_id': 'gd_taxp_1',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'gd_acc_120000',
                        'account_dest_id': 'gd_acc_121000',
                    }),
                    Command.create({
                        'account_src_id': 'gd_acc_220000',
                        'account_dest_id': 'gd_acc_221000',
                    }),
                    Command.create({
                        'account_src_id': 'gd_acc_760000',
                        'account_dest_id': 'gd_acc_761000',
                    }),
                    Command.create({
                        'account_src_id': 'gd_acc_762000',
                        'account_dest_id': 'gd_acc_763000',
                    }),
                ],
            },
        }
