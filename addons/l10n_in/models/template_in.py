# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_in_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_in_fiscal_position(template_code),
        }

    def _get_in_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'p10040',
            'property_account_payable_id': 'p11211',
            'property_account_expense_categ_id': 'p2107',
            'property_account_income_categ_id': 'p20011',
            'bank_account_code_prefix': '1002',
            'cash_account_code_prefix': '1001',
            'transfer_account_code_prefix': '1008',
            'code_digits': '6',
        }

    def _get_in_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.in',
                'account_default_pos_receivable_account_id': 'p10041',
                'income_currency_exchange_account_id': 'p2013',
                'expense_currency_exchange_account_id': 'p2117',
                'account_journal_early_pay_discount_loss_account_id': 'p2132',
                'account_journal_early_pay_discount_gain_account_id': '2012',
            },
        }

    def _get_in_account_tax(self, template_code):
        return {
            'cess_sale_5': {
                'name': 'CESS Sale 5%',
                'description': 'CESS 5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'cess_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
            },
            'cess_sale_1591': {
                'name': 'CESS Sale 1591 Per Thousand',
                'description': '1591 PER THOUSAND',
                'type_tax_use': 'none',
                'amount_type': 'fixed',
                'amount': 1.591,
                'tax_group_id': 'cess_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
            },
            'cess_5_plus_1591_sale': {
                'name': 'CESS 5% + RS.1591/THOUSAND',
                'description': 'CESS 5% + RS.1591/THOUSAND',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 0.0,
                'children_tax_ids': [
                    Command.set([
                        'cess_sale_5',
                        'cess_sale_1591',
                    ]),
                ],
                'tax_group_id': 'cess_group',
            },
            'cess_21_4170_higer_sale': {
                'name': 'CESS 21% or RS.4170/THOUSAND',
                'description': 'CESS 21% or RS.4170/THOUSAND',
                'type_tax_use': 'sale',
                'amount_type': 'code',
                'amount': 0.0,
                'python_compute': """result=base_amount * 0.21
tax=quantity * 4.17
if tax > result:result=tax""",
                'tax_group_id': 'cess_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
            },
            'exempt_sale': {
                'name': 'Exempt Sale',
                'description': 'Exempt',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'exempt_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_exempt',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_exempt',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'nil_rated_sale': {
                'name': 'Nil Rated',
                'description': 'Nil Rated',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'nil_rated_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_nil_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_nil_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'non_gst_supplies_sale': {
                'name': 'Non GST Supplies',
                'description': 'Non GST Supplies',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'non_gst_supplies_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_non_gst_supplies',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_non_gst_supplies',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'igst_sale_0': {
                'name': 'IGST 0%',
                'description': 'IGST 0%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_zero_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_zero_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'igst_sale_1': {
                'name': 'IGST 1%',
                'description': 'IGST 1%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_sale_2': {
                'name': 'IGST 2%',
                'description': 'IGST 2%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 2.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_sale_28': {
                'name': 'IGST 28%',
                'description': 'IGST 28%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 28.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_sale_18': {
                'name': 'IGST 18%',
                'description': 'IGST 18%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 18.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_sale_12': {
                'name': 'IGST 12%',
                'description': 'IGST 12%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 12.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_sale_5': {
                'name': 'IGST 5%',
                'description': 'IGST 5%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_0_5': {
                'name': 'SGST Sale 0.5%',
                'description': 'SGST 0.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 0.5,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_sale_0_5': {
                'name': 'CGST Sale 0.5%',
                'description': 'CGST 0.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 0.5,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_1': {
                'name': 'GST 1%',
                'description': 'GST 1%',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 1.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_sale_0_5',
                        'cgst_sale_0_5',
                    ]),
                ],
            },
            'sgst_sale_1_2': {
                'name': 'SGST Sale 1%',
                'description': 'SGST 1%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_sale_1_2': {
                'name': 'CGST Sale 1%',
                'description': 'CGST 1%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_2': {
                'name': 'GST 2%',
                'description': 'GST 2%',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 2.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_sale_1_2',
                        'cgst_sale_1_2',
                    ]),
                ],
            },
            'sgst_sale_14': {
                'name': 'SGST Sale 14%',
                'description': 'SGST 14%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 14.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_sale_14': {
                'name': 'CGST Sale 14%',
                'description': 'CGST 14%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 14.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_28': {
                'name': 'GST 28%',
                'description': 'GST 28%',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 28.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_sale_14',
                        'cgst_sale_14',
                    ]),
                ],
            },
            'sgst_sale_9': {
                'name': 'SGST Sale 9%',
                'description': 'SGST 9%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 9.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_sale_9': {
                'name': 'CGST Sale 9%',
                'description': 'CGST 9%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 9.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_18': {
                'name': 'GST 18%',
                'description': 'GST 18%',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 18.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_sale_9',
                        'cgst_sale_9',
                    ]),
                ],
            },
            'sgst_sale_6': {
                'name': 'SGST Sale 6%',
                'description': 'SGST 6%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 6.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_sale_6': {
                'name': 'CGST Sale 6%',
                'description': 'CGST 6%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 6.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_12': {
                'name': 'GST 12%',
                'description': 'GST 12%',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 12.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_sale_6',
                        'cgst_sale_6',
                    ]),
                ],
            },
            'sgst_sale_2_5': {
                'name': 'SGST Sale 2.5%',
                'description': 'SGST 2.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 2.5,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_sale_2_5': {
                'name': 'CGST Sale 2.5%',
                'description': 'CGST 2.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 2.5,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_sale_5': {
                'name': 'GST 5%',
                'description': 'GST 5%',
                'type_tax_use': 'sale',
                'amount_type': 'group',
                'amount': 5.0,
                'tax_group_id': 'gst_group',
                'sequence': 0,
                'children_tax_ids': [
                    Command.set([
                        'sgst_sale_2_5',
                        'cgst_sale_2_5',
                    ]),
                ],
            },
            'cess_purchase_5': {
                'name': 'CESS Purchase 5%',
                'description': 'CESS 5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'cess_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
            },
            'cess_purchase_1591': {
                'name': 'CESS Purchase 1591 Per Thousand',
                'description': '1591 PER THOUSAND',
                'type_tax_use': 'none',
                'amount_type': 'fixed',
                'amount': 1.591,
                'tax_group_id': 'cess_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
            },
            'cess_5_plus_1591_purchase': {
                'name': 'CESS 5% + RS.1591/THOUSAND',
                'description': 'CESS 5% + RS.1591/THOUSAND',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 0.0,
                'children_tax_ids': [
                    Command.set([
                        'cess_purchase_5',
                        'cess_purchase_1591',
                    ]),
                ],
                'tax_group_id': 'cess_group',
            },
            'cess_21_4170_higer_purchase': {
                'name': 'CESS 21% or RS.4170/THOUSAND',
                'description': 'CESS 21% or RS.4170/THOUSAND',
                'type_tax_use': 'purchase',
                'amount_type': 'code',
                'amount': 0.0,
                'python_compute': """result=base_amount * 0.21
tax=quantity * 4.17
if tax > result:result=tax""",
                'tax_group_id': 'cess_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess',
                            ]),
                        ],
                    }),
                ],
            },
            'exempt_purchase': {
                'name': 'Exempt purchase',
                'description': 'Exempt',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'exempt_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_exempt',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_exempt',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'nil_rated_purchase': {
                'name': 'Nil Rated',
                'description': 'Nil Rated',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'nil_rated_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_nil_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_nil_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'igst_purchase_0': {
                'name': 'IGST 0%',
                'description': 'IGST 0%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 0.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_zero_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_zero_rated',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'igst_purchase_1': {
                'name': 'IGST 1%',
                'description': 'IGST 1%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_2': {
                'name': 'IGST 2%',
                'description': 'IGST 2%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 2.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_28': {
                'name': 'IGST 28%',
                'description': 'IGST 28%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 28.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_18': {
                'name': 'IGST 18%',
                'description': 'IGST 18%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 18.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_12': {
                'name': 'IGST 12%',
                'description': 'IGST 12%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 12.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_5': {
                'name': 'IGST 5%',
                'description': 'IGST 5%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'igst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_0_5': {
                'name': 'SGST Purchase 0.5%',
                'description': 'SGST 0.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 0.5,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_0_5': {
                'name': 'CGST Purchase 0.5%',
                'description': 'CGST 0.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 0.5,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_1': {
                'name': 'GST 1%',
                'description': 'GST 1%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 1.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_0_5',
                        'cgst_purchase_0_5',
                    ]),
                ],
            },
            'sgst_purchase_1_2': {
                'name': 'SGST Purchase 1%',
                'description': 'SGST 1%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_1_2': {
                'name': 'CGST Purchase 1%',
                'description': 'CGST 1%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_2': {
                'name': 'GST 2%',
                'description': 'GST 2%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 2.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_1_2',
                        'cgst_purchase_1_2',
                    ]),
                ],
            },
            'sgst_purchase_14': {
                'name': 'SGST Purchase 14%',
                'description': 'SGST 14%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 14.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_14': {
                'name': 'CGST Purchase 14%',
                'description': 'CGST 14%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 14.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_28': {
                'name': 'GST 28%',
                'description': 'GST 28%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 28.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_14',
                        'cgst_purchase_14',
                    ]),
                ],
            },
            'sgst_purchase_9': {
                'name': 'SGST Purchase 9%',
                'description': 'SGST 9%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 9.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_9': {
                'name': 'CGST Purchase 9%',
                'description': 'CGST 9%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 9.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_18': {
                'name': 'GST 18%',
                'description': 'GST 18%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 18.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_9',
                        'cgst_purchase_9',
                    ]),
                ],
            },
            'sgst_purchase_6': {
                'name': 'SGST Purchase 6%',
                'description': 'SGST 6%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 6.0,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_6': {
                'name': 'CGST Purchase 6%',
                'description': 'CGST 6%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 6.0,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_12': {
                'name': 'GST 12%',
                'description': 'GST 12%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 12.0,
                'tax_group_id': 'gst_group',
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_6',
                        'cgst_purchase_6',
                    ]),
                ],
            },
            'sgst_purchase_2_5': {
                'name': 'SGST Purchase 2.5%',
                'description': 'SGST 2.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 2.5,
                'tax_group_id': 'sgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_2_5': {
                'name': 'CGST Purchase 2.5%',
                'description': 'CGST 2.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 2.5,
                'tax_group_id': 'cgst_group',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_5': {
                'name': 'GST 5%',
                'description': 'GST 5%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 5.0,
                'tax_group_id': 'gst_group',
                'sequence': 0,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_2_5',
                        'cgst_purchase_2_5',
                    ]),
                ],
            },
            'cess_purchase_5_rc': {
                'name': 'CESS Purchase 5% (RC)',
                'description': 'CESS 5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'cess_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cess_purchase_1591_rc': {
                'name': 'CESS Purchase 1591 Per Thousand (RC)',
                'description': '1591 PER THOUSAND',
                'type_tax_use': 'none',
                'amount_type': 'fixed',
                'amount': 1.591,
                'tax_group_id': 'cess_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cess_5_plus_1591_purchase_rc': {
                'name': 'CESS 5% + RS.1591/THOUSAND (RC)',
                'description': 'CESS 5% + RS.1591/THOUSAND',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 0.0,
                'children_tax_ids': [
                    Command.set([
                        'cess_purchase_5_rc',
                        'cess_purchase_1591_rc',
                    ]),
                ],
                'tax_group_id': 'cess_group',
                'l10n_in_reverse_charge': True,
            },
            'cess_21_4170_higer_purchase_rc': {
                'name': 'CESS 21% or RS.4170/THOUSAND (RC)',
                'description': 'CESS 21% or RS.4170/THOUSAND',
                'type_tax_use': 'purchase',
                'amount_type': 'code',
                'amount': 0.0,
                'python_compute': """result=base_amount * 0.21
tax=quantity * 4.17
if tax > result:result=tax""",
                'tax_group_id': 'cess_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11235',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cess_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10055',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cess_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_1_rc': {
                'name': 'IGST 1% (RC)',
                'description': 'IGST 1%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'igst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_2_rc': {
                'name': 'IGST 2% (RC)',
                'description': 'IGST 2%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 2.0,
                'tax_group_id': 'igst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_28_rc': {
                'name': 'IGST 28% (RC)',
                'description': 'IGST 28%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 28.0,
                'tax_group_id': 'igst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_18_rc': {
                'name': 'IGST 18% (RC)',
                'description': 'IGST 18%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 18.0,
                'tax_group_id': 'igst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_12_rc': {
                'name': 'IGST 12% (RC)',
                'description': 'IGST 12%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 12.0,
                'tax_group_id': 'igst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'igst_purchase_5_rc': {
                'name': 'IGST 5% (RC)',
                'description': 'IGST 5%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 5.0,
                'tax_group_id': 'igst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11234',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_igst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10053',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_igst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_0_5_rc': {
                'name': 'SGST Purchase 0.5% (RC)',
                'description': 'SGST 0.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 0.5,
                'tax_group_id': 'sgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_0_5_rc': {
                'name': 'CGST Purchase 0.5% (RC)',
                'description': 'CGST 0.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 0.5,
                'tax_group_id': 'cgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_1_rc': {
                'name': 'GST 1% (RC)',
                'description': 'GST 1%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 1.0,
                'tax_group_id': 'gst_group',
                'l10n_in_reverse_charge': True,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_0_5_rc',
                        'cgst_purchase_0_5_rc',
                    ]),
                ],
            },
            'sgst_purchase_1_2_rc': {
                'name': 'SGST Purchase 1% (RC)',
                'description': 'SGST 1%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'sgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_1_2_rc': {
                'name': 'CGST Purchase 1% (RC)',
                'description': 'CGST 1%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 1.0,
                'tax_group_id': 'cgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_2_rc': {
                'name': 'GST 2% (RC)',
                'description': 'GST 2%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 2.0,
                'tax_group_id': 'gst_group',
                'l10n_in_reverse_charge': True,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_1_2_rc',
                        'cgst_purchase_1_2_rc',
                    ]),
                ],
            },
            'sgst_purchase_14_rc': {
                'name': 'SGST Purchase 14% (RC)',
                'description': 'SGST 14%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 14.0,
                'tax_group_id': 'sgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_14_rc': {
                'name': 'CGST Purchase 14% (RC)',
                'description': 'CGST 14%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 14.0,
                'tax_group_id': 'cgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_28_rc': {
                'name': 'GST 28% (RC)',
                'description': 'GST 28%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 28.0,
                'tax_group_id': 'gst_group',
                'l10n_in_reverse_charge': True,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_14_rc',
                        'cgst_purchase_14_rc',
                    ]),
                ],
            },
            'sgst_purchase_9_rc': {
                'name': 'SGST Purchase 9% (RC)',
                'description': 'SGST 9%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 9.0,
                'tax_group_id': 'sgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_9_rc': {
                'name': 'CGST Purchase 9% (RC)',
                'description': 'CGST 9%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 9.0,
                'tax_group_id': 'cgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_18_rc': {
                'name': 'GST 18% (RC)',
                'description': 'GST 18%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 18.0,
                'tax_group_id': 'gst_group',
                'l10n_in_reverse_charge': True,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_9_rc',
                        'cgst_purchase_9_rc',
                    ]),
                ],
            },
            'sgst_purchase_6_rc': {
                'name': 'SGST Purchase 6% (RC)',
                'description': 'SGST 6%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 6.0,
                'tax_group_id': 'sgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_6_rc': {
                'name': 'CGST Purchase 6% (RC)',
                'description': 'CGST 6%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 6.0,
                'tax_group_id': 'cgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_12_rc': {
                'name': 'GST 12% (RC)',
                'description': 'GST 12%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 12.0,
                'tax_group_id': 'gst_group',
                'l10n_in_reverse_charge': True,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_6_rc',
                        'cgst_purchase_6_rc',
                    ]),
                ],
            },
            'sgst_purchase_2_5_rc': {
                'name': 'SGST Purchase 2.5% (RC)',
                'description': 'SGST 2.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 2.5,
                'tax_group_id': 'sgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11232',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_sgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10051',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_sgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'cgst_purchase_2_5_rc': {
                'name': 'CGST Purchase 2.5% (RC)',
                'description': 'CGST 2.5%',
                'type_tax_use': 'none',
                'amount_type': 'percent',
                'amount': 2.5,
                'tax_group_id': 'cgst_group',
                'l10n_in_reverse_charge': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p11233',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_base_cgst_rc',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'p10057',
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'p10052',
                        'tag_ids': [
                            Command.set([
                                'l10n_in.tax_tag_cgst_rc',
                            ]),
                        ],
                    }),
                ],
            },
            'sgst_purchase_5_rc': {
                'name': 'GST 5% (RC)',
                'description': 'GST 5%',
                'type_tax_use': 'purchase',
                'amount_type': 'group',
                'amount': 5.0,
                'tax_group_id': 'gst_group',
                'l10n_in_reverse_charge': True,
                'sequence': 0,
                'children_tax_ids': [
                    Command.set([
                        'sgst_purchase_2_5_rc',
                        'cgst_purchase_2_5_rc',
                    ]),
                ],
            },
        }

    def _get_in_fiscal_position(self, template_code):
        return {
            'fiscal_position_in_inter_state': {
                'name': 'Inter State',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'sgst_sale_1',
                        'tax_dest_id': 'igst_sale_1',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_2',
                        'tax_dest_id': 'igst_sale_2',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_5',
                        'tax_dest_id': 'igst_sale_5',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_12',
                        'tax_dest_id': 'igst_sale_12',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_18',
                        'tax_dest_id': 'igst_sale_18',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_28',
                        'tax_dest_id': 'igst_sale_28',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_1',
                        'tax_dest_id': 'igst_purchase_1',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_2',
                        'tax_dest_id': 'igst_purchase_2',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_5',
                        'tax_dest_id': 'igst_purchase_5',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_12',
                        'tax_dest_id': 'igst_purchase_12',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_18',
                        'tax_dest_id': 'igst_purchase_18',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_28',
                        'tax_dest_id': 'igst_purchase_28',
                    }),
                ],
            },
            'fiscal_position_in_export': {
                'name': 'Export',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'sgst_sale_1',
                        'tax_dest_id': 'igst_sale_1',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_2',
                        'tax_dest_id': 'igst_sale_2',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_5',
                        'tax_dest_id': 'igst_sale_5',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_12',
                        'tax_dest_id': 'igst_sale_12',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_18',
                        'tax_dest_id': 'igst_sale_18',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_sale_28',
                        'tax_dest_id': 'igst_sale_28',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_1',
                        'tax_dest_id': 'igst_purchase_1',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_2',
                        'tax_dest_id': 'igst_purchase_2',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_5',
                        'tax_dest_id': 'igst_purchase_5',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_12',
                        'tax_dest_id': 'igst_purchase_12',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_18',
                        'tax_dest_id': 'igst_purchase_18',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_28',
                        'tax_dest_id': 'igst_purchase_28',
                    }),
                ],
            },
            'fiscal_position_in_reverse_charge_intra': {
                'name': 'Reverse charge Intra State',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'sgst_purchase_1',
                        'tax_dest_id': 'sgst_purchase_1_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_2',
                        'tax_dest_id': 'sgst_purchase_2_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_5',
                        'tax_dest_id': 'sgst_purchase_5_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_12',
                        'tax_dest_id': 'sgst_purchase_12_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_18',
                        'tax_dest_id': 'sgst_purchase_18_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_28',
                        'tax_dest_id': 'sgst_purchase_28_rc',
                    }),
                ],
            },
            'fiscal_position_in_reverse_charge_inter': {
                'name': 'Reverse charge Inter State',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'sgst_purchase_1',
                        'tax_dest_id': 'igst_purchase_1_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_2',
                        'tax_dest_id': 'igst_purchase_2_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_5',
                        'tax_dest_id': 'igst_purchase_5_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_12',
                        'tax_dest_id': 'igst_purchase_12_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_18',
                        'tax_dest_id': 'igst_purchase_18_rc',
                    }),
                    Command.create({
                        'tax_src_id': 'sgst_purchase_28',
                        'tax_dest_id': 'igst_purchase_28_rc',
                    }),
                ],
            },
        }
