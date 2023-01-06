# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_mn_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_mn_fiscal_position(template_code),
        }

    def _get_mn_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'account_template_1201_0201',
            'property_account_payable_id': 'account_template_3101_0201',
            'property_account_expense_categ_id': 'account_template_6101_0101',
            'property_account_income_categ_id': 'account_template_5101_0101',
            'property_stock_account_input_categ_id': 'account_template_1407_0101',
            'property_stock_account_output_categ_id': 'account_template_1408_0101',
            'property_stock_valuation_account_id': 'account_template_1401_0101',
            'bank_account_code_prefix': '11',
            'cash_account_code_prefix': '10',
            'transfer_account_code_prefix': '1109',
            'code_digits': '8',
            'use_anglo_saxon': True,
        }

    def _get_mn_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.mn',
                'account_default_pos_receivable_account_id': 'account_template_1201_0202',
                'income_currency_exchange_account_id': 'account_template_5301_0201',
                'expense_currency_exchange_account_id': 'account_template_5302_0201',
                'account_journal_early_pay_discount_loss_account_id': 'account_template_9990_0003',
                'account_journal_early_pay_discount_gain_account_id': 'account_template_9990_0004',
            },
        }

    def _get_mn_account_tax(self, template_code):
        return {
            'account_tax_sale_vat1': {
                'name': 'НӨАТ бараа',
                'amount': 10.0,
                'price_include': True,
                'sequence': 1,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag5',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag5',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag5',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag5',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat1': {
                'name': 'НӨАТ-тэй худалдан авалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 1,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag36',
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag36',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag36',
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag36',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat2': {
                'name': 'НӨАТ-гүй худалдан авалт',
                'amount': 0.0,
                'price_include': True,
                'sequence': 10,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '0%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
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
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_sale_vat2': {
                'name': 'НӨАТ 0% борлуулалт',
                'amount': 0.0,
                'price_include': True,
                'sequence': 10,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '0%',
                'tax_group_id': 'account_tax_group6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag2',
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
                                'l10n_mn.vat_report_tag2',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_sale_vat3': {
                'name': 'НӨАТ чөлөөлөх борлуулалт',
                'amount': 0.0,
                'price_include': True,
                'sequence': 10,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '0%',
                'tax_group_id': 'account_tax_group6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag2',
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
                                'l10n_mn.vat_report_tag2',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_sale_vat4': {
                'name': 'НӨАТ бусад барааны борлуулалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag6',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag6',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag6',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag6',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat5': {
                'name': 'НӨАТ эрх борлуулалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag7',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag7',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag7',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag7',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat6': {
                'name': 'НӨАТ татан буугдах үеийн борлуулалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag8',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag8',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag8',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag8',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat7': {
                'name': 'НӨАТ өрийн төлбөрт өгсөн бараа',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag9',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag9',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag9',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag9',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat8': {
                'name': 'НӨАТ нотариат үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag11',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag11',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag11',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag11',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat9': {
                'name': 'НӨАТ өрийн төлбөрт өгсөн үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag12',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag12',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag12',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat10': {
                'name': 'НӨАТ цахилгаан, дулаан, ус, шуудан, холбоо',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag13',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag13',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag13',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag13',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat11': {
                'name': 'НӨАТ бараа түрээслүүлэх, эзэмшүүлэх',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag14',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag14',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag14',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag14',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat12': {
                'name': 'НӨАТ байр түрээслүүлэх, эзэмшүүлэх',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag15',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag15',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag15',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag15',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat13': {
                'name': 'НӨАТ хөрөнгө түрээслүүлэх, эзэмшүүлэх',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag16',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag16',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag16',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag16',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat14': {
                'name': 'НӨАТ бүтээл, загвар, зохиогчийн эрх',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag17',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag17',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag17',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag17',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat15': {
                'name': 'НӨАТ хонжворт сугалаа, таавар, бооцоо',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag18',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag18',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag18',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag18',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat16': {
                'name': 'НӨАТ зуучлалын үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag19',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag19',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag19',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag19',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat17': {
                'name': 'НӨАТ авсан хүү торгууль, алданги',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag20',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag20',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag20',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag20',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat18': {
                'name': 'НӨАТ хөрөнгийн үнэлгээний үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag21',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag21',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag21',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag21',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat19': {
                'name': 'НӨАТ төсвийн санхүүжилт, татаас',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag22',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag22',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag22',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag22',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat20': {
                'name': 'НӨАТ хууль зүйн үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag23',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag23',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag23',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag23',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat21': {
                'name': 'НӨАТ үсчин, гоо сайхан, угаалга, цэвэрлэгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag24',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag24',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag24',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag24',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat22': {
                'name': 'НӨАТ бусад үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 20,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag25',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag25',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag25',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag25',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat23': {
                'name': 'НӨАТ 0% экспорт бараа',
                'amount': 0.0,
                'price_include': True,
                'sequence': 30,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '0%',
                'tax_group_id': 'account_tax_group3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag28',
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
                                'l10n_mn.vat_report_tag28',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_sale_vat24': {
                'name': 'НӨАТ 0% экспорт үйлчилгээ',
                'amount': 0.0,
                'price_include': True,
                'sequence': 30,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '0%',
                'tax_group_id': 'account_tax_group3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag29',
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
                                'l10n_mn.vat_report_tag29',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'account_tax_purchase_vat3': {
                'name': 'НӨАТ импортоор авсан бараа, үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                                'l10n_mn.vat_report_tag35',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag35',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                                'l10n_mn.vat_report_tag35',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag35',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat4': {
                'name': 'НӨАТ төлөгчөөр бүртгүүлэх үед худалдан авсан',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                                'l10n_mn.vat_report_tag37',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag37',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                                'l10n_mn.vat_report_tag37',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag37',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat5': {
                'name': 'НӨАТ мал аж ахуй эрхлэгчээс худалдан авсан',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                                'l10n_mn.vat_report_tag38',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag38',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                                'l10n_mn.vat_report_tag38',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag38',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat6': {
                'name': 'НӨАТ автомашин, эд анги худалдан авалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag41',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag41',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat7': {
                'name': 'НӨАТ ажлын хэрэгцээнд авсан бараа',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag42',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag42',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat8': {
                'name': 'НӨАТ импортоор авсан үндсэн хөрөнгө',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag43',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag43',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat9': {
                'name': 'НӨАТ чөлөөлөгдөх үйлдвэрлэлд зориулсан бараа, үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag44',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag44',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat10': {
                'name': 'НӨАТ хайгуулд зориулсан импортын бараа, үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag45',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag45',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat11': {
                'name': 'НӨАТ импортын бусад хамааралгүй бараа, үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 40,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag46',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag33',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag46',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat25': {
                'name': 'НӨАТ дотоодод зарсан санхүүгийн түрээс',
                'amount': 10.0,
                'price_include': True,
                'sequence': 50,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag48',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag48',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag48',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag48',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_sale_vat26': {
                'name': 'НӨАТ Факторинг, форфайтинг хэлцлийн үйлчилгээ',
                'amount': 10.0,
                'price_include': True,
                'sequence': 50,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'description': '10%',
                'tax_group_id': 'account_tax_group5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag49',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag49',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag49',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_3401_0201',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag49',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat12': {
                'name': 'НӨАТ Санхүүгийн түрээсийн худалдан авалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 50,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag51',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag51',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag51',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag51',
                            ]),
                        ],
                    }),
                ],
            },
            'account_tax_purchase_vat13': {
                'name': 'НӨАТ Факторинг, форфайтинг худалдан авалт',
                'amount': 10.0,
                'price_include': True,
                'sequence': 50,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'description': '10%',
                'tax_group_id': 'account_tax_group5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag52',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag52',
                            ]),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag52',
                            ]),
                        ],
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_template_1204_0301',
                        'tag_ids': [
                            Command.set([
                                'l10n_mn.vat_report_tag52',
                            ]),
                        ],
                    }),
                ],
            },
        }

    def _get_mn_fiscal_position(self, template_code):
        return {
            'fiscal_position_vat0': {
                'name': 'Дотоодын борлуулалт - Худалдан авалт',
                'auto_apply': 1,
                'country_id': 'base.mn',
            },
            'fiscal_position_vat2': {
                'name': 'НӨАТ 0% (3000000)',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat1',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat4',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat5',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat6',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat7',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat8',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat9',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat10',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat11',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat12',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat13',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat14',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat15',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat16',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat17',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat18',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat19',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat20',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat21',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat22',
                        'tax_dest_id': 'account_tax_sale_vat2',
                    }),
                ],
            },
            'fiscal_position_vat3': {
                'name': 'НӨАТ-гүй (2000000)',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat1',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat4',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat5',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat6',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat7',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat8',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat9',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat10',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat11',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat12',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat13',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat14',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_dest_id': 'account_tax_sale_vat15',
                        'tax_src_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat16',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat17',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat18',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat19',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat20',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat21',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat22',
                        'tax_dest_id': 'account_tax_sale_vat3',
                    }),
                ],
            },
            'fiscal_position_vat4': {
                'name': 'Гадаад борлуулалт - Худалдан авалт',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat1',
                        'tax_dest_id': 'account_tax_sale_vat23',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat4',
                        'tax_dest_id': 'account_tax_sale_vat23',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat5',
                        'tax_dest_id': 'account_tax_sale_vat23',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat6',
                        'tax_dest_id': 'account_tax_sale_vat23',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat7',
                        'tax_dest_id': 'account_tax_sale_vat23',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat8',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat9',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat10',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat11',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat12',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat13',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat14',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_dest_id': 'account_tax_sale_vat15',
                        'tax_src_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat16',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat17',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat18',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat19',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat20',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat21',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_sale_vat22',
                        'tax_dest_id': 'account_tax_sale_vat24',
                    }),
                    Command.create({
                        'tax_src_id': 'account_tax_purchase_vat1',
                        'tax_dest_id': 'account_tax_purchase_vat2',
                    }),
                ],
            },
        }
