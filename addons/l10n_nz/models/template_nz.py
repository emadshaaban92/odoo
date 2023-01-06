# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_nz_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_nz_fiscal_position(template_code),
        }

    def _get_nz_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '1111',
            'cash_account_code_prefix': '1113',
            'transfer_account_code_prefix': '11170',
            'code_digits': '5',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'nz_11200',
            'property_account_payable_id': 'nz_21200',
            'property_account_expense_categ_id': 'nz_51110',
            'property_account_income_categ_id': 'nz_41110',
            'property_stock_account_input_categ_id': 'nz_21210',
            'property_stock_account_output_categ_id': 'nz_11340',
            'property_stock_valuation_account_id': 'nz_11330',
        }

    def _get_nz_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.nz',
                'account_default_pos_receivable_account_id': 'nz_11220',
                'income_currency_exchange_account_id': 'nz_61630',
                'expense_currency_exchange_account_id': 'nz_61630',
                'account_journal_early_pay_discount_loss_account_id': 'nz_61610',
                'account_journal_early_pay_discount_gain_account_id': 'nz_61620',
            },
        }

    def _get_nz_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'nz_tax_sale_15': {
                'name': 'Sale (15%)',
                'sequence': 1,
                'description': 'GST Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 15.0,
                'price_include': False,
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+BOX 5'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21310',
                        'tag_ids': tags('+BOX 5'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-BOX 5'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21310',
                        'tag_ids': tags('-BOX 5'),
                    }),
                ],
            },
            'nz_tax_sale_inc_15': {
                'name': 'GST Inc Sale (15%)',
                'sequence': 2,
                'description': 'GST Inclusive Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 15.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+BOX 5'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21310',
                        'tag_ids': tags('+BOX 5'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-BOX 5'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21310',
                        'tag_ids': tags('-BOX 5'),
                    }),
                ],
            },
            'nz_tax_sale_0': {
                'name': 'Zero/Export (0%) Sale',
                'sequence': 3,
                'description': 'Zero Rated (Export) Sales',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+BOX 5', '+BOX 6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-BOX 5', '-BOX 6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'nz_tax_purchase_15': {
                'name': 'Purch (15%)',
                'sequence': 1,
                'description': 'GST Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 15.0,
                'price_include': False,
                'tax_group_id': 'tax_group_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+BOX 11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21330',
                        'tag_ids': tags('+BOX 11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-BOX 11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21330',
                        'tag_ids': tags('-BOX 11'),
                    }),
                ],
            },
            'nz_tax_purchase_inc_15': {
                'name': 'GST Inc Purch (15%)',
                'sequence': 2,
                'description': 'GST Inclusive Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 15.0,
                'price_include': True,
                'tax_group_id': 'tax_group_gst_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+BOX 11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21330',
                        'tag_ids': tags('+BOX 11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-BOX 11'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21330',
                        'tag_ids': tags('-BOX 11'),
                    }),
                ],
            },
            'nz_tax_purchase_0': {
                'name': 'Zero/Import (0%) Purch',
                'sequence': 3,
                'description': 'Zero Rated Purchases',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_0',
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
            'nz_tax_purchase_taxable_import': {
                'name': 'Purch (Imports Taxable)',
                'sequence': 4,
                'description': 'Purchase (Taxable Imports) - Tax Paid Separately',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'amount': 0.0,
                'price_include': False,
                'tax_group_id': 'tax_group_0',
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
            'nz_tax_purchase_gst_only': {
                'name': 'GST Only - Imports',
                'sequence': 5,
                'description': 'GST Only on Imports',
                'type_tax_use': 'purchase',
                'amount_type': 'division',
                'amount': 100.0,
                'price_include': True,
                'tax_group_id': 'tax_group_100',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21330',
                        'tag_ids': tags('+BOX 11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'nz_21330',
                        'tag_ids': tags('-BOX 11'),
                    }),
                ],
            },
        }

    def _get_nz_fiscal_position(self, template_code):
        return {
            'fiscal_position_os_partner': {
                'name': 'OS Partner',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'nz_tax_sale_15',
                        'tax_dest_id': 'nz_tax_sale_0',
                    }),
                    Command.create({
                        'tax_src_id': 'nz_tax_sale_inc_15',
                        'tax_dest_id': 'nz_tax_sale_0',
                    }),
                    Command.create({
                        'tax_src_id': 'nz_tax_purchase_15',
                        'tax_dest_id': 'nz_tax_purchase_0',
                    }),
                    Command.create({
                        'tax_src_id': 'nz_tax_purchase_inc_15',
                        'tax_dest_id': 'nz_tax_purchase_0',
                    }),
                ],
            },
        }
