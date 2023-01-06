# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_hu_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_hu_fiscal_position(template_code),
        }

    def _get_hu_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_hu_311',
            'property_account_payable_id': 'l10n_hu_454',
            'property_account_expense_categ_id': 'l10n_hu_811',
            'property_account_income_categ_id': 'l10n_hu_911',
            'cash_account_code_prefix': '381',
            'bank_account_code_prefix': '384',
            'transfer_account_code_prefix': '389',
            'code_digits': '6',
        }

    def _get_hu_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.hu',
                'income_currency_exchange_account_id': 'l10n_hu_976',
                'expense_currency_exchange_account_id': 'l10n_hu_876',
            },
        }

    def _get_hu_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'F27': {
                'sequence': 10,
                'name': '27% VAT',
                'description': '27% VAT',
                'price_include': False,
                'amount': 27.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_27'),
                    }),
                ],
            },
            'F18': {
                'sequence': 20,
                'name': '18% VAT',
                'description': '18% VAT',
                'price_include': False,
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_18',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_18'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_pay_18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_18'),
                    }),
                ],
            },
            'F5': {
                'sequence': 30,
                'name': '5% VAT',
                'description': '5% VAT',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 5.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_5'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_pay_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_5'),
                    }),
                ],
            },
            'FA': {
                'sequence': 40,
                'name': '0% Subject',
                'description': '0% Subject',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_exempt_tax'),
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
                        'tag_ids': tags('-base_pay_exempt_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FT': {
                'sequence': 50,
                'name': '0% Material',
                'description': '0% Material',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_exempt_property'),
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
                        'tag_ids': tags('-base_pay_exempt_property'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FKKS': {
                'sequence': 60,
                'name': '0% Services Exempt',
                'description': '0% Services Exempt',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_exempt'),
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
                        'tag_ids': tags('-base_pay_exempt'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FKKT': {
                'sequence': 61,
                'name': '0% Goods Exempt',
                'description': '0% Goods Exempt',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_exempt'),
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
                        'tag_ids': tags('-base_pay_exempt'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FF': {
                'sequence': 70,
                'name': '0% VAT (Reverse)',
                'description': '0% VAT (Reverse)',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_reverse'),
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
                        'tag_ids': tags('-base_rec_reverse'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FEUSZ': {
                'sequence': 80,
                'name': '0% Services ICD',
                'description': '0% Services Intra-community Deliveries',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_intra'),
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
                        'tag_ids': tags('-base_pay_intra'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FEUT': {
                'sequence': 81,
                'name': '0% Goods ICD',
                'description': '0% Goods Intra-community Deliveries',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_intra'),
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
                        'tag_ids': tags('-base_pay_intra'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FEXS': {
                'sequence': 90,
                'name': '0% Services Export',
                'description': '0% Services Export',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_exports'),
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
                        'tag_ids': tags('-base_pay_exports'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'FEXT': {
                'sequence': 91,
                'name': '0% Goods Export',
                'description': '0% Goods Export',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_pay_exports'),
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
                        'tag_ids': tags('-base_pay_exports'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'V27': {
                'sequence': 100,
                'name': '27% VAT',
                'description': '27% VAT',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 27.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'V27TE': {
                'sequence': 110,
                'name': '27% Property, plant and equipment',
                'description': '27% Property, plant and equipment',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 27.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'V18': {
                'sequence': 120,
                'name': '18% VAT',
                'description': '18% VAT',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_18',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_18'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_18'),
                    }),
                ],
            },
            'V5': {
                'sequence': 130,
                'name': '5% VAT',
                'description': '5% VAT',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 5.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_5'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_5'),
                    }),
                ],
            },
            'VKOMP7': {
                'sequence': 140,
                'name': '7% Comp.',
                'description': '7% Compensation Surcharge',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_komp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_compensation'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_compensation'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_compensation'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_compensation'),
                    }),
                ],
            },
            'VKOMP12': {
                'sequence': 150,
                'name': '12% Comp.',
                'description': '12% Compensation Surcharge',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_komp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_compensation'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_compensation'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_compensation'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_compensation'),
                    }),
                ],
            },
            'VA': {
                'sequence': 160,
                'name': '0% Subject',
                'description': '0% Subject',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_exempt_tax'),
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
                        'tag_ids': tags('-base_rec_exempt_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VT': {
                'sequence': 170,
                'name': '0% Material',
                'description': '0% Material',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_exempt_material'),
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
                        'tag_ids': tags('-base_rec_exempt_material'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VKKS': {
                'sequence': 180,
                'name': '0% Services Exempt',
                'description': '0% Services Exempt',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_exempt'),
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
                        'tag_ids': tags('-base_rec_exempt'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VKKT': {
                'sequence': 181,
                'name': '0% Goods Exempt',
                'description': '0% Goods Exempt',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_exempt'),
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
                        'tag_ids': tags('-base_rec_exempt'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VF': {
                'sequence': 190,
                'name': '0% VAT (Reverse)',
                'description': '0% VAT (Reverse)',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_reverse'),
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
                        'tag_ids': tags('-base_rec_reverse'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VEU27S': {
                'sequence': 200,
                'name': '27% Services ICA',
                'description': '27% Services Intra-community Acquisition',
                'price_include': False,
                'amount': 27.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'VEU27T': {
                'sequence': 201,
                'name': '27% Goods ICA',
                'description': '27% Goods Intra-community Acquisition',
                'price_include': False,
                'amount': 27.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'VEU27TE': {
                'sequence': 210,
                'name': '27% ICA (Property)',
                'description': '27% ICA (Property)',
                'price_include': False,
                'amount': 27.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'VEUM': {
                'sequence': 220,
                'name': '0% ICA',
                'description': '0% Intra-community Acquisition',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_intra'),
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
                        'tag_ids': tags('-base_rec_intra'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VIMS': {
                'sequence': 230,
                'name': '27% Import',
                'description': '27% Import',
                'price_include': False,
                'amount': 27.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_import'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('+vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_import'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_467',
                        'tag_ids': tags('-vat_pay_27'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'VIMK': {
                'sequence': 240,
                'name': '27% Import (Sourcing)',
                'description': '27% Import (Sourcing)',
                'price_include': False,
                'amount': 27.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_27',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_import'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('+vat_rec_27'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-base_rec_import'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_hu_466',
                        'tag_ids': tags('-vat_rec_27'),
                    }),
                ],
            },
            'VIM': {
                'sequence': 250,
                'name': '0% Import',
                'description': '0% Import',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_afa_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+base_rec_import'),
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
                        'tag_ids': tags('-base_rec_import'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_hu_fiscal_position(self, template_code):
        return {
            'fiscal_position_hu_exempt': {
                'name': 'Exempt taxpayer',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'F27',
                        'tax_dest_id': 'FA',
                    }),
                    Command.create({
                        'tax_src_id': 'F18',
                        'tax_dest_id': 'FA',
                    }),
                    Command.create({
                        'tax_src_id': 'F5',
                        'tax_dest_id': 'FA',
                    }),
                    Command.create({
                        'tax_src_id': 'V27',
                        'tax_dest_id': 'VA',
                    }),
                    Command.create({
                        'tax_src_id': 'V27TE',
                        'tax_dest_id': 'VA',
                    }),
                    Command.create({
                        'tax_src_id': 'V18',
                        'tax_dest_id': 'VA',
                    }),
                    Command.create({
                        'tax_src_id': 'V5',
                        'tax_dest_id': 'VA',
                    }),
                ],
            },
            'fiscal_position_hu_national': {
                'name': 'Domestic',
                'sequence': 10,
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.hu',
            },
            'fiscal_position_hu_eu_private': {
                'name': 'EU partner private',
                'sequence': 20,
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_hu_eu': {
                'name': 'EU partner',
                'sequence': 30,
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'F27',
                        'tax_dest_id': 'FEUT',
                    }),
                    Command.create({
                        'tax_src_id': 'F18',
                        'tax_dest_id': 'FEUT',
                    }),
                    Command.create({
                        'tax_src_id': 'F5',
                        'tax_dest_id': 'FEUT',
                    }),
                    Command.create({
                        'tax_src_id': 'V27',
                        'tax_dest_id': 'VEU27T',
                    }),
                    Command.create({
                        'tax_src_id': 'V27TE',
                        'tax_dest_id': 'VEU27TE',
                    }),
                ],
            },
            'fiscal_position_hu_eu_out': {
                'name': 'Partner outside the EU',
                'sequence': 40,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'F27',
                        'tax_dest_id': 'FEXT',
                    }),
                    Command.create({
                        'tax_src_id': 'F18',
                        'tax_dest_id': 'FEUT',
                    }),
                    Command.create({
                        'tax_src_id': 'F5',
                        'tax_dest_id': 'FEXT',
                    }),
                    Command.create({
                        'tax_src_id': 'V27',
                        'tax_dest_id': 'VIMK',
                    }),
                    Command.create({
                        'tax_src_id': 'V27TE',
                        'tax_dest_id': 'VIMK',
                    }),
                ],
            },
        }
