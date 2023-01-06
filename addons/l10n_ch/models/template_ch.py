# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ch_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ch_fiscal_position(template_code),
        }

    def _get_ch_template_data(self, template_code):
        return {
            'code_digits': '4',
            'bank_account_code_prefix': '102',
            'cash_account_code_prefix': '100',
            'transfer_account_code_prefix': '1090',
            'property_account_receivable_id': 'ch_coa_1100',
            'property_account_payable_id': 'ch_coa_2000',
            'property_account_expense_categ_id': 'ch_coa_4200',
            'property_account_income_categ_id': 'ch_coa_3200',
        }

    def _get_ch_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ch',
                'account_default_pos_receivable_account_id': 'ch_coa_1101',
                'income_currency_exchange_account_id': 'ch_coa_3806',
                'expense_currency_exchange_account_id': 'ch_coa_4906',
                'account_journal_early_pay_discount_loss_account_id': 'ch_coa_4901',
                'account_journal_early_pay_discount_gain_account_id': 'ch_coa_3801',
            },
        }

    def _get_ch_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'vat_25': {
                'name': '2.5% Sales',
                'description': '2.50%',
                'amount': 2.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+312a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('+312b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-312a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('-312b'),
                    }),
                ],
            },
            'vat_25_incl': {
                'name': '2.5% Sales (incl.)',
                'description': '2.5% Incl.',
                'price_include': True,
                'amount': 2.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+312a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('+312b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-312a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('-312b'),
                    }),
                ],
            },
            'vat_25_purchase': {
                'name': '2.5% on goods and services',
                'description': '2.5% purch.',
                'amount': 2.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_25_purchase_incl': {
                'name': '2.5% on goods and services (incl.)',
                'description': '2.5% purch. Incl.',
                'price_include': True,
                'amount': 2.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_25_invest': {
                'name': '2.5% on invest. and others expenses',
                'description': '2.5% invest.',
                'amount': 2.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_25_invest_incl': {
                'name': '2.5% on invest. and others expenses (incl.)',
                'description': '2.5% invest. Incl.',
                'price_include': True,
                'amount': 2.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_37': {
                'name': '3.7% Sales',
                'description': '3.70%',
                'amount': 3.7,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_37',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+342a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('+342b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-342a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('-342b'),
                    }),
                ],
            },
            'vat_37_incl': {
                'name': '3.7% Sales (incl.)',
                'description': '3.7% Incl.',
                'price_include': True,
                'amount': 3.7,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_37',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+342a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('+342b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-342a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('-342b'),
                    }),
                ],
            },
            'vat_37_purchase': {
                'name': '3.7% on goods and services',
                'description': '3.7% purch.',
                'amount': 3.7,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_37',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_37_purchase_incl': {
                'name': '3.7% on goods and services (incl.)',
                'description': '3.7% purch. Incl.',
                'price_include': True,
                'amount': 3.7,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_37',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_37_invest': {
                'name': '3.7% on invest. and others expenses',
                'description': '3.7% invest',
                'amount': 3.7,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_37',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_37_invest_incl': {
                'name': '3.7% on invest. and others expenses (incl.)',
                'description': '3.7% invest Incl.',
                'price_include': True,
                'amount': 3.7,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_37',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_77': {
                'name': '7.7% Sales',
                'description': '7.70%',
                'amount': 7.7,
                'sequence': 0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_77',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+302a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('+302b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-302a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('-302b'),
                    }),
                ],
            },
            'vat_77_incl': {
                'name': '7.7% Sales (incl.)',
                'description': '7.7% Incl.',
                'price_include': True,
                'amount': 7.7,
                'sequence': 0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_77',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+302a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('+302b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-302a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_2200',
                        'tag_ids': tags('-302b'),
                    }),
                ],
            },
            'vat_77_purchase_incl': {
                'name': '7.7% on goods and services (incl.)',
                'description': '7.7% purch. Incl.',
                'price_include': True,
                'amount': 7.7,
                'amount_type': 'percent',
                'sequence': 0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_77',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_77_invest': {
                'name': '7.7% on invest. and others expenses',
                'description': '7.7% invest.',
                'amount': 7.7,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_77',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_77_invest_incl': {
                'name': '7.7% on invest. and others expenses (incl.)',
                'description': '7.7% invest. Incl.',
                'price_include': True,
                'amount': 7.7,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_77',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_XO': {
                'name': '0% Export',
                'amount': 0.0,
                'description': '0%',
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+220'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-220'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'vat_O_exclude': {
                'name': '0% Excluded',
                'description': '0% excl.',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+230'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-230'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'vat_O_import': {
                'name': '0% Import',
                'description': '0% import.',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
            },
            'vat_100_import': {
                'name': 'Customs VAT on goods and services',
                'description': '100% imp.',
                'amount': 100.0,
                'amount_type': 'division',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_100',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_100_import_invest': {
                'name': 'Customs VAT on invest. and others expenses',
                'description': '100% imp.invest.',
                'amount': 100.0,
                'amount_type': 'division',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_100',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('+405'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1171',
                        'tag_ids': tags('-405'),
                    }),
                ],
            },
            'vat_77_purchase_return': {
                'name': '7.7% Sales (reverse)',
                'description': '7.7% purch. (return)',
                'amount': -7.7,
                'amount_type': 'percent',
                'sequence': 0,
                'tax_group_id': 'tax_group_tva_77',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-382a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-382b'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+382a'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+382b'),
                    }),
                ],
            },
            'vat_77_purchase': {
                'name': '7.7% on goods and services',
                'description': '7.7% purch.',
                'amount': 7.7,
                'amount_type': 'percent',
                'sequence': 0,
                'tax_group_id': 'tax_group_tva_77',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('+400'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ch_coa_1170',
                        'tag_ids': tags('-400'),
                    }),
                ],
            },
            'vat_77_purchase_reverse': {
                'description': '7.7% rev.',
                'name': '7.7% on purchase of service abroad (reverse charge)',
                'amount_type': 'group',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_77',
                'children_tax_ids': [
                    Command.set([
                        'vat_77_purchase_return',
                        'vat_77_purchase',
                    ]),
                ],
            },
            'vat_other_movements_900': {
                'name': '0% - Subsidies, tourist taxes',
                'amount': 0.0,
                'description': '0% subventions',
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+900'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-900'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'vat_other_movements_910': {
                'name': '0% - Donations, dividends, compensation',
                'amount': 0.0,
                'description': '0% dons',
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+910'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-910'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_ch_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'name': 'Suisse national',
                'auto_apply': 1,
                'country_id': 'base.ch',
            },
            'fiscal_position_template_import': {
                'sequence': 1,
                'name': 'Import/Export',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'vat_25_purchase',
                        'tax_dest_id': 'vat_O_import',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_25_invest',
                        'tax_dest_id': 'vat_O_import',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_37_purchase',
                        'tax_dest_id': 'vat_O_import',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_37_invest',
                        'tax_dest_id': 'vat_O_import',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_77_purchase_reverse',
                        'tax_dest_id': 'vat_O_import',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_77_invest',
                        'tax_dest_id': 'vat_O_import',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_25',
                        'tax_dest_id': 'vat_XO',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_37',
                        'tax_dest_id': 'vat_XO',
                    }),
                    Command.create({
                        'tax_src_id': 'vat_77',
                        'tax_dest_id': 'vat_XO',
                    }),
                ],
            },
        }
