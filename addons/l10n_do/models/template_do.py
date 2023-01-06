# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_do_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_do_fiscal_position(template_code),
        }

    def _get_do_template_data(self, template_code):
        return {
            'code_digits': '8',
            'cash_account_code_prefix': '110101',
            'bank_account_code_prefix': '110102',
            'transfer_account_code_prefix': '11010100',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'do_niif_11030201',
            'property_account_payable_id': 'do_niif_21010200',
            'property_account_income_categ_id': 'do_niif_41010100',
            'property_account_expense_categ_id': 'do_niif_51010100',
            'property_stock_account_input_categ_id': 'do_niif_21021200',
            'property_stock_account_output_categ_id': 'do_niif_11050600',
            'property_stock_valuation_account_id': 'do_niif_11050100',
        }

    def _get_do_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.do',
                'account_default_pos_receivable_account_id': 'do_niif_11030210',
                'income_currency_exchange_account_id': 'do_niif_42040100',
                'expense_currency_exchange_account_id': 'do_niif_52070800',
                'account_journal_early_pay_discount_loss_account_id': 'do_niif_99900003',
                'account_journal_early_pay_discount_gain_account_id': 'do_niif_99900004',
            },
        }

    def _get_do_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_0_sale': {
                'sequence': 4,
                'name': 'Exento ITBIS Ventas',
                'description': 'Exento',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.A.3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-II.A.3'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax_0_purch': {
                'sequence': 10,
                'name': 'Exento ITBIS Compras',
                'description': 'Exento',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
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
            'tax_18_sale': {
                'sequence': 1,
                'name': '18% ITBIS Ventas',
                'description': '18% ITBIS',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.B.6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030102',
                        'tag_ids': tags('+III.8'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-II.B.6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030102',
                        'tag_ids': tags('-III.8'),
                    }),
                ],
            },
            'tax_18_sale_incl': {
                'sequence': 2,
                'name': '18% ITBIS Incl. Ventas',
                'description': '18% ITBIS',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': True,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+II.B.6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030102',
                        'tag_ids': tags('+III.8'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-II.B.6'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030102',
                        'tag_ids': tags('-III.8'),
                    }),
                ],
            },
            'tax_tip_sale': {
                'sequence': 3,
                'name': '10% Propina Legal',
                'description': '10% Legal',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'tax_group_tip',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030503',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030503',
                    }),
                ],
            },
            'tax_18_purch': {
                'name': '18% ITBIS Compras',
                'sequence': 11,
                'description': '18% ITBIS (B)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                        'tag_ids': tags('-III.11'),
                    }),
                ],
            },
            'tax_18_purch_incl': {
                'sequence': 12,
                'name': '18% ITBIS Incl. Compras',
                'description': '18% ITBIS (Incl B)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                        'tag_ids': tags('-III.11'),
                    }),
                ],
            },
            'tax_16_purch': {
                'name': '16% ITBIS Compras',
                'sequence': 13,
                'description': '16% ITBIS (B)',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
            },
            'tax_16_purch_incl': {
                'name': '16% ITBIS Incl. Compras',
                'sequence': 14,
                'description': '16% ITBIS (Incl B)',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
            },
            'tax_9_purch': {
                'name': '9% ITBIS Compras',
                'sequence': 15,
                'description': '9% ITBIS (L690-16)',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
            },
            'tax_9_purch_incl': {
                'name': '9% ITBIS Incl. Compras',
                'sequence': 16,
                'description': '9% ITBIS (L690-16)',
                'amount': 9.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
            },
            'tax_8_purch': {
                'name': '8% ITBIS Compras',
                'sequence': 17,
                'description': '8% ITBIS (L690-16)',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
            },
            'tax_8_purch_incl': {
                'name': '8% ITBIS Incl. Compras',
                'sequence': 18,
                'description': '8% ITBIS (L690-16)',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080101',
                    }),
                ],
            },
            'tax_tip_purch': {
                'sequence': 19,
                'name': '10% Propina Legal',
                'description': '10% Legal',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'tax_group_tip',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52080900',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52080900',
                    }),
                ],
            },
            'tax_18_purch_serv': {
                'sequence': 20,
                'name': '18% ITBIS Compras - Servicios',
                'description': '18% ITBIS (S)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080102',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080102',
                        'tag_ids': tags('-III.11'),
                    }),
                ],
            },
            'tax_18_purch_serv_incl': {
                'sequence': 20,
                'name': '18% ITBIS Incl. Compras - Servicios',
                'description': '18% ITBIS (Incl S)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080102',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080102',
                        'tag_ids': tags('-III.11'),
                    }),
                ],
            },
            'tax_18_importation': {
                'sequence': 20,
                'name': '18% ITBIS - Importaciones',
                'description': '18% ITBIS (IMP)',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080103',
                        'tag_ids': tags('+III.13'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080103',
                        'tag_ids': tags('-III.13'),
                    }),
                ],
            },
            'tax_18_of_10': {
                'sequence': 20,
                'name': '18% ITBIS sobre el 10% del Monto Total',
                'description': '18% del 10%',
                'amount': 1.8,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030102',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030102',
                    }),
                ],
            },
            'tax_0015_bank': {
                'sequence': 30,
                'name': '0.15% Transferencia Bancaria',
                'description': '0.15% Trans',
                'amount': 0.0015,
                'amount_type': 'percent',
                'type_tax_use': 'none',
                'price_include': True,
                'tax_group_id': 'group_tax',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52070200',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52070200',
                    }),
                ],
            },
            'tax_10_telco': {
                'sequence': 30,
                'name': '10% ISC Telecomunicaciones',
                'description': '10% ISC',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'tax_group_isc',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52020200',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52020200',
                    }),
                ],
            },
            'tax_2_telco': {
                'sequence': 30,
                'name': '2% CDT Telecomunicaciones',
                'description': '2% CDT',
                'amount': 2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_tax',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52020200',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_52020200',
                    }),
                ],
            },
            'tax_group_telco': {
                'sequence': 30,
                'name': 'Impuestos a las Telecomunicaciones',
                'amount': 18.0,
                'amount_type': 'group',
                'type_tax_use': 'purchase',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_purch',
                        'tax_10_telco',
                        'tax_2_telco',
                    ]),
                ],
                'tax_group_id': 'group_tax',
            },
            'ret_100_tax_security': {
                'sequence': 40,
                'name': 'Retención 100% ITBIS Servicios de Seguridad (N07-09)',
                'description': '-100% ITBIS (N07-09)',
                'amount': -18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030201',
                    }),
                ],
            },
            'ret_100_tax_nonprofit': {
                'sequence': 41,
                'name': 'Retención 100% ITBIS Servicios No Lucrativas (N01-11)',
                'description': '-100% ITBIS (N01-11)',
                'amount': -18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+A.25'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030203',
                        'tag_ids': tags('-A.30'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-A.25'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030203',
                        'tag_ids': tags('+A.30'),
                    }),
                ],
            },
            'ret_100_tax_person': {
                'sequence': 42,
                'name': 'Retención 100% ITBIS Servicios a Físicas (R293-11)',
                'description': '-100% ITBIS (R293-11)',
                'amount': -18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+A.25'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030202',
                        'tag_ids': tags('-A.30'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-A.25'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030202',
                        'tag_ids': tags('+A.30'),
                    }),
                ],
            },
            'ret_30_tax_moral': {
                'sequence': 43,
                'name': 'Retención 30% ITBIS Servicios a Jurídicas (N02-05)',
                'description': '-30% ITBIS (N02-05)',
                'amount': -5.4,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030201',
                    }),
                ],
            },
            'ret_30_tax_freelance': {
                'active': False,
                'sequence': 43,
                'name': 'Retención 30% ITBIS Servicios Profesionales (N02-05)',
                'description': '-30% ITBIS (N02-05)',
                'amount': -5.4,
                'amount_type': 'percent',
                'type_tax_use': 'none',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030201',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030201',
                    }),
                ],
            },
            'ret_75_tax_nonformal': {
                'sequence': 44,
                'name': 'Retención 75% ITBIS Bienes a Informales (N08-10)',
                'description': '-75% ITBIS (N08-10)',
                'amount': -13.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030205',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030205',
                    }),
                ],
            },
            'ret_10_income_person': {
                'sequence': 40,
                'name': 'Retención 10% ISR Honorarios a Físicas',
                'description': '-10% ISR',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030301',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030301',
                    }),
                ],
            },
            'ret_10_income_rent': {
                'sequence': 50,
                'name': 'Retención 10% ISR Alquileres a Físicas',
                'description': '-10% ISR',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030302',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030302',
                    }),
                ],
            },
            'ret_10_income_dividend': {
                'sequence': 51,
                'name': 'Retención 10% ISR por Dividendos (L253-12)',
                'description': '-10% ISR',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030303',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030303',
                    }),
                ],
            },
            'ret_2_income_person': {
                'sequence': 52,
                'name': 'Retención 2% ISR a Física (con Materiales)',
                'description': '-2% ISR (N07-07)',
                'amount': -2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030308',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030308',
                    }),
                ],
            },
            'ret_2_income_transfer': {
                'sequence': 53,
                'name': 'Retención 2% ISR por Transferencia de Títulos',
                'description': '-2% ISR',
                'amount': -2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030306',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030306',
                    }),
                ],
            },
            'ret_27_income_remittance': {
                'sequence': 49,
                'name': 'Retención 27% ISR por Remesas al Exterior (L253-12)',
                'description': '-27% ISR',
                'amount': -27.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030307',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_21030307',
                    }),
                ],
            },
            'ret_5_income_gov': {
                'sequence': 50,
                'name': 'Retención 5% ISR Gubernamentales',
                'description': '-5% ISR',
                'amount': -5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'price_include': False,
                'tax_group_id': 'group_isr',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080302',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080302',
                    }),
                ],
            },
            'tax_group_nonformal': {
                'sequence': 60,
                'name': 'Retención a Proveedores Informales de Bienes (75%)',
                'amount_type': 'group',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'tax_group_id': 'group_ret',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_purch',
                        'ret_75_tax_nonformal',
                    ]),
                ],
            },
            'tax_group_person_construction': {
                'sequence': 61,
                'name': 'Retención a Físicas por Servicios con Materiales (2%)',
                'amount_type': 'group',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_purch',
                        'ret_100_tax_person',
                        'ret_2_income_person',
                    ]),
                ],
                'tax_group_id': 'group_ret',
            },
            'tax_group_person_services': {
                'sequence': 58,
                'name': 'Retención a Físicas por Honorarios por Servicios (10%)',
                'amount_type': 'group',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_purch',
                        'ret_100_tax_person',
                        'ret_10_income_person',
                    ]),
                ],
                'tax_group_id': 'group_ret',
            },
            'tax_group_moral_services': {
                'sequence': 58,
                'name': 'Retención a Jurídicas por Servicios Profesionales (30%)',
                'amount_type': 'group',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_purch',
                        'ret_30_tax_moral',
                    ]),
                ],
                'tax_group_id': 'group_ret',
            },
            'tax_group_restaurant_sale': {
                'sequence': 64,
                'name': 'Ventas del Restaurante',
                'amount_type': 'group',
                'amount': 18.0,
                'type_tax_use': 'sale',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_sale',
                        'tax_tip_sale',
                    ]),
                ],
                'tax_group_id': 'group_ret',
            },
            'tax_group_restaurant_purch': {
                'sequence': 65,
                'name': 'Compras a Restaurantes',
                'amount_type': 'group',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'children_tax_ids': [
                    Command.set([
                        'tax_18_purch',
                        'tax_tip_purch',
                    ]),
                ],
                'tax_group_id': 'group_ret',
            },
            'tax_18_10_total_mount': {
                'name': '18% ITBIS sobre el 10% del Monto Total',
                'description': '18% del 10%',
                'amount': 1.8,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080102',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_11080102',
                    }),
                ],
            },
            'tax_18_property_cost': {
                'name': '18% ITBIS llevado al Costo Bienes',
                'description': '18%',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_51010500',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_51010500',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
            },
            'tax_18_serv_cost': {
                'name': '18% ITBIS llevado al Costo Servicios',
                'description': '18%',
                'amount': 18.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': False,
                'tax_group_id': 'group_itbis',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_51010500',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'do_niif_51010500',
                        'tag_ids': tags('+III.11'),
                    }),
                ],
            },
        }

    def _get_do_fiscal_position(self, template_code):
        return {
            'position_person': {
                'name': 'P. Física de Servicios',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'tax_group_person_services',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_purch_serv',
                        'tax_dest_id': 'tax_group_person_services',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_dest_id': 'do_niif_52030111',
                        'account_src_id': 'do_niif_52021500',
                    }),
                ],
            },
            'position_service_moral': {
                'name': 'P. Jurídica de Servicios',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'tax_group_moral_services',
                    }),
                ],
            },
            'position_security_moral': {
                'name': 'P. Jurídica de Vigilancia',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'ret_100_tax_security',
                    }),
                ],
            },
            'position_nonformal': {
                'name': 'Proveedor Informal de Bienes',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'tax_group_nonformal',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_purch_incl',
                        'tax_dest_id': 'tax_group_nonformal',
                    }),
                ],
            },
            'position_exterior': {
                'name': 'Servicios del Exterior',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch_serv',
                        'tax_dest_id': 'ret_27_income_remittance',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'ret_27_income_remittance',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_dest_id': 'do_niif_21010300',
                        'account_src_id': 'do_niif_21010200',
                    }),
                ],
            },
            'position_gov': {
                'name': 'Gubernamental',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_sale',
                        'tax_dest_id': 'ret_5_income_gov',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_sale_incl',
                        'tax_dest_id': 'ret_5_income_gov',
                    }),
                ],
            },
            'position_nonprofit': {
                'name': 'No Lucrativa de Servicios',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'ret_100_tax_nonprofit',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_purch_incl',
                        'tax_dest_id': 'ret_100_tax_nonprofit',
                    }),
                ],
            },
            'position_especial': {
                'name': 'Regímenes Especiales',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_sale',
                        'tax_dest_id': 'tax_0_sale',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_sale_incl',
                        'tax_dest_id': 'tax_0_sale',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_group_restaurant_sale',
                        'tax_dest_id': 'tax_tip_sale',
                    }),
                ],
            },
            'position_restaurant': {
                'name': 'Restaurantes',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_18_purch',
                        'tax_dest_id': 'tax_group_restaurant_purch',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_purch_incl',
                        'tax_dest_id': 'tax_group_restaurant_purch',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_sale',
                        'tax_dest_id': 'tax_group_restaurant_sale',
                    }),
                    Command.create({
                        'tax_src_id': 'tax_18_sale_incl',
                        'tax_dest_id': 'tax_group_restaurant_sale',
                    }),
                ],
            },
            'position_restaurant_takeout': {
                'name': 'Para Llevar',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax_group_restaurant_sale',
                        'tax_dest_id': 'tax_18_sale',
                    }),
                ],
            },
        }
