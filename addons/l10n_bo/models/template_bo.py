# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_bo_template_data(self, template_code):
        return {
            'code_digits': '6',
            'bank_account_code_prefix': '114',
            'cash_account_code_prefix': '111',
            'transfer_account_code_prefix': '117',
            'property_account_receivable_id': '121',
            'property_account_payable_id': '211',
            'property_account_expense_categ_id': '61_01',
            'property_account_income_categ_id': '411_01',
        }

    def _get_bo_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.bo',
                'account_default_pos_receivable_account_id': '121_001',
                'income_currency_exchange_account_id': 'ch_bo_426',
                'expense_currency_exchange_account_id': 'ch_bo_524',
            },
        }

    def _get_bo_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'ITAX_21': {
                'name': 'IVA 13% Venta',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_iva_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Impuesto al Valor Agregado con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                        'tag_ids': tags('+Impuesto Cobrado IVA'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Impuesto al Valor Agregado con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                        'tag_ids': tags('-Impuesto Cobrado IVA'),
                    }),
                ],
            },
            'OTAX_21': {
                'name': 'IVA 13% Compra',
                'amount': 13.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_iva_13',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras Gravadas con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                        'tag_ids': tags('+Impuesto Pagado IVA'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras Gravadas con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '231',
                        'tag_ids': tags('-Impuesto Pagado IVA'),
                    }),
                ],
            },
            'ITAX_03': {
                'name': 'IT 3%',
                'amount': 3.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_it_3',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Impuesto al Valor Agregado con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '232',
                        'tag_ids': tags('+Impuesto a las Transacciones IT (3%)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Impuesto al Valor Agregado con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': '232',
                        'tag_ids': tags('-Impuesto a las Transacciones IT (3%)'),
                    }),
                ],
            },
        }
