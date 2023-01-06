# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_de_skr03_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_de_skr03_fiscal_position(template_code),
            'account.reconcile.model': self._get_de_skr03_reconcile_model(template_code),
        }

    def _get_de_skr03_template_data(self, template_code):
        return {
            'code_digits': '4',
            'property_account_receivable_id': 'account_1410',
            'property_account_payable_id': 'account_1610',
            'property_account_expense_categ_id': 'account_3400',
            'property_account_income_categ_id': 'account_8400',
            'property_stock_account_input_categ_id': 'account_3970',
            'property_stock_account_output_categ_id': 'account_3980',
            'property_stock_valuation_account_id': 'account_3960',
            'property_tax_payable_account_id': 'account_1797',
            'property_tax_receivable_account_id': 'account_1545',
            'property_advance_tax_payment_account_id': 'account_1780',
            'cash_account_code_prefix': '100',
            'bank_account_code_prefix': '120',
            'transfer_account_code_prefix': '1360',
        }

    def _get_de_skr03_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.de',
                'account_default_pos_receivable_account_id': 'account_1411',
                'income_currency_exchange_account_id': 'account_2660',
                'expense_currency_exchange_account_id': 'account_2150',
                'account_journal_early_pay_discount_loss_account_id': 'account_2130',
                'account_journal_early_pay_discount_gain_account_id': 'account_2670',
            },
        }

    def _get_de_skr03_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_eu_19_purchase_skr03': {
                'sequence': 20,
                'name': 'Intragem. Acquisition 19%USt/19%VSt',
                'description': 'Intragem. Acquisition 19%',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+89_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1774',
                        'tag_ids': tags('-89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1574',
                        'tag_ids': tags('-61'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-89_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1774',
                        'tag_ids': tags('+89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1574',
                        'tag_ids': tags('+61'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_7_purchase_skr03': {
                'sequence': 25,
                'name': 'Intragem. Acquisition 7%USt/7%VSt',
                'description': 'Intragem. Acquisition 7%',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+93_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1772',
                        'tag_ids': tags('-93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1572',
                        'tag_ids': tags('-61'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-93_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1772',
                        'tag_ids': tags('+93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1572',
                        'tag_ids': tags('+61'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_19_purchase_no_vst_skr03': {
                'sequence': 20,
                'name': 'Intragem. Acquisition 19%USt/0%VSt',
                'description': 'Intragem. Acquisition 19% - 0% input tax',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+89_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1779',
                        'tag_ids': tags('-89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-89_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1779',
                        'tag_ids': tags('+89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_eu_7_purchase_no_vst_skr03': {
                'sequence': 20,
                'name': 'Intragem. Acquisition 7%USt/0%VSt',
                'description': 'Intragem. Acquisition 7% - 0% input tax',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+93_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1779',
                        'tag_ids': tags('-93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-93_BASE'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1779',
                        'tag_ids': tags('+93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_eu_car_purchase_skr03': {
                'sequence': 23,
                'name': 'Intragem. Acquisition of new vehicle 19%USt/19%VSt',
                'description': 'Intragem. Acquisition new vehicle 19%',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+94'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1772',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1572',
                        'tag_ids': tags('-59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-94'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1772',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1572',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_sale_skr03': {
                'sequence': 21,
                'name': 'Tax-exempt intra-Community. Delivery (§4 para. 1b UStG)',
                'description': 'Tax free intracomm. Delivery',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+41'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-41'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_export_skr03': {
                'sequence': 22,
                'name': 'Tax-free export (§4 No. 1a UStG)',
                'description': 'Tax free export',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+43'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-43'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_free_skr03_mit_vst': {
                'sequence': 23,
                'name': 'Tax-exempt turnover with input tax deduction (§ 4 No. 2-7)',
                'description': 'Taxable turnover(§ 4 No. 2-7)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+43'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-43'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_free_skr03_ohne_vst': {
                'sequence': 24,
                'name': 'Tax-exempt turnover without deduction of input tax (§ 4 No. 8-28)',
                'description': 'Taxable turnover(§ 4 No. 8-28)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-48'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+48'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_import_19_and_payable_skr03': {
                'sequence': 21,
                'name': '19% import sales tax (§21 Abs.3 UstG)',
                'description': 'Import sales tax 19%',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1588',
                        'tag_ids': tags('-62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1788',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1588',
                        'tag_ids': tags('+62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1788',
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_import_7_and_payable_skr03': {
                'sequence': 21,
                'name': '7% import sales tax (§21 Abs.3 UstG)',
                'description': 'Import sales tax 7%',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1588',
                        'tag_ids': tags('-62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1788',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1588',
                        'tag_ids': tags('+62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1788',
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_eu_purchase_tax_free_skr03': {
                'sequence': 22,
                'name': 'Tax-free intracompany Acquisition (§§ 4b and 25c UStG)',
                'description': 'Tax-free intracompany Acquisition (§§ 4b and 25c UStG)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-91'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+91'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_not_taxable_skr03': {
                'sequence': 20,
                'name': 'Non-taxable turnover',
                'description': 'Non-taxable turnover',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+45_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-45_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_skr03': {
                'sequence': 10,
                'name': '19% sales tax',
                'description': '19% VAT',
                'amount_type': 'percent',
                'amount': 19.0,
                'l10n_de_datev_code': '3',
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1776',
                        'tag_ids': tags('+81_TAX'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1776',
                        'tag_ids': tags('-81_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_ust_7_skr03': {
                'sequence': 15,
                'name': '7% sales tax',
                'description': '7% VAT',
                'amount_type': 'percent',
                'amount': 7.0,
                'l10n_de_datev_code': '2',
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+86_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1771',
                        'tag_ids': tags('+86_TAX'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-86_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1771',
                        'tag_ids': tags('-86_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_ust_no_ustpflicht_skr03': {
                'sequence': 16,
                'name': '0% VAT (compulsory exemption e.g. as a small business or for medical services)',
                'description': '0% VAT (exempt from duty)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_taxinclusive_skr03': {
                'sequence': 17,
                'name': '19% sales tax (included in price)',
                'description': '19% VAT (included in price)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1776',
                        'tag_ids': tags('+81_TAX'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1776',
                        'tag_ids': tags('-81_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_ust_7_taxinclusive_skr03': {
                'sequence': 18,
                'name': '7% sales tax (included in price)',
                'description': '7% VAT (included in price)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+86_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1771',
                        'tag_ids': tags('+86_TAX'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-86_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1771',
                        'tag_ids': tags('-86_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_ust_55_farmer_skr03': {
                'sequence': 26,
                'name': '5.5 % Sales tax agriculture/forestry',
                'description': '5.5% VAT agriculture/forestry',
                'amount_type': 'percent',
                'amount': 5.5,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+77'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1770',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-77'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1770',
                    }),
                ],
                'tax_group_id': 'tax_group_55',
            },
            'tax_ust_107_farmer_skr03': {
                'sequence': 27,
                'name': '10,7 % Umsatzsteuer Land-/Forstwirtschaft',
                'description': '10.7 % Sales tax agriculture/forestry',
                'amount_type': 'percent',
                'amount': 10.7,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+77'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1770',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-77'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1770',
                    }),
                ],
                'tax_group_id': 'tax_group_107',
            },
            'tax_ust_19_farmer_skr03': {
                'sequence': 28,
                'name': '19% sales tax agriculture/forestry (alcohol etc.)',
                'description': '19% VAT agriculture/forestry (alcohol etc.)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+76'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1776',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-76'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1776',
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_ust_x_skr03': {
                'sequence': 21,
                'name': 'x% Sales tax (at other tax rates)',
                'description': 'x% VAT (at other tax rates)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+35'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-35'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_x',
            },
            'tax_vst_19_skr03': {
                'sequence': 10,
                'name': '19% input tax',
                'description': '19% VAT',
                'amount_type': 'percent',
                'amount': 19.0,
                'l10n_de_datev_code': '9',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_vst_7_skr03': {
                'sequence': 15,
                'name': '7% input tax',
                'description': '7% VAT',
                'amount_type': 'percent',
                'amount': 7.0,
                'l10n_de_datev_code': '8',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1571',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1571',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_vst_no_ustpflicht_skr03': {
                'sequence': 16,
                'name': '0% VAT (compulsory exemption e.g. as a small business or for medical services)',
                'description': '0% VAT (exempt from duty)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_19_taxinclusive_skr03': {
                'sequence': 16,
                'name': '19% input tax (included in price)',
                'description': '19% VAT (included in price)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
                'price_include': True,
            },
            'tax_vst_7_taxinclusive_skr03': {
                'sequence': 17,
                'name': '7% input tax (included in price)',
                'description': '7% VAT (included in price)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1571',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1571',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
                'price_include': True,
            },
            'tax_vst_55_farmer_skr03': {
                'sequence': 26,
                'name': '5.5% Input tax agriculture/forestry',
                'description': '5.5% VAT agriculture/forestry',
                'amount_type': 'percent',
                'amount': 5.5,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1570',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1570',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_55',
            },
            'tax_vst_107_farmer_skr03': {
                'sequence': 27,
                'name': '10.7% Input tax agriculture/forestry',
                'description': '10.7% VAT agriculture/forestry',
                'amount_type': 'percent',
                'amount': 10.7,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1570',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1570',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_107',
            },
            'tax_ust_19_eu_skr03': {
                'sequence': 21,
                'name': '19% VAT EU delivery',
                'description': '19% VAT EU',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1778',
                        'tag_ids': tags('+81_TAX'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1778',
                        'tag_ids': tags('-81_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_eu_skr03': {
                'sequence': 22,
                'name': '7% VAT EU delivery',
                'description': '7% USt EU',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+86_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1777',
                        'tag_ids': tags('+86_TAX'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-86_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1777',
                        'tag_ids': tags('-86_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_13b_ausland_ohne_vst_skr03': {
                'sequence': 23,
                'name': '19% VAT according to §13b UStG - without VAT - (foreign work deliveries etc.)',
                'description': '19% VAT EU acc. to §13b UStG - without VAT - (foreign work deliveries etc.)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_7_13b_ausland_ohne_vst_skr03': {
                'sequence': 24,
                'name': '7% VAT according to §13b UStG - without VAT - (foreign work deliveries etc.)',
                'description': '7% VAT EU acc. to §13b UStG - without VAT - (foreign work deliveries etc.)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_13b_eu_ohne_vst_skr03': {
                'sequence': 25,
                'name': '19% VAT acc. to §13b UStG - without VAT - (other services EU)',
                'description': '19% VAT EU acc. to §13b UStG - without VAT - (other services EU)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_7_13b_eu_ohne_vst_skr03': {
                'sequence': 26,
                'name': '7% VAT according to §13b UStG - without VAT - (other services EU)',
                'description': '7% EU VAT according to §13b UStG - without VAT - (other EU services)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_13b_bau_ohne_vst_skr03': {
                'sequence': 27,
                'name': '19% VAT according to §13b UStG - without VAT - (recommended construction services)',
                'description': '19% EU VAT according to §13b UStG - without VAT - (recommended construction services)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_7_13b_bau_ohne_vst_skr03': {
                'sequence': 28,
                'name': '7% VAT according to §13b UStG - without VAT - (recommended construction services)',
                'description': '7% EU VAT according to §13b UStG - without VAT - (recommended construction services)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_free_eu_skr03': {
                'sequence': 20,
                'name': '0% Tax-free benefit EU',
                'description': '0% VAT EU',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-21'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_free_third_country_skr03': {
                'sequence': 20,
                'name': '0% Tax-exempt service third country',
                'description': '0% VAT third country',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+45_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-45_BASE'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_free_newcar_skr03': {
                'sequence': 30,
                'name': '0% Tax-free new vehicle delivery EU',
                'description': '0% VAT new vehicle EU',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+44'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-44'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_3eck_first_skr03': {
                'sequence': 40,
                'name': '0% Sales tax triangular transaction first customer',
                'description': '0% VAT triangular transaction first customer',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-42'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+42'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_free_bau_skr03': {
                'sequence': 50,
                'name': '0% Sales tax construction service (provider §13b)',
                'description': '0% Sales tax construction service (provider §13b)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+60'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-60'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_free_mobil_skr03': {
                'sequence': 50,
                'name': '0% VAT Supply of mobile telephones, etc. (§13b)',
                'description': '0% VAT Supply of mobile devices etc. (§13b)',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-68'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+68'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_19_purchase_goods_skr03': {
                'sequence': 20,
                'name': 'Taxable other services EU 19%USt/19%VSt',
                'description': 'Services EU 19%VAT/19%VAT',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1768',
                        'tag_ids': tags('-47'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1768',
                        'tag_ids': tags('+47'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_7_purchase_goods_skr03': {
                'sequence': 21,
                'name': 'Taxable other services EU 7%USt/7%VSt',
                'description': 'Tax ppl. Services EU 7%Tax/7%VAT',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1768',
                        'tag_ids': tags('-47'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1768',
                        'tag_ids': tags('+47'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_vst_19_purchase_13b_bau_skr03': {
                'sequence': 22,
                'name': 'Tax according to §13b UStG 19%USt/19%VSt (construction service recipient)',
                'description': 'Tax according to §13b UStG 19%USt/19%VSt (construction service recipient)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                        'tag_ids': tags('-85'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                        'tag_ids': tags('+85'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_vst_7_purchase_13b_bau_skr03': {
                'sequence': 23,
                'name': 'Tax according to §13b UStG 7%USt/7%VSt (construction service recipient)',
                'description': 'Tax according to §13b UStG 7%USt/7%VSt (construction service recipient)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1578',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                        'tag_ids': tags('-85'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1578',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1785',
                        'tag_ids': tags('+85'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_13b_mobil_skr03': {
                'sequence': 24,
                'name': 'Tax according to §13b 19%USt/19%VSt (reception of mobile devices etc.)',
                'description': 'Tax according to §13b 19%Ust/19%VSt (reception of mobile devices etc.)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+78'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                        'tag_ids': tags('-79'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-78'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1577',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1787',
                        'tag_ids': tags('+79'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_3eck_last_skr03': {
                'sequence': 105,
                'name': 'Triangular transaction Acquisition of last customer 19%USt/19%VSt',
                'description': 'Triangular transaction Acquisition of last customer 19%VAT/19%VAT',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('-69'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('+69'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_13b_werk_ausland_skr03': {
                'sequence': 25,
                'name': 'Tax acc. to §13b 19%USt/19%VSt (foreign work deliveries etc.)',
                'description': 'Tax acc. to §13b 19%USt/19%VSt (foreign work deliveries etc.)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('-53'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1576',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('+53'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_7_purchase_13b_werk_ausland_skr03': {
                'sequence': 26,
                'name': 'Tax acc. to §13b 7%USt/7%VSt (foreign work deliveries etc.)',
                'description': 'Tax acc. to §13b 7%USt/7%VSt (foreign work deliveries etc.)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1571',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('-53'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1571',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('+53'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_13a_auslagerung_skr03': {
                'sequence': 27,
                'name': 'Tax acc. to §13a para. 1 no. 6 UStG 19%USt/19%VSt (outsourcing)',
                'description': 'Tax acc. to §13a para. 1 no. 6 UStG 19%USt/19%VSt (outsourcing)',
                'amount_type': 'percent',
                'amount': 19.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1585',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('-69'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1585',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('+69'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_7_purchase_13a_auslagerung_skr03': {
                'sequence': 28,
                'name': 'Tax acc. to §13a Abs. 1 Nr. 6 UStG 7%USt/7%VSt (outsourcing)',
                'description': 'Tax acc. to §13a Abs. 1 Nr. 6 UStG 7%USt/7VSt (outsourcing)',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1585',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('-69'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1585',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_1783',
                        'tag_ids': tags('+69'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
        }

    def _get_de_skr03_fiscal_position(self, template_code):
        return {
            'fiscal_position_domestic_skr03': {
                'sequence': 1,
                'name': 'Domestic business partner',
                'auto_apply': 1,
                'country_id': 'base.de',
            },
            'fiscal_position_non_eu_partner_service_skr03': {
                'sequence': 6,
                'name': 'Service provider abroad (non-EU)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_free_third_country_skr03',
                        'tax_src_id': 'tax_ust_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_vst_ust_19_purchase_13b_werk_ausland_skr03',
                        'tax_src_id': 'tax_vst_19_skr03',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_8400',
                        'account_dest_id': 'account_8338',
                    }),
                    Command.create({
                        'account_src_id': 'account_3400',
                        'account_dest_id': 'account_3125',
                    }),
                ],
            },
            'fiscal_position_non_eu_partner_skr03': {
                'sequence': 5,
                'name': 'Business partner abroad (non-EU)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_export_skr03',
                        'tax_src_id': 'tax_ust_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_export_skr03',
                        'tax_src_id': 'tax_ust_7_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_import_19_and_payable_skr03',
                        'tax_src_id': 'tax_vst_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_import_7_and_payable_skr03',
                        'tax_src_id': 'tax_vst_7_skr03',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_8400',
                        'account_dest_id': 'account_8120',
                    }),
                    Command.create({
                        'account_src_id': 'account_8300',
                        'account_dest_id': 'account_8120',
                    }),
                    Command.create({
                        'account_src_id': 'account_3400',
                        'account_dest_id': 'account_3551',
                    }),
                    Command.create({
                        'account_src_id': 'account_3300',
                        'account_dest_id': 'account_3557',
                    }),
                ],
            },
            'fiscal_position_eu_vat_id_partner_skr03': {
                'sequence': 2,
                'name': 'Business partner EU (with VAT ID)',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_eu_sale_skr03',
                        'tax_src_id': 'tax_ust_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_sale_skr03',
                        'tax_src_id': 'tax_ust_7_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_19_purchase_skr03',
                        'tax_src_id': 'tax_vst_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_7_purchase_skr03',
                        'tax_src_id': 'tax_vst_7_skr03',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_2401',
                        'account_dest_id': 'account_2402',
                    }),
                    Command.create({
                        'account_src_id': 'account_2406',
                        'account_dest_id': 'account_2402',
                    }),
                    Command.create({
                        'account_src_id': 'account_2431',
                        'account_dest_id': 'account_2430',
                    }),
                    Command.create({
                        'account_src_id': 'account_2436',
                        'account_dest_id': 'account_2430',
                    }),
                    Command.create({
                        'account_src_id': 'account_8400',
                        'account_dest_id': 'account_8125',
                    }),
                    Command.create({
                        'account_src_id': 'account_8300',
                        'account_dest_id': 'account_8125',
                    }),
                    Command.create({
                        'account_src_id': 'account_3400',
                        'account_dest_id': 'account_3425',
                    }),
                    Command.create({
                        'account_src_id': 'account_3300',
                        'account_dest_id': 'account_3420',
                    }),
                ],
            },
            'fiscal_position_eu_vat_id_partner_service_skr03': {
                'sequence': 3,
                'name': 'Service provider EU (with VAT ID)',
                'vat_required': 1,
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_eu_19_purchase_goods_skr03',
                        'tax_src_id': 'tax_vst_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_7_purchase_goods_skr03',
                        'tax_src_id': 'tax_vst_7_skr03',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_3400',
                        'account_dest_id': 'account_3123',
                    }),
                    Command.create({
                        'account_src_id': 'account_3300',
                        'account_dest_id': 'account_3113',
                    }),
                ],
            },
            'fiscal_position_eu_no_id_partner_skr03': {
                'sequence': 4,
                'name': 'Business partner EU (without VAT ID)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_eu_19_purchase_no_vst_skr03',
                        'tax_src_id': 'tax_vst_19_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_ust_eu_skr03',
                        'tax_src_id': 'tax_ust_7_skr03',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_ust_19_eu_skr03',
                        'tax_src_id': 'tax_ust_19_skr03',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_2401',
                        'account_dest_id': 'account_2403',
                    }),
                    Command.create({
                        'account_src_id': 'account_2406',
                        'account_dest_id': 'account_2408',
                    }),
                    Command.create({
                        'account_src_id': 'account_2431',
                        'account_dest_id': 'account_2430',
                    }),
                    Command.create({
                        'account_src_id': 'account_2436',
                        'account_dest_id': 'account_2430',
                    }),
                    Command.create({
                        'account_src_id': 'account_8400',
                        'account_dest_id': 'account_8315',
                    }),
                    Command.create({
                        'account_src_id': 'account_8300',
                        'account_dest_id': 'account_8310',
                    }),
                    Command.create({
                        'account_src_id': 'account_3400',
                        'account_dest_id': 'account_3435',
                    }),
                    Command.create({
                        'account_src_id': 'account_3300',
                        'account_dest_id': 'account_3430',
                    }),
                ],
            },
        }

    def _get_de_skr03_reconcile_model(self, template_code):
        return {
            'reconcile_3731': {
                'name': 'Discount-EK-7%',
                'line_ids': [
                    Command.create({
                        'account_id': 'account_3731',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr03.tax_vst_7_taxinclusive_skr03',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-EK-7%',
                    }),
                ],
            },
            'reconcile_3736': {
                'name': 'Discount-EK-19%',
                'line_ids': [
                    Command.create({
                        'account_id': 'account_3736',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr03.tax_vst_19_taxinclusive_skr03',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-EK-19%',
                    }),
                ],
            },
            'reconcile_8731': {
                'name': 'Discount-VK-7%',
                'line_ids': [
                    Command.create({
                        'account_id': 'account_8731',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr03.tax_ust_7_taxinclusive_skr03',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-VK-7%',
                    }),
                ],
            },
            'reconcile_8736': {
                'name': 'Discount-VK-19%',
                'line_ids': [
                    Command.create({
                        'account_id': 'account_8736',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr03.tax_ust_19_taxinclusive_skr03',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-VK-19%',
                    }),
                ],
            },
            'reconcile_2401': {
                'name': 'Loss of receivables-7%',
                'line_ids': [
                    Command.create({
                        'account_id': 'account_2401',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr03.tax_ust_7_taxinclusive_skr03',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Loss of receivables-7%',
                    }),
                ],
            },
            'reconcile_2406': {
                'name': 'Loss of receivables-19%',
                'line_ids': [
                    Command.create({
                        'account_id': 'account_2406',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr03.tax_ust_19_taxinclusive_skr03',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Loss of receivables-19%',
                    }),
                ],
            },
        }
