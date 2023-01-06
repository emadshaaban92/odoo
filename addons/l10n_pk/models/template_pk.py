# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_pk_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_pk_1121001',
            'property_account_payable_id': 'l10n_pk_2221001',
            'property_account_income_categ_id': 'l10n_pk_3111001',
            'property_account_expense_categ_id': 'l10n_pk_4111001',
            'code_digits': '7',
            'bank_account_code_prefix': '112600',
            'cash_account_code_prefix': '112600',
            'transfer_account_code_prefix': '112600',
        }

    def _get_pk_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.pk',
                'account_default_pos_receivable_account_id': 'l10n_pk_1121001',
                'account_journal_suspense_account_id': 'l10n_pk_2226000',
                'account_journal_early_pay_discount_loss_account_id': 'l10n_pk_4411003',
                'account_journal_early_pay_discount_gain_account_id': 'l10n_pk_3112004',
            },
        }

    def _get_pk_account_tax(self, template_code):
        return {
            'pk_sales_tax_17': {
                'name': 'Standard Sales Tax 17%',
                'type_tax_use': 'sale',
                'amount': 17.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Tax 17%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_19_5': {
                'name': 'Sales Tax Telecommunication Services 19.5%',
                'type_tax_use': 'sale',
                'amount': 19.5,
                'amount_type': 'percent',
                'description': 'Sales Tax Telecommunication Services 19.5%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_17': {
                'name': 'Sales Tax Services 17%',
                'type_tax_use': 'sale',
                'amount': 17.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 17%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_16': {
                'name': 'Sales Tax Services 16%',
                'type_tax_use': 'sale',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 16%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_16_punjab': {
                'name': 'Standard Sales Service Tax Punjab 16%',
                'type_tax_use': 'sale',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Service Tax Punjab 16%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_16_ict': {
                'name': 'Standard Sales Service Tax ICT 16%',
                'type_tax_use': 'sale',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Service Tax Islamabad Capital Territory 16%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_16_ajk': {
                'name': 'Standard Sales Service Tax AJK 16%',
                'type_tax_use': 'sale',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Service Tax Azad Jammu and Kashmir 16%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_15': {
                'name': 'Sales Tax Services 15%',
                'type_tax_use': 'sale',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 15%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_15_kp': {
                'name': 'Standard Sales Service Tax KP 15%',
                'type_tax_use': 'sale',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Service Tax Khyber Pakhtunkhwa 15%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_15_balochistan': {
                'name': 'Standard Sales Service Tax Balochistan 15%',
                'type_tax_use': 'sale',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Service Tax Balochistan 15%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_13': {
                'name': 'Sales Tax Services 13%',
                'type_tax_use': 'sale',
                'amount': 13.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 13%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_13_sindh': {
                'name': 'Standard Sales Tax Services 13% Sindh',
                'type_tax_use': 'sale',
                'amount': 13.0,
                'amount_type': 'percent',
                'description': 'Standard Sales Tax Services 13% Sindh',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_10': {
                'name': 'Sales Tax Services 10%',
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 10%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_8': {
                'name': 'Sales Tax Services 8%',
                'type_tax_use': 'sale',
                'amount': 8.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 8%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_5': {
                'name': 'Sales Tax Services 5%',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 5%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_3': {
                'name': 'Sales Tax Services 3%',
                'type_tax_use': 'sale',
                'amount': 3.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 3%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_2': {
                'name': 'Sales Tax Services 2%',
                'type_tax_use': 'sale',
                'amount': 2.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 2%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_1': {
                'name': 'Sales Tax Services 1%',
                'type_tax_use': 'sale',
                'amount': 1.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 1%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'pk_sales_tax_services_0': {
                'name': 'Sales Tax Services 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Sales Tax Services 0%',
                'tax_group_id': 'tax_group_taxes_sales',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_17': {
                'name': 'Standard Purchases Tax 17%',
                'type_tax_use': 'purchase',
                'amount': 17.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Tax 17%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_19_5': {
                'name': 'Purchases Tax Telecommunication Services 19.5%',
                'type_tax_use': 'purchase',
                'amount': 19.5,
                'amount_type': 'percent',
                'description': 'Purchases Tax Telecommunication Services 19.5%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_17': {
                'name': 'Purchases Tax Services 17%',
                'type_tax_use': 'purchase',
                'amount': 17.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 17%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_16': {
                'name': 'Purchases Tax Services 16%',
                'type_tax_use': 'purchase',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 16%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_16_punjab': {
                'name': 'Standard Purchases Service Tax Punjab 16%',
                'type_tax_use': 'purchase',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Service Tax Punjab 16%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_16_ict': {
                'name': 'Standard Purchases Service Tax ICT 16%',
                'type_tax_use': 'purchase',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Service Tax Islamabad Capital Territory 16%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_16_ajk': {
                'name': 'Standard Purchases Service Tax AJK 16%',
                'type_tax_use': 'purchase',
                'amount': 16.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Service Tax Azad Jammu and Kashmir 16%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_15': {
                'name': 'Purchases Tax Services 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 15%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_15_kp': {
                'name': 'Standard Purchases Service Tax KP 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Service Tax Khyber Pakhtunkhwa 15%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_15_balochistan': {
                'name': 'Standard Purchases Service Tax Balochistan 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Service Tax Balochistan 15%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_13': {
                'name': 'Purchases Tax Services 13%',
                'type_tax_use': 'purchase',
                'amount': 13.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 13%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_13_sindh': {
                'name': 'Standard Purchases Tax Services 13% Sindh',
                'type_tax_use': 'purchase',
                'amount': 13.0,
                'amount_type': 'percent',
                'description': 'Standard Purchases Tax Services 13% Sindh',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_10': {
                'name': 'Purchases Tax Services 10%',
                'type_tax_use': 'purchase',
                'amount': 10.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 10%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_8': {
                'name': 'Purchases Tax Services 8%',
                'type_tax_use': 'purchase',
                'amount': 8.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 8%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_5': {
                'name': 'Purchases Tax Services 5%',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 5%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_3': {
                'name': 'Purchases Tax Services 3%',
                'type_tax_use': 'purchase',
                'amount': 3.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 3%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_2': {
                'name': 'Purchases Tax Services 2%',
                'type_tax_use': 'purchase',
                'amount': 2.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 2%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_1': {
                'name': 'Purchases Tax Services 1%',
                'type_tax_use': 'purchase',
                'amount': 1.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 1%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
            'purchases_tax_services_0': {
                'name': 'Purchases Tax Services 0%',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Purchases Tax Services 0%',
                'tax_group_id': 'tax_group_taxes_purchases',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_pk_2221005',
                    }),
                ],
            },
        }
