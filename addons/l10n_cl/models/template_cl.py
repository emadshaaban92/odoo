# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_cl_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_cl_fiscal_position(template_code),
        }

    def _get_cl_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '1101',
            'cash_account_code_prefix': '1101',
            'transfer_account_code_prefix': '117',
            'code_digits': '6',
            'use_anglo_saxon': True,
            'property_account_receivable_id': 'account_110310',
            'property_account_payable_id': 'account_210210',
            'property_account_expense_categ_id': 'account_410235',
            'property_account_income_categ_id': 'account_310115',
            'property_stock_account_input_categ_id': 'account_210230',
            'property_stock_account_output_categ_id': 'account_110640',
            'property_stock_valuation_account_id': 'account_110610',
        }

    def _get_cl_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.cl',
                'account_default_pos_receivable_account_id': 'account_110421',
                'income_currency_exchange_account_id': 'account_410195',
                'expense_currency_exchange_account_id': 'account_410195',
            },
        }

    def _get_cl_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'ITAX_19': {
                'name': 'IVA 19% Venta',
                'description': 'IVA 19% Vta',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'l10n_cl_sii_code': '14',
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Ventas Netas Gravadas con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210710',
                        'tag_ids': tags('+IVA Debito Fiscal'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Ventas Netas Gravadas con IVA'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210710',
                        'tag_ids': tags('-IVA Debito Fiscal'),
                    }),
                ],
            },
            'OTAX_19': {
                'name': 'IVA 19% Compra',
                'description': 'IVA 19% Comp',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras Netas Gravadas Con IVA (recuperable)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110710',
                        'tag_ids': tags('+IVA Pagado Compras Recuperables'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras Netas Gravadas Con IVA (recuperable)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110710',
                        'tag_ids': tags('-IVA Pagado Compras Recuperables'),
                    }),
                ],
            },
            'I_IU2C': {
                'name': 'Ret. 2da Categoría 2020',
                'description': 'Ret. 2da 2020',
                'active': False,
                'amount': -10.75,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_IR2C_2021': {
                'name': 'Ret. 2da Categoría 2021',
                'description': 'Ret. 2da 2021',
                'active': False,
                'amount': -11.5,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_IR2C_2022': {
                'name': 'Ret. 2da Categoría 2022',
                'description': 'Ret. 2da 2022',
                'amount': -12.25,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_IR2C_2023': {
                'name': 'Ret. 2da Categoría 2023',
                'description': 'Ret. 2da 2023',
                'amount': -13.0,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_IR2C_2024': {
                'name': 'Ret. 2da Categoría 2024',
                'description': 'Ret. 2da 2024',
                'amount': -13.75,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_IR2C_2025': {
                'name': 'Ret. 2da Categoría 2025',
                'description': 'Ret. 2da 2025',
                'amount': -14.5,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_IR2C_2026': {
                'name': 'Ret. 2da Categoría 2026',
                'description': 'Ret. 2da 2026',
                'amount': -15.25,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_2da_categ',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('+Retención Segunda Categoría'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retención Segunda Categoría'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'account_210740',
                        'tag_ids': tags('-Retención Segunda Categoría'),
                    }),
                ],
            },
            'I_RTI': {
                'name': 'Retención Total IVA',
                'description': 'Retención total IVA',
                'amount': -19.0,
                'sequence': 2,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '15',
                'tax_group_id': 'tax_group_retenciones',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Retención Total (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210715',
                        'tag_ids': tags('+Retención Total (compras)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Retención Total (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210715',
                        'tag_ids': tags('-Retención Total (compras)'),
                    }),
                ],
            },
            'especifico_compra': {
                'name': 'Específico Compra',
                'description': 'Espec. Comp',
                'amount': 63.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '29',
                'sequence': 5,
                'tax_group_id': 'tax_group_impuestos_especificos',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                    }),
                ],
            },
            'iva_activo_fijo': {
                'name': 'IVA Compra 19% Activo Fijo',
                'description': 'IVA 19% ActF',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'sequence': 6,
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras de Activo Fijo'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110730',
                        'tag_ids': tags('+Compras Activo Fijo'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras de Activo Fijo'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110730',
                        'tag_ids': tags('-Compras Activo Fijo'),
                    }),
                ],
            },
            'iva_activo_fijo_uso_comun': {
                'name': 'IVA Compra 19% Act. Fijo Uso Común',
                'description': 'IVA 19% ActFUC',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'sequence': 6,
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras de Activo Fijo Uso Común'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110730',
                        'tag_ids': tags('+Compras Activo Fijo Uso Común'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras de Activo Fijo Uso Común'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110730',
                        'tag_ids': tags('-Compras Activo Fijo Uso Común'),
                    }),
                ],
            },
            'iva_activo_fijo_uso_no_recup': {
                'name': 'IVA Compra 19% Activo Fijo No Recup',
                'description': 'IVA 19% ActFNR',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'sequence': 6,
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras de Activo Fijo No Recuperable'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('+Compras Activo Fijo No Recuperables'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras de Activo Fijo No Recuperable'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('-Compras Activo Fijo No Recuperables'),
                    }),
                ],
            },
            'ila_a_100_p': {
                'name': 'Beb. Analc. 10% (Compras)',
                'description': 'ILA C 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '27',
                'type_tax_use': 'purchase',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('+Retenciones ILA (compras)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('-Retenciones ILA (compras)'),
                    }),
                ],
            },
            'ila_a_180_p': {
                'name': 'Beb. Analc 18% (Compras)',
                'description': 'ILA C 18%',
                'amount': 18.0,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '26',
                'type_tax_use': 'purchase',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('+Retenciones ILA (compras)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('-Retenciones ILA (compras)'),
                    }),
                ],
            },
            'ila_v_205_p': {
                'name': 'Vinos (Compras)',
                'description': 'ILA C 20.5%',
                'amount': 20.5,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '25',
                'type_tax_use': 'purchase',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('+Retenciones ILA (compras)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('-Retenciones ILA (compras)'),
                    }),
                ],
            },
            'ila_l_315_p': {
                'name': 'Licores 31.5% (Compras)',
                'description': 'ILA C 31.5%',
                'amount': 31.5,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '24',
                'type_tax_use': 'purchase',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('+Retenciones ILA (compras)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (compras)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('-Retenciones ILA (compras)'),
                    }),
                ],
            },
            'ila_a_100_s': {
                'name': 'Beb. Analc. 10% (Ventas)',
                'description': 'ILA V 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '27',
                'type_tax_use': 'sale',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('+Retenciones ILA (ventas)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('-Retenciones ILA (ventas)'),
                    }),
                ],
            },
            'ila_a_180_s': {
                'name': 'Beb. Analc 18% (Ventas)',
                'description': 'ILA V 18%',
                'amount': 18.0,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '26',
                'type_tax_use': 'sale',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('+Retenciones ILA (ventas)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('-Retenciones ILA (ventas)'),
                    }),
                ],
            },
            'ila_v_205_s': {
                'name': 'Vinos (Ventas)',
                'description': 'ILA V 20.5%',
                'amount': 20.5,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '25',
                'type_tax_use': 'sale',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('+Retenciones ILA (ventas)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('-Retenciones ILA (ventas)'),
                    }),
                ],
            },
            'ila_l_315_s': {
                'name': 'Licores 31.5% (Ventas)',
                'description': 'ILA V 31.5%',
                'amount': 31.5,
                'amount_type': 'percent',
                'l10n_cl_sii_code': '24',
                'type_tax_use': 'sale',
                'sequence': 7,
                'tax_group_id': 'tax_group_ila',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('+Retenciones ILA (ventas)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Base Retenciones ILA (ventas)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_210760',
                        'tag_ids': tags('-Retenciones ILA (ventas)'),
                    }),
                ],
            },
            'iva_compra_no_recup': {
                'name': 'IVA Compra 19% No Recup.',
                'description': 'IVA 19% NoR',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'sequence': 6,
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras IVA No Recuperable'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('+IVA Pagado No Recuperable'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras IVA No Recuperable'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_420220',
                        'tag_ids': tags('-IVA Pagado No Recuperable'),
                    }),
                ],
            },
            'iva_compra_uso_comun': {
                'name': 'IVA Compra 19% Uso Común',
                'description': 'IVA 19% CUC',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'sequence': 6,
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compra Netas Gravadas Con IVA Uso Comun'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110730',
                        'tag_ids': tags('+IVA Pagado Compras Uso Común'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compra Netas Gravadas Con IVA Uso Comun'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110730',
                        'tag_ids': tags('-IVA Pagado Compras Uso Común'),
                    }),
                ],
            },
            'iva_supermercado_recup': {
                'name': 'IVA Compra 19% Superm.',
                'description': 'IVA 19% SupMRec',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'l10n_cl_sii_code': '14',
                'sequence': 6,
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Compras De Supermercado'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110710',
                        'tag_ids': tags('+IVA Pagado Compras Supermercado'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Compras De Supermercado'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'account_110710',
                        'tag_ids': tags('-IVA Pagado Compras Supermercado'),
                    }),
                ],
            },
        }

    def _get_cl_fiscal_position(self, template_code):
        return {
            'afpt_non_recoverable_vat_1': {
                'name': 'Compras - destinadas a generar operaciones no gravadas o exentas',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                        'tax_dest_id': 'iva_compra_no_recup',
                    }),
                ],
            },
            'afpt_non_recoverable_vat_2': {
                'name': 'Compras - Facturas de proveedores registrados fuera de plazo',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                        'tax_dest_id': 'iva_compra_no_recup',
                    }),
                ],
            },
            'afpt_non_recoverable_vat_3': {
                'name': 'Compras - Gastos rechazados',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                        'tax_dest_id': 'iva_compra_no_recup',
                    }),
                ],
            },
            'afpt_non_recoverable_vat_4': {
                'name': 'Compras - Entregas gratuitas (premios, bonificaciones, etc.) recibidos',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                        'tax_dest_id': 'iva_compra_no_recup',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_410235',
                        'account_dest_id': 'account_410165',
                    }),
                    Command.create({
                        'account_src_id': 'account_410230',
                        'account_dest_id': 'account_410165',
                    }),
                ],
            },
            'afpt_non_recoverable_vat_9': {
                'name': 'Compras - Otros',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                        'tax_dest_id': 'iva_compra_no_recup',
                    }),
                ],
            },
            'afpt_fixed_asset': {
                'name': 'Compras - Activo Fijo',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                        'tax_dest_id': 'iva_activo_fijo_uso_comun',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_410230',
                        'account_dest_id': 'account_121140',
                    }),
                    Command.create({
                        'account_src_id': 'account_410235',
                        'account_dest_id': 'account_121140',
                    }),
                ],
            },
            'afpt_purchase_exempt': {
                'name': 'Compras - Exentas',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'OTAX_19',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_410230',
                        'account_dest_id': 'account_410130',
                    }),
                ],
            },
            'afpt_purchase_supermarket': {
                'name': 'Compras - Supermercado',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'ITAX_19',
                        'tax_dest_id': 'iva_supermercado_recup',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_410230',
                        'account_dest_id': 'account_410233',
                    }),
                    Command.create({
                        'account_src_id': 'account_410235',
                        'account_dest_id': 'account_410233',
                    }),
                ],
            },
            'afpt_sale_exempt': {
                'name': 'Ventas - Exentas',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'ITAX_19',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'account_310115',
                        'account_dest_id': 'account_310120',
                    }),
                ],
            },
        }
