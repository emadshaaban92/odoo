# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_uy_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'uy_code_11300',
            'property_account_payable_id': 'uy_code_21100',
            'property_account_income_categ_id': 'uy_code_4100',
            'property_account_expense_categ_id': 'uy_code_5100',
            'code_digits': '6',
            'bank_account_code_prefix': '1111',
            'cash_account_code_prefix': '1112',
            'transfer_account_code_prefix': '11120',
        }

    def _get_uy_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.uy',
                'account_default_pos_receivable_account_id': 'uy_code_11307',
                'income_currency_exchange_account_id': 'uy_code_4302',
                'expense_currency_exchange_account_id': 'uy_code_5302',
                'account_journal_early_pay_discount_loss_account_id': 'uy_code_5303',
                'account_journal_early_pay_discount_gain_account_id': 'uy_code_4303',
            },
        }

    def _get_uy_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'vat1': {
                'name': 'IVA Ventas (22%)',
                'description': 'IVA Ventas (22%)',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Ventas 22%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_5202',
                        'tag_ids': tags('+IVA Ventas 22%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Imponible Ventas'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_5202',
                        'tag_ids': tags('-IVA Ventas - percibido'),
                    }),
                ],
            },
            'vat2': {
                'name': 'IVA Ventas (10%)',
                'description': 'IVA Ventas (10%)',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Ventas 10%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_5201',
                        'tag_ids': tags('+IVA Ventas 10%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Imponible Ventas'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_5201',
                        'tag_ids': tags('-IVA Ventas - percibido'),
                    }),
                ],
            },
            'vat3': {
                'name': 'Ventas Exentos IVA',
                'description': 'Ventas Exentos IVA',
                'amount': 0.0,
                'amount_type': 'fixed',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_exenton',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Ventas 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Imponible Ventas'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'vat4': {
                'name': 'IVA Compras (22%)',
                'description': 'IVA Compras (22%)',
                'amount': 22.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_22',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Compras 22%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_11502',
                        'tag_ids': tags('+IVA Compras 22%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Imponible Compras'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_11502',
                        'tag_ids': tags('-IVA Compras - pagado'),
                    }),
                ],
            },
            'vat5': {
                'name': 'IVA Compras (10%)',
                'description': 'IVA Compras (10%)',
                'amount': 10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Compras 10%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_11501',
                        'tag_ids': tags('+IVA Compras 10%'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Imponible Compras'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uy_code_11501',
                        'tag_ids': tags('-IVA Compras - pagado'),
                    }),
                ],
            },
            'vat6': {
                'name': 'Compras Exentos IVA',
                'description': 'Compras Exentos IVA',
                'amount': 0.0,
                'amount_type': 'fixed',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_exenton',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Compras 0%'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Imponible Compras'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }
