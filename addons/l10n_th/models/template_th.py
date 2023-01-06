# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_th_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'a_recv',
            'property_account_payable_id': 'a_pay',
            'property_account_expense_categ_id': 'a_exp_cogs',
            'property_account_income_categ_id': 'a_sales',
            'cash_account_code_prefix': '1100',
            'bank_account_code_prefix': '1110',
            'transfer_account_code_prefix': '16',
        }

    def _get_th_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.th',
                'account_default_pos_receivable_account_id': 'a_recv_pos',
                'income_currency_exchange_account_id': 'a_income_gain',
                'expense_currency_exchange_account_id': 'a_exp_loss',
            },
        }

    def _get_th_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_input_vat': {
                'name': 'Input VAT 7%',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_vat_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6. Purchase amount that is entitled to deduction of input tax from output tax in tax computation'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_input_vat',
                        'tag_ids': tags('+7. Input tax (according to invoice of purchase amount in 6.)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6. Purchase amount that is entitled to deduction of input tax from output tax in tax computation'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_input_vat',
                        'tag_ids': tags('-7. Input tax (according to invoice of purchase amount in 6.)'),
                    }),
                ],
            },
            'tax_output_vat': {
                'name': 'Output VAT 7%',
                'amount_type': 'percent',
                'amount': 7.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_vat_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1. Sales amount'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_output_vat',
                        'tag_ids': tags('+5. Output tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1. Sales amount'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_output_vat',
                        'tag_ids': tags('-5. Output tax'),
                    }),
                ],
            },
            'tax_input_vat_0': {
                'name': 'Input VAT 0%',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6. Purchase amount that is entitled to deduction of input tax from output tax in tax computation'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_input_vat',
                        'tag_ids': tags('+7. Input tax (according to invoice of purchase amount in 6.)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6. Purchase amount that is entitled to deduction of input tax from output tax in tax computation'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_input_vat',
                        'tag_ids': tags('+7. Input tax (according to invoice of purchase amount in 6.)'),
                    }),
                ],
            },
            'tax_output_vat_0': {
                'name': 'Output VAT 0%',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1. Sales amount', '+2. Less sales subject to 0% tax rate'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_output_vat',
                        'tag_ids': tags('+5. Output tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1. Sales amount', '-2. Less sales subject to 0% tax rate'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_output_vat',
                        'tag_ids': tags('-5. Output tax'),
                    }),
                ],
            },
            'tax_input_vat_exempted': {
                'name': 'Input VAT Exempted',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6. Purchase amount that is entitled to deduction of input tax from output tax in tax computation'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_input_vat',
                        'tag_ids': tags('+7. Input tax (according to invoice of purchase amount in 6.)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6. Purchase amount that is entitled to deduction of input tax from output tax in tax computation'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_input_vat',
                        'tag_ids': tags('-7. Input tax (according to invoice of purchase amount in 6.)'),
                    }),
                ],
            },
            'tax_output_vat_exempted': {
                'name': 'Output VAT Exempted',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1. Sales amount', '+3. Less exempted sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_output_vat',
                        'tag_ids': tags('+5. Output tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1. Sales amount', '-3. Less exempted sales'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_output_vat',
                        'tag_ids': tags('-5. Output tax'),
                    }),
                ],
            },
            'tax_wht_co_1': {
                'name': 'Company Withholding Tax 1% (Transportation)',
                'amount_type': 'percent',
                'amount': -1.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_co_2': {
                'name': 'Company Withholding Tax 2% (Advertising)',
                'amount_type': 'percent',
                'amount': -2.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_co_3': {
                'name': 'Company Withholding Tax 3% (Service)',
                'amount_type': 'percent',
                'amount': -3.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_co_5': {
                'name': 'Company Withholding Tax 5% (Rental)',
                'amount_type': 'percent',
                'amount': -5.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_pers_1': {
                'name': 'Personal Withholding Tax 1% (Transportation)',
                'amount_type': 'percent',
                'amount': -1.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_pers_2': {
                'name': 'Personal Withholding Tax 2% (Advertising)',
                'amount_type': 'percent',
                'amount': -2.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_pers_3': {
                'name': 'Personal Withholding Tax 3% (Service)',
                'amount_type': 'percent',
                'amount': -3.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_pers_5': {
                'name': 'Personal Withholding Tax 5% (Rental)',
                'amount_type': 'percent',
                'amount': -5.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht',
                    }),
                ],
            },
            'tax_wht_income_1': {
                'name': 'Withholding Income Tax 1% (Transportation)',
                'amount_type': 'percent',
                'amount': -1.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
            },
            'tax_wht_income_2': {
                'name': 'Withholding Income Tax 2% (Advertising)',
                'amount_type': 'percent',
                'amount': -2.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
            },
            'tax_wht_income_3': {
                'name': 'Withholding Income Tax 3% (Service)',
                'amount_type': 'percent',
                'amount': -3.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
            },
            'tax_wht_income_5': {
                'name': 'Withholding Income Tax 5% (Rental)',
                'amount_type': 'percent',
                'amount': -5.0,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a_wht_income',
                    }),
                ],
            },
        }
