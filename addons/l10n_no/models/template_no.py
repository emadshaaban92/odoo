# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_no_template_data(self, template_code):
        return {
            'cash_account_code_prefix': '1900',
            'bank_account_code_prefix': '1920',
            'transfer_account_code_prefix': '1940',
            'code_digits': '4',
            'property_account_receivable_id': 'chart1500',
            'property_account_payable_id': 'chart2400',
            'property_account_expense_categ_id': 'chart4000',
            'property_account_income_categ_id': 'chart3000',
            'property_account_expense_id': 'chart4300',
            'property_account_income_id': 'chart3000',
        }

    def _get_no_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.no',
                'account_default_pos_receivable_account_id': 'chart1501',
                'income_currency_exchange_account_id': 'chart8060',
                'expense_currency_exchange_account_id': 'chart8160',
                'account_journal_early_pay_discount_loss_account_id': 'chart4370',
                'account_journal_early_pay_discount_gain_account_id': 'chart3080',
            },
        }

    def _get_no_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax2': {
                'name': '1 Inngående mva høy sats 25%',
                'sequence': 0,
                'description': 'Fradrag for inngående mva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2711',
                        'tag_ids': tags('+Post 14'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2711',
                        'tag_ids': tags('-Post 14'),
                    }),
                ],
            },
            'tax1': {
                'name': '0 Ingen mvabehandling 0%',
                'description': 'Ingen mvabehandling(anskaffelser)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
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
            },
            'tax3': {
                'name': '3 Utgående mva høy sats 25%',
                'description': 'Utgående mva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 3 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2701',
                        'tag_ids': tags('+Post 3 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 3 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2701',
                        'tag_ids': tags('-Post 3 Tax'),
                    }),
                ],
            },
            'tax4': {
                'name': '5 Mvafritt salg 0%',
                'description': 'Mvafritt salg',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax5': {
                'name': '6 Omsetning utenfor mvaloven 0%',
                'description': 'Omsetning utenfor merverdiavgiftsloven',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax6': {
                'name': '7 Ingen mvabehandling(inntekter) 0%',
                'description': 'Ingen mvabehandling(inntekter)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
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
            },
            'tax7': {
                'name': '11 Inngående mva middel sats 15%',
                'description': 'Fradrag for inngående mva',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('+Post 15'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('-Post 15'),
                    }),
                ],
            },
            'tax8': {
                'name': '12 Inngående mva råfisk 11%',
                'description': 'Fradrag for inngående mva',
                'amount': 11.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('+Post 15'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('-Post 15'),
                    }),
                ],
            },
            'tax9': {
                'name': '13 Inngående mva lav sats 12%',
                'description': 'Fradrag for inngående mva',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2714',
                        'tag_ids': tags('+Post 16'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2714',
                        'tag_ids': tags('-Post 16'),
                    }),
                ],
            },
            'tax10': {
                'name': '14 Innførselsmva høy sats 25%',
                'description': 'Fradrag for innførselsmva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2711',
                        'tag_ids': tags('+Post 17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2711',
                        'tag_ids': tags('-Post 17'),
                    }),
                ],
            },
            'tax11': {
                'name': '15 Innførselsmva middel sats 15%',
                'description': 'Fradrag for innførselsmva',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('+Post 18'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('-Post 18'),
                    }),
                ],
            },
            'tax12': {
                'name': '20 Grunnlag ved innførsel av varer nullsats 0%',
                'description': 'Grunnlag ved innførsel av varer',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
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
            },
            'tax13': {
                'name': '21 Grunnlag ved innførsel av varer høy sats 25%',
                'description': 'Grunnlag ved innførsel av varer',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
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
            },
            'tax14': {
                'name': '22 Grunnlag ved innførsel av varer middel sats 15%',
                'description': 'Grunnlag ved innførsel av varer',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_15',
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
            },
            'tax15': {
                'name': '31 Utgående mva middel sats 15%',
                'description': 'Utgående mva',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 4 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('+Post 4 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 4 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('-Post 4 Tax'),
                    }),
                ],
            },
            'tax16': {
                'name': '32 Utgående mva råfisk 11%',
                'description': 'Utgående mva',
                'amount': 11.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 4 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('+Post 4 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 4 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('-Post 4 Tax'),
                    }),
                ],
            },
            'tax17': {
                'name': '33 Utgående mva lav sats 12%',
                'description': 'Utgående mva',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 5 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2704',
                        'tag_ids': tags('+Post 5 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 5 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2704',
                        'tag_ids': tags('-Post 5 Tax'),
                    }),
                ],
            },
            'tax18': {
                'name': '51 Innenlands omsetning med omvendt avgiftsplikt nullsats 0%',
                'description': 'Innlands omsetning med omvendt avgiftsplikt',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax19': {
                'name': '52 Utførsel av varer og tjenester nullsats 0%',
                'description': 'Utførsel av varer og tjenester',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 8'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 8'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax20': {
                'name': '81 Innførsel av varer med fradrag for innførselsmva høy sats 25%',
                'description': 'Innførsel av varer med fradrag for innførselsmva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 9 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2711',
                        'tag_ids': tags('+Post 9 Tax', '+Post 17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 9 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2701',
                        'tag_ids': tags('-Post 9 Tax', '-Post 17'),
                    }),
                ],
            },
            'tax21': {
                'name': '82 Innførsel av varer uten fradrag for innførselsmva høy sats 25%',
                'description': 'Innførsel av varer uten fradrag for innførselsmva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 9 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2701',
                        'tag_ids': tags('+Post 9 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 9 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2701',
                        'tag_ids': tags('-Post 9 Tax'),
                    }),
                ],
            },
            'tax22': {
                'name': '83 Innførsel av varer med fradrag for innførselsmva middel sats 15%',
                'description': 'Innførsel av varer med fradrag for innførselsmva',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 10 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2713',
                        'tag_ids': tags('+Post 10 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 10 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('-Post 10 Tax'),
                    }),
                ],
            },
            'tax23': {
                'name': '84 Innførsel av varer uten fradrag for innførselsmva middel sats 15%',
                'description': 'Innførsel av varer uten fradrag for innførselsmva',
                'amount': 15.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 10 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('+Post 10 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 10 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2703',
                        'tag_ids': tags('-Post 10 Tax'),
                    }),
                ],
            },
            'tax24': {
                'name': '85 Innførsel av varer uten mva beregning 0%',
                'description': 'Innførsel av varer som det ikke skal beregnes mervediavgift av',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax25': {
                'name': '86 Tjenester kjøpt fra utlandet med fradrag for mva høy sats 25%',
                'description': 'Tjenester kjøpt fra utlandet med fradrag for mva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2712',
                        'tag_ids': tags('+Post 12 Tax', '+Post 17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('-Post 12 Tax', '-Post 17'),
                    }),
                ],
            },
            'tax26': {
                'name': '87 Tjenester kjøpt fra utlandet uten fradrag for mva høy sats 25%',
                'description': 'Tjenester kjøpt fra utlandet uten fradrag for mva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('+Post 12 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('-Post 12 Tax'),
                    }),
                ],
            },
            'tax27': {
                'name': '88 Tjenester kjøpt fra utlandet med fradrag for mva lav sats 12%',
                'description': 'Tjenester kjøpt fra utlandet med fradrag for mva',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2712',
                        'tag_ids': tags('+Post 12 Tax', '+Post 17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('-Post 12 Tax', '-Post 17'),
                    }),
                ],
            },
            'tax28': {
                'name': '89 Tjenester kjøpt fra utlandet uten fradrag for mva lav sats 12%',
                'description': 'Tjenester kjøpt fra utlandet uten fradrag for mva',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('+Post 12 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 12 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('-Post 12 Tax'),
                    }),
                ],
            },
            'tax29': {
                'name': '91 Kjøp av klimakvoter eller gull med fradrag for mva høy sats 25%',
                'description': 'Kjøp av klimakvoter eller gull med fradrag for mva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 13 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2712',
                        'tag_ids': tags('+Post 13 Tax', '+Post 14'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 13 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('-Post 13 Tax', '-Post 14'),
                    }),
                ],
            },
            'tax30': {
                'name': '92 Kjøp av klimakvoter eller gull uten fradrag for mva høy sats 25%',
                'description': 'Kjøp av klimakvoter eller gull uten fradrag for mva',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Post 13 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('+Post 13 Tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Post 13 Base'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2702',
                        'tag_ids': tags('-Post 13 Tax'),
                    }),
                ],
            },
        }
