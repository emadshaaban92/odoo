# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ar_ex_template_data(self, template_code):
        return {
            'parent_id': 'l10nar_base_chart_template',
            'bank_account_code_prefix': '1.1.1.02.',
            'cash_account_code_prefix': '1.1.1.01.',
            'code_digits': '12',
            'transfer_account_code_prefix': '6.0.00.00.',
        }

    def _get_ar_ex_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ar',
                'account_default_pos_receivable_account_id': 'base_deudores_por_ventas_pos',
                'income_currency_exchange_account_id': 'base_diferencias_de_cambio',
                'expense_currency_exchange_account_id': 'base_diferencias_de_cambio',
            },
        }

    def _get_ar_ex_account_tax(self, template_code):
        return {
            'ri_tax_percepcion_iva_aplicada': {
                'name': 'Percepción IVA Aplicada',
                'description': 'Perc IVA A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iva_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iva_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iva',
            },
            'ri_tax_percepcion_ganancias_aplicada': {
                'name': 'Percepción Ganancias Aplicada',
                'description': 'Perc Ganancias A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_ganancias_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_ganancias_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_ganancias',
            },
            'ri_tax_percepcion_ganancias_sufrida': {
                'name': 'Percepción Ganancias Sufrida',
                'description': 'Perc Ganancias S',
                'sequence': 4,
                'amount_type': 'fixed',
                'amount': 1.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_ganancias_sufrida',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'base_percepcion_ganancias_sufrida',
                    }),
                ],
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_percepcion_ganancias',
            },
            'ri_tax_percepcion_iibb_caba_aplicada': {
                'name': 'Percepción IIBB CABA Aplicada',
                'description': 'Perc IIBB CABA A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_caba_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_caba_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_caba',
            },
            'ri_tax_percepcion_iibb_ba_aplicada': {
                'name': 'Percepción IIBB ARBA Aplicada',
                'description': 'Perc IIBB ARBA A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ba_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ba_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_ba',
            },
            'ri_tax_percepcion_iibb_ca_aplicada': {
                'name': 'Percepción IIBB Catamarca Aplicada',
                'description': 'Perc IIBB Catamarca A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ca_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ca_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_ca',
            },
            'ri_tax_percepcion_iibb_co_aplicada': {
                'name': 'Percepción IIBB Córdoba Aplicada',
                'description': 'Perc IIBB Córdoba A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_co_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_co_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_co',
            },
            'ri_tax_percepcion_iibb_rr_aplicada': {
                'name': 'Percepción IIBB Corrientes Aplicada',
                'description': 'Perc IIBB Corrientes A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_rr_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_rr_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_rr',
            },
            'ri_tax_percepcion_iibb_er_aplicada': {
                'name': 'Percepción IIBB Entre Ríos Aplicada',
                'description': 'Perc IIBB Entre Ríos A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_er_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_er_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_er',
            },
            'ri_tax_percepcion_iibb_ju_aplicada': {
                'name': 'Percepción IIBB Jujuy Aplicada',
                'description': 'Perc IIBB Jujuy A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ju_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ju_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_ju',
            },
            'ri_tax_percepcion_iibb_za_aplicada': {
                'name': 'Percepción IIBB Mendoza Aplicada',
                'description': 'Perc IIBB Mendoza A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_za_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_za_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_za',
            },
            'ri_tax_percepcion_iibb_lr_aplicada': {
                'name': 'Percepción IIBB La Rioja Aplicada',
                'description': 'Perc IIBB La Rioja A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_lr_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_lr_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_lr',
            },
            'ri_tax_percepcion_iibb_sa_aplicada': {
                'name': 'Percepción IIBB Salta Aplicada',
                'description': 'Perc IIBB Salta A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_sa_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_sa_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_sa',
            },
            'ri_tax_percepcion_iibb_nn_aplicada': {
                'name': 'Percepción IIBB San Juan Aplicada',
                'description': 'Perc IIBB San Juan A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_nn_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_nn_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_nn',
            },
            'ri_tax_percepcion_iibb_sl_aplicada': {
                'name': 'Percepción IIBB San Luis Aplicada',
                'description': 'Perc IIBB San Luis A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_sl_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_sl_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_sl',
            },
            'ri_tax_percepcion_iibb_sf_aplicada': {
                'name': 'Percepción IIBB Santa Fe Aplicada',
                'description': 'Perc IIBB Santa Fe A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_sf_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_sf_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_sf',
            },
            'ri_tax_percepcion_iibb_se_aplicada': {
                'name': 'Percepción IIBB Santiago del Estero Aplicada',
                'description': 'Perc IIBB Santiago del Estero A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_se_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_se_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_se',
            },
            'ri_tax_percepcion_iibb_tn_aplicada': {
                'name': 'Percepción IIBB Tucumán Aplicada',
                'description': 'Perc IIBB Tucumán A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_tn_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_tn_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_tn',
            },
            'ri_tax_percepcion_iibb_ha_aplicada': {
                'name': 'Percepción IIBB Chaco Aplicada',
                'description': 'Perc IIBB Chaco A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ha_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ha_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_ha',
            },
            'ri_tax_percepcion_iibb_ct_aplicada': {
                'name': 'Percepción IIBB Chubut Aplicada',
                'description': 'Perc IIBB Chubut A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ct_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ct_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_ct',
            },
            'ri_tax_percepcion_iibb_fo_aplicada': {
                'name': 'Percepción IIBB Formosa Aplicada',
                'description': 'Perc IIBB Formosa A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_fo_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_fo_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_fo',
            },
            'ri_tax_percepcion_iibb_mi_aplicada': {
                'name': 'Percepción IIBB Misiones Aplicada',
                'description': 'Perc IIBB Misiones A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_mi_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_mi_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_mi',
            },
            'ri_tax_percepcion_iibb_ne_aplicada': {
                'name': 'Percepción IIBB Neuquén Aplicada',
                'description': 'Perc IIBB Neuquén A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ne_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_ne_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_ne',
            },
            'ri_tax_percepcion_iibb_lp_aplicada': {
                'name': 'Percepción IIBB La Pampa Aplicada',
                'description': 'Perc IIBB La Pampa A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_lp_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_lp_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_lp',
            },
            'ri_tax_percepcion_iibb_rn_aplicada': {
                'name': 'Percepción IIBB Río Negro Aplicada',
                'description': 'Perc IIBB Río Negro A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_rn_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_rn_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_rn',
            },
            'ri_tax_percepcion_iibb_az_aplicada': {
                'name': 'Percepción IIBB Santa Cruz Aplicada',
                'description': 'Perc IIBB Santa Cruz A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_az_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_az_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_az',
            },
            'ri_tax_percepcion_iibb_tf_aplicada': {
                'name': 'Percepción IIBB Tierra del Fuego Aplicada',
                'description': 'Perc IIBB Tierra del Fuego A',
                'sequence': 4,
                'active': False,
                'amount_type': 'fixed',
                'amount': 0.0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_tf_aplicada',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ri_percepcion_iibb_tf_aplicada',
                    }),
                ],
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_percepcion_iibb_tf',
            },
        }
