# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_kz_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_kz_fiscal_position(template_code),
        }

    def _get_kz_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'kz1210',
            'property_account_payable_id': 'kz3310',
            'property_account_income_categ_id': 'kz6010',
            'property_account_expense_categ_id': 'kz1330',
            'property_tax_receivable_account_id': 'kz1400',
            'property_tax_payable_account_id': 'kz3100',
            'code_digits': '4',
            'bank_account_code_prefix': '103',
            'cash_account_code_prefix': '101',
            'transfer_account_code_prefix': '102',
        }

    def _get_kz_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.kz',
                'income_currency_exchange_account_id': 'kz6250',
                'expense_currency_exchange_account_id': 'kz7430',
                'account_journal_early_pay_discount_loss_account_id': 'kz7481',
                'account_journal_early_pay_discount_gain_account_id': 'kz6291',
                'default_cash_difference_income_account_id': 'kz6210',
                'default_cash_difference_expense_account_id': 'kz7410',
            },
        }

    def _get_kz_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'l10n_kz_tax_vat_12_sale': {
                'name': '12%',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase': {
                'name': '12%',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_0_sale': {
                'name': '0%',
                'tax_group_id': 'tax_group_vat_0',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'VAT 0%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Sales turnover subject to zero VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Sales turnover subject to zero VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_0_purchase': {
                'name': '0%',
                'tax_group_id': 'tax_group_vat_0',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'VAT 0%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Purchases without VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Purchases without VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_sale_included': {
                'name': '12% included',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'VAT 12% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase_included': {
                'name': '12% included',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'VAT 12% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_sale_included': {
                'name': '20% included',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'VAT 20% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_sale': {
                'name': '20%',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+I. With the issuance of invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+I. With the issuance of invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase_included': {
                'name': '20% included',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'VAT 20% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase': {
                'name': '20%',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+On invoices net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+On invoices tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_sale_export': {
                'name': '12% EX',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Export VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase_import': {
                'name': '12% EX',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Import VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_0_sale_export': {
                'name': '0% EX',
                'tax_group_id': 'tax_group_vat_0',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Export VAT 0%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Sales turnover subject to zero VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Sales turnover subject to zero VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_sale_included_export': {
                'name': '12% EX included',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Export VAT 12% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase_included_import': {
                'name': '12% EX included',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Import VAT 12% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_sale_included_export': {
                'name': '20% EX included',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Export VAT 20% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_sale_export': {
                'name': '20% EX',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Export VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase_included_import': {
                'name': '20% EX included',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Import VAT 20% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase_import': {
                'name': '20% EX',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Import VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from non-EEU states net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from non-EEU states tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase_non_resident': {
                'name': '12% S Non-resident',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'description': 'Non-resident VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Works, services purchased from a non-resident net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Works, services purchased from a non-resident tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Works, services purchased from a non-resident net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Works, services purchased from a non-resident tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase_non_resident': {
                'name': '20% S Non-resident',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'description': 'Non-resident VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Works, services purchased from a non-resident net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Works, services purchased from a non-resident tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Works, services purchased from a non-resident net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Works, services purchased from a non-resident tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_sale_eeu': {
                'name': '12% EEU',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Euroasian Economic Union VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase_eeu': {
                'name': '12% EEU',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Euroasian Economic Union VAT 12%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_0_sale_eeu': {
                'name': '0% EEU',
                'tax_group_id': 'tax_group_vat_0',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Euroasian Economic Union VAT 0%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Sales turnover subject to zero VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Sales turnover subject to zero VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_sale_included_eeu': {
                'name': '12% EEU included',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Euroasian Economic Union VAT 12% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_12_purchase_included_eeu': {
                'name': '12% EEU included',
                'tax_group_id': 'tax_group_vat_12',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Euroasian Economic Union VAT 12% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_sale_included_eeu': {
                'name': '20% EEU included',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Euroasian Economic Union VAT 20% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_sale_eeu': {
                'name': '20% EEU',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Euroasian Economic Union VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz3130',
                        'tag_ids': tags('+Turnover - not in the Republic of Kazakhstan net'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase_included_eeu': {
                'name': '20% EEU included',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Euroasian Economic Union VAT 20% included',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_20_purchase_eeu': {
                'name': '20% EEU',
                'tax_group_id': 'tax_group_vat_20',
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Euroasian Economic Union VAT 20%',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Imports from member states of the EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'kz1420',
                        'tag_ids': tags('+Imports from member states of the EEU tax'),
                    }),
                ],
            },
            'l10n_kz_tax_vat_exempt_sale': {
                'name': 'Exempt',
                'tax_group_id': 'tax_group_vat_exempt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'VAT Exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover exempt from VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover exempt from VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_exempt_purchase': {
                'name': 'Exempt',
                'tax_group_id': 'tax_group_vat_exempt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'VAT Exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Purchases without VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Purchases without VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_exempt_sale_export': {
                'name': 'Exempt EX',
                'tax_group_id': 'tax_group_vat_exempt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Export VAT Exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover exempt from VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover exempt from VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_exempt_purchase_import': {
                'name': 'Exempt EX',
                'tax_group_id': 'tax_group_vat_exempt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Import VAT Exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Exempted imports of goods non-EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Exempted imports of goods non-EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_exempt_sale_eeu': {
                'name': 'Exempt EEU',
                'tax_group_id': 'tax_group_vat_exempt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': 'Euroasian Economic Union VAT Exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover exempt from VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Turnover exempt from VAT net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_kz_tax_vat_exempt_purchase_eeu': {
                'name': 'Exempt EEU',
                'tax_group_id': 'tax_group_vat_exempt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': 'Euroasian Economic Union VAT Exempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Exempted imports of goods EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Exempted imports of goods EEU net'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_kz_fiscal_position(self, template_code):
        return {
            'l10n_kz_fiscal_position_template_national': {
                'sequence': 1,
                'name': 'National',
                'auto_apply': 1,
                'country_id': 'base.kz',
            },
            'l10n_kz_fiscal_position_template_eeu': {
                'sequence': 2,
                'name': 'EEU',
                'auto_apply': 1,
                'country_group_id': 'base.eurasian_economic_union',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_purchase',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_purchase_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_purchase_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_purchase_included_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_purchase',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_purchase_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_purchase_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_purchase_included_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_sale',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_sale_included_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_sale_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_sale_included_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_sale',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_sale_included_eeu',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_sale_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_sale_included_eeu',
                    }),
                ],
            },
            'l10n_kz_fiscal_position_template_international': {
                'sequence': 3,
                'name': 'International',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_purchase',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_purchase_import',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_purchase_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_purchase_included_import',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_purchase',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_purchase_import',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_purchase_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_purchase_included_import',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_sale',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_sale_included_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_12_sale_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_12_sale_included_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_sale',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_sale_included_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_kz_tax_vat_20_sale_included',
                        'tax_dest_id': 'l10n_kz_tax_vat_20_sale_included_export',
                    }),
                ],
            },
        }
