# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ar_base_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'base_deudores_por_ventas',
            'property_account_payable_id': 'base_proveedores',
            'property_account_expense_categ_id': 'base_compra_mercaderia',
            'property_account_income_categ_id': 'base_venta_de_mercaderia',
            'bank_account_code_prefix': '1.1.1.02.',
            'cash_account_code_prefix': '1.1.1.01.',
            'code_digits': '12',
            'transfer_account_code_prefix': '6.0.00.00.',
        }

    def _get_ar_base_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ar',
                'account_default_pos_receivable_account_id': 'base_deudores_por_ventas_pos',
                'income_currency_exchange_account_id': 'base_diferencias_de_cambio',
                'expense_currency_exchange_account_id': 'base_diferencias_de_cambio',
            },
        }

    def _get_ar_base_account_tax(self, template_code):
        return {
            'ri_tax_percepcion_iibb_caba_sufrida': {
                'name': 'Percepción IIBB CABA Sufrida',
                'description': 'Perc IIBB CABA S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_caba_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_caba_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_caba',
            },
            'ri_tax_percepcion_iibb_ba_sufrida': {
                'name': 'Percepción IIBB ARBA Sufrida',
                'description': 'Perc IIBB ARBA S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ba_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ba_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_ba',
            },
            'ri_tax_percepcion_iibb_ca_sufrida': {
                'name': 'Percepción IIBB Catamarca Sufrida',
                'description': 'Perc IIBB Catamarca S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ca_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ca_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_ca',
            },
            'ri_tax_percepcion_iibb_co_sufrida': {
                'name': 'Percepción IIBB Córdoba Sufrida',
                'description': 'Perc IIBB Córdoba S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_co_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_co_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_co',
            },
            'ri_tax_percepcion_iibb_rr_sufrida': {
                'name': 'Percepción IIBB Corrientes Sufrida',
                'description': 'Perc IIBB Corrientes S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_rr_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_rr_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_rr',
            },
            'ri_tax_percepcion_iibb_er_sufrida': {
                'name': 'Percepción IIBB Entre Ríos Sufrida',
                'description': 'Perc IIBB Entre Ríos S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_er_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_er_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_er',
            },
            'ri_tax_percepcion_iibb_ju_sufrida': {
                'name': 'Percepción IIBB Jujuy Sufrida',
                'description': 'Perc IIBB Jujuy S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ju_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ju_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_ju',
            },
            'ri_tax_percepcion_iibb_za_sufrida': {
                'name': 'Percepción IIBB Mendoza Sufrida',
                'description': 'Perc IIBB Mendoza S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_za_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_za_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_za',
            },
            'ri_tax_percepcion_iibb_lr_sufrida': {
                'name': 'Percepción IIBB La Rioja Sufrida',
                'description': 'Perc IIBB La Rioja S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_lr_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_lr_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_lr',
            },
            'ri_tax_percepcion_iibb_sa_sufrida': {
                'name': 'Percepción IIBB Salta Sufrida',
                'description': 'Perc IIBB Salta S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_sa_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_sa_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_sa',
            },
            'ri_tax_percepcion_iibb_nn_sufrida': {
                'name': 'Percepción IIBB San Juan Sufrida',
                'description': 'Perc IIBB San Juan S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_nn_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_nn_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_nn',
            },
            'ri_tax_percepcion_iibb_sl_sufrida': {
                'name': 'Percepción IIBB San Luis Sufrida',
                'description': 'Perc IIBB San Luis S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_sl_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_sl_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_sl',
            },
            'ri_tax_percepcion_iibb_sf_sufrida': {
                'name': 'Percepción IIBB Santa Fe Sufrida',
                'description': 'Perc IIBB Santa Fe S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_sf_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_sf_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_sf',
            },
            'ri_tax_percepcion_iibb_se_sufrida': {
                'name': 'Percepción IIBB Santiago del Estero Sufrida',
                'description': 'Perc IIBB Santiago del Estero S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_se_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_se_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_se',
            },
            'ri_tax_percepcion_iibb_tn_sufrida': {
                'name': 'Percepción IIBB Tucumán Sufrida',
                'description': 'Perc IIBB Tucumán S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_tn_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_tn_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_tn',
            },
            'ri_tax_percepcion_iibb_ha_sufrida': {
                'name': 'Percepción IIBB Chaco Sufrida',
                'description': 'Perc IIBB Chaco S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ha_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ha_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_ha',
            },
            'ri_tax_percepcion_iibb_ct_sufrida': {
                'name': 'Percepción IIBB Chubut Sufrida',
                'description': 'Perc IIBB Chubut S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ct_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ct_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_ct',
            },
            'ri_tax_percepcion_iibb_fo_sufrida': {
                'name': 'Percepción IIBB Formosa Sufrida',
                'description': 'Perc IIBB Formosa S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_fo_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_fo_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_fo',
            },
            'ri_tax_percepcion_iibb_mi_sufrida': {
                'name': 'Percepción IIBB Misiones Sufrida',
                'description': 'Perc IIBB Misiones S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_mi_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_mi_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_mi',
            },
            'ri_tax_percepcion_iibb_ne_sufrida': {
                'name': 'Percepción IIBB Neuquén Sufrida',
                'description': 'Perc IIBB Neuquén S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ne_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_ne_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_ne',
            },
            'ri_tax_percepcion_iibb_lp_sufrida': {
                'name': 'Percepción IIBB La Pampa Sufrida',
                'description': 'Perc IIBB La Pampa S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_lp_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_lp_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_lp',
            },
            'ri_tax_percepcion_iibb_rn_sufrida': {
                'name': 'Percepción IIBB Río Negro Sufrida',
                'description': 'Perc IIBB Río Negro S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_rn_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_rn_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_rn',
            },
            'ri_tax_percepcion_iibb_az_sufrida': {
                'name': 'Percepción IIBB Santa Cruz Sufrida',
                'description': 'Perc IIBB Santa Cruz S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_az_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_az_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_az',
            },
            'ri_tax_percepcion_iibb_tf_sufrida': {
                'name': 'Percepción IIBB Tierra del Fuego Sufrida',
                'description': 'Perc IIBB Tierra del Fuego S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_tf_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_iibb_tf_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_iibb_tf',
            },
        }
