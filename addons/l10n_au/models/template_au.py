# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_au_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_au_fiscal_position(template_code),
        }

    def _get_au_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '1111',
            'cash_account_code_prefix': '1113',
            'transfer_account_code_prefix': '11170',
            'code_digits': '5',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'au_11200',
            'property_account_payable_id': 'au_21200',
            'property_account_expense_categ_id': 'au_51110',
            'property_account_income_categ_id': 'au_41110',
            'property_stock_account_input_categ_id': 'au_21210',
            'property_stock_account_output_categ_id': 'au_11340',
            'property_stock_valuation_account_id': 'au_11330',
        }

    def _get_au_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.au',
                'account_default_pos_receivable_account_id': 'au_11201',
                'income_currency_exchange_account_id': 'au_61640',
                'expense_currency_exchange_account_id': 'au_61630',
                'account_journal_early_pay_discount_loss_account_id': 'au_61610',
                'account_journal_early_pay_discount_gain_account_id': 'au_61620',
            },
        }

    def _get_au_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'au_tax_witheld': {
                'name': 'Tax Withheld',
                'sequence': 1000,
                'description': 'Tax Withheld for Partners without ABN',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': -47.0,
                'price_include': False,
                'tax_group_id': 'tax_group_withheld',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21380',
                        'tag_ids': [
                            Command.link('l10n_au.tax_withheld_tag'),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21380',
                        'tag_ids': [
                            Command.link('l10n_au.tax_withheld_tag'),
                        ],
                    }),
                ],
            },
            'au_tax_sale_10': {
                'name': 'Sale (10%)',
                'sequence': 1,
                'description': 'GST Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21310',
                        'tag_ids': tags('+G1', '-GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21310',
                        'tag_ids': tags('-G1', '+GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_sale_inc_10': {
                'name': 'GST Inc Sale (10%)',
                'sequence': 2,
                'description': 'GST Inclusive Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21310',
                        'tag_ids': tags('+G1', '-GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G1'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21310',
                        'tag_ids': tags('-G1', '+GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_sale_0': {
                'name': 'Zero (Export) Sale',
                'sequence': 3,
                'description': 'Zero Rated (Export) Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G1', '+G2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G1', '-G2'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'au_tax_sale_exempt': {
                'name': 'Exempt Sale',
                'sequence': 4,
                'description': 'Exempt Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G1', '+G3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G1', '-G3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'au_tax_sale_input': {
                'name': 'Input Taxed',
                'sequence': 5,
                'description': 'Input Taxed Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G1', '+G4'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G1', '-G4'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'au_tax_sale_adj': {
                'name': 'Sale Adj (10%)',
                'sequence': 6,
                'description': 'Tax Adjustments (Sales)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21310',
                        'tag_ids': tags('+G7', '-GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G7'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21310',
                        'tag_ids': tags('-G7', '+GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_10_service': {
                'name': 'Purch (10%)',
                'sequence': 1,
                'description': 'GST Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G11', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G11', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_10_service_tpar': {
                'name': 'Purch (10%) TPAR',
                'sequence': 1,
                'description': 'GST Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G11', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G11', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_10_service_tpar_no_abn': {
                'name': 'Purch (10%) TPAR without ABN',
                'sequence': 1,
                'description': 'GST Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_10_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_inc_10_service': {
                'name': 'GST Inc Purch (10%)',
                'sequence': 2,
                'description': 'GST Inclusive Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G11', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G11', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_inc_10_service_tpar': {
                'name': 'GST Inc Purch (10%) TPAR',
                'sequence': 2,
                'description': 'GST Inclusive Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G11', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G11', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_inc_10_service_tpar_no_abn': {
                'name': 'GST Inc Purch (10%) TPAR without ABN',
                'sequence': 2,
                'description': 'GST Inclusive Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_inc_10_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_capital_service': {
                'name': 'Capital (10.0%)',
                'sequence': 3,
                'description': 'Capital Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G10'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G10', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G10'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G10', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_capital_service_tpar': {
                'name': 'Capital (10.0%) TPAR',
                'sequence': 3,
                'description': 'Capital Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G10'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G10', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G10'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G10', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_capital_service_tpar_no_abn': {
                'name': 'Capital (10%) TPAR without ABN',
                'sequence': 3,
                'description': 'Capital Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_capital_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_0_service': {
                'name': 'Zero Rated Purch',
                'sequence': 4,
                'description': 'Capital Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'au_tax_purchase_0_service_tpar': {
                'name': 'Zero Rated Purch TPAR',
                'sequence': 4,
                'description': 'Capital Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.link('l10n_au.service_tag'),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.link('l10n_au.service_tag'),
                        ],
                    }),
                ],
            },
            'au_tax_purchase_0_service_tpar_no_abn': {
                'name': 'Zero Rated Purch TPAR without ABN',
                'sequence': 4,
                'description': 'Capital Purchases',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_0_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_taxable_import_service': {
                'name': 'Purch (Taxable Imports)',
                'sequence': 5,
                'description': 'Purchase (Taxable Imports) - Tax Paid Separately',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 100.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_100000000',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'au_tax_purchase_taxable_import_service_tpar': {
                'name': 'Purch (Taxable Imports) TPAR',
                'sequence': 5,
                'description': 'Purchase (Taxable Imports) - Tax Paid Separately',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 100.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_100000000',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.link('l10n_au.service_tag'),
                        ],
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G14'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': [
                            Command.link('l10n_au.service_tag'),
                        ],
                    }),
                ],
            },
            'au_tax_purchase_taxable_import_service_tpar_no_abn': {
                'name': 'Purch (Taxable Imports) TPAR without ABN',
                'sequence': 5,
                'description': 'Purchase (Taxable Imports) - Tax Paid Separately',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_taxable_import_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_input_service': {
                'name': 'Purch for Input Sales',
                'sequence': 6,
                'description': 'Purchases for Input Taxed Sales',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G13'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+G11', '+G13'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G13'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-G11', '-G13'),
                    }),
                ],
            },
            'au_tax_purchase_input_service_tpar': {
                'name': 'Purch for Input Sales TPAR',
                'sequence': 6,
                'description': 'Purchases for Input Taxed Sales',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G13'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+G11', '+G13'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G13'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-G11', '-G13'),
                    }),
                ],
            },
            'au_tax_purchase_input_service_tpar_no_abn': {
                'name': 'Purch for Input Sales TPAR without ABN',
                'sequence': 6,
                'description': 'Purchases for Input Taxed Sales',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_input_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_private_service': {
                'name': 'Purch Private (10%)',
                'sequence': 7,
                'description': 'Purchases for Private use or not deductible',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G15'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+G11', '+G15'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G15'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-G11', '-G15'),
                    }),
                ],
            },
            'au_tax_purchase_private_service_tpar': {
                'name': 'Purch Private (10%) TPAR',
                'sequence': 7,
                'description': 'Purchases for Private use or not deductible',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G11', '+G15'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+G11', '+G15'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G11', '-G15'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-G11', '-G15'),
                    }),
                ],
            },
            'au_tax_purchase_private_service_tpar_no_abn': {
                'name': 'Purch Private (10%) TPAR without ABN',
                'sequence': 7,
                'description': 'Purchases for Private use or not deductible',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_private_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_gst_only_service': {
                'name': 'GST Only on Imports',
                'sequence': 8,
                'description': 'GST Only on Imports',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 100.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_100000000',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+ONLY', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-ONLY', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_gst_only_service_tpar': {
                'name': 'GST Only on Imports TPAR',
                'sequence': 8,
                'description': 'GST Only on Imports',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 100.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_100000000',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+ONLY', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-ONLY', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_gst_only_service_tpar_no_abn': {
                'name': 'GST Only on Imports TPAR without ABN',
                'sequence': 8,
                'description': 'GST Only on Imports',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_gst_only_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
            'au_tax_purchase_adj_service': {
                'name': 'Purch Adj (10%)',
                'sequence': 9,
                'description': 'Tax Adjustments (Purchases)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G18'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G18', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G18'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G18', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_adj_service_tpar': {
                'name': 'Purch Adj (10%) TPAR',
                'sequence': 9,
                'description': 'Tax Adjustments (Purchases)',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount_type': 'percent',
                'amount': 10.0,
                'price_include': False,
                'tax_group_id': 'tax_group_gst_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+G18'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('+G18', '+GST from General Ledger'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-G18'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'au_21330',
                        'tag_ids': tags('-G18', '-GST from General Ledger'),
                    }),
                ],
            },
            'au_tax_purchase_adj_service_tpar_no_abn': {
                'name': 'Purch Adj (10%) TPAR without ABN',
                'sequence': 9,
                'description': 'Tax Adjustments (Purchases)',
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'amount': 100.0,
                'amount_type': 'group',
                'children_tax_ids': [
                    Command.set([
                        'au_tax_purchase_adj_service_tpar',
                        'au_tax_witheld',
                    ]),
                ],
                'tax_group_id': 'tax_group_gst_10',
            },
        }

    def _get_au_fiscal_position(self, template_code):
        return {
            'fiscal_position_os_partner': {
                'name': 'OS Partner',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'au_tax_sale_10',
                        'tax_dest_id': 'au_tax_sale_0',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_sale_inc_10',
                        'tax_dest_id': 'au_tax_sale_0',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_10_service',
                        'tax_dest_id': 'au_tax_purchase_0_service',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_inc_10_service',
                        'tax_dest_id': 'au_tax_purchase_0_service',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_capital_service',
                        'tax_dest_id': 'au_tax_purchase_0_service',
                    }),
                ],
            },
            'fiscal_position_tpar_partner': {
                'name': 'TPAR',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_10_service',
                        'tax_dest_id': 'au_tax_purchase_10_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_inc_10_service',
                        'tax_dest_id': 'au_tax_purchase_inc_10_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_capital_service',
                        'tax_dest_id': 'au_tax_purchase_capital_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_0_service',
                        'tax_dest_id': 'au_tax_purchase_0_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_input_service',
                        'tax_dest_id': 'au_tax_purchase_input_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_private_service',
                        'tax_dest_id': 'au_tax_purchase_private_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_gst_only_service',
                        'tax_dest_id': 'au_tax_purchase_gst_only_service_tpar',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_adj_service',
                        'tax_dest_id': 'au_tax_purchase_adj_service_tpar',
                    }),
                ],
            },
            'fiscal_position_tpar_partner_no_abn': {
                'name': 'TPAR without ABN',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_10_service',
                        'tax_dest_id': 'au_tax_purchase_10_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_inc_10_service',
                        'tax_dest_id': 'au_tax_purchase_inc_10_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_capital_service',
                        'tax_dest_id': 'au_tax_purchase_capital_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_0_service',
                        'tax_dest_id': 'au_tax_purchase_0_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_input_service',
                        'tax_dest_id': 'au_tax_purchase_input_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_private_service',
                        'tax_dest_id': 'au_tax_purchase_private_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_gst_only_service',
                        'tax_dest_id': 'au_tax_purchase_gst_only_service_tpar_no_abn',
                    }),
                    Command.create({
                        'tax_src_id': 'au_tax_purchase_adj_service',
                        'tax_dest_id': 'au_tax_purchase_adj_service_tpar_no_abn',
                    }),
                ],
            },
        }
