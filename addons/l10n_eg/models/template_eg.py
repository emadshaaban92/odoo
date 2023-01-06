# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_eg_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_eg_fiscal_position(template_code),
        }

    def _get_eg_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '101',
            'cash_account_code_prefix': '105',
            'transfer_account_code_prefix': '100',
            'property_account_receivable_id': 'egy_account_102011',
            'property_account_payable_id': 'egy_account_201002',
            'property_account_expense_categ_id': 'egy_account_400028',
            'property_account_income_categ_id': 'egy_account_500001',
            'property_account_expense_id': 'egy_account_400028',
            'property_account_income_id': 'egy_account_500001',
            'property_tax_payable_account_id': 'egy_account_202003',
            'property_tax_receivable_account_id': 'egy_account_100103',
        }

    def _get_eg_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.eg',
                'account_default_pos_receivable_account_id': 'egy_account_102012',
                'income_currency_exchange_account_id': 'egy_account_500011',
                'expense_currency_exchange_account_id': 'egy_account_400053',
                'account_journal_suspense_account_id': 'egy_account_201001',
                'account_journal_early_pay_discount_loss_account_id': 'egy_account_400079',
                'account_journal_early_pay_discount_gain_account_id': 'egy_account_500014',
                'account_journal_payment_debit_account_id': 'egy_account_101004',
                'account_journal_payment_credit_account_id': 'egy_account_105003',
                'default_cash_difference_income_account_id': 'egy_account_999002',
                'default_cash_difference_expense_account_id': 'egy_account_999001',
            },
        }

    def _get_eg_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'eg_standard_sale_14': {
                'name': 'VAT 14%',
                'type_tax_use': 'sale',
                'amount': 14.0,
                'amount_type': 'percent',
                'description': 'VAT 14%',
                'l10n_eg_eta_code': 't1_v009',
                'tax_group_id': 'eg_tax_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1. VAT 14% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201017',
                        'tag_ids': tags('+1. VAT 14% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1. VAT 14% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201017',
                        'tag_ids': tags('-1. VAT 14% (Tax)'),
                    }),
                ],
            },
            'eg_standard_purchase_14': {
                'name': 'VAT 14%',
                'type_tax_use': 'purchase',
                'amount': 14.0,
                'amount_type': 'percent',
                'description': 'VAT 14%',
                'l10n_eg_eta_code': 't1_v009',
                'tax_group_id': 'eg_tax_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+5. VAT 14% Expenses (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104041',
                        'tag_ids': tags('+5. VAT 14% Expenses (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-5. VAT 14% Expenses (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104041',
                        'tag_ids': tags('-5. VAT 14% Expenses (Tax)'),
                    }),
                ],
            },
            'eg_zero_sale_0': {
                'name': 'Zero Rated 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Zero Rated 0%',
                'tax_group_id': 'eg_tax_group_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+2. Zero Rated (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('+2. Zero Rated (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-2. Zero Rated (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('-2. Zero Rated (Tax)'),
                    }),
                ],
            },
            'eg_zero_purchase_0': {
                'name': 'Zero Rated 0%',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Zero Rated 0%',
                'tax_group_id': 'eg_tax_group_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6. Zero Rated (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('+6. Zero Rated (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6. Zero Rated (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('-6. Zero Rated (Tax)'),
                    }),
                ],
            },
            'eg_exempt_sale': {
                'name': 'Exempt',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Exempt',
                'l10n_eg_eta_code': 't1_v003',
                'tax_group_id': 'eg_tax_group_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3. Exempt Sales (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('+3. Exempt Sales (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3. Exempt Sales (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('-3. Exempt Sales (Tax)'),
                    }),
                ],
            },
            'eg_exempt_purchase': {
                'name': 'Exempt',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Exempt',
                'l10n_eg_eta_code': 't1_v003',
                'tax_group_id': 'eg_tax_group_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7. Exempt Expenses (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('+7. Exempt Expenses (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7. Exempt Expenses (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': False,
                        'tag_ids': tags('-7. Exempt Expenses (Tax)'),
                    }),
                ],
            },
            'eg_stamp_tax_20_sale': {
                'name': 'Stamp',
                'type_tax_use': 'sale',
                'amount': 20.0,
                'amount_type': 'percent',
                'description': 'Stamp',
                'l10n_eg_eta_code': 't5_st01',
                'tax_group_id': 'eg_tax_group_stamp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Stamp Tax Sales 20% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201025',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+Stamp Tax Sales 20% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Stamp Tax Sales 20% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201025',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-Stamp Tax Sales 20% (Tax)'),
                    }),
                ],
            },
            'eg_stamp_tax_20_purchase': {
                'name': 'Stamp',
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'description': 'Stamp',
                'l10n_eg_eta_code': 't5_st01',
                'tax_group_id': 'eg_tax_group_stamp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Stamp Tax Purchases 20% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400077',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+Stamp Tax Purchases 20% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Stamp Tax Purchases 20% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400077',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-Stamp Tax Purchases 20% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_8_purchase': {
                'name': 'Schedule 8%',
                'type_tax_use': 'purchase',
                'amount': 8.0,
                'amount_type': 'percent',
                'description': 'SCHD 8%',
                'l10n_eg_eta_code': 't2_tbl01',
                'tax_group_id': 'eg_tax_group_schedule_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 8% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 8% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 8% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 8% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_8_sale': {
                'name': 'Schedule 8%',
                'type_tax_use': 'sale',
                'amount': 8.0,
                'amount_type': 'percent',
                'description': 'SCHD 8%',
                'l10n_eg_eta_code': 't2_tbl01',
                'tax_group_id': 'eg_tax_group_schedule_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 8% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 8% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 8% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 8% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_1_sale': {
                'name': 'Withholding -1%',
                'type_tax_use': 'sale',
                'amount': -1.0,
                'amount_type': 'percent',
                'description': 'WH -1%',
                'tax_group_id': 'eg_tax_group_withholding_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH on Sales -1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Sales -1% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH on Sales -1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Sales -1% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_10_purchase': {
                'name': 'Schedule 10%',
                'type_tax_use': 'purchase',
                'amount': 10.0,
                'amount_type': 'percent',
                'description': 'SCHD 10%',
                'tax_group_id': 'eg_tax_group_schedule_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 10% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 10% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 10% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 10% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_05_sale': {
                'name': 'Withholding -0.5%',
                'type_tax_use': 'sale',
                'amount': -0.5,
                'amount_type': 'percent',
                'description': 'WH -0.5%',
                'tax_group_id': 'eg_tax_group_withholding_half',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH Sales -0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Sales -0.5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH Sales -0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Sales -0.5% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_05_purchase': {
                'name': 'Withholding -0.5%',
                'type_tax_use': 'purchase',
                'amount': -0.5,
                'amount_type': 'percent',
                'description': 'WH -0.5%',
                'tax_group_id': 'eg_tax_group_withholding_half',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH Purchases -0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Purchases -0.5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH Purchases -0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Purchases -0.5% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_1_purchase': {
                'name': 'Withholding -1%',
                'type_tax_use': 'purchase',
                'amount': -1.0,
                'amount_type': 'percent',
                'description': 'WH -1%',
                'tax_group_id': 'eg_tax_group_withholding_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH Purchases -1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Purchases -1% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH Purchases -1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Purchases -1% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_10_sale': {
                'name': 'Schedule 10%',
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'description': 'SCHD 10%',
                'tax_group_id': 'eg_tax_group_schedule_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 10% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 10% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 10% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 10% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_3_sale': {
                'name': 'Withholding -3%',
                'type_tax_use': 'sale',
                'amount': -3.0,
                'amount_type': 'percent',
                'description': 'WH -3%',
                'l10n_eg_eta_code': 't4_w004',
                'tax_group_id': 'eg_tax_group_withholding_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH on Sales -3% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Sales -3% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH on Sales -3% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Sales -3% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_1_sale': {
                'name': 'Schedule 1%',
                'type_tax_use': 'sale',
                'amount': 1.0,
                'amount_type': 'percent',
                'description': 'SCHD 1%',
                'tax_group_id': 'eg_tax_group_schedule_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 1% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 1% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_3_purchase': {
                'name': 'Withholding -3%',
                'type_tax_use': 'purchase',
                'amount': -3.0,
                'amount_type': 'percent',
                'description': 'WH -3%',
                'l10n_eg_eta_code': 't4_w004',
                'tax_group_id': 'eg_tax_group_withholding_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH Purchases -3% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Purchases -3% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH Purchases -3% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Purchases -3% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_1_purchase': {
                'name': 'Schedule 1%',
                'type_tax_use': 'purchase',
                'amount': 1.0,
                'amount_type': 'percent',
                'description': 'SCHD 1%',
                'tax_group_id': 'eg_tax_group_schedule_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 1% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 1% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 1% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_5_sale': {
                'name': 'Withholding -5%',
                'type_tax_use': 'sale',
                'amount': -5.0,
                'amount_type': 'percent',
                'description': 'WH -5%',
                'tax_group_id': 'eg_tax_group_withholding_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH on Sales -5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Sales -5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH on Sales -5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_104042',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Sales -5% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_15_purchase': {
                'name': 'Schedule 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'SCHD 15%',
                'tax_group_id': 'eg_tax_group_schedule_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 15% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 15% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 15% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 15% (Tax)'),
                    }),
                ],
            },
            'eg_withholding_5_purchase': {
                'name': 'Withholding -5%',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'description': 'WH -5%',
                'tax_group_id': 'eg_tax_group_withholding_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+WH Purchases -5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-WH Purchases -5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-WH Purchases -5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201020',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+WH Purchases -5% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_15_sale': {
                'name': 'Schedule 15%',
                'type_tax_use': 'sale',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'SCHD 15%',
                'tax_group_id': 'eg_tax_group_schedule_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 15% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 15% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 15% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 15% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_30_sale': {
                'name': 'Schedule 30%',
                'type_tax_use': 'sale',
                'amount': 30.0,
                'amount_type': 'percent',
                'description': 'SCHD 30%',
                'tax_group_id': 'eg_tax_group_schedule_30',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 30% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 30% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 30% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 30% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_30_purchase': {
                'name': 'Schedule 30%',
                'type_tax_use': 'purchase',
                'amount': 30.0,
                'amount_type': 'percent',
                'description': 'SCHD 30%',
                'tax_group_id': 'eg_tax_group_schedule_30',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 30% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 30% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 30% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 30% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_05_purchase': {
                'name': 'Schedule 0.5%',
                'type_tax_use': 'purchase',
                'amount': 0.5,
                'amount_type': 'percent',
                'description': 'SCHD 0.5%',
                'tax_group_id': 'eg_tax_group_schedule_half',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 0.5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 0.5% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_05_sale': {
                'name': 'Schedule 0.5%',
                'type_tax_use': 'sale',
                'amount': 0.5,
                'amount_type': 'percent',
                'description': 'SCHD 0.5%',
                'tax_group_id': 'eg_tax_group_schedule_half',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 0.5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 0.5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 0.5% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_5_purchase': {
                'name': 'Schedule 5%',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'SCHD 5%',
                'tax_group_id': 'eg_tax_group_schedule_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Purchases 5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Purchases 5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Purchases 5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_400075',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Purchases 5% (Tax)'),
                    }),
                ],
            },
            'eg_schedule_tax_5_sale': {
                'name': 'Schedule 5%',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'SCHD 5%',
                'tax_group_id': 'eg_tax_group_schedule_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+SCHD Sales 5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('+SCHD Sales 5% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-SCHD Sales 5% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'egy_account_201024',
                        'use_in_tax_closing': False,
                        'tag_ids': tags('-SCHD Sales 5% (Tax)'),
                    }),
                ],
            },
        }

    def _get_eg_fiscal_position(self, template_code):
        return {
            'account_fiscal_position_egypt': {
                'name': 'Egypt',
                'sequence': 19,
                'auto_apply': 1,
                'country_id': 'base.eg',
            },
            'account_fiscal_position_non_egypt': {
                'name': 'Non-Egypt',
                'sequence': 20,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'eg_standard_sale_14',
                        'tax_dest_id': 'eg_zero_sale_0',
                    }),
                    Command.create({
                        'tax_src_id': 'eg_standard_purchase_14',
                        'tax_dest_id': 'eg_zero_purchase_0',
                    }),
                ],
            },
        }
