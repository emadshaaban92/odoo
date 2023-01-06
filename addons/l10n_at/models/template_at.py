# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_at_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_at_fiscal_position(template_code),
        }

    def _get_at_template_data(self, template_code):
        return {
            'visible': True,
            'property_account_receivable_id': 'chart_at_template_2000',
            'property_account_payable_id': 'chart_at_template_3300',
            'property_account_income_categ_id': 'chart_at_template_4000',
            'property_account_expense_categ_id': 'chart_at_template_5000',
            'property_stock_account_input_categ_id': 'chart_at_template_3740',
            'property_stock_account_output_categ_id': 'chart_at_template_5000',
            'property_stock_valuation_account_id': 'chart_at_template_1600',
            'code_digits': '4',
            'bank_account_code_prefix': '280',
            'cash_account_code_prefix': '270',
            'transfer_account_code_prefix': '288',
        }

    def _get_at_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.at',
                'account_default_pos_receivable_account_id': 'chart_at_template_2099',
                'income_currency_exchange_account_id': 'chart_at_template_4860',
                'expense_currency_exchange_account_id': 'chart_at_template_7860',
                'account_journal_early_pay_discount_loss_account_id': 'chart_at_template_5800',
                'account_journal_early_pay_discount_gain_account_id': 'chart_at_template_8350',
            },
        }

    def _get_at_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'account_tax_template_sales_rev_charge_0_code021': {
                'name': 'UST_021 Steuerschuld betrifft Leistungsempfänger',
                'description': 'USt. 0%',
                'sequence': 400,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 021'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 021'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 021'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 021'),
                    }),
                ],
            },
            'account_tax_template_sales_non_eu_0_code011': {
                'name': 'UST_011 Export 0%',
                'description': 'USt. 0%',
                'sequence': 300,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 011', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 011', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_non_eu_0_code012': {
                'name': 'UST_012 Lohnveredelung 0%',
                'description': 'USt. 0%',
                'sequence': 200,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 012', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 012', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_non_eu_0_code015': {
                'name': 'UST_015 Export 0% (§ 6 Abs. 1 Z 2 bis 6)',
                'description': 'USt. 0%',
                'sequence': 300,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 015', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 015', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_eu_0_code017': {
                'name': 'UST_017 IGL 0% (ohne Art. 6 Abs. 1)',
                'description': 'USt. 0%',
                'sequence': 200,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 017', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 017', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_eu_0_code018': {
                'name': 'UST_018 IGL 0% (Art. 6 Abs. 1)',
                'description': 'USt. 0%',
                'sequence': 200,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 018', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 018', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_0_code019': {
                'name': 'UST_019 Grundstücksumsätze 0% (§ 6 Abs. 1 Z 9 lit. a)',
                'description': 'USt. 0%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 019', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 019', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_0_code016': {
                'name': 'UST_016 Kleinunternehmer 0% (§ 6 Abs. 1 Z 27)',
                'description': 'USt. 0%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 016', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 016', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_0_code020': {
                'name': 'UST_020 Übrige steuerfreie Umsätze 0%',
                'description': 'USt. 0%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 020', '+KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 020', '-KZ 000'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_20_code022': {
                'name': 'UST_022 Normalsteuersatz 20%',
                'description': 'USt. 20%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 022 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3500',
                        'tag_ids': tags('-KZ 022 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 022 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3500',
                        'tag_ids': tags('+KZ 022 Umsatzsteuer'),
                    }),
                ],
                'tax_group_id': 'tax_group_20',
            },
            'account_tax_template_sales_20_katalog022': {
                'name': 'UST_022 Normalsteuersatz 20% (Sonstige Leistungen)',
                'description': 'USt. 20%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 022 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3500',
                        'tag_ids': tags('-KZ 022 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 022 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3500',
                        'tag_ids': tags('+KZ 022 Umsatzsteuer'),
                    }),
                ],
                'tax_group_id': 'tax_group_20',
            },
            'account_tax_template_sales_10_code029': {
                'name': 'UST_029 ermäßigter Steuersatz 10%',
                'description': 'USt. 10%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 029 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3501',
                        'tag_ids': tags('-KZ 029 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 029 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3501',
                        'tag_ids': tags('+KZ 029 Umsatzsteuer'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'account_tax_template_sales_13_code006': {
                'name': 'UST_006 ermäßigter Steuersatz 13%',
                'description': 'USt. 13%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 13.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 006 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3502',
                        'tag_ids': tags('-KZ 006 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 006 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3502',
                        'tag_ids': tags('+KZ 006 Umsatzsteuer'),
                    }),
                ],
                'tax_group_id': 'tax_group_13',
            },
            'account_tax_template_sales_19_code037': {
                'name': 'UST_037 Steuersatz 19%',
                'description': 'USt. 19%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 19.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 037 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 037 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 037 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 037 Umsatzsteuer'),
                    }),
                ],
            },
            'account_tax_template_sales_add10_code052': {
                'name': 'UST_052 Zusatzsteuersatz 10% (LWB/FWB)',
                'description': 'USt. 10%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 052 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 052 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 052 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 052 Umsatzsteuer'),
                    }),
                ],
            },
            'account_tax_template_sales_add7_code007': {
                'name': 'UST_007 Zusatzsteuersatz 7% (LWB/FWB)',
                'description': 'USt. 7%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 7.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 000', '+KZ 007 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 007 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 000', '-KZ 007 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 007 Umsatzsteuer'),
                    }),
                ],
            },
            'account_tax_template_sales_self_20_code022': {
                'name': 'UST_022 Normalsteuersatz 20% (Eigenverbrauch)',
                'description': 'USt. 20%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 001', '+KZ 022 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3500',
                        'tag_ids': tags('-KZ 022 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 001', '-KZ 022 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3500',
                        'tag_ids': tags('+KZ 022 Umsatzsteuer'),
                    }),
                ],
                'tax_group_id': 'tax_group_20',
            },
            'account_tax_template_sales_self_10_code029': {
                'name': 'UST_029 ermäßigter Steuersatz 10% (Eigenverbrauch)',
                'description': 'USt. 10%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 001', '+KZ 029 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3501',
                        'tag_ids': tags('-KZ 029 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 001', '-KZ 029 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3501',
                        'tag_ids': tags('+KZ 029 Umsatzsteuer'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'account_tax_template_sales_self_19_code037': {
                'name': 'UST_037 Steuersatz 19% (Eigenverbrauch)',
                'description': 'USt. 19%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 19.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 001', '+KZ 037 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 037 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 001', '-KZ 037 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 037 Umsatzsteuer'),
                    }),
                ],
            },
            'account_tax_template_sales_self_add10_code052': {
                'name': 'UST_052 Zusatzsteuersatz 10% (LWB/FWB - Eigenverbrauch)',
                'description': 'USt. 10%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 001', '+KZ 052 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 052 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 001', '-KZ 052 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 052 Umsatzsteuer'),
                    }),
                ],
            },
            'account_tax_template_sales_self_add7_code007': {
                'name': 'UST_007 Zusatzsteuersatz 7% (LWB/FWB - Eigenverbrauch)',
                'description': 'USt. 7%',
                'sequence': 100,
                'type_tax_use': 'sale',
                'amount': 7.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 001', '+KZ 007 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 007 Umsatzsteuer'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 001', '-KZ 007 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 007 Umsatzsteuer'),
                    }),
                ],
            },
            'account_tax_template_purchase_tax_invoiced_accepted_code056': {
                'name': 'UST_056 Tax invoiced accepted (§ 11 Abs. 12 und 14, § 16 Abs. 2 sowie gemäß Art. 7 Abs. 4)',
                'description': 'USt. 20%',
                'sequence': 100,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('+KZ 056'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 056'),
                    }),
                ],
                'tax_group_id': 'tax_group_20',
            },
            'account_tax_template_sales_eu_0_services': {
                'name': 'UST_EU Dienstleistung (Sonstige Leistungen) 0%',
                'description': 'USt. 0%',
                'sequence': 200,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_sales_non_eu_0_services': {
                'name': 'UST_NON_EU Dienstleistung (Drittstaaten) 0%',
                'description': 'USt. 0%',
                'sequence': 300,
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_eu_0_code071': {
                'name': 'UST_071 IGE 0% (Art. 6 Abs. 2)',
                'description': 'USt. 0%',
                'sequence': 200,
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 070', '-KZ 071'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 070', '+KZ 071'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                    }),
                ],
            },
            'account_tax_template_purchase_eu_20': {
                'name': 'IGE 20%',
                'description': 'IGE 20%',
                'sequence': 500,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 070', '-KZ 072 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3511',
                        'tag_ids': tags('+KZ 072 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2511',
                        'tag_ids': tags('+KZ 065'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 070', '+KZ 072 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3511',
                        'tag_ids': tags('-KZ 072 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2511',
                        'tag_ids': tags('-KZ 065'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_eu_10': {
                'name': 'IGE 10%',
                'description': 'IGE 10%',
                'sequence': 500,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 10.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 070', '-KZ 073 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3512',
                        'tag_ids': tags('+KZ 073 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2512',
                        'tag_ids': tags('+KZ 065'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 070', '+KZ 073 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3512',
                        'tag_ids': tags('-KZ 073 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2512',
                        'tag_ids': tags('-KZ 065'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_eu_13': {
                'name': 'IGE 13%',
                'description': 'IGE 13%',
                'sequence': 500,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 070', '-KZ 008 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3513',
                        'tag_ids': tags('+KZ 008 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2513',
                        'tag_ids': tags('+KZ 065'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 070', '+KZ 008 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3513',
                        'tag_ids': tags('-KZ 008 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2513',
                        'tag_ids': tags('-KZ 065'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_eu_19': {
                'name': 'IGE 19%',
                'description': 'IGE 19%',
                'sequence': 500,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'amount': 19.0,
                'amount_type': 'group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 070', '-KZ 088 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3511',
                        'tag_ids': tags('+KZ 088 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+KZ 065'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 070', '+KZ 088 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3511',
                        'tag_ids': tags('-KZ 088 Umsatzsteuer'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-KZ 065'),
                    }),
                ],
            },
            'account_tax_template_purchase_rev_charge_1a': {
                'name': 'Reverse Charge 20% (§ 19 Abs. 1a - Bauleistungen)',
                'description': 'RC 20% § 19 Abs. 1a',
                'sequence': 550,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('+KZ 048'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('+KZ 082'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('-KZ 048'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('-KZ 082'),
                    }),
                ],
            },
            'account_tax_template_purchase_rev_charge_1b': {
                'name': 'Reverse Charge 20% (§ 19 Abs. 1b - Sicherungseigentum)',
                'description': 'RC 20% § 19 Abs. 1b',
                'sequence': 550,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('+KZ 044'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('+KZ 087'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('-KZ 044'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('-KZ 087'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_rev_charge_1c': {
                'name': 'Reverse Charge 20% (§ 19 Abs. 1c - Sonstige Leistungen)',
                'description': 'RC 20% § 19 Abs. 1c',
                'sequence': 550,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('+KZ 057'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('+KZ 066'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('-KZ 057'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('-KZ 066'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_rev_charge_1d': {
                'name': 'Reverse Charge 20% (§ 19 Abs. 1d - Schrott und Abfallstoffe)',
                'description': 'RC 20% § 19 Abs. 1d',
                'sequence': 550,
                'type_tax_use': 'purchase',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('+KZ 032'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('+KZ 089'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3510',
                        'tag_ids': tags('-KZ 032'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2510',
                        'tag_ids': tags('-KZ 089'),
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'account_tax_template_purchase_eu_xx_code076': {
                'name': 'Erwerbe gemäß Art. 3 Abs. 8 zweiter Satz, die im Mitgliedstaat des Bestimmungslandes besteuert worden sind (IGE-UST)',
                'description': 'UST_076 IGE (im Bestimmungsland besteuert)',
                'amount': 0.0,
                'sequence': 200,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 076', '-KZ 077'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 076', '+KZ 077'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
            },
            'account_tax_template_purchase_eu_xx_code077': {
                'name': 'Erwerbe gemäß Art. 3 Abs. 8 zweiter Satz, die gemäß Art. 25 Abs. 2 im Inland als besteuert gelten (IGE-UST)',
                'description': 'UST_077 IGE (im Inland besteuert)',
                'amount': 0.0,
                'sequence': 200,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 077', '+KZ 037 Bemessungsgrundlage'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3505',
                        'tag_ids': tags('-KZ 077'),
                    }),
                ],
            },
            'account_tax_template_purchase_20_code060': {
                'name': 'VST_060 Normalsteuersatz 20%',
                'description': 'VSt. 20%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2500',
                        'tag_ids': tags('+KZ 060'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2500',
                        'tag_ids': tags('-KZ 060'),
                    }),
                ],
                'tax_group_id': 'tax_group_20',
            },
            'account_tax_template_purchase_20_misc_code060': {
                'name': 'VST_060 sonstige Leistungen 20%',
                'description': 'VSt. 20%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2500',
                        'tag_ids': tags('+KZ 060'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2500',
                        'tag_ids': tags('-KZ 060'),
                    }),
                ],
                'tax_group_id': 'tax_group_20',
            },
            'account_tax_template_purchase_10_code060': {
                'name': 'VST_060 ermäßigter Steuersatz 10%',
                'description': 'VSt. 10%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 10.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2501',
                        'tag_ids': tags('+KZ 060'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2501',
                        'tag_ids': tags('-KZ 060'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'account_tax_template_purchase_13_code060': {
                'name': 'VST_060 ermäßigter Steuersatz 13%',
                'description': 'VSt. 13%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 13.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2502',
                        'tag_ids': tags('+KZ 060'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2502',
                        'tag_ids': tags('-KZ 060'),
                    }),
                ],
                'tax_group_id': 'tax_group_13',
            },
            'account_tax_template_purchase_19_code060': {
                'name': 'VST_060 Jungholz und Mittelberg 19%',
                'description': 'VSt. 19%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 19.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('+KZ 060'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('-KZ 060'),
                    }),
                ],
            },
            'account_tax_template_purchase_12_code060': {
                'name': 'VST_060 Weineinkauf 12% (LWB)',
                'description': 'VSt. 12%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 12.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('+KZ 060'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('-KZ 060'),
                    }),
                ],
            },
            'account_tax_template_purchase_xx_code061': {
                'name': 'VST_061 entrichtete EUst (§ 12 Abs. 1 Z 2 lit. a)',
                'description': 'VSt. 20%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+KZ 061'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-KZ 061'),
                    }),
                ],
            },
            'account_tax_template_purchase_xx_code083': {
                'name': 'VST_083 verbuchte EUst. (§ 12 Abs. 1 Z 2 lit. b)',
                'description': 'VSt. 20%',
                'sequence': 400,
                'type_tax_use': 'none',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2515',
                        'tag_ids': tags('+KZ 083'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_3515',
                        'tag_ids': tags('-KZ 083'),
                    }),
                ],
            },
            'account_tax_template_purchase_correct_code063': {
                'name': 'VST_063 (§12 Abs. 10 und 11 - Berichtigung)',
                'description': 'VSt. 0%',
                'amount': 0.0,
                'sequence': 400,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
            },
            'account_tax_template_purchase_correct_code067': {
                'name': 'VST_067 (§ 16 - Berichtigung)',
                'description': 'VSt. 0%',
                'amount': 0.0,
                'sequence': 400,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('+KZ 067'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('+KZ 067'),
                    }),
                ],
            },
            'account_tax_template_purchase_correct_code090': {
                'name': 'VST_090 (Sonstige Berichtigungen)',
                'description': 'VSt. 0%',
                'amount': 0.0,
                'sequence': 600,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('+KZ 090'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('-KZ 090'),
                    }),
                ],
            },
            'account_tax_template_purchase_cars_buildings_code027': {
                'name': 'VST_027 betreffend KFZ nach EKR 063, 064, 732-733 und 744-747',
                'description': 'VSt. 20%',
                'sequence': 400,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
            },
            'account_tax_template_purchase_cars_buildings_code028': {
                'name': 'VST_028 betreffend Gebäude nach EKR 030-037 und 070, 071',
                'description': 'VSt. 20%',
                'amount': 20.0,
                'sequence': 400,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
            },
            'account_tax_template_purchase_eu_0_vst_071': {
                'name': 'VST_071 IGE 0%',
                'description': 'VST_071 IGE 0% (Art. 6 Abs. 2)',
                'amount': 0.0,
                'sequence': 500,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('+KZ 065'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                        'tag_ids': tags('-KZ 065'),
                    }),
                ],
            },
            'account_tax_template_purchase_eu_xx_vst_076': {
                'name': 'VST_076 IGE (im Bestimmungsland besteuert)',
                'description': 'VSt. 20%',
                'sequence': 500,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-KZ 076', '-KZ 077'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+KZ 076', '+KZ 077'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
            },
            'account_tax_template_purchase_eu_xx_vst_077': {
                'name': 'VST_077 IGE (im Inland besteuert)',
                'description': 'VSt. 20%',
                'sequence': 500,
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'price_include': False,
                'active': False,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart_at_template_2505',
                    }),
                ],
            },
        }

    def _get_at_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_national': {
                'name': 'National',
                'auto_apply': 1,
                'country_id': 'base.at',
            },
            'fiscal_position_template_eu': {
                'name': 'Europäische Union',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_20_code022',
                        'tax_dest_id': 'account_tax_template_sales_eu_0_code017',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_20_katalog022',
                        'tax_dest_id': 'account_tax_template_sales_eu_0_services',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_10_code029',
                        'tax_dest_id': 'account_tax_template_sales_eu_0_code017',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_add7_code007',
                        'tax_dest_id': 'account_tax_template_sales_eu_0_code017',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_purchase_20_code060',
                        'tax_dest_id': 'account_tax_template_purchase_eu_20',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_purchase_20_misc_code060',
                        'tax_dest_id': 'account_tax_template_purchase_rev_charge_1c',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_purchase_10_code060',
                        'tax_dest_id': 'account_tax_template_purchase_eu_10',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_purchase_19_code060',
                        'tax_dest_id': 'account_tax_template_purchase_eu_19',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_at_template_4000',
                        'account_dest_id': 'chart_at_template_4100',
                    }),
                    Command.create({
                        'account_src_id': 'chart_at_template_4001',
                        'account_dest_id': 'chart_at_template_4110',
                    }),
                    Command.create({
                        'account_src_id': 'chart_at_template_2000',
                        'account_dest_id': 'chart_at_template_2100',
                    }),
                    Command.create({
                        'account_src_id': 'chart_at_template_5000',
                        'account_dest_id': 'chart_at_template_5050',
                    }),
                ],
            },
            'fiscal_position_template_non_eu': {
                'name': 'Drittstaaten',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_20_code022',
                        'tax_dest_id': 'account_tax_template_sales_non_eu_0_code011',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_10_code029',
                        'tax_dest_id': 'account_tax_template_sales_non_eu_0_services',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_template_sales_add7_code007',
                        'tax_dest_id': 'account_tax_template_sales_non_eu_0_code011',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart_at_template_4000',
                        'account_dest_id': 'chart_at_template_4200',
                    }),
                    Command.create({
                        'account_src_id': 'chart_at_template_2000',
                        'account_dest_id': 'chart_at_template_2150',
                    }),
                    Command.create({
                        'account_src_id': 'chart_at_template_5000',
                        'account_dest_id': 'chart_at_template_5090',
                    }),
                ],
            },
        }
