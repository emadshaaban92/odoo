# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_hr_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_hr_fiscal_position(template_code),
        }

    def _get_hr_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '100',
            'cash_account_code_prefix': '102',
            'transfer_account_code_prefix': '1009',
            'code_digits': '6',
            'use_storno_accounting': True,
            'property_account_receivable_id': 'hr_120000',
            'property_account_payable_id': 'hr_220000',
            'property_account_expense_categ_id': 'hr_400000',
            'property_account_income_categ_id': 'hr_750000',
        }

    def _get_hr_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.hr',
                'account_default_pos_receivable_account_id': 'hr_120100',
                'income_currency_exchange_account_id': 'hr_772000',
                'expense_currency_exchange_account_id': 'hr_475000',
            },
        }

    def _get_hr_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'VAT_S_IN_ROC_25': {
                'sequence': 1,
                'description': 'Sale 25% in country',
                'name': '25%',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240000',
                        'tag_ids': tags('+II.3_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240000',
                        'tag_ids': tags('+II.3_tax'),
                    }),
                ],
            },
            'VAT_S_IN_ROC_13': {
                'sequence': 2,
                'description': 'Sale 13% in country',
                'name': '13%',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240000',
                        'tag_ids': tags('+II.2_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240000',
                        'tag_ids': tags('+II.2_tax'),
                    }),
                ],
            },
            'VAT_S_IN_ROC_5': {
                'sequence': 3,
                'description': 'Sale 5% in country',
                'name': '5%',
                'price_include': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240000',
                        'tag_ids': tags('+II.1_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240000',
                        'tag_ids': tags('+II.1_tax'),
                    }),
                ],
            },
            'VAT_S_TAX_PERSON_25%': {
                'sequence': 4,
                'description': 'Taxable person not in ROC 25%',
                'name': '25% EX',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.13_base', '+III.13_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240420',
                        'tag_ids': tags('+II.13_tax'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140420',
                        'tag_ids': tags('-III.13_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.13_base', '+III.13_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240420',
                        'tag_ids': tags('+II.13_tax'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140420',
                        'tag_ids': tags('-III.13_tax'),
                    }),
                ],
            },
            'VAT_S_TAX_PERSON_13%': {
                'sequence': 5,
                'description': 'Taxable person not in ROC 13%',
                'name': '13% EX',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.12_base', '+III.12_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240410',
                        'tag_ids': tags('+II.12_tax'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140410',
                        'tag_ids': tags('-III.12_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.12_base', '+III.12_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240410',
                        'tag_ids': tags('+II.12_tax'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140410',
                        'tag_ids': tags('-III.12_tax'),
                    }),
                ],
            },
            'VAT_S_TAX_PERSON_5%': {
                'sequence': 6,
                'description': 'Taxable person not in ROC 5%',
                'name': '5% EX',
                'price_include': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.11_base', '+III.11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240400',
                        'tag_ids': tags('+II.11_tax'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140400',
                        'tag_ids': tags('-III.11_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.11_base', '+III.11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240400',
                        'tag_ids': tags('+II.11_tax'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140400',
                        'tag_ids': tags('-III.11_tax'),
                    }),
                ],
            },
            'VAT_S_EU_G': {
                'sequence': 7,
                'description': 'Sale goods 0% in EU',
                'name': '0% EU G',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.3_base'),
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
                        'tag_ids': tags('+I.3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_EU_S': {
                'sequence': 8,
                'description': 'Sale service 0% in EU',
                'name': '0% EU S',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.4_base'),
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
                        'tag_ids': tags('+I.4_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_EX_O': {
                'sequence': 9,
                'description': 'Sale 0% not in EU',
                'name': '0% EX',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.9_base'),
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
                        'tag_ids': tags('+I.9_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_reverse_O': {
                'sequence': 10,
                'description': 'Reverse charge 0%',
                'name': '0% reverse',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.1_base'),
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
                        'tag_ids': tags('+I.1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_carried_other_state_O': {
                'sequence': 11,
                'description': 'Supplies carried out in another member state',
                'name': '0% EU M',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.2_base'),
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
                        'tag_ids': tags('+I.2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_person_not_in_ROC_O': {
                'sequence': 12,
                'description': 'Supplies to persons not established in the republic of croatia',
                'name': '0% EX M',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.5_base'),
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
                        'tag_ids': tags('+I.5_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_new_transport_other_state_O': {
                'sequence': 13,
                'description': 'Supplies of new means of transport to another member state',
                'name': '0% EU Trans',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.7_base'),
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
                        'tag_ids': tags('+I.7_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_S_other_exempt_O': {
                'sequence': 14,
                'description': 'Other exempt',
                'name': '0%',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.10_base'),
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
                        'tag_ids': tags('+I.10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_P_install_assemb_goods_O': {
                'sequence': 15,
                'description': '0% installed and assembled goods in another state',
                'name': '0% EU M INST',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.6_base'),
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
                        'tag_ids': tags('+I.6_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'VAT_P_IN_ROC_25': {
                'sequence': 16,
                'description': 'Purchase 25% in country',
                'name': '25%',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+III.3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140000',
                        'tag_ids': tags('+III.3_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+III.3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140000',
                        'tag_ids': tags('+III.3_tax'),
                    }),
                ],
            },
            'VAT_P_IN_ROC_13': {
                'sequence': 17,
                'description': 'Purchase 13% in country',
                'name': '13%',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140000',
                        'tag_ids': tags('+II.2_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140000',
                        'tag_ids': tags('+II.2_tax'),
                    }),
                ],
            },
            'VAT_P_IN_ROC_5': {
                'sequence': 18,
                'description': 'Purchase 5% in country',
                'name': '5%',
                'price_include': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140000',
                        'tag_ids': tags('+II.1_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140000',
                        'tag_ids': tags('+II.1_tax'),
                    }),
                ],
            },
            'VAT_P_G_IN_EU_25': {
                'sequence': 19,
                'description': 'Purchase goods 25% in EU',
                'name': '25% EU G',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.7_base', '+III.7_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240220',
                        'tag_ids': tags('-II.7_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140220',
                        'tag_ids': tags('+III.7_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.7_base', '+III.7_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240220',
                        'tag_ids': tags('-II.7_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140220',
                        'tag_ids': tags('+III.7_tax'),
                    }),
                ],
            },
            'VAT_P_S_IN_EU_25': {
                'sequence': 20,
                'description': 'Purchase service 25% in EU',
                'name': '25% EU S',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.10_base', '+III.10_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240320',
                        'tag_ids': tags('-II.10_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140320',
                        'tag_ids': tags('+III.10_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.10_base', '+III.10_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240320',
                        'tag_ids': tags('-II.10_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140320',
                        'tag_ids': tags('+III.10_tax'),
                    }),
                ],
            },
            'VAT_P_G_IN_EU_13': {
                'sequence': 21,
                'description': 'Purchase goods 13% in EU',
                'name': '13% EU G',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.6_base', '+III.6_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240210',
                        'tag_ids': tags('-II.6_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140210',
                        'tag_ids': tags('+III.6_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.6_base', '+III.6_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240210',
                        'tag_ids': tags('-II.6_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140210',
                        'tag_ids': tags('+III.6_tax'),
                    }),
                ],
            },
            'VAT_P_S_IN_EU_13': {
                'sequence': 22,
                'description': 'Purchase service 13% in EU',
                'name': '13% EU S',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.9_base', '+III.9_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240310',
                        'tag_ids': tags('-II.9_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140310',
                        'tag_ids': tags('+III.9_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.9_base', '+III.9_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240310',
                        'tag_ids': tags('-II.9_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140310',
                        'tag_ids': tags('+III.9_tax'),
                    }),
                ],
            },
            'VAT_P_G_IN_EU_5': {
                'sequence': 23,
                'description': 'Purchase goods 5% in EU',
                'name': '5% EU G',
                'price_include': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.5_base', '+III.5_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240200',
                        'tag_ids': tags('-II.5_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140200',
                        'tag_ids': tags('+III.5_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.5_base', '+III.5_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240200',
                        'tag_ids': tags('-II.5_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140200',
                        'tag_ids': tags('+III.5_tax'),
                    }),
                ],
            },
            'VAT_P_S_IN_EU_5': {
                'sequence': 24,
                'description': 'Purchase service 5% in EU',
                'name': '5% EU S',
                'price_include': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.8_base', '+III.8_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240300',
                        'tag_ids': tags('-II.8_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140300',
                        'tag_ids': tags('+III.8_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.8_base', '+III.8_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240300',
                        'tag_ids': tags('-II.8_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140300',
                        'tag_ids': tags('+III.8_tax'),
                    }),
                ],
            },
            'VAT_P_NOT_IN_EU_25': {
                'sequence': 25,
                'description': 'Purchase 25% not in EU',
                'name': '25% EX',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.15_base', '+III.14_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240500',
                        'tag_ids': tags('-II.15_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140500',
                        'tag_ids': tags('+III.14_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.15_base', '+III.14_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240500',
                        'tag_ids': tags('-II.15_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140500',
                        'tag_ids': tags('+III.14_tax'),
                    }),
                ],
            },
            'VAT_P_NOT_IN_EU_13': {
                'sequence': 26,
                'description': 'Purchase 13% not in EU',
                'name': '13% EX',
                'price_include': False,
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.15_base', '+III.14_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240500',
                        'tag_ids': tags('-II.15_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140500',
                        'tag_ids': tags('+III.14_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.15_base', '+III.14_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240500',
                        'tag_ids': tags('-II.15_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140500',
                        'tag_ids': tags('+III.14_tax'),
                    }),
                ],
            },
            'VAT_P_NOT_IN_EU_5': {
                'sequence': 27,
                'description': 'Purchase 5% not in EU',
                'name': '5% EX',
                'price_include': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.15_base', '+III.14_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240500',
                        'tag_ids': tags('-II.15_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140500',
                        'tag_ids': tags('+III.14_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.15_base', '+III.14_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240500',
                        'tag_ids': tags('-II.15_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140500',
                        'tag_ids': tags('+III.14_tax'),
                    }),
                ],
            },
            'VAT_P_reverse_charge': {
                'sequence': 28,
                'description': 'Domestic reverse charge',
                'name': '25% R',
                'price_include': False,
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.4_base', '+III.4_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240100',
                        'tag_ids': tags('-II.4_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140100',
                        'tag_ids': tags('+III.4_tax'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.4_base', '+III.4_base'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_240100',
                        'tag_ids': tags('-II.4_tax'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'hr_140100',
                        'tag_ids': tags('+III.4_tax'),
                    }),
                ],
            },
            'VAT_P_O': {
                'sequence': 29,
                'description': '0% Domestic supplies',
                'name': '0%',
                'price_include': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_pdv_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+I.8_base'),
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
                        'tag_ids': tags('+I.8_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_hr_fiscal_position(self, template_code):
        return {
            'fiscal_position_hr_exempt': {
                'name': 'Exempt taxpayer',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_5',
                        'tax_dest_id': 'VAT_S_other_exempt_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_13',
                        'tax_dest_id': 'VAT_S_other_exempt_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_25',
                        'tax_dest_id': 'VAT_S_other_exempt_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_5',
                        'tax_dest_id': 'VAT_P_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_13',
                        'tax_dest_id': 'VAT_P_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_25',
                        'tax_dest_id': 'VAT_P_O',
                    }),
                ],
            },
            'fiscal_position_hr_national': {
                'name': 'Domestic',
                'sequence': 10,
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.hr',
            },
            'fiscal_position_hr_person_private': {
                'name': 'Partner private',
                'sequence': 20,
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_hr_eu': {
                'name': 'EU partner',
                'sequence': 30,
                'auto_apply': 1,
                'vat_required': 1,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_5',
                        'tax_dest_id': 'VAT_S_EU_G',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_13',
                        'tax_dest_id': 'VAT_S_EU_G',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_25',
                        'tax_dest_id': 'VAT_S_EU_G',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_P_IN_ROC_5',
                        'tax_dest_id': 'VAT_P_G_IN_EU_5',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_P_IN_ROC_13',
                        'tax_dest_id': 'VAT_P_G_IN_EU_13',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_P_IN_ROC_25',
                        'tax_dest_id': 'VAT_P_G_IN_EU_25',
                    }),
                ],
            },
            'fiscal_position_hr_eu_out': {
                'name': 'Partner outside the EU',
                'sequence': 40,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_5',
                        'tax_dest_id': 'VAT_S_EX_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_13',
                        'tax_dest_id': 'VAT_S_EX_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_S_IN_ROC_25',
                        'tax_dest_id': 'VAT_S_EX_O',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_P_IN_ROC_5',
                        'tax_dest_id': 'VAT_P_NOT_IN_EU_5',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_P_IN_ROC_13',
                        'tax_dest_id': 'VAT_P_NOT_IN_EU_13',
                    }),
                    Command.create({
                        'tax_src_id': 'VAT_P_IN_ROC_25',
                        'tax_dest_id': 'VAT_P_NOT_IN_EU_25',
                    }),
                ],
            },
        }
