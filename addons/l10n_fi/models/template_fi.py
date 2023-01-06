# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_fi_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_fi_fiscal_position(template_code),
        }

    def _get_fi_template_data(self, template_code):
        return {
            'code_digits': '4',
            'property_account_receivable_id': 'account_1700',
            'property_account_payable_id': 'account_2870',
            'property_account_expense_categ_id': 'account_4000',
            'property_account_income_categ_id': 'account_3000',
            'property_account_expense_id': 'account_4000',
            'property_account_income_id': 'account_3000',
            'property_tax_payable_account_id': 'account_2930',
            'property_tax_receivable_account_id': 'account_1765',
            'cash_account_code_prefix': '1910',
            'bank_account_code_prefix': '1921',
            'transfer_account_code_prefix': '1950',
        }

    def _get_fi_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.fi',
                'account_default_pos_receivable_account_id': 'account_1701',
                'income_currency_exchange_account_id': 'account_3500',
                'expense_currency_exchange_account_id': 'account_4380',
                'account_journal_early_pay_discount_loss_account_id': 'account_4230',
                'account_journal_early_pay_discount_gain_account_id': 'account_3500',
            },
        }

    def _get_fi_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_dom_sales_goods_24': {
                'name': '24%',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_301'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_301'),
                    }),
                ],
            },
            'tax_dom_sales_goods_14': {
                'name': '14%',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_302'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_302'),
                    }),
                ],
            },
            'tax_dom_sales_goods_10': {
                'name': '10%',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_303'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_303'),
                    }),
                ],
            },
            'tax_dom_sales_goods_0': {
                'name': '0%',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_304'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_304'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_dom_sales_service_24': {
                'name': '24% S',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_301'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_301'),
                    }),
                ],
            },
            'tax_dom_sales_service_14': {
                'name': '14% S',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_302'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_302'),
                    }),
                ],
            },
            'tax_dom_sales_service_10': {
                'name': '10% S',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_303'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_303'),
                    }),
                ],
            },
            'tax_dom_purchase_goods_24': {
                'name': '24%',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_goods_14': {
                'name': '14%',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_goods_10': {
                'name': '10%',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_service_24': {
                'name': '24% S',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_service_14': {
                'name': '14% S',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_service_10': {
                'name': '10% S',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_brutto_24': {
                'name': '24% incl',
                'description': '24% incl',
                'price_include': True,
                'include_base_amount': 1,
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_brutto_14': {
                'name': '14% incl',
                'description': '14% incl',
                'price_include': True,
                'include_base_amount': 1,
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_brutto_10': {
                'name': '10% incl',
                'description': '10% incl',
                'price_include': True,
                'include_base_amount': 1,
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_dom_purchase_0': {
                'name': '0%',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
            },
            'tax_eu_sales_goods_0': {
                'name': '0% EU G',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_311'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_311'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_eu_sales_service_0': {
                'name': '0% EU S',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_312'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_312'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_eu_purchase_goods_24': {
                'name': '24% EU G',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_purchase_goods_eu'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_305'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_purchase_goods_eu'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_305'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_eu_purchase_goods_14': {
                'name': '14% EU',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_purchase_goods_eu'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_305'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_purchase_goods_eu'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_305'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_eu_purchase_goods_10': {
                'name': '10% EU G',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_purchase_goods_eu'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_305'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_purchase_goods_eu'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_305'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_eu_purchase_service_24': {
                'name': '24% EU S',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_306'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_tax_306'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_306'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_tax_306'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_eu_purchase_service_14': {
                'name': '14% EU S',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_306'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_tax_306'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_306'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_tax_306'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_eu_purchase_service_10': {
                'name': '10% EU S',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_306'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_tax_306'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_306'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_tax_306'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'vat0triangulation': {
                'name': '0% ABC',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
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
            'triangulation_purchase': {
                'name': 'ABC',
                'description': 'ABC',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                    }),
                ],
            },
            'tax_construct_sales_0': {
                'name': '0% Construct',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_319'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_319'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_construct_purchase_24': {
                'name': '24% Construct',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
            'tax_construct_purchase_24_finland': {
                'name': '24% FI Construct',
                'description': '24%',
                'tax_group_id': 'tax_group_24',
                'amount': 24.0,
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_318'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('-fi_318'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_318'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                        'tag_ids': tags('+fi_318'),
                    }),
                ],
            },
            'aland_sales_0': {
                'name': '0% Aland',
                'description': '0%',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_304'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_304'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_non_eu_purchase_goods_24': {
                'name': '24% EX G',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_340'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_340'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_non_eu_purchase_goods_14': {
                'name': '14% EX G',
                'description': '14%',
                'amount': 14.0,
                'tax_group_id': 'tax_group_14',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_340'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_340'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'tax_non_eu_purchase_goods_10': {
                'name': '10% EX G',
                'description': '10%',
                'amount': 10.0,
                'tax_group_id': 'tax_group_10',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307', '+fi_340'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307', '-fi_340'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'account_2930',
                    }),
                ],
            },
            'vat0export': {
                'name': '0% EX',
                'description': '0% EX',
                'amount': 0.0,
                'tax_group_id': 'tax_group_0',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_304'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_304'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'import_pay24': {
                'name': '24% Import Pay',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_340'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-fi_base_340'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_340'),
                    }),
                ],
            },
            'import_deduct24': {
                'name': '24% Import Deduct',
                'description': '24%',
                'amount': 24.0,
                'tax_group_id': 'tax_group_24',
                'type_tax_use': 'purchase',
                'active': False,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('+fi_307'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_1765',
                        'tag_ids': tags('-fi_307'),
                    }),
                ],
            },
        }

    def _get_fi_fiscal_position(self, template_code):
        return {
            'aland': {
                'name': 'Aland',
                'country_id': 'base.ax',
                'auto_apply': 1,
                'vat_required': 1,
                'sequence': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_24',
                        'tax_dest_id': 'aland_sales_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_14',
                        'tax_dest_id': 'aland_sales_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_10',
                        'tax_dest_id': 'aland_sales_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_24',
                        'tax_dest_id': 'aland_sales_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_14',
                        'tax_dest_id': 'aland_sales_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_10',
                        'tax_dest_id': 'aland_sales_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_24',
                        'tax_dest_id': 'tax_non_eu_purchase_goods_24',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_14',
                        'tax_dest_id': 'tax_non_eu_purchase_goods_14',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_10',
                        'tax_dest_id': 'tax_non_eu_purchase_goods_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_24',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_14',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_10',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                ],
            },
            'finland': {
                'name': 'Finland',
                'country_id': 'base.fi',
                'auto_apply': 1,
                'vat_required': 1,
                'sequence': 3,
            },
            'eu': {
                'name': 'EU',
                'country_group_id': 'base.europe',
                'auto_apply': 1,
                'vat_required': 1,
                'sequence': 4,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_24',
                        'tax_dest_id': 'tax_eu_sales_goods_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_14',
                        'tax_dest_id': 'tax_eu_sales_goods_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_10',
                        'tax_dest_id': 'tax_eu_sales_goods_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_24',
                        'tax_dest_id': 'tax_eu_sales_service_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_14',
                        'tax_dest_id': 'tax_eu_sales_service_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_10',
                        'tax_dest_id': 'tax_eu_sales_service_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_24',
                        'tax_dest_id': 'tax_eu_purchase_goods_24',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_14',
                        'tax_dest_id': 'tax_eu_purchase_goods_14',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_10',
                        'tax_dest_id': 'tax_eu_purchase_goods_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_24',
                        'tax_dest_id': 'tax_eu_purchase_service_24',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_14',
                        'tax_dest_id': 'tax_eu_purchase_service_14',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_10',
                        'tax_dest_id': 'tax_eu_purchase_service_10',
                    }),
                ],
            },
            'eu_no_vat': {
                'name': 'EU no VAT',
                'country_group_id': 'base.europe',
                'auto_apply': 1,
                'sequence': 5,
            },
            'non_eu': {
                'name': 'Non EU',
                'auto_apply': 1,
                'sequence': 6,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_24',
                        'tax_dest_id': 'vat0export',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_14',
                        'tax_dest_id': 'vat0export',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_10',
                        'tax_dest_id': 'vat0export',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_24',
                        'tax_dest_id': 'vat0export',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_14',
                        'tax_dest_id': 'vat0export',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_service_10',
                        'tax_dest_id': 'vat0export',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_24',
                        'tax_dest_id': 'tax_non_eu_purchase_goods_24',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_14',
                        'tax_dest_id': 'tax_non_eu_purchase_goods_24',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_goods_10',
                        'tax_dest_id': 'tax_non_eu_purchase_goods_24',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_24',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_14',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_service_10',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_brutto_24',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_brutto_14',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_purchase_brutto_10',
                        'tax_dest_id': 'tax_dom_purchase_0',
                    }),
                ],
            },
            'construction': {
                'name': 'Construction services + Scrap metal',
                'country_id': 'base.fi',
                'sequence': 7,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_construct_purchase_24',
                        'tax_dest_id': 'tax_construct_purchase_24_finland',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_dom_sales_goods_24',
                        'tax_dest_id': 'tax_construct_sales_0',
                    }),
                ],
            },
        }
