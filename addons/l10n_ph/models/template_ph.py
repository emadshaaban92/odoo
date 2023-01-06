# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ph_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ph_fiscal_position(template_code),
        }

    def _get_ph_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_ph_110000',
            'property_account_payable_id': 'l10n_ph_200000',
            'property_account_income_categ_id': 'l10n_ph_430400',
            'property_account_expense_categ_id': 'l10n_ph_620000',
            'property_stock_valuation_account_id': 'l10n_ph_110300',
            'property_stock_account_input_categ_id': 'l10n_ph_110302',
            'property_stock_account_output_categ_id': 'l10n_ph_110303',
            'bank_account_code_prefix': '1000',
            'cash_account_code_prefix': '1001',
            'transfer_account_code_prefix': '1002',
            'code_digits': '6',
            'use_anglo_saxon': True,
        }

    def _get_ph_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_default_pos_receivable_account_id': 'l10n_ph_110003',
                'income_currency_exchange_account_id': 'l10n_ph_710100',
                'expense_currency_exchange_account_id': 'l10n_ph_710101',
                'account_journal_suspense_account_id': 'l10n_ph_100000',
                'default_cash_difference_income_account_id': 'l10n_ph_710102',
                'default_cash_difference_expense_account_id': 'l10n_ph_710103',
            },
        }

    def _get_ph_account_tax(self, template_code):
        return {
            'l10n_ph_tax_sale_vat_12': {
                'sequence': 10,
                'name': '12% VAT',
                'description': '12% VAT',
                'type_tax_use': 'sale',
                'amount': 12.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200300',
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
                        'account_id': 'l10n_ph_200300',
                    }),
                ],
            },
            'l10n_ph_tax_sale_vat_exempt': {
                'sequence': 10,
                'name': 'VAT Exempt',
                'description': 'VAT Exempt',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_vat_exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200300',
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
                        'account_id': 'l10n_ph_200300',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_vat_12': {
                'sequence': 20,
                'name': '12% VAT',
                'description': '12% VAT',
                'type_tax_use': 'purchase',
                'amount': 12.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_110201',
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
                        'account_id': 'l10n_ph_110201',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_vat_exempt': {
                'sequence': 20,
                'name': 'VAT Exempt',
                'description': 'VAT Exempt',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_vat_exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_110201',
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
                        'account_id': 'l10n_ph_110201',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi010': {
                'sequence': 30,
                'name': '5% WI010 - Prof Fees',
                'description': 'Prof Fees',
                'l10n_ph_atc': 'WI010',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi011': {
                'sequence': 30,
                'name': '10% WI011 - Prof Fees',
                'description': 'Prof Fees',
                'l10n_ph_atc': 'WI011',
                'type_tax_use': 'purchase',
                'amount': -10.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi100': {
                'sequence': 40,
                'name': '5% WI100 - Gross rental of property',
                'description': 'Gross rental of property',
                'l10n_ph_atc': 'WI100',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi120': {
                'sequence': 50,
                'name': '2% WI120 - Contractors',
                'description': 'Contractors',
                'l10n_ph_atc': 'WI120',
                'type_tax_use': 'purchase',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi139': {
                'sequence': 60,
                'name': '5% WI139 - Commission of service fees',
                'description': 'Commission of service fees',
                'l10n_ph_atc': 'WI139',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi140': {
                'sequence': 60,
                'name': '10% WI140 - Commission of service fees',
                'description': 'Commission of service fees',
                'l10n_ph_atc': 'WI140',
                'type_tax_use': 'purchase',
                'amount': -10.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi158_p5': {
                'sequence': 70,
                'name': '0.5% WI158 - Credit card companies',
                'description': 'Credit card companies',
                'l10n_ph_atc': 'WI158',
                'type_tax_use': 'purchase',
                'amount': -0.5,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_p5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi640': {
                'sequence': 80,
                'name': '1% WI640 - Supplier of goods',
                'description': 'Supplier of goods',
                'l10n_ph_atc': 'WI640',
                'type_tax_use': 'purchase',
                'amount': -1.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi157': {
                'sequence': 80,
                'name': '2% WI157 - Supplier of services',
                'description': 'Supplier of services',
                'l10n_ph_atc': 'WI157',
                'type_tax_use': 'purchase',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi158_1': {
                'sequence': 90,
                'name': '1% WI158 - Supplier of goods by top w/holding agents',
                'description': 'Supplier of goods by top w/holding agents',
                'l10n_ph_atc': 'WI158',
                'type_tax_use': 'purchase',
                'amount': -1.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi160': {
                'sequence': 90,
                'name': '2% WI160 - Supplier of goods by top w/holding agents',
                'description': 'Supplier of goods by top w/holding agents',
                'l10n_ph_atc': 'WI160',
                'type_tax_use': 'purchase',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi515': {
                'sequence': 100,
                'name': '5% WI515 - Commission, rebates, discounts',
                'description': 'Commission, rebates, discounts',
                'l10n_ph_atc': 'WI515',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wi516': {
                'sequence': 100,
                'name': '10% WI516 - Commission, rebates, discounts',
                'description': 'Commission, rebates, discounts',
                'l10n_ph_atc': 'WI516',
                'type_tax_use': 'purchase',
                'amount': -10.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc010': {
                'sequence': 110,
                'name': '10% WC010 - Prof Fees',
                'description': 'Prof Fees',
                'l10n_ph_atc': 'WC010',
                'type_tax_use': 'purchase',
                'amount': -10.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc011': {
                'sequence': 110,
                'name': '15% WC011 - Prof Fees',
                'description': 'Prof Fees',
                'l10n_ph_atc': 'WC011',
                'type_tax_use': 'purchase',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc100': {
                'sequence': 120,
                'name': '5% WC100 - Gross rental of property',
                'description': 'Gross rental of property',
                'l10n_ph_atc': 'WC100',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc120': {
                'sequence': 130,
                'name': '2% WC120 - Contractors',
                'description': 'Contractors',
                'l10n_ph_atc': 'WC120',
                'type_tax_use': 'purchase',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc139': {
                'sequence': 140,
                'name': '10% WC139 - Commission of service fees',
                'description': 'Commission of service fees',
                'l10n_ph_atc': 'WC139',
                'type_tax_use': 'purchase',
                'amount': -10.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc140': {
                'sequence': 140,
                'name': '15% WC140 - Commission of service fees',
                'description': 'Commission of service fees',
                'l10n_ph_atc': 'WC140',
                'type_tax_use': 'purchase',
                'amount': -15.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc158_p5': {
                'sequence': 150,
                'name': '0.5% WC158 - Credit card companies',
                'description': 'Credit card companies',
                'l10n_ph_atc': 'WC158',
                'type_tax_use': 'purchase',
                'amount': -0.5,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_p5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc640': {
                'sequence': 160,
                'name': '1% WC640 - Supplier of goods',
                'description': 'Supplier of goods',
                'l10n_ph_atc': 'WC640',
                'type_tax_use': 'purchase',
                'amount': -1.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc157': {
                'sequence': 160,
                'name': '2% WC157 - Supplier of services',
                'description': 'Supplier of services',
                'l10n_ph_atc': 'WC157',
                'type_tax_use': 'purchase',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc158_1': {
                'sequence': 170,
                'name': '1% WC158 - Supplier of goods by top w/holding agents',
                'description': 'Supplier of goods by top w/holding agents',
                'l10n_ph_atc': 'WC158',
                'type_tax_use': 'purchase',
                'amount': -1.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc160': {
                'sequence': 170,
                'name': '2% WC160 - Supplier of goods by top w/holding agents',
                'description': 'Supplier of goods by top w/holding agents',
                'l10n_ph_atc': 'WC160',
                'type_tax_use': 'purchase',
                'amount': -2.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc515': {
                'sequence': 180,
                'name': '5% WC515 - Commission, rebates, discounts',
                'description': 'Commission, rebates, discounts',
                'l10n_ph_atc': 'WC515',
                'type_tax_use': 'purchase',
                'amount': -5.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
            'l10n_ph_tax_purchase_wc516': {
                'sequence': 180,
                'name': '10% WC516 - Commission, rebates, discounts',
                'description': 'Commission, rebates, discounts',
                'l10n_ph_atc': 'WC516',
                'type_tax_use': 'purchase',
                'amount': -10.0,
                'amount_type': 'percent',
                'tax_group_id': 'l10n_ph_tax_group_wht_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_ph_200303',
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
                        'account_id': 'l10n_ph_200303',
                    }),
                ],
            },
        }

    def _get_ph_fiscal_position(self, template_code):
        return {
            'l10n_ph_fiscal_position_vat_registered': {
                'sequence': 1,
                'name': 'VAT Registered',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.ph',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'l10n_ph_tax_sale_vat_exempt',
                        'tax_dest_id': 'l10n_ph_tax_sale_vat_12',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_ph_tax_purchase_vat_exempt',
                        'tax_dest_id': 'l10n_ph_tax_purchase_vat_12',
                    }),
                ],
            },
            'l10n_ph_fiscal_position_vat_exempt': {
                'sequence': 2,
                'name': 'VAT Exempt',
                'auto_apply': 1,
                'country_id': 'base.ph',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'l10n_ph_tax_sale_vat_12',
                        'tax_dest_id': 'l10n_ph_tax_sale_vat_exempt',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_ph_tax_purchase_vat_12',
                        'tax_dest_id': 'l10n_ph_tax_purchase_vat_exempt',
                    }),
                ],
            },
        }
