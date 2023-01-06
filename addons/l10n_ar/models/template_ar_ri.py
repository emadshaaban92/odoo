# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ar_ri_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ar_ri_fiscal_position(template_code),
        }

    def _get_ar_ri_template_data(self, template_code):
        return {
            'parent_id': 'l10nar_ex_chart_template',
            'bank_account_code_prefix': '1.1.1.02.',
            'cash_account_code_prefix': '1.1.1.01.',
            'code_digits': '12',
            'transfer_account_code_prefix': '6.0.00.00.',
        }

    def _get_ar_ri_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ar',
                'account_default_pos_receivable_account_id': 'base_deudores_por_ventas_pos',
                'income_currency_exchange_account_id': 'base_diferencias_de_cambio',
                'expense_currency_exchange_account_id': 'base_diferencias_de_cambio',
            },
        }

    def _get_ar_ri_account_tax(self, template_code):
        return {
            'ri_tax_vat_no_corresponde_ventas': {
                'description': 'IVA No Corresponde',
                'name': 'IVA No Corresponde',
                'active': False,
                'sequence': 2,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_no_corresponde',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_no_corresponde_compras': {
                'description': 'IVA No Corresponde',
                'name': 'IVA No Corresponde',
                'sequence': 2,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_no_corresponde',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_no_gravado_ventas': {
                'description': 'IVA No Gravado',
                'name': 'IVA No Gravado',
                'sequence': 2,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_no_gravado',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_no_gravado_compras': {
                'description': 'IVA No Gravado',
                'name': 'IVA No Gravado',
                'sequence': 2,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_no_gravado',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_exento_ventas': {
                'description': 'IVA Exento',
                'name': 'IVA Exento',
                'sequence': 2,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_exento',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_exento_compras': {
                'description': 'IVA Exento',
                'name': 'IVA Exento',
                'sequence': 2,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_exento',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_0_ventas': {
                'description': 'IVA 0%',
                'name': 'IVA 0%',
                'sequence': 2,
                'amount': 0.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_0',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_0_compras': {
                'description': 'IVA 0%',
                'name': 'IVA 0%',
                'sequence': 2,
                'amount': 0.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_0',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_10_ventas': {
                'description': 'IVA 10.5%',
                'name': 'IVA 10.5%',
                'sequence': 2,
                'amount': 10.5,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_105',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_10_compras': {
                'description': 'IVA 10.5%',
                'name': 'IVA 10.5%',
                'sequence': 2,
                'amount': 10.5,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_105',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_21_ventas': {
                'name': 'IVA 21%',
                'description': 'IVA 21%',
                'sequence': 1,
                'amount': 21.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_21',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_21_compras': {
                'name': 'IVA 21%',
                'description': 'IVA 21%',
                'sequence': 1,
                'amount': 21.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_21',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_27_ventas': {
                'name': 'IVA 27%',
                'description': 'IVA 27%',
                'sequence': 3,
                'amount': 27.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_27',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_27_compras': {
                'name': 'IVA 27%',
                'description': 'IVA 27%',
                'sequence': 3,
                'amount': 27.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_27',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_25_ventas': {
                'name': 'IVA 2,5%',
                'description': 'IVA 2,5%',
                'sequence': 9,
                'active': False,
                'amount': 2.5,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_025',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_25_compras': {
                'name': 'IVA 2,5%',
                'description': 'IVA 2,5%',
                'sequence': 9,
                'active': False,
                'amount': 2.5,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_025',
                'type_tax_use': 'purchase',
            },
            'ri_tax_vat_5_ventas': {
                'name': 'IVA 5%',
                'description': 'IVA 5%',
                'sequence': 10,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_5',
                'type_tax_use': 'sale',
            },
            'ri_tax_vat_5_compras': {
                'name': 'IVA 5%',
                'description': 'IVA 5%',
                'sequence': 10,
                'active': False,
                'amount': 5.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_credito_fiscal',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_iva_debito_fiscal',
                    }),
                ],
                'tax_group_id': 'tax_group_iva_5',
                'type_tax_use': 'purchase',
            },
            'ri_tax_percepcion_iva_sufrida': {
                'name': 'Percepción IVA Sufrida',
                'description': 'Perc IVA S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iva_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iva_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iva',
            },
            'ri_tax_ganancias_iva_adicional': {
                'name': 'IVA Adicional 20%',
                'description': 'IVA Adicional 20%',
                'sequence': 4,
                'amount': 20.0,
                'amount_type': 'percent',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iva_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iva_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iva',
            },
        }

    def _get_ar_ri_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_exempt_operations': {
                'name': 'Compras / Ventas al exterior',
                'auto_apply': 1,
                'l10n_ar_afip_responsibility_type_ids': [
                    Command.set([
                        'l10n_ar.res_EXT',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_0_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_10_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_21_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_27_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_0_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_10_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_21_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_27_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_exento_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_no_gravado_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                ],
            },
            'fiscal_position_template_free_zone': {
                'name': 'Compras / Ventas Zona Franca',
                'auto_apply': 1,
                'l10n_ar_afip_responsibility_type_ids': [
                    Command.set([
                        'l10n_ar.res_IVA_LIB',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_0_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_10_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_21_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_27_ventas',
                        'tax_dest_id': 'ri_tax_vat_exento_ventas',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_0_compras',
                        'tax_dest_id': 'ri_tax_vat_exento_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_10_compras',
                        'tax_dest_id': 'ri_tax_vat_exento_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_21_compras',
                        'tax_dest_id': 'ri_tax_vat_exento_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_27_compras',
                        'tax_dest_id': 'ri_tax_vat_exento_compras',
                    }),
                ],
            },
            'fiscal_position_template_iva_no_corresponde': {
                'name': 'Compras IVA no corresponde',
                'auto_apply': 1,
                'l10n_ar_afip_responsibility_type_ids': [
                    Command.set([
                        'l10n_ar.res_IVAE',
                        'l10n_ar.res_RM',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_0_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_10_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_21_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_27_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_exento_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                    Command.create({
                        'tax_src_id': 'ri_tax_vat_no_gravado_compras',
                        'tax_dest_id': 'ri_tax_vat_no_corresponde_compras',
                    }),
                ],
            },
        }
