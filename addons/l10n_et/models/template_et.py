# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_et_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '211',
            'cash_account_code_prefix': '211',
            'transfer_account_code_prefix': '212',
            'property_account_receivable_id': 'l10n_et2211',
            'property_account_payable_id': 'l10n_et3002',
            'property_account_expense_categ_id': 'l10n_et2301',
            'property_account_income_categ_id': 'l10n_et1100',
        }

    def _get_et_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.et',
                'account_default_pos_receivable_account_id': 'l10n_et2215',
                'income_currency_exchange_account_id': 'l10n_et6435',
                'expense_currency_exchange_account_id': 'l10n_et6436',
                'account_journal_early_pay_discount_loss_account_id': 'l10n_et626001',
                'account_journal_early_pay_discount_gain_account_id': 'l10n_et120001',
            },
        }

    def _get_et_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'id_tax03': {
                'name': 'VAT 15% rated sales',
                'description': 'tax03',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Sales VAT Rated 15%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3007',
                        'tag_ids': tags('-Sales VAT Rated 15%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Sales VAT Rated 15%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3007',
                        'tag_ids': tags('+Sales VAT Rated 15%'),
                    }),
                ],
            },
            'id_tax04': {
                'name': 'VAT 0% rated sales',
                'description': 'tax04',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Sales VAT Rated 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Sales VAT Rated 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'id_tax06': {
                'name': 'VAT Exempt rated sales',
                'description': 'tax06',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Sales VAT Exempt'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Sales VAT Exempt'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'id_tax11': {
                'name': 'VAT Out of Scope rated sales',
                'description': 'tax11',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Sales VAT Out of Scope (Sales)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Sales VAT Out of Scope (Sales)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'id_tax02': {
                'name': 'Withholding 2% rated sales',
                'amount': -2.0,
                'amount_type': 'percent',
                'description': 'tax02',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_withh_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable 2% Withholding on Sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3006',
                        'tag_ids': tags('-2% Withheld on Sales'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable 2% Withholding on Sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3006',
                        'tag_ids': tags('+2% Withheld on Sales'),
                    }),
                ],
            },
            'id_tax13': {
                'name': 'Withholding 35% rated sales',
                'description': 'tax13',
                'amount': -35.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_withh_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable 35% Withholding on Sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3006',
                        'tag_ids': tags('+35% Withheld on Sales'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable 35% Withholding on Sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3006',
                        'tag_ids': tags('-35% Withheld on Sales'),
                    }),
                ],
            },
            'id_tax14': {
                'name': 'Withholding VAT 15% rated sales',
                'description': 'tax14',
                'amount': -15.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_withh_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable VAT Withholding on Sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3006',
                        'tag_ids': tags('+VAT Withheld on Sales'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable VAT Withholding on Sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et3006',
                        'tag_ids': tags('-VAT Withheld on Sales'),
                    }),
                ],
            },
            'id_tax08': {
                'name': 'VAT 15% rated purchases',
                'description': 'tax08',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Purchase VAT Rated 15%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et2212',
                        'tag_ids': tags('+Purchase VAT Rated 15%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Purchase VAT Rated 15%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et2212',
                        'tag_ids': tags('-Purchase VAT Rated 15%'),
                    }),
                ],
            },
            'id_tax07': {
                'name': 'VAT 0% rated purchases',
                'description': 'tax07',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Purchase VAT Rated 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Purchase VAT Rated 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'id_tax10': {
                'name': 'VAT Exempt rated purchases',
                'description': 'tax10',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Purchase VAT Exempt'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Purchase VAT Exempt'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'id_tax09': {
                'name': 'VAT Out of Scope rated purchases',
                'description': 'tax09',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable Purchase VAT Out of Scope'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable Purchase VAT Out of Scope'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'id_tax05': {
                'name': 'Withholding 2% rated purchases',
                'description': 'tax05',
                'amount': -2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_withh_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable 2% Withholding on Purchases'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et2213',
                        'tag_ids': tags('+2% Withholding on Purchases'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable 2% Withholding on Purchases'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et2213',
                        'tag_ids': tags('-2% Withholding on Purchases'),
                    }),
                ],
            },
            'id_tax12': {
                'name': 'Withholding 35% rated purchases',
                'description': 'tax12',
                'amount': -35.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_withh_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Taxable 35% Withholding on Purchases'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et2213',
                        'tag_ids': tags('+35% Withholding on Purchases'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Taxable 35% Withholding on Purchases'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'l10n_et2213',
                        'tag_ids': tags('-35% Withholding on Purchases'),
                    }),
                ],
            },
        }
