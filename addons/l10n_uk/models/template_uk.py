# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_uk_template_data(self, template_code):
        return {
            'property_account_receivable_id': '1100',
            'property_account_payable_id': '2100',
            'property_account_expense_categ_id': '5000',
            'property_account_income_categ_id': '4000',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '1200',
            'cash_account_code_prefix': '1210',
            'transfer_account_code_prefix': '1220',
            'code_digits': '6',
        }

    def _get_uk_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.uk',
                'account_default_pos_receivable_account_id': '1104',
                'income_currency_exchange_account_id': '7700',
                'expense_currency_exchange_account_id': '7700',
            },
        }

    def _get_uk_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'ST0': {
                'description': 'ST0',
                'type_tax_use': 'sale',
                'name': 'Zero rated sales',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'ST2': {
                'description': 'ST2',
                'type_tax_use': 'sale',
                'name': 'Exempt sales',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'PT0': {
                'description': 'PT0',
                'type_tax_use': 'purchase',
                'name': 'Zero rated purchases',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'PT2': {
                'description': 'PT2',
                'type_tax_use': 'purchase',
                'name': 'Exempt purchases',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'PT8': {
                'description': 'PT8',
                'type_tax_use': 'purchase',
                'name': 'Standard rated purchases from EC',
                'amount_type': 'percent',
                'amount': 20.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+9', '+7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('+2'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('-4'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-9', '-7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('-2'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('+4'),
                    }),
                ],
            },
            'PT5': {
                'description': 'PT5',
                'type_tax_use': 'purchase',
                'name': 'Lower rate purchases (5%)',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('+4'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('-4'),
                    }),
                ],
            },
            'ST5': {
                'description': 'ST5',
                'type_tax_use': 'sale',
                'name': 'Lower rate sales (5%)',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2200',
                        'tag_ids': tags('+1'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2200',
                        'tag_ids': tags('-1'),
                    }),
                ],
            },
            'ST4': {
                'description': 'ST4',
                'type_tax_use': 'sale',
                'name': 'Sales to customers in EC',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+8', '+6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-8', '-6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'PT7': {
                'description': 'PT7',
                'type_tax_use': 'purchase',
                'name': 'Zero rated purchases from EC',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+9', '+7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-9', '-7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'ST11': {
                'description': 'ST11',
                'type_tax_use': 'sale',
                'name': 'Standard rate sales (20%)',
                'amount_type': 'percent',
                'amount': 20.0,
                'tax_group_id': 'tax_group_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2200',
                        'tag_ids': tags('+1'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2200',
                        'tag_ids': tags('-1'),
                    }),
                ],
            },
            'PT11': {
                'description': 'PT11',
                'type_tax_use': 'purchase',
                'name': 'Standard rate purchases (20%)',
                'amount_type': 'percent',
                'amount': 20.0,
                'tax_group_id': 'tax_group_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('+4'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '2201',
                        'tag_ids': tags('-4'),
                    }),
                ],
            },
        }
