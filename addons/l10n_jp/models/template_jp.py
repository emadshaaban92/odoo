# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_jp_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_jp_fiscal_position(template_code),
        }

    def _get_jp_template_data(self, template_code):
        return {
            'code_digits': '7',
            'bank_account_code_prefix': 'A11102',
            'cash_account_code_prefix': 'A11105',
            'transfer_account_code_prefix': 'A11109',
            'property_account_receivable_id': 'A11211',
            'property_account_payable_id': 'A21211',
            'property_account_expense_id': 'A21219',
            'property_account_income_id': 'B41001',
            'property_account_expense_categ_id': 'A21219',
            'property_account_income_categ_id': 'B41001',
        }

    def _get_jp_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.jp',
                'account_default_pos_receivable_account_id': 'A11213',
                'income_currency_exchange_account_id': 'B61501',
                'expense_currency_exchange_account_id': 'B62501',
            },
        }

    def _get_jp_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_in_e': {
                'sequence': 1,
                'name': '仮受消費税(外) 8%',
                'description': '仮受消費税(外) 8%',
                'amount_type': 'percent',
                'amount': 8.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象売上(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('+仮受消費税(8%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象売上(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('-仮受消費税(8%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_8',
            },
            'tax_in_e_10': {
                'sequence': 1,
                'name': '仮受消費税(外) 10%',
                'description': '仮受消費税(外) 10%',
                'amount_type': 'percent',
                'amount': 10.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象売上(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('+仮受消費税(10%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象売上(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('-仮受消費税(10%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'tax_in_i': {
                'sequence': 1,
                'name': '仮受消費税(内) 8%',
                'description': '仮受消費税(内) 8%',
                'amount_type': 'percent',
                'amount': 8.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象売上(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('+仮受消費税(8%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象売上(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('-仮受消費税(8%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_8',
            },
            'tax_in_i_10': {
                'sequence': 1,
                'name': '仮受消費税(内) 10%',
                'description': '仮受消費税(内) 10%',
                'amount_type': 'percent',
                'amount': 10.0,
                'type_tax_use': 'sale',
                'price_include': True,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象売上(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('+仮受消費税(10%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象売上(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A21809',
                        'tag_ids': tags('-仮受消費税(10%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'tax_in_x': {
                'sequence': 1,
                'name': '輸出免税',
                'description': '輸出免税',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-免税売上'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+免税売上'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_in_o': {
                'sequence': 1,
                'name': '非課税販売',
                'description': '非課税販売',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-不課税売上'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+不課税売上'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_out_e': {
                'sequence': 1,
                'name': '仮払消費税(外) 8%',
                'description': '仮払消費税(外) 8%',
                'amount_type': 'percent',
                'amount': 8.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象仕入(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('+仮払消費税(8%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象仕入(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('-仮払消費税(8%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_8',
            },
            'tax_out_e_10': {
                'sequence': 1,
                'name': '仮払消費税(外) 10%',
                'description': '仮払消費税(外) 10%',
                'amount_type': 'percent',
                'amount': 10.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象仕入(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('+仮払消費税(10%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象仕入(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('-仮払消費税(10%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'tax_out_i': {
                'sequence': 1,
                'name': '仮払消費税(内) 8%',
                'description': '仮払消費税(内) 8%',
                'amount_type': 'percent',
                'amount': 8.0,
                'type_tax_use': 'purchase',
                'price_include': True,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象仕入(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('+仮払消費税(8%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象仕入(8%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('-仮払消費税(8%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_8',
            },
            'tax_out_i_10': {
                'sequence': 1,
                'name': '仮払消費税(内) 10%',
                'description': '仮払消費税(内) 10%',
                'amount_type': 'percent',
                'amount': 10.0,
                'type_tax_use': 'purchase',
                'price_include': True,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+課税対象仕入(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('+仮払消費税(10%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-課税対象仕入(10%)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'A11809',
                        'tag_ids': tags('-仮払消費税(10%)'),
                    }),
                ],
                'tax_group_id': 'tax_group_10',
            },
            'tax_out_im': {
                'sequence': 1,
                'name': '海外仕入',
                'description': '海外仕入',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+輸入仕入'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-輸入仕入'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
            'tax_out_o': {
                'sequence': 1,
                'name': '非課税購買',
                'description': '非課税購買',
                'amount_type': 'percent',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'price_include': False,
                'active': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+不課税仕入'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-不課税仕入'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'tax_group_id': 'tax_group_0',
            },
        }

    def _get_jp_fiscal_position(self, template_code):
        return {
            'fiscal_position_tax_inclusive_template': {
                'name': '内税',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_in_e_10',
                        'tax_dest_id': 'tax_in_i_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_e_10',
                        'tax_dest_id': 'tax_out_i_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_in_e',
                        'tax_dest_id': 'tax_in_i',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_e',
                        'tax_dest_id': 'tax_out_i',
                    }),
                ],
            },
            'fiscal_position_tax_exclusive_template': {
                'name': '外税',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_in_i_10',
                        'tax_dest_id': 'tax_in_e_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_i_10',
                        'tax_dest_id': 'tax_out_e_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_in_i',
                        'tax_dest_id': 'tax_in_e',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_i',
                        'tax_dest_id': 'tax_out_e',
                    }),
                ],
            },
            'fiscal_position_tax_exempt_template': {
                'name': '海外取引先',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_in_e_10',
                        'tax_dest_id': 'tax_in_x',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_in_i_10',
                        'tax_dest_id': 'tax_in_x',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_e_10',
                        'tax_dest_id': 'tax_out_im',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_i_10',
                        'tax_dest_id': 'tax_out_im',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_in_e',
                        'tax_dest_id': 'tax_in_x',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_in_i',
                        'tax_dest_id': 'tax_in_x',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_e',
                        'tax_dest_id': 'tax_out_im',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_i',
                        'tax_dest_id': 'tax_out_im',
                    }),
                ],
            },
            'fiscal_position_tax_reduction_template': {
                'name': '軽減税率',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_in_e_10',
                        'tax_dest_id': 'tax_in_e',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_in_i_10',
                        'tax_dest_id': 'tax_in_i',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_e_10',
                        'tax_dest_id': 'tax_out_e',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_out_i_10',
                        'tax_dest_id': 'tax_out_i',
                    }),
                ],
            },
        }
