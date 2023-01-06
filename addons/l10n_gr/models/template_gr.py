# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_gr_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'chartgr_30_00',
            'property_account_payable_id': 'chartgr_50_00',
            'property_account_expense_categ_id': 'chartgr_64_98',
            'property_account_income_categ_id': 'chartgr_71_00',
            'bank_account_code_prefix': '38',
            'cash_account_code_prefix': '38',
            'transfer_account_code_prefix': '38.07',
            'code_digits': '6',
        }

    def _get_gr_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.gr',
                'account_default_pos_receivable_account_id': 'chartgr_30_00_01',
                'income_currency_exchange_account_id': 'chartgr_79_79',
                'expense_currency_exchange_account_id': 'chartgr_64_98_06',
            },
        }

    def _get_gr_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'ivat19': {
                'name': 'Πωλήσεις ΦΠΑ 19%',
                'description': 'Πωλήσεις ΦΠΑ 19%',
                'amount': 19.0,
                'sequence': 3,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+303 Πωλήσεις 19-23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+333 ΦΠΑ 19-23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'ivat21': {
                'name': 'Πωλήσεις ΦΠΑ 21%',
                'description': 'Πωλήσεις ΦΠΑ 21%',
                'amount': 21.0,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+303 Πωλήσεις 19-23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+333 ΦΠΑ 19-23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'ivat23': {
                'name': 'Πωλήσεις ΦΠΑ 23%',
                'description': 'Πωλήσεις ΦΠΑ 23%',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+303 Πωλήσεις 19-23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+333 ΦΠΑ 19-23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'pvat19': {
                'name': 'Αγορές ΦΠΑ19%',
                'description': 'Αγορές ΦΠΑ19%',
                'amount': 19.0,
                'sequence': 3,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+353 Αγορές ΦΠΑ 19-23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+373 ΦΠΑ Αγορών 19-23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'pvat21': {
                'name': 'Αγορές ΦΠΑ21%',
                'description': 'Αγορές ΦΠΑ21%',
                'amount': 21.0,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+353 Αγορές ΦΠΑ 19-23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+373 ΦΠΑ Αγορών 19-23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'pvat23': {
                'name': 'Αγορές ΦΠΑ23%',
                'description': 'Αγορές ΦΠΑ23%',
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+353 Αγορές ΦΠΑ 19-23%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+373 ΦΠΑ Αγορών 19-23%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'evat19': {
                'name': 'Δαπάνες ΦΠΑ19%',
                'description': 'Δαπάνες ΦΠΑ19%',
                'amount': 19.0,
                'sequence': 3,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+357 Δαπάνες/Έξοδα φορολ.'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+377 ΦΠΑ Δαπανών'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'evat21': {
                'name': 'Δαπάνες ΦΠΑ21%',
                'description': 'Δαπάνες ΦΠΑ21%',
                'amount': 21.0,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+357 Δαπάνες/Έξοδα φορολ.'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+377 ΦΠΑ Δαπανών'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
            'evat23': {
                'name': 'Δαπάνες ΦΠΑ23%',
                'description': 'Δαπάνες ΦΠΑ23%',
                'amount': 23.0,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+357 Δαπάνες/Έξοδα φορολ.'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                        'tag_ids': tags('+377 ΦΠΑ Δαπανών'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chartgr_54_00',
                    }),
                ],
            },
        }
