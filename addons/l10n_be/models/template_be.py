# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_be_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_be_fiscal_position(template_code),
            'account.reconcile.model': self._get_be_reconcile_model(template_code),
        }

    def _get_be_template_data(self, template_code):
        return {
            'code_digits': '6',
            'property_account_receivable_id': 'a400',
            'property_account_payable_id': 'a440',
            'property_account_expense_categ_id': 'a600',
            'property_account_income_categ_id': 'a7000',
            'property_tax_payable_account_id': 'a4512',
            'property_tax_receivable_account_id': 'a4112',
            'bank_account_code_prefix': '550',
            'cash_account_code_prefix': '570',
            'transfer_account_code_prefix': '580',
        }

    def _get_be_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.be',
                'account_default_pos_receivable_account_id': 'a4001',
                'income_currency_exchange_account_id': 'a754',
                'expense_currency_exchange_account_id': 'a654',
                'account_journal_suspense_account_id': 'a499',
                'account_journal_early_pay_discount_loss_account_id': 'a657000',
                'account_journal_early_pay_discount_gain_account_id': 'a757000',
            },
        }

    def _get_be_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'attn_VAT-OUT-21-L': {
                'sequence': 10,
                'description': '21%',
                'name': '21%',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+54'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+64'),
                    }),
                ],
            },
            'attn_VAT-OUT-21-S': {
                'sequence': 11,
                'description': '21%',
                'name': '21% S',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+03'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+54'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+64'),
                    }),
                ],
            },
            'attn_VAT-OUT-12-S': {
                'sequence': 20,
                'description': '12%',
                'name': '12% S',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+54'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+64'),
                    }),
                ],
            },
            'attn_VAT-OUT-12-L': {
                'sequence': 21,
                'description': '12%',
                'name': '12%',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+02'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+54'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+64'),
                    }),
                ],
            },
            'attn_VAT-OUT-06-S': {
                'sequence': 30,
                'description': '6%',
                'name': '6% S',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+01'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+54'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+64'),
                    }),
                ],
            },
            'attn_VAT-OUT-06-L': {
                'sequence': 31,
                'description': '6%',
                'name': '6%',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+01'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+54'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a451',
                        'tag_ids': tags('+64'),
                    }),
                ],
            },
            'attn_VAT-OUT-00-S': {
                'sequence': 40,
                'description': '0%',
                'name': '0% S',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+00'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-OUT-00-L': {
                'sequence': 41,
                'description': '0%',
                'name': '0%',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+00'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-OUT-00-CC': {
                'sequence': 50,
                'description': '0%',
                'name': '0% Cocont',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+45'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-OUT-00-EU-S': {
                'sequence': 60,
                'description': '0%',
                'name': '0% EU S',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
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
                        'tag_ids': tags('+48s44'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-OUT-00-EU-L': {
                'sequence': 61,
                'description': '0%',
                'name': '0% EU M',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+46L'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+48s46L'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-OUT-00-EU-T': {
                'sequence': 62,
                'description': '0%',
                'name': '0% EU T',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+46T'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+48s46T'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-OUT-00-ROW': {
                'sequence': 70,
                'description': '0%',
                'name': '0% EX',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+47'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+49'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V81-21': {
                'sequence': 110,
                'description': '21%',
                'name': '21% M',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V81-12': {
                'sequence': 120,
                'description': '12%',
                'name': '12% M',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V81-06': {
                'sequence': 130,
                'description': '6%',
                'name': '6% M',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V81-00': {
                'sequence': 140,
                'description': '0%',
                'name': '0% M',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_TVA-21-inclus-dans-prix': {
                'sequence': 150,
                'description': '21%',
                'name': '21% S.TTC',
                'price_include': True,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-21-S': {
                'sequence': 210,
                'description': '21%',
                'name': '21% S',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-21-G': {
                'sequence': 220,
                'description': '21%',
                'name': '21% G',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-12-S': {
                'sequence': 230,
                'description': '12%',
                'name': '12% S',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-12-G': {
                'sequence': 240,
                'description': '12%',
                'name': '12% G',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-06-S': {
                'sequence': 250,
                'description': '6%',
                'name': '6% S',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-06-G': {
                'sequence': 260,
                'description': '6%',
                'name': '6% G',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V82-00-S': {
                'sequence': 270,
                'description': '0%',
                'name': '0% S',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V82-00-G': {
                'sequence': 280,
                'description': '0%',
                'name': '0% G',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V83-21': {
                'sequence': 310,
                'description': '21%',
                'name': '21% IG',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V83-12': {
                'sequence': 320,
                'description': '12%',
                'name': '12% IG',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V83-06': {
                'sequence': 330,
                'description': '6%',
                'name': '6% IG',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V83-00': {
                'sequence': 340,
                'description': '0%',
                'name': '0% IG',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V81-21-CC': {
                'sequence': 410,
                'description': '21%',
                'name': '21% M.Cocont',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V81-12-CC': {
                'sequence': 420,
                'description': '12%',
                'name': '12% M.Cocont',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V81-06-CC': {
                'sequence': 430,
                'description': '6%',
                'name': '6% M.Cocont',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V81-00-CC': {
                'sequence': 440,
                'description': '0%',
                'name': '0% M.Cocont',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V82-21-CC': {
                'sequence': 510,
                'description': '21%',
                'name': '21% S.Cocont',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V82-12-CC': {
                'sequence': 520,
                'description': '12%',
                'name': '12% S.Cocont',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V82-06-CC': {
                'sequence': 530,
                'description': '6%',
                'name': '6% S.Cocont',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V82-00-CC': {
                'sequence': 540,
                'description': '0%',
                'name': '0% S.Cocont',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V83-21-CC': {
                'sequence': 610,
                'description': '21%',
                'name': '21% IG.Cocont',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V83-12-CC': {
                'sequence': 620,
                'description': '12%',
                'name': '12% IG.Cocont',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V83-06-CC': {
                'sequence': 630,
                'description': '6%',
                'name': '6% IG.Cocont',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                        'tag_ids': tags('-56'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451056',
                    }),
                ],
            },
            'attn_VAT-IN-V83-00-CC': {
                'sequence': 640,
                'description': '0%',
                'name': '0% IG.Cocont',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V82-CAR-EXC': {
                'sequence': 720,
                'description': '21%',
                'name': '21% Car',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'tag_ids': tags('+82'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+85', '-82'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'tag_ids': tags('-82', '+85'),
                    }),
                    Command.create({
                        'factor_percent': 50,
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+63'),
                    }),
                ],
            },
            'attn_VAT-IN-V81-21-EU': {
                'sequence': 1110,
                'description': '21%',
                'name': '21% EU M',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V81-12-EU': {
                'sequence': 1120,
                'description': '12%',
                'name': '12% EU M',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V81-06-EU': {
                'sequence': 1130,
                'description': '6%',
                'name': '6% EU M',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V81-00-EU': {
                'sequence': 1140,
                'description': '0%',
                'name': '0% EU M',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V82-21-EU-S': {
                'sequence': 1210,
                'description': '21%',
                'name': '21% EU S',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+88'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-88', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-21-EU-G': {
                'sequence': 1220,
                'description': '21%',
                'name': '21% EU G',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-12-EU-S': {
                'sequence': 1230,
                'description': '12%',
                'name': '12% EU S',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+88'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-88', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-12-EU-G': {
                'sequence': 1240,
                'description': '12%',
                'name': '12% EU G',
                'price_include': False,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-06-EU-S': {
                'sequence': 1250,
                'description': '6%',
                'name': '6% EU S',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+88'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-88', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-06-EU-G': {
                'sequence': 1260,
                'description': '6%',
                'name': '6% EU G',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-00-EU-S': {
                'sequence': 1270,
                'description': '0%',
                'name': '0% EU S',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+88'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-88', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V83-21-EU': {
                'sequence': 1310,
                'description': '21%',
                'name': '21% EU IG',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V82-00-EU-G': {
                'sequence': 1280,
                'description': '0%',
                'name': '0% EU G',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V83-12-EU': {
                'sequence': 1320,
                'description': '12%',
                'name': '12% EU IG',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V83-06-EU': {
                'sequence': 1330,
                'description': '6%',
                'name': '6% EU IG',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 6.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                        'tag_ids': tags('-55'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451055',
                    }),
                ],
            },
            'attn_VAT-IN-V83-00-EU': {
                'sequence': 1340,
                'description': '0%',
                'name': '0% EU IG',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+86'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-86', '+84'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V81-21-ROW-CC': {
                'sequence': 2110,
                'description': '21%',
                'name': '21% EX M',
                'price_include': False,
                'amount': 21.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V81-12-ROW-CC': {
                'sequence': 2120,
                'description': '12%',
                'name': '12% EX M',
                'amount': 12.0,
                'price_include': False,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V81-06-ROW-CC': {
                'sequence': 2130,
                'description': '6%',
                'name': '6% EX M',
                'price_include': False,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V81-00-ROW-CC': {
                'sequence': 2140,
                'description': '0%',
                'name': '0% EX M',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+81', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-81', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V82-21-ROW-CC': {
                'sequence': 2210,
                'description': '21%',
                'name': '21% EX S',
                'amount': 21.0,
                'price_include': False,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V82-12-ROW-CC': {
                'sequence': 2220,
                'description': '12%',
                'name': '12% EX S',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V82-06-ROW-CC': {
                'sequence': 2230,
                'description': '6%',
                'name': '6% EX S',
                'price_include': False,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'amount': 6.0,
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V82-00-ROW-CC': {
                'sequence': 2240,
                'description': '0%',
                'name': '0% EX S',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+82', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-82', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'attn_VAT-IN-V83-21-ROW-CC': {
                'sequence': 2310,
                'description': '21%',
                'name': '21% EX IG',
                'amount': 21.0,
                'price_include': False,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V83-12-ROW-CC': {
                'sequence': 2320,
                'description': '12%',
                'name': '12% EX IG',
                'price_include': False,
                'amount_type': 'percent',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V83-06-ROW-CC': {
                'sequence': 2330,
                'description': '6%',
                'name': '6% EX IG',
                'price_include': False,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'amount': 6.0,
                'active': False,
                'tax_group_id': 'tax_group_tva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                        'tag_ids': tags('+59'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                        'tag_ids': tags('-57'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a411',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a451057',
                    }),
                ],
            },
            'attn_VAT-IN-V83-00-ROW-CC': {
                'sequence': 2340,
                'description': '0%',
                'name': '0% EX IG',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': False,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+83', '+87'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-83', '-87', '+85'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_be_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'sequence': 1,
                'name': 'Régime National',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.be',
            },
            'fiscal_position_template_5': {
                'sequence': 2,
                'name': 'EU privé',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_2': {
                'sequence': 4,
                'name': 'Régime Extra-Communautaire',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-00-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-00-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-06-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-06-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-12-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-12-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-21-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-21-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-ROW',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-06',
                        'tax_dest_id': 'attn_VAT-IN-V81-06-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-12',
                        'tax_dest_id': 'attn_VAT-IN-V81-12-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-21',
                        'tax_dest_id': 'attn_VAT-IN-V81-21-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-06-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-06-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-06-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-06-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-12-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-12-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-12-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-12-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-21-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-21-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-21-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-21-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-06',
                        'tax_dest_id': 'attn_VAT-IN-V83-06-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-12',
                        'tax_dest_id': 'attn_VAT-IN-V83-12-ROW-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-21',
                        'tax_dest_id': 'attn_VAT-IN-V83-21-ROW-CC',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'a7000',
                        'account_dest_id': 'a7002',
                    }),
                    Command.create({
                        'account_src_id': 'a7010',
                        'account_dest_id': 'a7012',
                    }),
                    Command.create({
                        'account_src_id': 'a7050',
                        'account_dest_id': 'a7052',
                    }),
                ],
            },
            'fiscal_position_template_3': {
                'sequence': 3,
                'name': 'Régime Intra-Communautaire',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-00-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-00-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-L',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-06-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-06-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-L',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-12-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-12-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-L',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-21-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-21-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-EU-L',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-00',
                        'tax_dest_id': 'attn_VAT-IN-V81-00-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-06',
                        'tax_dest_id': 'attn_VAT-IN-V81-06-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-12',
                        'tax_dest_id': 'attn_VAT-IN-V81-12-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-21',
                        'tax_dest_id': 'attn_VAT-IN-V81-21-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-00-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-00-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-00-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-00-EU-G',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-06-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-06-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-06-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-06-EU-G',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-12-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-12-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-12-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-12-EU-G',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-21-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-21-EU-S',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-21-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-21-EU-G',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-00',
                        'tax_dest_id': 'attn_VAT-IN-V83-00-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-06',
                        'tax_dest_id': 'attn_VAT-IN-V83-06-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-12',
                        'tax_dest_id': 'attn_VAT-IN-V83-12-EU',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-21',
                        'tax_dest_id': 'attn_VAT-IN-V83-21-EU',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'a7000',
                        'account_dest_id': 'a7001',
                    }),
                    Command.create({
                        'account_src_id': 'a7010',
                        'account_dest_id': 'a7011',
                    }),
                    Command.create({
                        'account_src_id': 'a7050',
                        'account_dest_id': 'a7051',
                    }),
                ],
            },
            'fiscal_position_template_4': {
                'name': 'Régime Cocontractant',
                'sequence': 5,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-00-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-00-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-06-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-06-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-12-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-12-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-21-S',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-OUT-21-L',
                        'tax_dest_id': 'attn_VAT-OUT-00-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-06',
                        'tax_dest_id': 'attn_VAT-IN-V81-06-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-12',
                        'tax_dest_id': 'attn_VAT-IN-V81-12-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V81-21',
                        'tax_dest_id': 'attn_VAT-IN-V81-21-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-06-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-06-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-06-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-06-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-12-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-12-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-12-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-12-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-21-S',
                        'tax_dest_id': 'attn_VAT-IN-V82-21-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V82-21-G',
                        'tax_dest_id': 'attn_VAT-IN-V82-21-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-06',
                        'tax_dest_id': 'attn_VAT-IN-V83-06-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-12',
                        'tax_dest_id': 'attn_VAT-IN-V83-12-CC',
                    }),
                    Command.create({
                        'tax_src_id': 'attn_VAT-IN-V83-21',
                        'tax_dest_id': 'attn_VAT-IN-V83-21-CC',
                    }),
                ],
            },
        }

    def _get_be_reconcile_model(self, template_code):
        return {
            'escompte_template': {
                'name': 'Escompte',
                'line_ids': [
                    Command.create({
                        'account_id': 'a653',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Escompte accordé',
                    }),
                ],
            },
            'frais_bancaires_htva_template': {
                'name': 'Frais bancaires HTVA',
                'line_ids': [
                    Command.create({
                        'account_id': 'a6560',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Frais bancaires HTVA',
                    }),
                ],
            },
            'frais_bancaires_tva21_template': {
                'name': 'Frais bancaires TVA21',
                'line_ids': [
                    Command.create({
                        'account_id': 'a6560',
                        'amount_type': 'percentage',
                        'tax_ids': [
                            Command.set([
                                'l10n_be.attn_TVA-21-inclus-dans-prix',
                            ]),
                        ],
                        'amount_string': '100',
                        'label': 'Frais bancaires TVA21',
                    }),
                ],
            },
            'virements_internes_template': {
                'name': 'Virements internes',
                'to_check': False,
                'line_ids': [
                    Command.create({
                        'account_id': None,
                        'amount_type': 'percentage',
                        'amount_string': '100',
                        'label': 'Virements internes',
                    }),
                ],
            },
        }
