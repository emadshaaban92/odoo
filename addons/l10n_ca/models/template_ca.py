# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ca_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ca_fiscal_position(template_code),
        }

    def _get_ca_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'chart1151_en',
            'property_account_payable_id': 'chart2111_en',
            'property_account_income_categ_id': 'chart411_en',
            'property_account_expense_categ_id': 'chart5111_en',
            'property_stock_account_input_categ_id': 'chart2171_en',
            'property_stock_account_output_categ_id': 'chart1145_en',
            'property_stock_valuation_account_id': 'chart1141_en',
            'cash_account_code_prefix': '111',
            'bank_account_code_prefix': '112',
            'transfer_account_code_prefix': '113',
            'use_anglo_saxon': True,
        }

    def _get_ca_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ca',
                'account_default_pos_receivable_account_id': 'chart11511_en',
                'income_currency_exchange_account_id': 'chart42_en',
                'expense_currency_exchange_account_id': 'chart55_en',
                'account_journal_early_pay_discount_loss_account_id': 'chart550001_en',
                'account_journal_early_pay_discount_gain_account_id': 'chart420001_en',
            },
        }

    def _get_ca_account_tax(self, template_code):
        return {
            'gstpst_sale_bc_gst_en': {
                'name': 'GST for sales - 5% (BC)',
                'description': 'GST 5%',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'include_base_amount': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
            },
            'pst_bc_sale_en': {
                'name': 'PST for sales - 7% (BC)',
                'description': 'PST 7%',
                'type_tax_use': 'none',
                'amount': 7.0,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_gst_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
            },
            'gstpst_bc_sale_en': {
                'name': 'GST + PST for sales (BC)',
                'description': 'GST + PST',
                'type_tax_use': 'sale',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'pst_bc_sale_en',
                        'gstpst_sale_bc_gst_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'gstpst_sale_mb_gst_en': {
                'name': 'GST for sales - 5% (MB)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'include_base_amount': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
            },
            'pst_mb_sale_en': {
                'name': 'PST for sales - 8% (MB)',
                'description': 'PST 8%',
                'type_tax_use': 'none',
                'amount': 8.0,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_gst_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
            },
            'gstpst_mb_sale_en': {
                'name': 'GST + PST for sales (MB)',
                'description': 'GST + PST',
                'type_tax_use': 'sale',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstpst_sale_mb_gst_en',
                        'pst_mb_sale_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'gstqst_sale_gst_en': {
                'name': 'GST for sales - 5% (QC)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
            },
            'qst_sale_en': {
                'name': 'QST for sales - 9.975%',
                'description': 'QST 9.975%',
                'type_tax_use': 'none',
                'amount': 9.975,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_qst_9975',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
            },
            'gstqst_sale_en': {
                'name': 'GST + QST for sales',
                'description': 'GST + QST',
                'type_tax_use': 'sale',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstqst_sale_gst_en',
                        'qst_sale_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'gstpst_sale_sk_gst_en': {
                'name': 'GST for sales - 5% (SK)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'include_base_amount': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
            },
            'pst_sk_sale_en': {
                'name': 'PST for sales - 5% (SK)',
                'description': 'PST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_pst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2132_en',
                    }),
                ],
            },
            'gstpst_sk_sale_en': {
                'name': 'GST + PST for sales (SK)',
                'description': 'GST + PST',
                'type_tax_use': 'sale',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstpst_sale_sk_gst_en',
                        'pst_sk_sale_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'hst13_sale_en': {
                'name': 'HST for sales - 13%',
                'description': 'HST 13%',
                'type_tax_use': 'sale',
                'amount': 13.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_hst_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart21331_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart21331_en',
                    }),
                ],
            },
            'hst15_sale_en': {
                'name': 'HST for sales - 15%',
                'description': 'HST 15%',
                'type_tax_use': 'sale',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_hst_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart21333_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart21333_en',
                    }),
                ],
            },
            'gst_sale_en': {
                'name': 'GST for sales - 5%',
                'description': 'GST 5%',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart2131_en',
                    }),
                ],
            },
            'gstpst_purc_bc_gst_en': {
                'name': 'GST for purchases - 5% (BC)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'include_base_amount': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
            },
            'pst_bc_purc_en': {
                'name': 'PST for purchases - 7% (BC)',
                'description': 'PST 7%',
                'type_tax_use': 'none',
                'amount': 7.0,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_gst_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
            },
            'gstpst_bc_purc_en': {
                'name': 'GST + PST for purchases (BC)',
                'description': 'GST + PST',
                'type_tax_use': 'purchase',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstpst_purc_bc_gst_en',
                        'pst_bc_purc_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'gstpst_purc_mb_gst_en': {
                'name': 'GST for purchases - 5% (MB)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'include_base_amount': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
            },
            'pst_mb_purc_en': {
                'name': 'PST for purchases - 8% (MB)',
                'description': 'PST 8%',
                'type_tax_use': 'none',
                'amount': 8.0,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_pst_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
            },
            'gstpst_mb_purc_en': {
                'name': 'GST + PST for purchases (MB)',
                'description': 'GST + PST',
                'type_tax_use': 'purchase',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstpst_purc_mb_gst_en',
                        'pst_mb_purc_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'gstqst_purc_gst_en': {
                'name': 'GST for purchases - 5% (QC)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
            },
            'qst_purc_en': {
                'name': 'QST for purchases - 9.975%',
                'description': 'QST 9.975%',
                'type_tax_use': 'none',
                'amount': 9.975,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_qst_9975',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
            },
            'gstqst_purc_en': {
                'name': 'GST + QST for purchases',
                'description': 'GST + QST',
                'type_tax_use': 'purchase',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstqst_purc_gst_en',
                        'qst_purc_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'gstpst_purc_sk_gst_en': {
                'name': 'GST for purchases - 5% (SK)',
                'description': 'GST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 1,
                'include_base_amount': False,
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
            },
            'pst_sk_purc_en': {
                'name': 'PST for purchases - 5% (SK)',
                'description': 'PST 5%',
                'type_tax_use': 'none',
                'amount': 5.0,
                'amount_type': 'percent',
                'sequence': 2,
                'tax_group_id': 'tax_group_pst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1182_en',
                    }),
                ],
            },
            'gstpst_sk_purc_en': {
                'name': 'GST + PST for purchases (SK)',
                'description': 'GST + PST',
                'type_tax_use': 'purchase',
                'amount': 1.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'gstpst_purc_sk_gst_en',
                        'pst_sk_purc_en',
                    ]),
                ],
                'tax_group_id': 'tax_group_fix',
            },
            'hst13_purc_en': {
                'name': 'HST for purchases - 13%',
                'description': 'HST 13%',
                'type_tax_use': 'purchase',
                'amount': 13.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_hst_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart11831_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart11831_en',
                    }),
                ],
            },
            'hst15_purc_en': {
                'name': 'HST for purchases - 15%',
                'description': 'HST 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_hst_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart11833_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart11833_en',
                    }),
                ],
            },
            'gst_purc_en': {
                'name': 'GST for purchases - 5%',
                'description': 'GST 5%',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_gst_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart1181_en',
                    }),
                ],
            },
        }

    def _get_ca_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_ab_en': {
                'name': 'Alberta (AB)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_ab',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_bc_en': {
                'name': 'British Columbia (BC)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_bc',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_mb_en': {
                'name': 'Manitoba (MB)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_mb',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_nb_en': {
                'name': 'New Brunswick (NB)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_nb',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gst_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart412_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5112_en',
                    }),
                ],
            },
            'fiscal_position_template_nl_en': {
                'name': 'Newfoundland and Labrador (NL)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_nl',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gst_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart412_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5112_en',
                    }),
                ],
            },
            'fiscal_position_template_ns_en': {
                'name': 'Nova Scotia (NS)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_ns',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gst_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart412_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5112_en',
                    }),
                ],
            },
            'fiscal_position_template_nt_en': {
                'name': 'Northwest Territories (NT)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_nt',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_nu_en': {
                'name': 'Nunavut (NU)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_nu',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_on_en': {
                'name': 'Ontario (ON)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_on',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gst_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart412_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5112_en',
                    }),
                ],
            },
            'fiscal_position_template_pe_en': {
                'name': 'Prince Edward Islands (PE)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_pe',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gst_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart412_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5112_en',
                    }),
                ],
            },
            'fiscal_position_template_qc_en': {
                'name': 'Quebec (QC)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_qc',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_sk_en': {
                'name': 'Saskatchewan (SK)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_sk',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_yt_en': {
                'name': 'Yukon (YT)',
                'auto_apply': 1,
                'country_id': 'base.ca',
                'state_ids': [
                    Command.set([
                        'base.state_ca_yt',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                        'tax_dest_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                        'tax_dest_id': 'gst_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart413_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5113_en',
                    }),
                ],
            },
            'fiscal_position_template_intl_en': {
                'sequence': 1,
                'name': 'International (INTL)',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'gst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_bc_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_mb_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst13_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'hst15_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstqst_purc_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_sale_en',
                    }),
                    Command.create({
                        'tax_src_id': 'gstpst_sk_purc_en',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'chart411_en',
                        'account_dest_id': 'chart414_en',
                    }),
                    Command.create({
                        'account_src_id': 'chart5111_en',
                        'account_dest_id': 'chart5114_en',
                    }),
                ],
            },
        }
