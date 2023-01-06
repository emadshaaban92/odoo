# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ro_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ro_fiscal_position(template_code),
            'account.reconcile.model': self._get_ro_reconcile_model(template_code),
        }

    def _get_ro_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'ro_pcg_recv',
            'property_account_payable_id': 'pcg_4011',
            'property_account_expense_categ_id': 'ro_pcg_expense',
            'property_account_income_categ_id': 'ro_pcg_sale',
            'property_tax_payable_account_id': 'pcg_44231',
            'property_tax_receivable_account_id': 'pcg_4424',
            'bank_account_code_prefix': '512',
            'cash_account_code_prefix': '531',
            'transfer_account_code_prefix': '581',
            'code_digits': '6',
            'use_storno_accounting': True,
        }

    def _get_ro_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ro',
                'account_default_pos_receivable_account_id': 'ro_pcg_recv',
                'income_currency_exchange_account_id': 'pcg_7651',
                'expense_currency_exchange_account_id': 'pcg_6651',
                'account_journal_suspense_account_id': 'pcg_5125',
                'account_journal_early_pay_discount_loss_account_id': 'pcg_6092',
                'account_journal_early_pay_discount_gain_account_id': 'pcg_709',
            },
        }

    def _get_ro_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tvac_00': {
                'sequence': 4,
                'description': 'VAT collected 0% Goods',
                'name': 'VAT collected 0% Goods',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvac_05': {
                'sequence': 3,
                'name': 'VAT collected 5% Goods',
                'description': 'VAT collected 5% Goods',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+11 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-11 - VAT'),
                    }),
                ],
            },
            'tvac_09': {
                'sequence': 2,
                'name': 'VAT collected 9% Goods',
                'description': 'VAT collected 9% Goods',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+10 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+10 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-10 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-10 - VAT'),
                    }),
                ],
            },
            'tvac_19': {
                'sequence': 1,
                'name': 'VAT collected 19% Goods',
                'description': 'VAT collected 19% Goods',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+09 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+09 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-09 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-09 - VAT'),
                    }),
                ],
            },
            'tvac_00_s': {
                'sequence': 4,
                'description': 'VAT collected 0% Services',
                'name': 'VAT collected 0% Services',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvac_05_s': {
                'sequence': 3,
                'name': 'VAT collected 5% Services',
                'description': 'VAT collected 5% Services',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+11 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-11 - VAT'),
                    }),
                ],
            },
            'tvac_09_s': {
                'sequence': 2,
                'name': 'VAT collected 9% Services',
                'description': 'VAT collected 9% Services',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+10 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+10 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-10 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-10 - VAT'),
                    }),
                ],
            },
            'tvac_19_s': {
                'sequence': 1,
                'name': 'VAT collected 19% Services',
                'description': 'VAT collected 19% Services',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+09 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+09 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-09 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-09 - VAT'),
                    }),
                ],
            },
            'tvad_00': {
                'sequence': 43,
                'name': 'VAT deductible 0% Goods',
                'description': 'VAT deductible 0% Goods',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvad_05': {
                'sequence': 42,
                'name': 'VAT deductible 5% Goods',
                'description': 'VAT deductible 5% Goods',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+26_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+26_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-26_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-26_1 - VAT'),
                    }),
                ],
            },
            'tvad_09': {
                'sequence': 41,
                'name': 'VAT deductible 9% Goods',
                'description': 'VAT deductible 9% Goods',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+25_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+25_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-25_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-25_1 - VAT'),
                    }),
                ],
            },
            'tvad_19': {
                'sequence': 40,
                'name': 'VAT deductible 19% Goods',
                'description': 'VAT deductible 19% Goods',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+24_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+24_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-24_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-24_1 - VAT'),
                    }),
                ],
            },
            'tvad_00_s': {
                'sequence': 43,
                'name': 'VAT deductible 0% Services',
                'description': 'VAT deductible 0% Services',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvad_05_s': {
                'sequence': 42,
                'name': 'VAT deductible 5% Services',
                'description': 'VAT deductible 5% Services',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+26_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+26_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-26_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-26_1 - VAT'),
                    }),
                ],
            },
            'tvad_09_s': {
                'sequence': 41,
                'name': 'VAT deductible 9% Services',
                'description': 'VAT deductible 9% Services',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+25_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+25_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-25_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-25_1 - VAT'),
                    }),
                ],
            },
            'tvad_19_s': {
                'sequence': 40,
                'name': 'VAT deductible 19% Services',
                'description': 'VAT deductible 19% Services',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+24_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+24_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-24_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-24_1 - VAT'),
                    }),
                ],
            },
            'tvaic_00': {
                'sequence': 13,
                'name': 'VAT on collection - 0% collected',
                'description': 'VAT collected 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvaic_05': {
                'sequence': 12,
                'name': 'VAT on collection - collected 5%',
                'description': 'VAT collected 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44281',
                'tax_group_id': 'tax_group_tva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-11 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+11 - VAT'),
                    }),
                ],
            },
            'tvaic_09': {
                'sequence': 11,
                'name': 'VAT on collection - collected 9%',
                'description': 'VAT collected 9%',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44281',
                'tax_group_id': 'tax_group_tva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-10 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-10 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+10 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+10 - VAT'),
                    }),
                ],
            },
            'tvaic_19': {
                'sequence': 10,
                'name': 'VAT on collection - collected 19%',
                'description': 'VAT collected 19%',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44281',
                'tax_group_id': 'tax_group_tva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-09 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-09 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+09 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+09 - VAT'),
                    }),
                ],
            },
            'tvaid_00': {
                'sequence': 53,
                'name': 'VAT on collection - 0% deductible',
                'description': '0% deductible VAT',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvaid_05': {
                'sequence': 52,
                'name': 'VAT on collection - 5% deductible',
                'description': '5% VAT deductible',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44282',
                'tax_group_id': 'tax_group_tva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+26_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+26_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-26_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-26_1 - VAT'),
                    }),
                ],
            },
            'tvaid_09': {
                'sequence': 51,
                'name': 'VAT on collection - 9% deductible',
                'description': '9% VAT deductible',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44282',
                'tax_group_id': 'tax_group_tva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+25_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+25_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-25_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-25_1 - VAT'),
                    }),
                ],
            },
            'tvaid_19': {
                'sequence': 50,
                'name': 'VAT on collection - 19% deductible',
                'description': '19% VAT deductible',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44282',
                'tax_group_id': 'tax_group_tva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+24_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+24_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-24_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-24_1 - VAT'),
                    }),
                ],
            },
            'tvati': {
                'sequence': 20,
                'name': 'VAT Reverse Tax',
                'description': 'VAT Reverse Tax',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_ti',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+13 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-13 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatip00': {
                'sequence': 63,
                'name': 'VAT Reverse Tax 0%',
                'description': 'VAT Reverse Tax 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ti',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatip05': {
                'sequence': 62,
                'name': 'VAT Reverse Tax 5%',
                'description': 'VAT Reverse Tax 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ti',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_3 - TAX BASE', '+27_3 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-12_3 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+27_3 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_3 - TAX BASE', '-27_3 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+12_3 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-27_3 - VAT'),
                    }),
                ],
            },
            'tvatip09': {
                'sequence': 61,
                'name': 'VAT Reverse Tax 9%',
                'description': 'VAT Reverse Tax 9%',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ti',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_2 - TAX BASE', '+27_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-12_2 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+27_2 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_2 - TAX BASE', '-27_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+12_2 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-27_2 - VAT'),
                    }),
                ],
            },
            'tvatip19': {
                'sequence': 60,
                'name': 'VAT Reverse Tax 19%',
                'description': 'VAT Reverse Tax 19%',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ti',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_1 - TAX BASE', '+27_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-12_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+27_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_1 - TAX BASE', '-27_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('+12_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-27_1 - VAT'),
                    }),
                ],
            },
            'tvatiscded': {
                'sequence': 31,
                'name': 'VAT Tax exempt Deliveries with the right to deduct',
                'description': 'Exempt-L1',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatiscnoded': {
                'sequence': 32,
                'name': 'VAT Tax exempt Deliveries without the right to deduct',
                'description': 'Exempt-L2',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+15 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-15 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatiscdeda': {
                'sequence': 61,
                'name': 'VAT Tax Exemption Acquisitions',
                'description': 'Exempt-A',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatiscdeda_intr': {
                'sequence': 61,
                'name': 'VAT Exempt Taxation Intra-Community Acquisitions',
                'description': 'Exempt-AI',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE', '+30_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE', '-30_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatine': {
                'sequence': 33,
                'name': 'VAT Non-Taxable Taxes Deliveries',
                'description': 'Non-Taxable-L',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_neimp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+15 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-15 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvatinea': {
                'sequence': 62,
                'name': 'VAT Tax Non-Taxable Acquisitions',
                'description': 'Non-Taxable-A',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_neimp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_intrab': {
                'sequence': 34,
                'name': 'Intra-Community VAT Goods Delivery',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+01 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-01 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_intras': {
                'sequence': 34,
                'name': 'Intra-Community VAT Delivery Services',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-03 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_extra': {
                'sequence': 35,
                'name': 'VAT Exportation',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-14 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_intrap0b': {
                'sequence': 66,
                'name': 'Intra-Community VAT Acquisitions 0% - Goods',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_intrap5b': {
                'sequence': 65,
                'name': 'Intra-Community VAT Acquisitions 5% - Goods',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_5_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+05 - TAX BASE', '+05_1 - TAX BASE', '+20 - TAX BASE', '+20_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-05 - VAT', '-05_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+20 - VAT', '+20_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-05 - TAX BASE', '-05_1 - TAX BASE', '-20 - TAX BASE', '-20_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+05 - VAT', '+05_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-20 - VAT', '-20_1 - VAT'),
                    }),
                ],
            },
            'tvati_intrap9b': {
                'sequence': 64,
                'name': 'Intra-Community VAT Acquisitions 9% - Goods',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_9_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+05 - TAX BASE', '+05_1 - TAX BASE', '+20 - TAX BASE', '+20_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-05 - VAT', '-05_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+20 - VAT', '+20_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-05 - TAX BASE', '-05_1 - TAX BASE', '-20 - TAX BASE', '-20_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+05 - VAT', '+05_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-20 - VAT', '-20_1 - VAT'),
                    }),
                ],
            },
            'tvati_intrap19b': {
                'sequence': 63,
                'name': 'Intra-Community VAT Acquisitions 19% - Goods',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_19_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+05 - TAX BASE', '+05_1 - TAX BASE', '+20 - TAX BASE', '+20_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-05 - VAT', '-05_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+20 - VAT', '+20_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-05 - TAX BASE', '-05_1 - TAX BASE', '-20 - TAX BASE', '-20_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+05 - VAT', '+05_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-20 - VAT', '-20_1 - VAT'),
                    }),
                ],
            },
            'tvati_intrap0s': {
                'sequence': 70,
                'name': 'Intra-Community VAT Acquisitions 0% - Services',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-30 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_intrap5s': {
                'sequence': 69,
                'name': 'Intra-Community VAT Acquisitions 5% - Services',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_5_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+07 - TAX BASE', '+07_1 - TAX BASE', '+22 - TAX BASE', '+22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-07 - VAT', '-07_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+22 - VAT', '+22_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-07 - TAX BASE', '-07_1 - TAX BASE', '-22 - TAX BASE', '-22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+07 - VAT', '+07_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-22 - VAT', '-22_1 - VAT'),
                    }),
                ],
            },
            'tvati_intrap9s': {
                'sequence': 68,
                'name': 'Intra-Community VAT Acquisitions 9% - Services',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_9_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+07 - TAX BASE', '+07_1 - TAX BASE', '+22 - TAX BASE', '+22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-07 - VAT', '-07_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+22 - VAT', '+22_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-07 - TAX BASE', '-07_1 - TAX BASE', '-22 - TAX BASE', '-22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+07 - VAT', '+07_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-22 - VAT', '-22_1 - VAT'),
                    }),
                ],
            },
            'tvati_intrap19s': {
                'sequence': 67,
                'name': 'Intra-Community VAT Acquisitions 19% - Services',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_19_eu',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+07 - TAX BASE', '+07_1 - TAX BASE', '+22 - TAX BASE', '+22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-07 - VAT', '-07_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+22 - VAT', '+22_1 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-07 - TAX BASE', '-07_1 - TAX BASE', '-22 - TAX BASE', '-22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+07 - VAT', '+07_1 - VAT'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4427',
                        'tag_ids': tags('-22 - VAT', '-22_1 - VAT'),
                    }),
                ],
            },
            'tvati_extrap0b': {
                'sequence': 66,
                'name': 'VAT Import Goods',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+07 - TAX BASE', '+07_1 - TAX BASE', '+22 - TAX BASE', '+22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-07 - TAX BASE', '-07_1 - TAX BASE', '-22 - TAX BASE', '-22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tvati_extrap0s': {
                'sequence': 70,
                'name': 'VAT Import Services',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_scutit',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+07 - TAX BASE', '+07_1 - TAX BASE', '+22 - TAX BASE', '+22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-07 - TAX BASE', '-07_1 - TAX BASE', '-22 - TAX BASE', '-22_1 - TAX BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_ned_5_50': {
                'sequence': 72,
                'name': 'VAT 5% Non-deductible 50%',
                'description': 'VAT 5% Non-deductible 50%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ned',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+26_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-26_2 - VAT'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_6352',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+26_2 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-26_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+26_2 - VAT'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_6352',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-26_2 - VAT'),
                    }),
                ],
            },
            'tva_ned_9_50': {
                'sequence': 71,
                'name': 'VAT 9% Non-deductible 50%',
                'description': 'VAT 9% Non-deductible 50%',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ned',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+25_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-25_2 - VAT'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_6352',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+25_2 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-25_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+25_2 - VAT'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_6352',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-25_2 - VAT'),
                    }),
                ],
            },
            'tva_ned_19_50': {
                'sequence': 70,
                'name': 'VAT 19% Non-deductible 50%',
                'description': 'VAT 19% Non-deductible 50%',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_ned',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+24_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-24_2 - VAT'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_6352',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+24_2 - VAT'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-24_2 - TAX BASE'),
                    }),
                    Command.create({
                        'factor_percent': -50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('+24_2 - VAT'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_6352',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4426',
                        'tag_ids': tags('-24_2 - VAT'),
                    }),
                ],
            },
        }

    def _get_ro_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'name': 'National Regime (VAT)',
                'country_id': 'base.ro',
                'auto_apply': 1,
                'vat_required': 1,
                'sequence': 10,
            },
            'fiscal_position_template_11': {
                'name': 'National Regime',
                'country_id': 'base.ro',
                'auto_apply': 1,
                'sequence': 11,
            },
            'fiscal_position_template_2': {
                'name': 'Reverse Tax Regime',
                'country_id': 'base.ro',
                'vat_required': 1,
                'sequence': 12,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvati',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvatip00',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvatip05',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvatip09',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvatip19',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvatip00',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvatip05',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvatip09',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvatip19',
                    }),
                ],
            },
            'fiscal_position_template_8': {
                'name': 'VAT collection system',
                'vat_required': 1,
                'country_id': 'base.ro',
                'sequence': 13,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvaic_00',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvaic_05',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvaic_09',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvaic_19',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvaic_00',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvaic_05',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvaic_09',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvaic_19',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvaid_00',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvaid_05',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvaid_09',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvaid_19',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvaid_00',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvaid_05',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvaid_09',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvaid_19',
                    }),
                ],
            },
            'fiscal_position_template_3': {
                'name': 'Intra-Community Scheme (VAT)',
                'country_group_id': 'base.europe',
                'auto_apply': 1,
                'sequence': 14,
                'vat_required': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvati_intrap0b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvati_intrap5b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvati_intrap9b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvati_intrap19b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvati_intrap0s',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvati_intrap5s',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvati_intrap9s',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvati_intrap19s',
                    }),
                ],
            },
            'fiscal_position_template_4': {
                'name': 'Exempted Intra-Community Regime',
                'country_group_id': 'base.europe',
                'auto_apply': 1,
                'sequence': 15,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvati_intrab',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvati_intras',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvatiscdeda_intr',
                    }),
                ],
            },
            'fiscal_position_template_51': {
                'name': 'Exempt regime - with the right of deduction',
                'sequence': 16,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvatiscded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                ],
            },
            'fiscal_position_template_52': {
                'name': 'Exempt regime - no right of deduction',
                'sequence': 17,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvatiscnoded',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvatiscdeda',
                    }),
                ],
            },
            'fiscal_position_template_6': {
                'name': 'Intra-Community Regime Non-taxable',
                'country_group_id': 'base.europe',
                'sequence': 18,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvatine',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvatinea',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvatinea',
                    }),
                ],
            },
            'fiscal_position_template_7': {
                'name': 'Extra-Community Regime',
                'sequence': 19,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tvac_00',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_00_s',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_05_s',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_09_s',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvac_19_s',
                        'tax_dest_id': 'tvati_extra',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00',
                        'tax_dest_id': 'tvati_extrap0b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05',
                        'tax_dest_id': 'tvati_extrap0b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09',
                        'tax_dest_id': 'tvati_extrap0b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19',
                        'tax_dest_id': 'tvati_extrap0b',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_00_s',
                        'tax_dest_id': 'tvati_extrap0s',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_05_s',
                        'tax_dest_id': 'tvati_extrap0s',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_09_s',
                        'tax_dest_id': 'tvati_extrap0s',
                    }),
                    Command.create({
                        'tax_src_id': 'tvad_19_s',
                        'tax_dest_id': 'tvati_extrap0s',
                    }),
                ],
            },
        }

    def _get_ro_reconcile_model(self, template_code):
        return {
            'suppadvance_template': {
                'name': 'Avans Furnizor - Imobilizări Necorporale',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_4094',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Supplier Advance - Intangible Assets',
                    }),
                ],
            },
            'custadvance_template': {
                'name': 'Customer Advances',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_419',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Customer Advances',
                    }),
                ],
            },
            'bankcomm_template': {
                'name': 'Bank Commission',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_627',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Bank Commission',
                    }),
                ],
            },
            'interest_template': {
                'name': 'Interests',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_766',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Interests',
                    }),
                ],
            },
            'inttransfer_template': {
                'name': 'Internal transfer',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_581',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Internal transfer',
                    }),
                ],
            },
            'payroll_template': {
                'name': 'Wages',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_421',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Wages',
                    }),
                ],
            },
            'pendsettl_template': {
                'name': 'Operations being clarified',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_473',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Operations being clarified',
                    }),
                ],
            },
        }
