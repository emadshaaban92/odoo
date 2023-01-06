# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_de_skr04_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_de_skr04_fiscal_position(template_code),
            'account.reconcile.model': self._get_de_skr04_reconcile_model(template_code),
        }

    def _get_de_skr04_template_data(self, template_code):
        return {
            'cash_account_code_prefix': '160',
            'bank_account_code_prefix': '180',
            'transfer_account_code_prefix': '1460',
            'code_digits': '4',
            'property_account_receivable_id': 'chart_skr04_1205',
            'property_account_payable_id': 'chart_skr04_3301',
            'property_account_expense_categ_id': 'chart_skr04_5400',
            'property_account_income_categ_id': 'chart_skr04_4400',
            'property_tax_payable_account_id': 'chart_skr04_3860',
            'property_tax_receivable_account_id': 'chart_skr04_1421',
            'property_advance_tax_payment_account_id': 'chart_skr04_3820',
        }

    def _get_de_skr04_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.de',
                'account_default_pos_receivable_account_id': 'chart_skr04_1206',
                'income_currency_exchange_account_id': 'chart_skr04_4840',
                'expense_currency_exchange_account_id': 'chart_skr04_6880',
                'account_journal_early_pay_discount_loss_account_id': 'chart_skr04_4730',
                'account_journal_early_pay_discount_gain_account_id': 'chart_skr04_5730',
            },
        }

    def _get_de_skr04_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_eu_19_purchase_skr04': {
                'sequence': 20,
                'name': 'Intragem. Acquisition 19%VAT/19%VSt',
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
                        'account_id': 'chart_skr04_3804',
                        'tag_ids': tags('-89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1404',
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
                        'account_id': 'chart_skr04_3804',
                        'tag_ids': tags('+89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1404',
                        'tag_ids': tags('+61'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_7_purchase_skr04': {
                'sequence': 25,
                'name': 'Intragem. Acquisition 7%VAT/7%VSt',
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
                        'account_id': 'chart_skr04_3802',
                        'tag_ids': tags('-93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1402',
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
                        'account_id': 'chart_skr04_3802',
                        'tag_ids': tags('+93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1402',
                        'tag_ids': tags('+61'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_19_purchase_no_vst_skr04': {
                'sequence': 20,
                'name': 'Intragem. Acquisition 19%VAT/0%VSt',
                'description': 'Intragem. Acquisition 19% - 0% Input tax',
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
                        'account_id': 'chart_skr04_3809',
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
                        'account_id': 'chart_skr04_3809',
                        'tag_ids': tags('+89_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_eu_7_purchase_no_vst_skr04': {
                'sequence': 20,
                'name': 'Intragem. Acquisition 7%VAT/0%VSt',
                'description': 'Intragem. Acquisition 7% - 0% Input tax',
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
                        'account_id': 'chart_skr04_3809',
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
                        'account_id': 'chart_skr04_3809',
                        'tag_ids': tags('+93_TAX'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_eu_car_purchase_skr04': {
                'sequence': 23,
                'name': 'Intra. Acquisition of new vehicle 19%VAT/19%VSt',
                'description': 'Intra. Acquisition of new vehicle 19%',
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
                        'account_id': 'chart_skr04_3802',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1402',
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
                        'account_id': 'chart_skr04_3802',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1402',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_sale_skr04': {
                'sequence': 21,
                'name': 'Tax free intracomm. Delivery (§4 Abs. 1b UStG)',
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
            'tax_export_skr04': {
                'sequence': 22,
                'name': 'Tax free export (§4 Nr. 1a UStG)',
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
            'tax_free_skr04_mit_vst': {
                'sequence': 23,
                'name': 'Tax-exempt turnover with input tax deduction (§ 4 Nr. 2-7)',
                'description': 'Tax-free turnover(§ 4 Nr. 2-7)',
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
            'tax_free_skr04_ohne_vst': {
                'sequence': 24,
                'name': 'Tax-exempt turnover without input tax deduction (§ 4 Nr. 8-28)',
                'description': 'Tax-free turnover(§ 4 Nr. 8-28)',
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
            'tax_import_19_and_payable_skr04': {
                'sequence': 21,
                'name': '19% Import sales tax (§21 Abs.3 UstG)',
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
                        'account_id': 'chart_skr04_1433',
                        'tag_ids': tags('-62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3850',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1433',
                        'tag_ids': tags('+62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3850',
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_import_7_and_payable_skr04': {
                'sequence': 21,
                'name': '7% Import sales tax (§21 Abs.3 UstG)',
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
                        'account_id': 'chart_skr04_1433',
                        'tag_ids': tags('-62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3850',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1433',
                        'tag_ids': tags('+62'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3850',
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_eu_purchase_tax_free_skr04': {
                'sequence': 22,
                'name': 'Tax-free intracompany Acquisition (§§ 4b und 25c UStG)',
                'description': 'Tax-free intracompany Acquisition (§§ 4b und 25c UStG)',
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
            'tax_not_taxable_skr04': {
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
            'tax_ust_19_skr04': {
                'sequence': 10,
                'name': '19% Sales tax',
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
                        'account_id': 'chart_skr04_3806',
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
                        'account_id': 'chart_skr04_3806',
                        'tag_ids': tags('-81_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_ust_7_skr04': {
                'sequence': 15,
                'name': '7% Sales tax',
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
                        'account_id': 'chart_skr04_3801',
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
                        'account_id': 'chart_skr04_3801',
                        'tag_ids': tags('-86_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_ust_no_ustpflicht_skr04': {
                'sequence': 16,
                'name': '0% VAT (Compulsory exemption e.g. as a small business or for medical services.)',
                'description': '0% VAT (Mandatory Exempt)',
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
            'tax_ust_19_taxinclusive_skr04': {
                'sequence': 17,
                'name': '19% Value added tax (included in price)',
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
                        'account_id': 'chart_skr04_3806',
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
                        'account_id': 'chart_skr04_3806',
                        'tag_ids': tags('-81_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_ust_7_taxinclusive_skr04': {
                'sequence': 18,
                'name': '7% Value added tax (included in price)',
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
                        'account_id': 'chart_skr04_3801',
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
                        'account_id': 'chart_skr04_3801',
                        'tag_ids': tags('-86_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_ust_55_farmer_skr04': {
                'sequence': 26,
                'name': '5,5 % Sales tax agriculture/forestry',
                'description': '5,5% VAT Agriculture/Forestry',
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
                        'account_id': 'chart_skr04_3800',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-77'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3800',
                    }),
                ],
                'tax_group_id': 'tax_group_55',
            },
            'tax_ust_107_farmer_skr04': {
                'sequence': 27,
                'name': '10,7 % Sales tax agriculture/forestry',
                'description': '10,7% VAT agriculture/forestry',
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
                        'account_id': 'chart_skr04_3800',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-77'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3800',
                    }),
                ],
                'tax_group_id': 'tax_group_107',
            },
            'tax_ust_19_farmer_skr04': {
                'sequence': 28,
                'name': '19% Sales tax agriculture/forestry (alcohol etc.)',
                'description': '19% Sales tax agriculture/forestry (alcohol etc.)',
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
                        'account_id': 'chart_skr04_3806',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-76'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3806',
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_ust_x_skr04': {
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
            'tax_vst_19_skr04': {
                'sequence': 10,
                'name': '19% Input tax',
                'description': '19% VSt',
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
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
            },
            'tax_vst_7_skr04': {
                'sequence': 15,
                'name': '7% Input tax',
                'description': '7% VSt',
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
                        'account_id': 'chart_skr04_1401',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1401',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
            },
            'tax_vst_no_ustpflicht_skr04': {
                'sequence': 16,
                'name': '0% VSt (Compulsory exemption e.g. as a small business or for medical services.)',
                'description': '0% VSt (Mandatory Exempt)',
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
            'tax_vst_19_taxinclusive_skr04': {
                'sequence': 16,
                'name': '19% Input tax (included in price)',
                'description': '19% VSt (included in price)',
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
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_19',
                'price_include': True,
            },
            'tax_vst_7_taxinclusive_skr04': {
                'sequence': 17,
                'name': '7% Input tax (included in price)',
                'description': '7% VSt (included in price)',
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
                        'account_id': 'chart_skr04_1401',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1401',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_7',
                'price_include': True,
            },
            'tax_vst_55_farmer_skr04': {
                'sequence': 26,
                'name': '5,5% Input tax agriculture/forestry',
                'description': '5,5% VSt agriculture/forestry',
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
                        'account_id': 'chart_skr04_1400',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1400',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_55',
            },
            'tax_vst_107_farmer_skr04': {
                'sequence': 27,
                'name': '10,7% Input tax agriculture/forestry',
                'description': '10,7% VSt agriculture/forestry',
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
                        'account_id': 'chart_skr04_1400',
                        'tag_ids': tags('-66'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1400',
                        'tag_ids': tags('+66'),
                    }),
                ],
                'tax_group_id': 'tax_group_107',
            },
            'tax_ust_19_eu_skr04': {
                'sequence': 21,
                'name': '19 % VAT EU delivery',
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
                        'account_id': 'chart_skr04_3808',
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
                        'account_id': 'chart_skr04_3808',
                        'tag_ids': tags('-81_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_eu_skr04': {
                'sequence': 22,
                'name': '7% VAT EU delivery',
                'description': '7% VAT EU',
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
                        'account_id': 'chart_skr04_3807',
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
                        'account_id': 'chart_skr04_3807',
                        'tag_ids': tags('-86_TAX'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_13b_ausland_ohne_vst_skr04': {
                'sequence': 23,
                'name': '19% VAT according to §13b UStG - without VAT - (foreign supplies of goods and services, etc.)',
                'description': '19% VAT EU according to §13b UStG - without VAT - (foreign supplies of goods and services, etc.)',
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
                        'account_id': 'chart_skr04_3837',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_7_13b_ausland_ohne_vst_skr04': {
                'sequence': 24,
                'name': '7% VAT according to §13b UStG - without VAT - (foreign supplies of goods and services, etc.)',
                'description': '7% VAT EU according to §13b UStG - without VAT - (foreign supplies of goods and services, etc.)',
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
                        'account_id': 'chart_skr04_3835',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-52'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3835',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_13b_eu_ohne_vst_skr04': {
                'sequence': 25,
                'name': '19% VAT according to §13b UStG - without VAT - (other services EU)',
                'description': '19% VAT EU according to §13b UStG - without VAT - (other services EU)',
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
                        'account_id': 'chart_skr04_3837',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_7_13b_eu_ohne_vst_skr04': {
                'sequence': 26,
                'name': '7% VAT according to §13b UStG - without VAT - (other services EU)',
                'description': '7% VAT EU according to §13b UStG - without VAT - (other services EU)',
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
                        'account_id': 'chart_skr04_3835',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-46'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3835',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_19_13b_bau_ohne_vst_skr04': {
                'sequence': 27,
                'name': '19% VAT according to §13b UStG - without VAT - (rec. Construction work)',
                'description': '19% VAT EU according to §13b UStG - without VAT - (rec. Construction work)',
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
                        'account_id': 'chart_skr04_3837',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_7_13b_bau_ohne_vst_skr04': {
                'sequence': 28,
                'name': '7% VAT according to §13b UStG - without VAT - (recommended construction services)',
                'description': '7% VAT EU according to §13b UStG - without VAT - (recommended construction services)',
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
                        'account_id': 'chart_skr04_3835',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3835',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_free_eu_skr04': {
                'sequence': 20,
                'name': '0% Tax free benefit EU',
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
            'tax_free_third_country_skr04': {
                'sequence': 20,
                'name': '0% Tax free service third country',
                'description': '0% VAT Third country',
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
            'tax_free_newcar_skr04': {
                'sequence': 30,
                'name': '0% Tax free new vehicle delivery EU',
                'description': '0% VAT New vehicle EU',
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
            'tax_ust_19_3eck_first_skr04': {
                'sequence': 40,
                'name': '0% Sales tax triangular transaction first buyer',
                'description': '0% VAT Triangular business first customer',
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
            'tax_ust_free_bau_skr04': {
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
            'tax_ust_free_mobil_skr04': {
                'sequence': 50,
                'name': '0% Value added tax supply of mobile telephones etc. (§13b)',
                'description': '0% VAT Supply of mobile telephones, etc. (§13b)',
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
            'tax_eu_19_purchase_goods_skr04': {
                'sequence': 20,
                'name': 'Taxable other services EU 19%VAT/19%VSt',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3818',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3818',
                        'tag_ids': tags('+47'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_eu_7_purchase_goods_skr04': {
                'sequence': 21,
                'name': 'Taxable other services EU 7%VAT/7%VSt',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3818',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3818',
                        'tag_ids': tags('+47'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_vst_19_purchase_13b_bau_skr04': {
                'sequence': 22,
                'name': 'Tax according to §13b UStG 19%VAT/19%VSt (construction service recipient)',
                'description': 'Tax according to §13b UStG 19%VAT/19%VSt (construction service recipient)',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
                        'tag_ids': tags('+85'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_ust_vst_7_purchase_13b_bau_skr04': {
                'sequence': 23,
                'name': 'Tax according to §13b UStG 7%VAT/7%VSt (construction service recipient)',
                'description': 'Tax according to §13b UStG 7%VAT/7%VSt (construction service recipient)',
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
                        'account_id': 'chart_skr04_1408',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3835',
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
                        'account_id': 'chart_skr04_1408',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3835',
                        'tag_ids': tags('+85'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_13b_mobil_skr04': {
                'sequence': 24,
                'name': 'Tax according to §13b 19%VAT/19%VSt (reception of mobile devices etc.)',
                'description': 'Tax according to §13b 19%VAT/19%VSt (reception of mobile devices etc.)',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('-67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
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
                        'account_id': 'chart_skr04_1407',
                        'tag_ids': tags('+67'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3837',
                        'tag_ids': tags('+79'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_3eck_last_skr04': {
                'sequence': 25,
                'name': 'Triangular transaction Acquisition of last customer 19%VAT/19%VSt',
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
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('-69'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('+69'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_13b_werk_ausland_skr04': {
                'sequence': 25,
                'name': 'Tax acc. to §13b 19%VAT/19%VSt (foreign work deliveries etc.)',
                'description': 'Tax acc. to §13b 19%VAT/19%VSt (foreign work deliveries etc.)',
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
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
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
                        'account_id': 'chart_skr04_1406',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('+53'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_7_purchase_13b_werk_ausland_skr04': {
                'sequence': 26,
                'name': 'Tax acc. to §13b 7%VAT/7%VSt (foreign work deliveries etc.)',
                'description': 'Tax acc. to §13b 7%VAT/7%VSt (foreign work deliveries etc.)',
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
                        'account_id': 'chart_skr04_1401',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
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
                        'account_id': 'chart_skr04_1401',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('+53'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_19_purchase_13a_auslagerung_skr04': {
                'sequence': 27,
                'name': 'Tax acc. to §13a para. 1 no. 6 UStG 19%VAT/19%VSt (outsourcing)',
                'description': 'Tax acc. to §13a para. 1 no. 6 UStG 19%VAT/19%VSt (outsourcing)',
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
                        'account_id': 'chart_skr04_1431',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('-69'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1431',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('+69'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_vst_ust_7_purchase_13a_auslagerung_skr04': {
                'sequence': 28,
                'name': 'Tax acc. to §13a para. 1 no. 6 UStG 7%VAT/7%VSt (outsourcing)',
                'description': 'Tax acc. to §13a para. 1 no. 6 UStG 7%VAT/7%VSt (outsourcing)',
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
                        'account_id': 'chart_skr04_1431',
                        'tag_ids': tags('-66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('-69'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_1431',
                        'tag_ids': tags('+66'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_skr04_3851',
                        'tag_ids': tags('+69'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
        }

    def _get_de_skr04_fiscal_position(self, template_code):
        return {
            'fiscal_position_domestic_skr04': {
                'sequence': 1,
                'name': 'Domestic business partner',
                'auto_apply': 1,
                'country_id': 'base.de',
            },
            'fiscal_position_non_eu_partner_service_skr04': {
                'sequence': 6,
                'name': 'Service provider abroad (non-EU)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_free_third_country_skr04',
                        'tax_src_id': 'tax_ust_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_vst_ust_19_purchase_13b_werk_ausland_skr04',
                        'tax_src_id': 'tax_vst_19_skr04',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_skr04_4400',
                        'account_dest_id': 'chart_skr04_4338',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5400',
                        'account_dest_id': 'chart_skr04_5925',
                    }),
                ],
            },
            'fiscal_position_non_eu_partner_skr04': {
                'sequence': 5,
                'name': 'Business partners abroad (non-EU)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_export_skr04',
                        'tax_src_id': 'tax_ust_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_export_skr04',
                        'tax_src_id': 'tax_ust_7_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_import_19_and_payable_skr04',
                        'tax_src_id': 'tax_vst_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_import_7_and_payable_skr04',
                        'tax_src_id': 'tax_vst_7_skr04',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_skr04_4400',
                        'account_dest_id': 'chart_skr04_4120',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_4300',
                        'account_dest_id': 'chart_skr04_4120',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5400',
                        'account_dest_id': 'chart_skr04_5551',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5300',
                        'account_dest_id': 'chart_skr04_5557',
                    }),
                ],
            },
            'fiscal_position_eu_vat_id_partner_skr04': {
                'sequence': 2,
                'name': 'Business partner EU (with VAT ID)',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_eu_sale_skr04',
                        'tax_src_id': 'tax_ust_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_sale_skr04',
                        'tax_src_id': 'tax_ust_7_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_19_purchase_skr04',
                        'tax_src_id': 'tax_vst_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_7_purchase_skr04',
                        'tax_src_id': 'tax_vst_7_skr04',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_skr04_6931',
                        'account_dest_id': 'chart_skr04_6932',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_6936',
                        'account_dest_id': 'chart_skr04_6938',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_6281',
                        'account_dest_id': 'chart_skr04_6280',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_6286',
                        'account_dest_id': 'chart_skr04_6280',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_4400',
                        'account_dest_id': 'chart_skr04_4125',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_4300',
                        'account_dest_id': 'chart_skr04_4125',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5400',
                        'account_dest_id': 'chart_skr04_5425',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5300',
                        'account_dest_id': 'chart_skr04_5420',
                    }),
                ],
            },
            'fiscal_position_eu_vat_id_partner_service_skr04': {
                'sequence': 3,
                'name': 'Service provider EU (with VAT ID)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_eu_19_purchase_goods_skr04',
                        'tax_src_id': 'tax_vst_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_eu_7_purchase_goods_skr04',
                        'tax_src_id': 'tax_vst_7_skr04',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_skr04_5400',
                        'account_dest_id': 'chart_skr04_5923',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5300',
                        'account_dest_id': 'chart_skr04_5913',
                    }),
                ],
            },
            'fiscal_position_eu_no_id_partner_skr04': {
                'sequence': 4,
                'name': 'Business partner EU (without VAT ID)',
                'tax_ids': [
                    Command.create({
                        'tax_dest_id': 'tax_eu_19_purchase_no_vst_skr04',
                        'tax_src_id': 'tax_vst_19_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_ust_eu_skr04',
                        'tax_src_id': 'tax_ust_7_skr04',
                    }),
                    Command.create({
                        'tax_dest_id': 'tax_ust_19_eu_skr04',
                        'tax_src_id': 'tax_ust_19_skr04',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_skr04_6931',
                        'account_dest_id': 'chart_skr04_6933',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_6936',
                        'account_dest_id': 'chart_skr04_6938',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_6281',
                        'account_dest_id': 'chart_skr04_6280',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_6286',
                        'account_dest_id': 'chart_skr04_6280',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_4400',
                        'account_dest_id': 'chart_skr04_4315',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_4300',
                        'account_dest_id': 'chart_skr04_4310',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5400',
                        'account_dest_id': 'chart_skr04_5435',
                    }),
                    Command.create({
                        'account_src_id': 'chart_skr04_5300',
                        'account_dest_id': 'chart_skr04_5430',
                    }),
                ],
            },
        }

    def _get_de_skr04_reconcile_model(self, template_code):
        return {
            'reconcile_5731': {
                'name': 'Discount-EK-7%',
                'line_ids': [
                    Command.create({
                        'account_id': 'chart_skr04_5731',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr04.tax_vst_7_taxinclusive_skr04',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-EK-7%',
                    }),
                ],
            },
            'reconcile_5736': {
                'name': 'Discount-EK-19%',
                'line_ids': [
                    Command.create({
                        'account_id': 'chart_skr04_5736',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr04.tax_vst_19_taxinclusive_skr04',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-EK-19%',
                    }),
                ],
            },
            'reconcile_4731': {
                'name': 'Skonto-VK-7%',
                'line_ids': [
                    Command.create({
                        'account_id': 'chart_skr04_4731',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr04.tax_ust_7_taxinclusive_skr04',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-VK-7%',
                    }),
                ],
            },
            'reconcile_4736': {
                'name': 'Discount-VK-19%',
                'line_ids': [
                    Command.create({
                        'account_id': 'chart_skr04_4736',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr04.tax_ust_19_taxinclusive_skr04',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Discount-VK-19%',
                    }),
                ],
            },
            'reconcile_6931': {
                'name': 'Loss of receivables-7%',
                'line_ids': [
                    Command.create({
                        'account_id': 'chart_skr04_6931',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr04.tax_ust_7_taxinclusive_skr04',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Loss of receivables-7%',
                    }),
                ],
            },
            'reconcile_6936': {
                'name': 'Loss of receivables-19%',
                'line_ids': [
                    Command.create({
                        'account_id': 'chart_skr04_6936',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_de_skr04.tax_ust_19_taxinclusive_skr04',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Loss of receivables-19%',
                    }),
                ],
            },
        }
