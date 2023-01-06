# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_rs_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_rs_fiscal_position(template_code),
        }

    def _get_rs_template_data(self, template_code):
        return {
            'property_account_expense_categ_id': 'rs_501',
            'property_account_income_categ_id': 'rs_604',
            'property_account_payable_id': 'rs_435',
            'property_account_receivable_id': 'rs_204',
            'property_tax_payable_account_id': 'rs_470',
            'property_tax_receivable_account_id': 'rs_270',
            'code_digits': '4',
            'use_anglo_saxon': True,
            'bank_account_code_prefix': '241',
            'cash_account_code_prefix': '243',
            'transfer_account_code_prefix': '250',
            'use_storno_accounting': True,
        }

    def _get_rs_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.rs',
                'income_currency_exchange_account_id': 'rs_663',
                'expense_currency_exchange_account_id': 'rs_563',
                'default_cash_difference_income_account_id': 'rs_6791',
                'default_cash_difference_expense_account_id': 'rs_5791',
            },
        }

    def _get_rs_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'rs_sale_vat_20': {
                'sequence': 10,
                'description': 'VAT 20%',
                'name': '20%',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': True,
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+003'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_470',
                        'tag_ids': tags('+103'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_470',
                        'tag_ids': tags('-103'),
                    }),
                ],
            },
            'rs_sale_vat_10': {
                'sequence': 20,
                'description': 'VAT 10%',
                'name': '10%',
                'price_include': False,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': True,
                'tax_group_id': 'tax_group_vat_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+004'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_471',
                        'tag_ids': tags('+104'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_471',
                        'tag_ids': tags('-104'),
                    }),
                ],
            },
            'rs_sale_vat_0': {
                'sequence': 30,
                'description': 'VAT 0%',
                'name': '0%',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': True,
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_471',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_471',
                    }),
                ],
            },
            'rs_sale_vat_0_deduct_previous_tax': {
                'sequence': 40,
                'description': 'VAT 0% with the right to deduct previous tax',
                'name': '0% - prev. tax deductible',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': True,
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+001'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'rs_sale_vat_0_no_deduct_previous_tax': {
                'sequence': 50,
                'description': 'VAT 0% without the right to deduct previous tax',
                'name': '0% - prev. tax not deductible',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'active': True,
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+002'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'rs_purchase_vat_20': {
                'sequence': 60,
                'description': 'VAT 20%',
                'name': '20%',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+008'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_270',
                        'tag_ids': tags('+108'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_270',
                        'tag_ids': tags('-108'),
                    }),
                ],
            },
            'rs_purchase_vat_10': {
                'sequence': 70,
                'description': 'VAT 10%',
                'name': '10%',
                'price_include': False,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+008'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_271',
                        'tag_ids': tags('+108'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_271',
                        'tag_ids': tags('-108'),
                    }),
                ],
            },
            'rs_purchase_vat_0': {
                'sequence': 80,
                'description': 'VAT 0%',
                'name': '0%',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'rs_purchase_import_vat_0': {
                'sequence': 90,
                'description': 'VAT 0% - import VAT exempt',
                'name': '0% - import',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+006'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'rs_purchase_import_vat_20': {
                'sequence': 100,
                'description': 'VAT 20% - import general rate',
                'name': '20% - import',
                'price_include': False,
                'amount': 20.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+006'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_274',
                        'tag_ids': tags('+106'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_274',
                        'tag_ids': tags('-106'),
                    }),
                ],
            },
            'rs_purchase_import_vat_10': {
                'sequence': 110,
                'description': 'VAT 10% - import specific rate',
                'name': '10% - import',
                'price_include': False,
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+006'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_275',
                        'tag_ids': tags('+106'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_275',
                        'tag_ids': tags('-106'),
                    }),
                ],
            },
            'rs_purchase_farmer_deductible_vat_8': {
                'sequence': 120,
                'description': 'VAT 8% - deductible farmers compensation',
                'name': '8% - farmers deductible',
                'price_include': False,
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_compensation',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+007'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_278',
                        'tag_ids': tags('+107'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'rs_278',
                        'tag_ids': tags('-107'),
                    }),
                ],
            },
            'rs_purchase_farmer_non_deductible_vat_8': {
                'sequence': 130,
                'description': 'VAT 8% - non-deductible farmers compensation',
                'name': '8% - farmers non-deductible',
                'price_include': False,
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'active': True,
                'tax_group_id': 'tax_group_vat_compensation',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+007'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_rs_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_domestic': {
                'sequence': 1,
                'name': 'Domestic Customer',
                'auto_apply': 1,
                'country_id': 'base.rs',
            },
            'fiscal_position_template_foreign': {
                'sequence': 2,
                'name': 'Foreign Customer',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'rs_purchase_vat_10',
                        'tax_dest_id': 'rs_purchase_vat_0',
                    }),
                    Command.create({
                        'tax_src_id': 'rs_purchase_vat_20',
                        'tax_dest_id': 'rs_purchase_vat_0',
                    }),
                    Command.create({
                        'tax_src_id': 'rs_sale_vat_10',
                        'tax_dest_id': 'rs_sale_vat_0',
                    }),
                    Command.create({
                        'tax_src_id': 'rs_sale_vat_20',
                        'tax_dest_id': 'rs_sale_vat_0',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'rs_604',
                        'account_dest_id': 'rs_605',
                    }),
                ],
            },
        }
