# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_vn_template_data(self, template_code):
        return {
            'code_digits': '0',
            'bank_account_code_prefix': '112',
            'cash_account_code_prefix': '111',
            'transfer_account_code_prefix': '113',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'chart131',
            'property_account_payable_id': 'chart331',
            'property_account_expense_categ_id': 'chart1561',
            'property_account_income_categ_id': 'chart5111',
        }

    def _get_vn_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.vn',
                'account_default_pos_receivable_account_id': 'chart132',
                'income_currency_exchange_account_id': 'chart515',
                'expense_currency_exchange_account_id': 'chart635',
                'account_journal_early_pay_discount_loss_account_id': 'chart9993',
                'account_journal_early_pay_discount_gain_account_id': 'chart9994',
            },
        }

    def _get_vn_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_purchase_vat10': {
                'name': 'Deductible VAT 10%',
                'description': 'Deductible VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Untaxed Purchase of Goods and Services taxed 10%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1331',
                        'tag_ids': tags('+VAT on purchase of goods and services 10%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Untaxed Purchase of Goods and Services taxed 10%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1331',
                        'tag_ids': tags('-VAT on purchase of goods and services 10%'),
                    }),
                ],
            },
            'tax_purchase_vat5': {
                'name': 'Deductible VAT 5%',
                'description': 'Deductible VAT 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Untaxed Purchase of Goods and Services taxed 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1331',
                        'tag_ids': tags('+VAT on purchase of goods and services 5%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Untaxed Purchase of Goods and Services taxed 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1331',
                        'tag_ids': tags('-VAT on purchase of goods and services 5%'),
                    }),
                ],
            },
            'tax_purchase_vat0': {
                'name': 'Deductible VAT 0%',
                'description': 'Deductible VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Untaxed Purchase of Goods and Services taxed 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Untaxed Purchase of Goods and Services taxed 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_sale_vat10': {
                'name': 'Value Added Tax (VAT) 10%',
                'description': 'Value Added Tax (VAT) 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Untaxed sales of goods and services taxed 10%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart33311',
                        'tag_ids': tags('+VAT on sales of goods and services 10%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Untaxed sales of goods and services taxed 10%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart33311',
                        'tag_ids': tags('-VAT on sales of goods and services 10%'),
                    }),
                ],
            },
            'tax_sale_vat5': {
                'name': 'Value Added Tax (VAT) 5%',
                'description': 'Value Added Tax (VAT) 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Untaxed sales of goods and services taxed 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart33311',
                        'tag_ids': tags('+VAT on sales of goods and services 5%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Untaxed sales of goods and services taxed 5%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart33311',
                        'tag_ids': tags('-VAT on sales of goods and services 5%'),
                    }),
                ],
            },
            'tax_sale_vat0': {
                'name': 'Value Added Tax (VAT) 0%',
                'description': 'Value Added Tax (VAT) 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Untaxed sales of goods and services taxed 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Untaxed sales of goods and services taxed 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }
