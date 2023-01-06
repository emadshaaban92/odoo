# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_br_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_br_fiscal_position(template_code),
        }

    def _get_br_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '1.01.01.02.00',
            'cash_account_code_prefix': '1.01.01.01.00',
            'transfer_account_code_prefix': '1.01.01.12.00',
            'property_account_receivable_id': 'account_template_101010401',
            'property_account_payable_id': 'account_template_201010301',
            'property_account_expense_categ_id': 'account_template_30101030101',
            'property_account_income_categ_id': 'account_template_30101010105',
        }

    def _get_br_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.br',
                'account_default_pos_receivable_account_id': 'account_template_101010402',
                'income_currency_exchange_account_id': 'br_3_01_01_05_01_47',
                'expense_currency_exchange_account_id': 'br_3_11_01_09_01_40',
                'account_journal_early_pay_discount_loss_account_id': 'account_template_31101010202',
                'account_journal_early_pay_discount_gain_account_id': 'account_template_30101050148',
            },
        }

    def _get_br_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_template_out_icms_interno17': {
                'description': 'ICMS Interno 17%',
                'name': 'ICMS Saída Interno 17%',
                'amount': 17.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
            },
            'tax_template_out_icms_externo17': {
                'description': 'ICMS Externo 17%',
                'name': 'ICMS Saída Externo 17%',
                'amount': 17.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
            },
            'tax_template_in_icms_interno17': {
                'description': 'ICMS Interno 17%',
                'name': 'ICMS Entrada Interno 17%',
                'amount': 17.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
            },
            'tax_template_in_icms_externo17': {
                'description': 'ICMS Externo 17%',
                'name': 'ICMS Entrada Externo 17%',
                'amount': 17.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_17',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
            },
            'tax_template_out_icms_interno': {
                'description': 'ICMS Interno',
                'name': 'ICMS Saída Interno 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_icms_externo': {
                'description': 'ICMS Externo',
                'name': 'ICMS Saída Externo 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_icms_interno': {
                'description': 'ICMS Interno',
                'name': 'ICMS Entrada Interno 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_icms_externo': {
                'description': 'ICMS Externo',
                'name': 'ICMS Entrada Externo 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_icms_externo7': {
                'description': 'ICMS Externo 7%',
                'name': 'ICMS Saída Externo 7%',
                'amount': 7.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
            },
            'tax_template_in_icms_externo7': {
                'description': 'ICMS Externo 7%',
                'name': 'ICMS Entrada Externo 7%',
                'amount': 7.0,
                'type_tax_use': 'purchase',
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
            },
            'tax_template_out_icms_externo12': {
                'description': 'ICMS Externo 12%',
                'name': 'ICMS Saída Externo 12%',
                'amount': 12.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
            },
            'tax_template_in_icms_externo12': {
                'description': 'ICMS Externo 12%',
                'name': 'ICMS Entrada Externo 12%',
                'amount': 12.0,
                'type_tax_use': 'purchase',
                'tax_discount': 1,
                'tax_group_id': 'tax_group_icms_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010903',
                        'tag_ids': tags('+ICMS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020302',
                        'tag_ids': tags('-ICMS_2'),
                    }),
                ],
            },
            'tax_template_out_icms_subist': {
                'description': 'ICMS Subist',
                'name': 'ICMS Saída Subist 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_icms_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMSST_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMSST_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_icms_subist': {
                'description': 'ICMS Subist',
                'name': 'ICMS Entrada Subist 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_icms_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ICMSST_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ICMSST_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_ipi10': {
                'description': 'IPI 10%',
                'name': 'IPI Saída 10%',
                'amount': 10.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_ipi_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010902',
                        'tag_ids': tags('+IPI_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020301',
                        'tag_ids': tags('-IPI_2'),
                    }),
                ],
            },
            'tax_template_in_ipi10': {
                'description': 'IPI 10%',
                'name': 'IPI Entrada 10%',
                'amount': 10.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_ipi_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020301',
                        'tag_ids': tags('-IPI_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010902',
                        'tag_ids': tags('+IPI_2'),
                    }),
                ],
            },
            'tax_template_out_ipi': {
                'description': 'IPI',
                'name': 'IPI Saída 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_ipi_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_ipi': {
                'description': 'IPI',
                'name': 'IPI Entrada 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_ipi_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+IPI_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_pis': {
                'description': 'PIS',
                'name': 'PIS Saída 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_pis_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+PIS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-PIS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_pis065': {
                'description': 'PIS 0,65%',
                'name': 'PIS Saída 0,65%',
                'amount': 0.65,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_pis_065',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+PIS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010904',
                        'tag_ids': tags('+PIS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-PIS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020303',
                        'tag_ids': tags('-PIS_2'),
                    }),
                ],
            },
            'tax_template_in_pis': {
                'description': 'PIS',
                'name': 'PIS Entrada 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_pis_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-PIS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+PIS_2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_pis065': {
                'description': 'PIS 0,65%',
                'name': 'PIS Entrada 0,65%',
                'amount': 0.65,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_pis_065',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-PIS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020303',
                        'tag_ids': tags('-PIS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+PIS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010904',
                        'tag_ids': tags('+PIS_2'),
                    }),
                ],
            },
            'tax_template_out_cofins': {
                'description': 'COFINS',
                'name': 'COFINS Saída 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_cofins_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_cofins3': {
                'description': 'COFINS 3%',
                'name': 'COFINS Saída 3%',
                'amount': 3.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_cofins_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010905',
                        'tag_ids': tags('+COFINS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020305',
                        'tag_ids': tags('-COFINS_2'),
                    }),
                ],
            },
            'tax_template_in_cofins': {
                'description': 'COFINS',
                'name': 'COFINS Entrada 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_cofins_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_cofins3': {
                'description': 'COFINS 3%',
                'name': 'COFINS Entrada 3%',
                'amount': 3.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_cofins_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020305',
                        'tag_ids': tags('-COFINS_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+COFINS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010905',
                        'tag_ids': tags('+COFINS_2'),
                    }),
                ],
            },
            'tax_template_out_irpj': {
                'description': 'IRPJ',
                'name': 'IRPJ 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_irpj_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+IRPJ_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-IRPJ_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_ir': {
                'description': 'IR',
                'name': 'IR 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_ir_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+IR_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-IR_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_issqn2': {
                'description': 'ISSQN 2%',
                'name': 'ISSQN Saída 2%',
                'amount': 2.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_issqn_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ISSQN_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020340',
                        'tag_ids': tags('+ISSQN_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ISSQN_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010928',
                        'tag_ids': tags('-ISSQN_2'),
                    }),
                ],
            },
            'tax_template_in_issqn2': {
                'description': 'ISSQN 2%',
                'name': 'ISSQN Entrada 2%',
                'amount': 2.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_issqn_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-ISSQN_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_101020340',
                        'tag_ids': tags('-ISSQN_2'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+ISSQN_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_201010928',
                        'tag_ids': tags('+ISSQN_2'),
                    }),
                ],
            },
            'tax_template_out_csll': {
                'description': 'CSLL',
                'name': 'CSLL 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 1,
                'tax_group_id': 'tax_group_csll_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+CSLL_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-CSLL_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_ii0': {
                'description': 'II',
                'name': 'II Saída 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_ii_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+II_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-II_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_ii0': {
                'description': 'II',
                'name': 'II Entrada 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_ii_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+II_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-II_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_out_inss0': {
                'description': 'INSS',
                'name': 'INSS Saída 0%',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_inss_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+INSS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-INSS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_template_in_inss0': {
                'description': 'INSS',
                'name': 'INSS Entrada 0%',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_discount': 0,
                'tax_group_id': 'tax_group_inss_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+INSS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-INSS_1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_br_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_1': {
                'sequence': 1,
                'name': 'Internal (within one state)',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.br',
                'l10n_br_fp_type': 'internal',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_externo17',
                        'tax_dest_id': 'tax_template_out_icms_interno17',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_externo17',
                        'tax_dest_id': 'tax_template_in_icms_interno17',
                    }),
                ],
            },
            'fiscal_position_template_2': {
                'sequence': 2,
                'name': 'Foreign',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_interno17',
                        'tax_dest_id': 'tax_template_out_icms_externo',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_externo17',
                        'tax_dest_id': 'tax_template_out_icms_externo',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_out_ipi10',
                        'tax_dest_id': 'tax_template_out_ipi',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_interno17',
                        'tax_dest_id': 'tax_template_in_icms_interno',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_externo17',
                        'tax_dest_id': 'tax_template_in_icms_externo',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_ipi10',
                        'tax_dest_id': 'tax_template_in_ipi',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_template_30101010105',
                        'account_dest_id': 'account_template_30101010101',
                    }),
                    Command.create({
                        'account_src_id': 'account_template_30101010106',
                        'account_dest_id': 'account_template_30101010103',
                    }),
                ],
            },
            'fiscal_position_template_ss_nnm': {
                'sequence': 3,
                'name': 'South and Southeast to North, Northeast, and Midwest',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.br',
                'l10n_br_fp_type': 'ss_nnm',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_externo17',
                        'tax_dest_id': 'tax_template_out_icms_externo7',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_interno17',
                        'tax_dest_id': 'tax_template_out_icms_externo7',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_externo17',
                        'tax_dest_id': 'tax_template_in_icms_externo7',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_interno17',
                        'tax_dest_id': 'tax_template_in_icms_externo7',
                    }),
                ],
            },
            'fiscal_position_template_interstate': {
                'sequence': 4,
                'name': 'Interstate',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.br',
                'l10n_br_fp_type': 'interstate',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_externo17',
                        'tax_dest_id': 'tax_template_out_icms_externo12',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_out_icms_interno17',
                        'tax_dest_id': 'tax_template_out_icms_externo12',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_externo17',
                        'tax_dest_id': 'tax_template_in_icms_externo12',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_template_in_icms_interno17',
                        'tax_dest_id': 'tax_template_in_icms_externo12',
                    }),
                ],
            },
        }
