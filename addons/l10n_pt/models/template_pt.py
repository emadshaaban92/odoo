# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_pt_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_pt_fiscal_position(template_code),
        }

    def _get_pt_template_data(self, template_code):
        return {
            'cash_account_code_prefix': '11',
            'bank_account_code_prefix': '12',
            'transfer_account_code_prefix': '15',
            'property_account_receivable_id': 'chart_2111',
            'property_account_payable_id': 'chart_2211',
            'property_account_expense_id': 'chart_311',
            'property_account_income_id': 'chart_711',
            'property_account_income_categ_id': 'chart_711',
            'property_account_expense_categ_id': 'chart_311',
        }

    def _get_pt_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.pt',
                'account_default_pos_receivable_account_id': 'chart_2117',
                'income_currency_exchange_account_id': 'chart_7861',
                'expense_currency_exchange_account_id': 'chart_6863',
                'account_journal_early_pay_discount_loss_account_id': 'chart_682',
                'account_journal_early_pay_discount_gain_account_id': 'chart_728',
            },
        }

    def _get_pt_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'iva_pt_sale_normal': {
                'name': '23%',
                'description': 'VAT 23%',
                'sequence': 10,
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_3'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_4'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_3'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_4'),
                    }),
                ],
            },
            'iva_pt_sale_intermedia': {
                'name': '13%',
                'description': 'VAT 13%',
                'sequence': 20,
                'amount': 13.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_6'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_6'),
                    }),
                ],
            },
            'iva_pt_sale_reduzida': {
                'name': '6%',
                'description': 'VAT 6%',
                'sequence': 30,
                'amount': 6.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_2'),
                    }),
                ],
            },
            'iva_pt_sale_isenta': {
                'name': '0%',
                'description': 'VAT 0%',
                'sequence': 40,
                'amount': 0.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_8'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_8'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                    }),
                ],
            },
            'iva_pt_purchase_normal': {
                'name': '23%',
                'description': 'VAT 23%',
                'sequence': 70,
                'amount': 23.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_22'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_purchase_intermedia': {
                'name': '13%',
                'description': 'VAT 13%',
                'sequence': 80,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_23'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_purchase_reduzida': {
                'name': '6%',
                'description': 'VAT 6%',
                'sequence': 90,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_21'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_purchase_isenta': {
                'name': '0%',
                'description': 'VAT 0%',
                'sequence': 100,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
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
                        'account_id': 'chart_2432',
                    }),
                ],
            },
            'iva_pt_sale_eu_isenta': {
                'name': '0% EU',
                'description': 'VAT 0%',
                'sequence': 103,
                'active': True,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_7'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_7'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                    }),
                ],
            },
            'iva_pt_sale_non_eu_isenta': {
                'name': '0% Non-EU',
                'description': 'VAT 0%',
                'sequence': 105,
                'active': True,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
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
                        'account_id': 'chart_2433',
                    }),
                ],
            },
            'iva_pt_purchase_eu_isenta': {
                'name': '0% EU',
                'description': 'VAT 0%',
                'sequence': 107,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
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
                        'account_id': 'chart_2432',
                    }),
                ],
            },
            'iva_pt_purchase_non_eu_isenta': {
                'name': '0% Non-EU',
                'description': 'VAT 0%',
                'sequence': 108,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
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
                        'account_id': 'chart_2432',
                    }),
                ],
            },
            'iva_pt_purchase_eu_normal_bens': {
                'name': '23% EU G.',
                'description': 'VAT 23%',
                'sequence': 110,
                'amount': 23.0,
                'active': True,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_purchase_eu_normal_servicos': {
                'name': '23% EU S.',
                'description': 'VAT 23%',
                'sequence': 120,
                'amount': 23.0,
                'active': True,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_23',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_purchase_eu_intermedia_bens': {
                'name': '13% EU G.',
                'description': 'VAT 13%',
                'sequence': 130,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_purchase_eu_intermedia_servicos': {
                'name': '13% EU S.',
                'description': 'VAT 13%',
                'sequence': 140,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_purchase_eu_reduzida_bens': {
                'name': '6% EU G.',
                'description': 'VAT 6%',
                'sequence': 150,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_purchase_eu_reduzida_servicos': {
                'name': '6% EU S.',
                'description': 'VAT 6%',
                'sequence': 160,
                'amount': 6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_ma_sale_normal': {
                'name': '22% (MA)',
                'description': 'VAT 22%',
                'sequence': 200,
                'amount': 22.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_3'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_4'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_3'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_4'),
                    }),
                ],
            },
            'iva_pt_ma_sale_intermedia': {
                'name': '12% (MA)',
                'description': 'VAT 12%',
                'sequence': 210,
                'amount': 12.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_6'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_6'),
                    }),
                ],
            },
            'iva_pt_ma_sale_reduzida': {
                'name': '5% (MA)',
                'description': 'VAT 5%',
                'sequence': 220,
                'amount': 5.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_2'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_normal': {
                'name': '22% (MA)',
                'description': 'VAT 22%',
                'sequence': 230,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_22'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_intermedia': {
                'name': '12% (MA)',
                'description': 'VAT 12%',
                'sequence': 240,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_23'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_reduzida': {
                'name': '5% (MA)',
                'description': 'VAT 5%',
                'sequence': 250,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_21'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_eu_normal_bens': {
                'name': '22% EU G. (MA)',
                'description': 'VAT 22%',
                'sequence': 260,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_eu_normal_servicos': {
                'name': '22% EU S. (MA)',
                'description': 'VAT 22%',
                'sequence': 270,
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_eu_intermedia_bens': {
                'name': '12% EU G. (MA)',
                'description': 'VAT 12%',
                'sequence': 280,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_eu_intermedia_servicos': {
                'name': '12% EU S. (MA)',
                'description': 'VAT 12%',
                'sequence': 290,
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_eu_reduzida_bens': {
                'name': '5% EU G. (MA)',
                'description': 'VAT 5%',
                'sequence': 300,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_ma_purchase_eu_reduzida_servicos': {
                'name': '5% EU S. (MA)',
                'description': 'VAT 5%',
                'sequence': 310,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_ac_sale_normal': {
                'name': '16% (AZ)',
                'description': 'VAT 16%',
                'sequence': 400,
                'amount': 16.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_3'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_4'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_3'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_4'),
                    }),
                ],
            },
            'iva_pt_ac_sale_intermedia': {
                'name': '9% (AZ)',
                'description': 'VAT 9%',
                'sequence': 410,
                'amount': 9.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_6'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_5'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_6'),
                    }),
                ],
            },
            'iva_pt_ac_sale_reduzida': {
                'name': '4% (AZ)',
                'description': 'VAT 4%',
                'sequence': 420,
                'amount': 4.0,
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_state_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_state_2'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_normal': {
                'name': '16% (AZ)',
                'description': 'VAT 16%',
                'sequence': 430,
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_22'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_intermedia': {
                'name': '9% (AZ)',
                'description': 'VAT 9%',
                'sequence': 440,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_23'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_reduzida': {
                'name': '4% (AZ)',
                'description': 'VAT 4%',
                'sequence': 450,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_company_21'),
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
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_eu_normal_bens': {
                'name': '16% EU G. (AZ)',
                'description': 'VAT 16%',
                'sequence': 460,
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_eu_normal_servicos': {
                'name': '16% EU S. (AZ)',
                'description': 'VAT 16%',
                'sequence': 470,
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_22'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_eu_intermedia_bens': {
                'name': '9% EU G. (AZ)',
                'description': 'VAT 9%',
                'sequence': 480,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_eu_intermedia_servicos': {
                'name': '9% EU S. (AZ)',
                'description': 'VAT 9%',
                'sequence': 490,
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_9',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_23'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_eu_reduzida_bens': {
                'name': '4% EU G. (AZ)',
                'description': 'VAT 4%',
                'sequence': 500,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_12'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_13'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('+trp_tax_favor_company_21'),
                    }),
                ],
            },
            'iva_pt_ac_purchase_eu_reduzida_servicos': {
                'name': '4% EU S. (AZ)',
                'description': 'VAT 4%',
                'sequence': 510,
                'amount': 4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_iva_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('+trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-trp_base_16'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2432',
                        'tag_ids': tags('-trp_tax_favor_state_17'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'chart_2433',
                        'tag_ids': tags('-trp_tax_favor_company_21'),
                    }),
                ],
            },
        }

    def _get_pt_fiscal_position(self, template_code):
        return {
            'fiscal_position_national_customers': {
                'sequence': 1,
                'name': 'Portugal',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.pt',
            },
            'fiscal_position_foreign_eu_private': {
                'sequence': 2,
                'name': 'Private EU',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_foreign_eu': {
                'sequence': 3,
                'name': 'Inside EU',
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_normal',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_intermedia',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_reduzida',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_isenta',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_sale_normal',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_sale_intermedia',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_sale_reduzida',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_sale_normal',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_sale_intermedia',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_sale_reduzida',
                        'tax_dest_id': 'iva_pt_sale_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_normal',
                        'tax_dest_id': 'iva_pt_purchase_eu_normal_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_intermedia',
                        'tax_dest_id': 'iva_pt_purchase_eu_intermedia_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_reduzida',
                        'tax_dest_id': 'iva_pt_purchase_eu_reduzida_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_isenta',
                        'tax_dest_id': 'iva_pt_purchase_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_purchase_normal',
                        'tax_dest_id': 'iva_pt_ma_purchase_eu_normal_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_purchase_intermedia',
                        'tax_dest_id': 'iva_pt_ma_purchase_eu_intermedia_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_purchase_reduzida',
                        'tax_dest_id': 'iva_pt_ma_purchase_eu_reduzida_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_purchase_normal',
                        'tax_dest_id': 'iva_pt_ac_purchase_eu_normal_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_purchase_intermedia',
                        'tax_dest_id': 'iva_pt_ac_purchase_eu_intermedia_bens',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_purchase_reduzida',
                        'tax_dest_id': 'iva_pt_ac_purchase_eu_reduzida_bens',
                    }),
                ],
            },
            'fiscal_position_foreign_other': {
                'sequence': 4,
                'name': 'Outside EU',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_normal',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_intermedia',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_reduzida',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_sale_isenta',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_sale_normal',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_sale_intermedia',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_sale_reduzida',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_sale_normal',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_sale_intermedia',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_sale_reduzida',
                        'tax_dest_id': 'iva_pt_sale_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_normal',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_intermedia',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_reduzida',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_purchase_isenta',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_purchase_normal',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_purchase_intermedia',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ma_purchase_reduzida',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_purchase_normal',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_purchase_intermedia',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                    Command.create({
                        'tax_src_id': 'iva_pt_ac_purchase_reduzida',
                        'tax_dest_id': 'iva_pt_purchase_non_eu_isenta',
                    }),
                ],
            },
        }
