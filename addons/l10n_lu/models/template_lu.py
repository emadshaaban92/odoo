# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_lu_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_lu_fiscal_position(template_code),
            'account.reconcile.model': self._get_lu_reconcile_model(template_code),
        }

    def _get_lu_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'lu_2011_account_4011',
            'property_account_payable_id': 'lu_2011_account_44111',
            'property_account_expense_categ_id': 'lu_2011_account_6061',
            'property_account_income_categ_id': 'lu_2020_account_703001',
            'property_stock_account_input_categ_id': 'lu_2011_account_321',
            'property_stock_account_output_categ_id': 'lu_2011_account_321',
            'property_stock_valuation_account_id': 'lu_2020_account_60761',
            'property_tax_payable_account_id': 'lu_2011_account_461412',
            'property_tax_receivable_account_id': 'lu_2011_account_421612',
            'property_advance_tax_payment_account_id': 'lu_2011_account_421613',
            'bank_account_code_prefix': '513',
            'cash_account_code_prefix': '516',
            'transfer_account_code_prefix': '517',
            'code_digits': '6',
        }

    def _get_lu_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.lu',
                'account_default_pos_receivable_account_id': 'lu_2011_account_40111',
                'income_currency_exchange_account_id': 'lu_2020_account_7561',
                'expense_currency_exchange_account_id': 'lu_2020_account_6561',
                'account_journal_suspense_account_id': 'lu_2011_account_485',
                'account_journal_early_pay_discount_loss_account_id': 'lu_2020_account_65562',
                'account_journal_early_pay_discount_gain_account_id': 'lu_2020_account_75562',
            },
        }

    def _get_lu_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'lu_2011_tax_AB-EC-0': {
                'sequence': 171,
                'description': '0%',
                'name': 'EX-EC-P-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+195'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-195'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2015_tax_AB-EC-14': {
                'sequence': 105,
                'description': '14%',
                'name': '14-EC-P-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+723'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+724'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-723'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-724'),
                    }),
                ],
            },
            'lu_2015_tax_AB-EC-17': {
                'sequence': 111,
                'description': '17%',
                'name': '17-EC-P-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+721'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+722'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-721'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-722'),
                    }),
                ],
            },
            'lu_2015_tax_AB-EC-16': {
                'sequence': 112,
                'description': '16%',
                'name': '16-EC-P-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+921'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+922'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-921'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-922'),
                    }),
                ],
            },
            'lu_2015_tax_AB-EC-13': {
                'sequence': 113,
                'description': '13%',
                'name': '13-EC-P-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+923'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+924'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-923'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-924'),
                    }),
                ],
            },
            'lu_2015_tax_AB-EC-7': {
                'sequence': 114,
                'description': '7%',
                'name': '7-EC-P-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+925'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+926'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-925'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-926'),
                    }),
                ],
            },
            'lu_2011_tax_AB-EC-3': {
                'sequence': 114,
                'description': '3%',
                'name': '3-EC-P-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+059'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+068'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-059'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-068'),
                    }),
                ],
            },
            'lu_2015_tax_AB-EC-8': {
                'sequence': 120,
                'description': '8%',
                'name': '8-EC-P-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+725'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+726'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-725'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-726'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-0': {
                'sequence': 123,
                'description': '0%',
                'name': 'EX-EC(P)-P-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+196'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-196'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-14': {
                'sequence': 127,
                'description': '14%',
                'name': '14-EC(P)-P-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+733'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+734'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-733'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-734'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-17': {
                'sequence': 133,
                'description': '17%',
                'name': '17-EC(P)-P-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+731'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+732'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-731'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-732'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-16': {
                'sequence': 134,
                'description': '16%',
                'name': '16-EC(P)-P-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+931'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+932'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-931'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-932'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-13': {
                'sequence': 135,
                'description': '13%',
                'name': '13-EC(P)-P-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+933'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+934'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-933'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-934'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-7': {
                'sequence': 136,
                'description': '7%',
                'name': '7-EC(P)-P-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+935'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+936'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-935'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-936'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-3': {
                'sequence': 137,
                'description': '3%',
                'name': '3-EC(P)-P-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+063'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+073'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-063'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-073'),
                    }),
                ],
            },
            'lu_2015_tax_AB-ECP-8': {
                'sequence': 142,
                'description': '8%',
                'name': '8-EC(P)-P-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+735'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+736'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-735'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-736'),
                    }),
                ],
            },
            'lu_2011_tax_AB-IC-0': {
                'sequence': 145,
                'description': '0%',
                'name': 'EX-IC-P-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+194'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-194'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2015_tax_AB-IC-14': {
                'sequence': 149,
                'description': '14%',
                'name': '14-IC-P-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+713'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+714'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-713'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-714'),
                    }),
                ],
            },
            'lu_2015_tax_AB-IC-17': {
                'sequence': 155,
                'description': '17%',
                'name': '17-IC-P-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+711'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+712'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-711'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-712'),
                    }),
                ],
            },
            'lu_2015_tax_AB-IC-16': {
                'sequence': 155,
                'description': '16%',
                'name': '16-IC-P-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+911'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+912'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-911'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-912'),
                    }),
                ],
            },
            'lu_2015_tax_AB-IC-13': {
                'sequence': 156,
                'description': '13%',
                'name': '13-IC-P-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+913'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+914'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-913'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-914'),
                    }),
                ],
            },
            'lu_2015_tax_AB-IC-7': {
                'sequence': 157,
                'description': '7%',
                'name': '7-IC-P-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+915'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+916'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-915'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-916'),
                    }),
                ],
            },
            'lu_2011_tax_AB-IC-3': {
                'sequence': 158,
                'description': '3%',
                'name': '3-IC-P-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+049'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+054'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-049'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-054'),
                    }),
                ],
            },
            'lu_2015_tax_AB-IC-8': {
                'sequence': 164,
                'description': '8%',
                'name': '8-IC-P-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+715'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+716'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-715'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-716'),
                    }),
                ],
            },
            'lu_2011_tax_AB-PA-0': {
                'sequence': 167,
                'description': '0%',
                'name': '0-P-G',
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
            'lu_2015_tax_AB-PA-14': {
                'sequence': 169,
                'description': '14%',
                'name': '14-P-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AB-PA-17': {
                'sequence': 101,
                'description': '17%',
                'name': '17-P-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AB-PA-16': {
                'sequence': 102,
                'description': '16%',
                'name': '16-P-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AB-PA-13': {
                'sequence': 103,
                'description': '13%',
                'name': '13-P-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AB-PA-8': {
                'sequence': 174,
                'description': '8%',
                'name': '8-P-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AB-PA-7': {
                'sequence': 104,
                'description': '7%',
                'name': '7-P-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2011_tax_AB-PA-3': {
                'sequence': 172,
                'description': '3%',
                'name': '3-P-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2011_tax_AP-EC-0': {
                'sequence': 175,
                'description': '0%',
                'name': 'EX-EC-P-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+445'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-445'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2015_tax_AP-EC-14': {
                'sequence': 179,
                'description': '14%',
                'name': '14-EC-P-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+753'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+754'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-753'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-754'),
                    }),
                ],
            },
            'lu_2015_tax_AP-EC-17': {
                'sequence': 185,
                'description': '17%',
                'name': '17-EC-P-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+751'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+752'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-751'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-752'),
                    }),
                ],
            },
            'lu_2015_tax_AP-EC-16': {
                'sequence': 185,
                'description': '16%',
                'name': '16-EC-P-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+951'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+952'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-951'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-952'),
                    }),
                ],
            },
            'lu_2015_tax_AP-EC-13': {
                'sequence': 186,
                'description': '13%',
                'name': '13-EC-P-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+953'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+954'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-953'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-954'),
                    }),
                ],
            },
            'lu_2015_tax_AP-EC-7': {
                'sequence': 187,
                'description': '7%',
                'name': '7-EC-P-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+955'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+956'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-955'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-956'),
                    }),
                ],
            },
            'lu_2011_tax_AP-EC-3': {
                'sequence': 188,
                'description': '3%',
                'name': '3-EC-P-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+441'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+442'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-441'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-442'),
                    }),
                ],
            },
            'lu_2015_tax_AP-EC-8': {
                'sequence': 194,
                'description': '8%',
                'name': '8-EC-P-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+755'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+756'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-755'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-756'),
                    }),
                ],
            },
            'lu_2011_tax_AP-IC-0': {
                'sequence': 197,
                'description': '0%',
                'name': 'EX-IC-P-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+435'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-435'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2015_tax_AP-IC-14': {
                'sequence': 201,
                'description': '14%',
                'name': '14-IC-P-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+743'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+744'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-743'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-744'),
                    }),
                ],
            },
            'lu_2015_tax_AP-IC-17': {
                'sequence': 207,
                'description': '17%',
                'name': '17-IC-P-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+741'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+742'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-741'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-742'),
                    }),
                ],
            },
            'lu_2015_tax_AP-IC-16': {
                'sequence': 208,
                'description': '16%',
                'name': '16-IC-P-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+941'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+942'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-941'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-942'),
                    }),
                ],
            },
            'lu_2015_tax_AP-IC-13': {
                'sequence': 209,
                'description': '13%',
                'name': '13-IC-P-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+943'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+944'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-943'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-944'),
                    }),
                ],
            },
            'lu_2015_tax_AP-IC-7': {
                'sequence': 210,
                'description': '7%',
                'name': '7-IC-P-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+945'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+946'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-945'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-946'),
                    }),
                ],
            },
            'lu_2011_tax_AP-IC-3': {
                'sequence': 211,
                'description': '3%',
                'name': '3-IC-P-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+431'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+432'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-431'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-432'),
                    }),
                ],
            },
            'lu_2015_tax_AP-IC-8': {
                'sequence': 216,
                'description': '8%',
                'name': '8-IC-P-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+745'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+746'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-745'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-746'),
                    }),
                ],
            },
            'lu_2011_tax_AP-PA-0': {
                'sequence': 219,
                'description': '0%',
                'name': '0-P-S',
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
            'lu_2015_tax_AP-PA-14': {
                'sequence': 221,
                'description': '14%',
                'name': '14-P-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AP-PA-17': {
                'sequence': 223,
                'description': '17%',
                'name': '17-P-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AP-PA-16': {
                'sequence': 223,
                'description': '16%',
                'name': '16-P-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AP-PA-13': {
                'sequence': 223,
                'description': '13%',
                'name': '13-P-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AP-PA-7': {
                'sequence': 223,
                'description': '7%',
                'name': '7-P-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2011_tax_AP-PA-3': {
                'sequence': 224,
                'description': '3%',
                'name': '3-P-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2015_tax_AP-PA-8': {
                'sequence': 226,
                'description': '8%',
                'name': '8-P-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
            },
            'lu_2011_tax_FB-EC-0': {
                'sequence': 227,
                'description': '0%',
                'name': 'EX-EC-E-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+195'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-195'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-EC-14': {
                'sequence': 231,
                'description': '14%',
                'name': '14-EC-E-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+723'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+724'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-723'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-724'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-EC-17': {
                'sequence': 237,
                'description': '17%',
                'name': '17-EC-E-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+721'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+722'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-721'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-722'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-EC-16': {
                'sequence': 238,
                'description': '16%',
                'name': '16-EC-E-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+921'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+922'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-921'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-922'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-EC-13': {
                'sequence': 239,
                'description': '13%',
                'name': '13-EC-E-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+923'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+924'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-923'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-924'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-EC-7': {
                'sequence': 240,
                'description': '7%',
                'name': '7-EC-E-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+925'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+926'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-925'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-926'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FB-EC-3': {
                'sequence': 241,
                'description': '3%',
                'name': '3-EC-E-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+059'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+068'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-059'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-068'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-EC-8': {
                'sequence': 246,
                'description': '8%',
                'name': '8-EC-E-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+725'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+726'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-725'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-726'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-0': {
                'sequence': 249,
                'description': '0%',
                'name': 'EX-EC(P)-E-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+196'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-196'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-14': {
                'sequence': 253,
                'description': '14%',
                'name': '14-EC(P)-E-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+733'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+734'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-733'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-734'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-17': {
                'sequence': 259,
                'description': '17%',
                'name': '17-EC(P)-E-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+731'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+732'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-731'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-732'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-16': {
                'sequence': 260,
                'description': '16%',
                'name': '16-EC(P)-E-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+931'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+932'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-931'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-932'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-13': {
                'sequence': 261,
                'description': '13%',
                'name': '13-EC(P)-E-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+933'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+934'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-933'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-934'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-7': {
                'sequence': 262,
                'description': '7%',
                'name': '7-EC(P)-E-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+935'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+936'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-935'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-936'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-3': {
                'sequence': 263,
                'description': '3%',
                'name': '3-EC(P)-E-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+063'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+073'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-063'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-073'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-ECP-8': {
                'sequence': 268,
                'description': '8%',
                'name': '8-EC(P)-E-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+735'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+736'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-735'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-736'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FB-IC-0': {
                'sequence': 271,
                'description': '0%',
                'name': 'EX-IC-E-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+194'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-194'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-IC-14': {
                'sequence': 275,
                'description': '14%',
                'name': '14-IC-E-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+713'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+714'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-713'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-714'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-IC-17': {
                'sequence': 281,
                'description': '17%',
                'name': '17-IC-E-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+711'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+712'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-711'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-712'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-IC-16': {
                'sequence': 282,
                'description': '16%',
                'name': '16-IC-E-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+911'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+912'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-911'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-912'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-IC-13': {
                'sequence': 283,
                'description': '13%',
                'name': '13-IC-E-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+913'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+914'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-913'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-914'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-IC-7': {
                'sequence': 284,
                'description': '7%',
                'name': '7-IC-E-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+915'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+916'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-915'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-916'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FB-IC-3': {
                'sequence': 285,
                'description': '3%',
                'name': '3-IC-E-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+049'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+054'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-049'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-054'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-IC-8': {
                'sequence': 290,
                'description': '8%',
                'name': '8-IC-E-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+715'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+716'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-715'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-716'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FB-PA-0': {
                'sequence': 293,
                'description': '0%',
                'name': '0-E-G',
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
                'active': False,
            },
            'lu_2015_tax_FB-PA-14': {
                'sequence': 295,
                'description': '14%',
                'name': '14-E-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-PA-17': {
                'sequence': 297,
                'description': '17%',
                'name': '17-E-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-PA-16': {
                'sequence': 298,
                'description': '16%',
                'name': '16-E-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-PA-13': {
                'sequence': 299,
                'description': '13%',
                'name': '13-E-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-PA-7': {
                'sequence': 300,
                'description': '7%',
                'name': '7-E-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FB-PA-3': {
                'sequence': 301,
                'description': '3%',
                'name': '3-E-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FB-PA-8': {
                'sequence': 302,
                'description': '8%',
                'name': '8-E-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FP-EC-0': {
                'sequence': 303,
                'description': '0%',
                'name': '0-EC-E-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+445'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-445'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-EC-14': {
                'sequence': 305,
                'description': '14%',
                'name': '14-EC-E-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+753'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+754'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-753'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-754'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-EC-17': {
                'sequence': 311,
                'description': '17%',
                'name': '17-EC-E-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+751'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+752'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-751'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-752'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-EC-16': {
                'sequence': 312,
                'description': '16%',
                'name': '16-EC-E-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+951'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+952'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-951'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-952'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-EC-13': {
                'sequence': 313,
                'description': '13%',
                'name': '13-EC-E-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+953'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+954'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-953'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-954'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-EC-7': {
                'sequence': 314,
                'description': '7%',
                'name': '7-EC-E-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+955'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+956'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-955'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-956'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FP-EC-3': {
                'sequence': 315,
                'description': '3%',
                'name': '3-EC-E-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+441'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+442'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-441'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-442'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-EC-8': {
                'sequence': 320,
                'description': '8%',
                'name': '8-EC-E-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+755'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+756'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-755'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-756'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FP-IC-0': {
                'sequence': 323,
                'description': '0%',
                'name': 'EX-IC-E-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+435'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-435'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-IC-14': {
                'sequence': 327,
                'description': '14%',
                'name': '14-IC-E-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+743'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+744'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-743'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-744'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-IC-17': {
                'sequence': 333,
                'description': '17%',
                'name': '17-IC-E-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+741'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+742'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-741'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-742'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-IC-16': {
                'sequence': 334,
                'description': '16%',
                'name': '16-IC-E-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+941'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+942'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-941'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-942'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-IC-13': {
                'sequence': 335,
                'description': '13%',
                'name': '13-IC-E-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+943'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+944'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-943'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-944'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-IC-7': {
                'sequence': 336,
                'description': '7%',
                'name': '7-IC-E-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+945'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+946'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-945'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-946'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FP-IC-3': {
                'sequence': 337,
                'description': '3%',
                'name': '3-IC-E-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+431'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+432'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-431'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-432'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-IC-8': {
                'sequence': 342,
                'description': '8%',
                'name': '8-IC-E-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+745'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+746'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-745'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-746'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FP-PA-0': {
                'sequence': 345,
                'description': '0%',
                'name': '0-E-S',
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
                'active': False,
            },
            'lu_2015_tax_FP-PA-14': {
                'sequence': 347,
                'description': '14%',
                'name': '14-E-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-PA-17': {
                'sequence': 349,
                'description': '17%',
                'name': '17-E-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-PA-16': {
                'sequence': 350,
                'description': '16%',
                'name': '16-E-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-PA-13': {
                'sequence': 351,
                'description': '13%',
                'name': '13-E-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-PA-7': {
                'sequence': 352,
                'description': '7%',
                'name': '7-E-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_FP-PA-3': {
                'sequence': 353,
                'description': '3%',
                'name': '3-E-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_FP-PA-8': {
                'sequence': 354,
                'description': '8%',
                'name': '8-E-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IB-EC-0': {
                'sequence': 355,
                'description': '0%',
                'name': '0-EC-IG',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+195'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-195'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-EC-14': {
                'sequence': 357,
                'description': '14%',
                'name': '14-EC-IG',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+723'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+724'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-723'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-724'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-EC-17': {
                'sequence': 363,
                'description': '17%',
                'name': '17-EC-IG',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+721'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+722'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-721'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-722'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-EC-16': {
                'sequence': 364,
                'description': '16%',
                'name': '16-EC-IG',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+921'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+922'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-921'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-922'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-EC-13': {
                'sequence': 365,
                'description': '13%',
                'name': '13-EC-IG',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+923'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+924'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-923'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-924'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-EC-7': {
                'sequence': 366,
                'description': '7%',
                'name': '7-EC-IG',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+925'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+926'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-925'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-926'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IB-EC-3': {
                'sequence': 367,
                'description': '3%',
                'name': '3-EC-IG',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+059'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+068'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-059'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-068'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-EC-8': {
                'sequence': 372,
                'description': '8%',
                'name': '8-EC-IG',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+725'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+726'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-725'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-726'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-0': {
                'sequence': 375,
                'description': '5%',
                'name': '0-EC(P)-IG',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+196'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-196'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-14': {
                'sequence': 379,
                'description': '14%',
                'name': '14-EC(P)-IG',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+733'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+734'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-733'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-734'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-17': {
                'sequence': 385,
                'description': '17%',
                'name': '17-EC(P)-IG',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+731'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+732'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-731'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-732'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-16': {
                'sequence': 386,
                'description': '16%',
                'name': '16-EC(P)-IG',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+931'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+932'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-931'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-932'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-13': {
                'sequence': 387,
                'description': '13%',
                'name': '13-EC(P)-IG',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+933'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+934'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-933'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-934'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-7': {
                'sequence': 388,
                'description': '7%',
                'name': '7-EC(P)-IG',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+935'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+936'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-935'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-936'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-3': {
                'sequence': 389,
                'description': '3%',
                'name': '3-EC(P)-IG',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+063'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+073'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-063'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-073'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-ECP-8': {
                'sequence': 394,
                'description': '8%',
                'name': '8-EC(P)-IG',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+735'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+736'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-735'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+460'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-736'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IB-IC-0': {
                'sequence': 397,
                'description': '0%',
                'name': '0-IC-IG',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+194'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-194'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-IC-14': {
                'sequence': 401,
                'description': '14%',
                'name': '14-IC-IG',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+713'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+714'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-713'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-714'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-IC-17': {
                'sequence': 407,
                'description': '17%',
                'name': '17-IC-IG',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+711'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+712'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-711'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-712'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-IC-16': {
                'sequence': 407,
                'description': '16%',
                'name': '16-IC-IG',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+911'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+912'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-911'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-912'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-IC-13': {
                'sequence': 408,
                'description': '13%',
                'name': '13-IC-IG',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+913'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+914'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-913'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-914'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-IC-7': {
                'sequence': 409,
                'description': '7%',
                'name': '7-IC-IG',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+915'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+916'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-915'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-916'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IB-IC-3': {
                'sequence': 410,
                'description': '3%',
                'name': '3-IC-IG',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+049'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+054'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-049'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-054'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-IC-8': {
                'sequence': 416,
                'description': '8%',
                'name': '8-IC-IG',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+715'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+716'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-715'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+459'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-716'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IB-PA-0': {
                'sequence': 419,
                'description': '0%',
                'name': '0-IG',
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
                'active': False,
            },
            'lu_2015_tax_IB-PA-14': {
                'sequence': 421,
                'description': '14%',
                'name': '14-IG',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-PA-17': {
                'sequence': 423,
                'description': '17%',
                'name': '17-IG',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-PA-16': {
                'sequence': 424,
                'description': '16%',
                'name': '16-IG',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-PA-13': {
                'sequence': 425,
                'description': '13%',
                'name': '13-IG',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-PA-7': {
                'sequence': 426,
                'description': '7%',
                'name': '7-IG',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IB-PA-3': {
                'sequence': 427,
                'description': '3%',
                'name': '3-IG',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IB-PA-8': {
                'sequence': 428,
                'description': '8%',
                'name': '8-IG',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IP-EC-0': {
                'sequence': 429,
                'description': '0%',
                'name': '0-EC-IS',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+445'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-445'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-EC-14': {
                'sequence': 431,
                'description': '14%',
                'name': '14-EC-IS',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+753'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+754'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-753'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-754'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-EC-17': {
                'sequence': 437,
                'description': '17%',
                'name': '17-EC-IS',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+751'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+752'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-751'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-752'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-EC-16': {
                'sequence': 438,
                'description': '16%',
                'name': '16-EC-IS',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+951'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+952'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-951'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-952'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-EC-13': {
                'sequence': 439,
                'description': '13%',
                'name': '13-EC-IS',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+953'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+954'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-953'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-954'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-EC-7': {
                'sequence': 440,
                'description': '7%',
                'name': '7-EC-IS',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+955'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+956'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-955'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-956'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IP-EC-3': {
                'sequence': 441,
                'description': '3%',
                'name': '3-EC-IS',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+441'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+442'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-441'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-442'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-EC-8': {
                'sequence': 446,
                'description': '8%',
                'name': '8-EC-IS',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+755'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+756'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-755'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-756'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IP-IC-0': {
                'sequence': 449,
                'description': '0%',
                'name': '0-IC-IS',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+435'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-435'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-IC-14': {
                'sequence': 453,
                'description': '14%',
                'name': '14-IC-IS',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+743'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+744'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-743'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-744'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-IC-17': {
                'sequence': 459,
                'description': '17%',
                'name': '17-IC-IS',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+741'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+742'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-741'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-742'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-IC-16': {
                'sequence': 459,
                'description': '16%',
                'name': '16-IC-IS',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+941'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+942'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-941'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-942'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-IC-13': {
                'sequence': 460,
                'description': '13%',
                'name': '13-IC-IS',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+943'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+944'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-943'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-944'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-IC-7': {
                'sequence': 461,
                'description': '7%',
                'name': '7-IC-IS',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+945'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+946'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-945'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-946'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IP-IC-3': {
                'sequence': 462,
                'description': '3%',
                'name': '3-IC-IS',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+431'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+432'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-431'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-432'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-IC-8': {
                'sequence': 468,
                'description': '8%',
                'name': '8-IC-IS',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+745'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+746'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-745'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+461'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-746'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IP-PA-0': {
                'sequence': 471,
                'description': '0%',
                'name': '0-IS',
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
                'active': False,
            },
            'lu_2015_tax_IP-PA-14': {
                'sequence': 473,
                'description': '14%',
                'name': '14-IS',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-PA-17': {
                'sequence': 475,
                'description': '17%',
                'name': '17-IS',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-PA-16': {
                'sequence': 476,
                'description': '16%',
                'name': '16-IS',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-PA-13': {
                'sequence': 477,
                'description': '13%',
                'name': '13-IS',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-PA-7': {
                'sequence': 478,
                'description': '7%',
                'name': '7-IS',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_IP-PA-3': {
                'sequence': 479,
                'description': '3%',
                'name': '3-IS',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_IP-PA-8': {
                'sequence': 480,
                'description': '8%',
                'name': '8-IS',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('+458'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_421611',
                        'tag_ids': tags('-458'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_V-ART-43_60b': {
                'sequence': 489,
                'description': '0%',
                'name': '0-E-Art.43&60b',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+015'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-015'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_V-ART-44_56q': {
                'sequence': 480,
                'description': '0%',
                'name': '0-E-Art.44&56q',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+016'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-016'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_VB-EC-0': {
                'sequence': 481,
                'description': '0%',
                'name': '0-EC-S-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+014'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-014'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_VB-EC-Tab': {
                'sequence': 482,
                'description': '0%',
                'name': '0-EC-ST-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+017'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-017'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_VB-IC-0': {
                'sequence': 483,
                'description': '0%',
                'name': '0-IC-S-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+457'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-457'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2011_tax_VB-IC-Tab': {
                'sequence': 484,
                'description': '0%',
                'name': '0-IC-ST-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+017'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-017'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_VB-PA-0': {
                'sequence': 485,
                'description': '0%',
                'name': '0-S-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+033'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-033'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-PA-14': {
                'sequence': 487,
                'description': '14%',
                'name': '14-S-G',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+703'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+704'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-703'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-704'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-PA-17': {
                'sequence': 502,
                'description': '17%',
                'name': '17-S-G',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+701'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+702'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-701'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-702'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-PA-16': {
                'sequence': 503,
                'description': '16%',
                'name': '16-S-G',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+901'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+902'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-901'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-902'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-PA-13': {
                'sequence': 504,
                'description': '13%',
                'name': '13-S-G',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+903'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+904'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-903'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-904'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-PA-7': {
                'sequence': 505,
                'description': '7%',
                'name': '7-S-G',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+905'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+906'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-905'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-906'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_VB-PA-3': {
                'sequence': 490,
                'description': '3%',
                'name': '3-S-G',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+031'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+040'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-031'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-040'),
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-PA-8': {
                'sequence': 492,
                'description': '8%',
                'name': '8-S-G',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+705'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+706'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-705'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-706'),
                    }),
                ],
                'active': False,
            },
            'lu_2011_tax_VB-PA-Tab': {
                'sequence': 493,
                'description': '0%',
                'name': '0-ST-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+017'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-017'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'active': False,
            },
            'lu_2015_tax_VB-TR-0': {
                'sequence': 494,
                'description': '0%',
                'name': '0-ICT-S-G',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+018'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-018'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2011_tax_VP-EC-0': {
                'sequence': 495,
                'description': '0%',
                'name': '0-EC-S-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+019'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-019'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2011_tax_VP-IC-0': {
                'sequence': 496,
                'description': '0%',
                'name': '0-IC-S-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+423'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-423'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2011_tax_VP-IC-EX': {
                'sequence': 497,
                'description': '0%',
                'name': 'EX-IC-S-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+424'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-424'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2011_tax_VP-PA-0': {
                'sequence': 498,
                'description': '0%',
                'name': '0-S-S',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+033'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-033'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'lu_2015_tax_VP-PA-14': {
                'sequence': 500,
                'description': '14%',
                'name': '14-S-S',
                'amount': 14.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+703'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+704'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-703'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-704'),
                    }),
                ],
            },
            'lu_2015_tax_VP-PA-17': {
                'sequence': 479,
                'description': '17%',
                'name': '17-S-S',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+701'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+702'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-701'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-702'),
                    }),
                ],
            },
            'lu_2015_tax_VP-PA-16': {
                'sequence': 480,
                'description': '16%',
                'name': '16-S-S',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+901'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+902'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-901'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-902'),
                    }),
                ],
            },
            'lu_2015_tax_VP-PA-13': {
                'sequence': 481,
                'description': '13%',
                'name': '13-S-S',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+903'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+904'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-903'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-904'),
                    }),
                ],
            },
            'lu_2015_tax_VP-PA-7': {
                'sequence': 482,
                'description': '7%',
                'name': '7-S-S',
                'amount': 7.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+905'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+906'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-905'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-906'),
                    }),
                ],
            },
            'lu_2011_tax_VP-PA-3': {
                'sequence': 503,
                'description': '3%',
                'name': '3-S-S',
                'amount': 3.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+031'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+040'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-031'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-040'),
                    }),
                ],
            },
            'lu_2015_tax_VP-PA-8': {
                'sequence': 505,
                'description': '8%',
                'name': '8-S-S',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+705'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+706'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-705'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-706'),
                    }),
                ],
            },
            'lu_2015_tax_SANS': {
                'sequence': 506,
                'description': '0%',
                'name': '0-P-Tax-Free',
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
            'lu_2015_tax_SANS_sale': {
                'sequence': 507,
                'description': '0%',
                'name': '0-S-Tax-Free',
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
            'lu_2015_tax_ATN_sale': {
                'sequence': 510,
                'description': '17%',
                'name': '17-ATN',
                'amount': 17.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+456', '+701'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+702'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-456', '-701'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-702'),
                    }),
                ],
            },
            'lu_2015_tax_ATN_sale_16': {
                'sequence': 511,
                'description': '16%',
                'name': '16-ATN',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+456', '+901'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('+902'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-456', '-901'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'lu_2020_account_461411',
                        'tag_ids': tags('-902'),
                    }),
                ],
            },
        }

    def _get_lu_fiscal_position(self, template_code):
        return {
            'account_fiscal_position_template_LU_NO': {
                'name': 'Not liable to VAT',
                'sequence': 0,
            },
            'account_fiscal_position_template_LU_LU': {
                'name': 'Luxembourgish Taxable Person',
                'sequence': 1,
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.lu',
            },
            'account_fiscal_position_template_private_LU_IC': {
                'name': 'EU private',
                'sequence': 2,
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'account_fiscal_position_template_LU_IC': {
                'name': 'Intra-Community Taxable Person',
                'sequence': 3,
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-17',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-16',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-14',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-13',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-8',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-7',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_VB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-17',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-16',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-14',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-13',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-8',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-7',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_VP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-17',
                        'tax_dest_id': 'lu_2015_tax_FB-IC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-16',
                        'tax_dest_id': 'lu_2015_tax_FB-IC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-14',
                        'tax_dest_id': 'lu_2015_tax_FB-IC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-13',
                        'tax_dest_id': 'lu_2015_tax_FB-IC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-8',
                        'tax_dest_id': 'lu_2015_tax_FB-IC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-7',
                        'tax_dest_id': 'lu_2015_tax_FB-IC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_FB-IC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_FB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-17',
                        'tax_dest_id': 'lu_2015_tax_FP-IC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-16',
                        'tax_dest_id': 'lu_2015_tax_FP-IC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-14',
                        'tax_dest_id': 'lu_2015_tax_FP-IC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-13',
                        'tax_dest_id': 'lu_2015_tax_FP-IC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-8',
                        'tax_dest_id': 'lu_2015_tax_FP-IC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-7',
                        'tax_dest_id': 'lu_2015_tax_FP-IC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_FP-IC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_FP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-17',
                        'tax_dest_id': 'lu_2015_tax_IB-IC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-16',
                        'tax_dest_id': 'lu_2015_tax_IB-IC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-14',
                        'tax_dest_id': 'lu_2015_tax_IB-IC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-13',
                        'tax_dest_id': 'lu_2015_tax_IB-IC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-8',
                        'tax_dest_id': 'lu_2015_tax_IB-IC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-7',
                        'tax_dest_id': 'lu_2015_tax_IB-IC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_IB-IC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_IB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-17',
                        'tax_dest_id': 'lu_2015_tax_IP-IC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-16',
                        'tax_dest_id': 'lu_2015_tax_IP-IC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-14',
                        'tax_dest_id': 'lu_2015_tax_IP-IC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-13',
                        'tax_dest_id': 'lu_2015_tax_IP-IC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-8',
                        'tax_dest_id': 'lu_2015_tax_IP-IC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-7',
                        'tax_dest_id': 'lu_2015_tax_IP-IC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_IP-IC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_IP-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-17',
                        'tax_dest_id': 'lu_2015_tax_AB-IC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-16',
                        'tax_dest_id': 'lu_2015_tax_AB-IC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-14',
                        'tax_dest_id': 'lu_2015_tax_AB-IC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-13',
                        'tax_dest_id': 'lu_2015_tax_AB-IC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-8',
                        'tax_dest_id': 'lu_2015_tax_AB-IC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-7',
                        'tax_dest_id': 'lu_2015_tax_AB-IC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_AB-IC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_AB-IC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-17',
                        'tax_dest_id': 'lu_2015_tax_AP-IC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-16',
                        'tax_dest_id': 'lu_2015_tax_AP-IC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-14',
                        'tax_dest_id': 'lu_2015_tax_AP-IC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-13',
                        'tax_dest_id': 'lu_2015_tax_AP-IC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-8',
                        'tax_dest_id': 'lu_2015_tax_AP-IC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-7',
                        'tax_dest_id': 'lu_2015_tax_AP-IC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_AP-IC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_AP-IC-0',
                    }),
                ],
            },
            'account_fiscal_position_template_LU_EC': {
                'name': 'Extra-Community Taxable Person',
                'sequence': 4,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-17',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-16',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-14',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-13',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-8',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VB-PA-7',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_VB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-17',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-16',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-14',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-13',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-8',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_VP-PA-7',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_VP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_VP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-17',
                        'tax_dest_id': 'lu_2015_tax_FB-EC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-16',
                        'tax_dest_id': 'lu_2015_tax_FB-EC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-14',
                        'tax_dest_id': 'lu_2015_tax_FB-EC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-13',
                        'tax_dest_id': 'lu_2015_tax_FB-EC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-8',
                        'tax_dest_id': 'lu_2015_tax_FB-EC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FB-PA-7',
                        'tax_dest_id': 'lu_2015_tax_FB-EC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_FB-EC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_FB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-17',
                        'tax_dest_id': 'lu_2015_tax_FP-EC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-16',
                        'tax_dest_id': 'lu_2015_tax_FP-EC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-14',
                        'tax_dest_id': 'lu_2015_tax_FP-EC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-13',
                        'tax_dest_id': 'lu_2015_tax_FP-EC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-8',
                        'tax_dest_id': 'lu_2015_tax_FP-EC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_FP-PA-7',
                        'tax_dest_id': 'lu_2015_tax_FP-EC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_FP-EC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_FP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_FP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-17',
                        'tax_dest_id': 'lu_2015_tax_IB-EC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-16',
                        'tax_dest_id': 'lu_2015_tax_IB-EC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-14',
                        'tax_dest_id': 'lu_2015_tax_IB-EC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-13',
                        'tax_dest_id': 'lu_2015_tax_IB-EC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-8',
                        'tax_dest_id': 'lu_2015_tax_IB-EC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IB-PA-7',
                        'tax_dest_id': 'lu_2015_tax_IB-EC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_IB-EC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_IB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-17',
                        'tax_dest_id': 'lu_2015_tax_IP-EC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-16',
                        'tax_dest_id': 'lu_2015_tax_IP-EC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-14',
                        'tax_dest_id': 'lu_2015_tax_IP-EC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-13',
                        'tax_dest_id': 'lu_2015_tax_IP-EC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-8',
                        'tax_dest_id': 'lu_2015_tax_IP-EC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_IP-PA-7',
                        'tax_dest_id': 'lu_2015_tax_IP-EC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_IP-EC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_IP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_IP-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-17',
                        'tax_dest_id': 'lu_2015_tax_AB-EC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-16',
                        'tax_dest_id': 'lu_2015_tax_AB-EC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-14',
                        'tax_dest_id': 'lu_2015_tax_AB-EC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-13',
                        'tax_dest_id': 'lu_2015_tax_AB-EC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-8',
                        'tax_dest_id': 'lu_2015_tax_AB-EC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AB-PA-7',
                        'tax_dest_id': 'lu_2015_tax_AB-EC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AB-PA-3',
                        'tax_dest_id': 'lu_2011_tax_AB-EC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AB-PA-0',
                        'tax_dest_id': 'lu_2011_tax_AB-EC-0',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-17',
                        'tax_dest_id': 'lu_2015_tax_AP-EC-17',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-16',
                        'tax_dest_id': 'lu_2015_tax_AP-EC-16',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-14',
                        'tax_dest_id': 'lu_2015_tax_AP-EC-14',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-13',
                        'tax_dest_id': 'lu_2015_tax_AP-EC-13',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-8',
                        'tax_dest_id': 'lu_2015_tax_AP-EC-8',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2015_tax_AP-PA-7',
                        'tax_dest_id': 'lu_2015_tax_AP-EC-7',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AP-PA-3',
                        'tax_dest_id': 'lu_2011_tax_AP-EC-3',
                    }),
                    Command.create({
                        'tax_src_id': 'lu_2011_tax_AP-PA-0',
                        'tax_dest_id': 'lu_2011_tax_AP-EC-0',
                    }),
                ],
            },
        }

    def _get_lu_reconcile_model(self, template_code):
        return {
            'bank_fees_template': {
                'name': 'Bank Fees',
                'rule_type': 'writeoff_button',
                'line_ids': [
                    Command.create({
                        'account_id': 'lu_2011_account_61333',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Bank Fees',
                    }),
                ],
            },
            'cash_discount_template': {
                'name': 'Cash Discount',
                'rule_type': 'writeoff_button',
                'line_ids': [
                    Command.create({
                        'account_id': 'lu_2020_account_65562',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Cash Discount',
                    }),
                ],
            },
        }
