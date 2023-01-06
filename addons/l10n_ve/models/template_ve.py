# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ve_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '1113',
            'cash_account_code_prefix': '1111',
            'transfer_account_code_prefix': '1129003',
            'code_digits': '7',
            'property_account_receivable_id': 'account_activa_account_1122001',
            'property_account_payable_id': 'account_activa_account_2122001',
            'property_account_expense_categ_id': 'account_activa_account_7151001',
            'property_account_income_categ_id': 'account_activa_account_5111001',
        }

    def _get_ve_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ve',
                'account_default_pos_receivable_account_id': 'account_activa_account_1122003',
                'income_currency_exchange_account_id': 'account_activa_account_9212003',
                'expense_currency_exchange_account_id': 'account_activa_account_9113006',
            },
        }

    def _get_ve_account_tax(self, template_code):
        return {
            'tax0sale': {
                'name': 'Exento (ventas)',
                'description': 'Exento (ventas)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_0',
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
            'tax1sale': {
                'name': 'IVA (12.0%) ventas',
                'description': 'IVA (12.0%) ventas',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_2172003',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_2172003',
                    }),
                ],
            },
            'tax2sale': {
                'name': 'IVA (8.0%) ventas',
                'description': 'IVA (8.0%) ventas',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_2172003',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_2172003',
                    }),
                ],
            },
            'tax3sale': {
                'name': 'IVA (22.0%) ventas',
                'description': 'IVA (22.0%) ventas',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_2172003',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_2172003',
                    }),
                ],
            },
            'tax0purchase': {
                'name': 'Exento (compras)',
                'description': 'Exento (compras)',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_0',
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
            'tax1purchase': {
                'name': 'IVA (12.0%) compras',
                'description': 'IVA (12.0%) compras',
                'amount': 12.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_1151004',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_1151004',
                    }),
                ],
            },
            'tax2purchase': {
                'name': 'IVA (8.0%) compras',
                'description': 'IVA (8.0%) compras',
                'amount': 8.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_8',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_1151004',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_1151004',
                    }),
                ],
            },
            'tax3purchase': {
                'name': 'IVA (22.0%) compras',
                'description': 'IVA (22.0%) compras',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_1151004',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_activa_account_1151004',
                    }),
                ],
            },
        }
