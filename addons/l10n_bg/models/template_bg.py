# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_bg_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_bg_fiscal_position(template_code),
        }

    def _get_bg_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'l10n_bg_411',
            'property_account_payable_id': 'l10n_bg_401',
            'property_account_expense_categ_id': 'l10n_bg_601',
            'property_account_income_categ_id': 'l10n_bg_701',
            'bank_account_code_prefix': '503',
            'cash_account_code_prefix': '501',
            'transfer_account_code_prefix': '430',
            'code_digits': '6',
        }

    def _get_bg_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.bg',
                'income_currency_exchange_account_id': 'l10n_bg_624',
                'expense_currency_exchange_account_id': 'l10n_bg_624',
            },
        }

    def _get_bg_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'l10n_bg_sale_vat_20': {
                'sequence': 101,
                'name': '20% VAT',
                'description': '20% VAT',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
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
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-21'),
                    }),
                ],
            },
            'l10n_bg_sale_vat_20_remote': {
                'sequence': 102,
                'name': '20% Remote',
                'description': '20% Remote',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11', '+18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-11', '-18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-21'),
                    }),
                ],
            },
            'l10n_bg_sale_vat_20_personal': {
                'sequence': 103,
                'name': '20% Personal use',
                'description': '20% Personal use',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+11'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+23'),
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
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-23'),
                    }),
                ],
            },
            'l10n_bg_sale_vat_9': {
                'sequence': 111,
                'name': '9% VAT',
                'description': '9% VAT',
                'price_include': False,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
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
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-24'),
                    }),
                ],
            },
            'l10n_bg_sale_vat_9_personal': {
                'sequence': 112,
                'name': '9% Personal use',
                'description': '9% Personal use',
                'price_include': False,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+13'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
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
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-23'),
                    }),
                ],
            },
            'l10n_bg_sale_vat_0_export': {
                'sequence': 121,
                'name': '0% Export',
                'description': '0% Export',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+14'),
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
                        'tag_ids': tags('-14'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_sale_vat_0_icd': {
                'sequence': 122,
                'name': '0% ICD',
                'description': '0% Intra-Community Deliveries',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
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
            'l10n_bg_sale_vat_0_140': {
                'sequence': 123,
                'name': '0% Art. 140, 146, 173',
                'description': '0% Art. 140, 146, 173',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+16'),
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
                        'tag_ids': tags('-16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_sale_vat_0_21': {
                'sequence': 124,
                'name': '0% Art. 21',
                'description': '0% Art. 21',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+17'),
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
                        'tag_ids': tags('-17'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_sale_vat_0_exempt': {
                'sequence': 125,
                'name': '0% Exempt',
                'description': '0% Exempt',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+19'),
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
                        'tag_ids': tags('-19'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_sale_vat_0_tri': {
                'sequence': 126,
                'name': '0% Tripartite',
                'description': '0% Tripartite',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+18'),
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
                        'tag_ids': tags('-18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ftc': {
                'sequence': 201,
                'name': '20% FTC',
                'description': '20% Foreign Tax Credit',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
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
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ptc': {
                'sequence': 202,
                'name': '20% PTC',
                'description': '20% Payable Tax Credit',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+42'),
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
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-42'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_otc': {
                'sequence': 203,
                'name': '20% OTC',
                'description': '20% Other Tax Credit',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+30'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+30'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-30'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-30'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ftc_exempt': {
                'sequence': 204,
                'name': '20% FTC (Exempt)',
                'description': '20% Foreign Tax Credit – Exempt',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+19', '+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+41'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-19', '-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-41'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+22'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ftc_ica': {
                'sequence': 204,
                'name': '20% FTC (ICA)',
                'description': '20% Foreign Tax Credit – Intra-Community Acquisition',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_1', '+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+41'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_1', '-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-41'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+22'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ftc_82': {
                'sequence': 205,
                'name': '20% FTC (Art. 82)',
                'description': '20% Foreign Tax Credit – Art. 82',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_2', '+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+41'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_2', '-31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-41'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+22'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ptc_exempt': {
                'sequence': 206,
                'name': '20% PTC (Exempt)',
                'description': '20% Payable Tax Credit – Exempt',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+19', '+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+42'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-19', '-32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-42'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+22'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ptc_ica': {
                'sequence': 206,
                'name': '20% PTC (ICA)',
                'description': '20% Payable Tax Credit – Intra-Community Acquisition',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_1', '+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+42'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_1', '-32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-42'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+22'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_20_ptc_82': {
                'sequence': 207,
                'name': '20% PTC (Art. 82)',
                'description': '20% Payable Tax Credit - Art. 82',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+12_2', '+32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+42'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('-22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-12_2', '-32'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-42'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4532',
                        'tag_ids': tags('+22'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_9_ftc': {
                'sequence': 211,
                'name': '9% FTC',
                'description': '9% Foreign Tax Credit',
                'price_include': False,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+31'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
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
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-41'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_9_otc': {
                'sequence': 212,
                'name': '9% OTC',
                'description': '9% Other Tax Credit',
                'price_include': False,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+30'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('+30'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-30'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'l10n_bg_4531',
                        'tag_ids': tags('-30'),
                    }),
                ],
            },
            'l10n_bg_purchase_vat_0_otc_ica': {
                'sequence': 231,
                'name': '0% OTC (ICA)',
                'description': '0% Other Tax Credit – Intra-Community Acquisition',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+19', '+30'),
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
                        'tag_ids': tags('-19', '-30'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_purchase_vat_0_otc_exempt': {
                'sequence': 232,
                'name': '0% OTC (Exempt)',
                'description': '0% Other Tax Credit – Exempt',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+30'),
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
                        'tag_ids': tags('-30'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'l10n_bg_purchase_vat_0_tri': {
                'sequence': 233,
                'name': '0% Tripartite',
                'description': '0% Tripartite',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+18'),
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
                        'tag_ids': tags('-18'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_bg_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_dom': {
                'sequence': 10,
                'name': 'Domestic',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.bg',
            },
            'fiscal_position_bg_private_eu': {
                'name': 'Private EU',
                'sequence': 20,
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_in_eu': {
                'sequence': 30,
                'name': 'Inside EU',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_20',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_icd',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_20_personal',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_icd',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_9',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_icd',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_9_personal',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_icd',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_0_exempt',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_icd',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_purchase_vat_20_otc',
                        'tax_dest_id': 'l10n_bg_purchase_vat_0_otc_ica',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_purchase_vat_20_ftc',
                        'tax_dest_id': 'l10n_bg_purchase_vat_20_ftc_ica',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_purchase_vat_20_ptc',
                        'tax_dest_id': 'l10n_bg_purchase_vat_20_ptc_ica',
                    }),
                ],
            },
            'fiscal_position_template_out_eu': {
                'sequence': 40,
                'name': 'Outside EU',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_20',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_20_personal',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_9',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_sale_vat_0_exempt',
                        'tax_dest_id': 'l10n_bg_sale_vat_0_export',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_purchase_vat_20_otc',
                        'tax_dest_id': 'l10n_bg_purchase_vat_0_otc_exempt',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_purchase_vat_20_ftc',
                        'tax_dest_id': 'l10n_bg_purchase_vat_20_ftc_exempt',
                    }),
                    Command.create({
                        'tax_src_id': 'l10n_bg_purchase_vat_20_ptc',
                        'tax_dest_id': 'l10n_bg_purchase_vat_20_ptc_exempt',
                    }),
                ],
            },
        }
