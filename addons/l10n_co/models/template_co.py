# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_co_template_data(self, template_code):
        return {
            'bank_account_code_prefix': '1110',
            'cash_account_code_prefix': '1105',
            'transfer_account_code_prefix': '1115',
            'property_account_receivable_id': 'co_puc_130505',
            'property_account_payable_id': 'co_puc_220505',
            'property_account_expense_categ_id': 'co_puc_613595',
            'property_account_income_categ_id': 'co_puc_413595',
        }

    def _get_co_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.co',
                'account_default_pos_receivable_account_id': 'co_puc_130507',
                'income_currency_exchange_account_id': 'co_puc_421020',
                'expense_currency_exchange_account_id': 'co_puc_530525',
                'account_journal_early_pay_discount_loss_account_id': 'co_puc_530535',
                'account_journal_early_pay_discount_gain_account_id': 'co_puc_421040',
            },
        }

    def _get_co_account_tax(self, template_code):
        return {
            'l10n_co_tax_0': {
                'sequence': 1,
                'name': 'IVA Compra 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408100510',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408101010',
                    }),
                ],
            },
            'l10n_co_tax_1': {
                'sequence': 0,
                'name': 'IVA Compra 19%',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408100505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408101005',
                    }),
                ],
            },
            'l10n_co_tax_2': {
                'sequence': 1,
                'name': 'IVA Descontable Compra 16% (2016 y Enero 2017)',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_16',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408100515',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408101015',
                    }),
                ],
            },
            'l10n_co_tax_3': {
                'sequence': 1,
                'name': 'RteFte Salarios y Pagos Laborales',
                'amount': 0.0,
                'amount_type': 'fixed',
                'type_tax_use': 'none',
                'tax_group_id': 'tax_group_r_ren_0',
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
            'l10n_co_tax_4': {
                'sequence': 1,
                'name': 'IVA Devoluciones Ventas 16% 2016',
                'amount': 16.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_16',
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
            'l10n_co_tax_5': {
                'sequence': 1,
                'name': 'IVA Compra Importaciones',
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
            'l10n_co_tax_6': {
                'sequence': 1,
                'name': 'IVA Compra Excluido',
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
            'l10n_co_tax_7': {
                'sequence': 1,
                'name': 'IVA Compra Exento',
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
            'l10n_co_tax_8': {
                'sequence': 0,
                'name': 'IVA Ventas 19%',
                'amount': 19.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_19',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408050505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408051005',
                    }),
                ],
            },
            'l10n_co_tax_9': {
                'sequence': 1,
                'name': 'IVA Ventas 5%',
                'amount': 5.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_iva_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408050510',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_2408051010',
                    }),
                ],
            },
            'l10n_co_tax_10': {
                'sequence': 1,
                'name': 'IVA Excento',
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
            'l10n_co_tax_11': {
                'sequence': 1,
                'name': 'IVA Excluido',
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
            'l10n_co_tax_12': {
                'sequence': 1,
                'name': 'RteIVA 15% sobre el 19% IVA',
                'amount': -2.85,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_iva_285',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236705',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236705',
                    }),
                ],
            },
            'l10n_co_tax_13': {
                'sequence': 1,
                'name': 'RteIVA 15% sobre el 5% IVA',
                'amount': -0.75,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_iva_075',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236705',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236705',
                    }),
                ],
            },
            'l10n_co_tax_14': {
                'sequence': 1,
                'name': 'RteIVA 15% sobre el 5% IVA Contrapartida',
                'amount': 0.75,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_iva_075',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_24082005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_24082005',
                    }),
                ],
            },
            'l10n_co_tax_15': {
                'sequence': 1,
                'name': 'RteIVA 15% sobre el 19% IVA Contrapartida',
                'amount': 2.85,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_iva_285',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_24082005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_24082005',
                    }),
                ],
            },
            'l10n_co_tax_16': {
                'sequence': 1,
                'name': 'RteFte Compra Combustibles 0.1%',
                'amount': -0.1,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_01',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654025',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654025',
                    }),
                ],
            },
            'l10n_co_tax_17': {
                'sequence': 1,
                'name': 'RteFte Compra Cafe 0.5%',
                'amount': -0.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_05',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654020',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654020',
                    }),
                ],
            },
            'l10n_co_tax_18': {
                'sequence': 1,
                'name': 'RteFte Comisiones Persona Natural 10%',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652005',
                    }),
                ],
            },
            'l10n_co_tax_19': {
                'sequence': 1,
                'name': 'RteFte Compras Declarantes 2.5%',
                'amount': -2.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654005',
                    }),
                ],
            },
            'l10n_co_tax_20': {
                'sequence': 1,
                'name': 'RteFte Consultorias, Servicios Tecnicos y Asistencia Tecnica Pagos al Exterior 10%',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23655005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23655005',
                    }),
                ],
            },
            'l10n_co_tax_21': {
                'sequence': 1,
                'name': 'RteFte Adquisicion de Vehiculos 1%',
                'amount': -1.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654030',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654030',
                    }),
                ],
            },
            'l10n_co_tax_22': {
                'sequence': 1,
                'name': 'RteFte Compras de Bienes Raices 1%',
                'amount': -1.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654040',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654040',
                    }),
                ],
            },
            'l10n_co_tax_23': {
                'sequence': 1,
                'name': 'RteFte Servicios P Jurídicas y PN Declarantes 4%',
                'amount': -4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652505',
                    }),
                ],
            },
            'l10n_co_tax_24': {
                'sequence': 1,
                'name': 'RteFte Servicio Transporte Nacional Carga 1%',
                'amount': -1.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_1',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652515',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652515',
                    }),
                ],
            },
            'l10n_co_tax_25': {
                'sequence': 1,
                'name': 'RteFte Servicios en General Personas Naturales No Declarantes Renta 6%',
                'amount': -6.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_6',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652510',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652510',
                    }),
                ],
            },
            'l10n_co_tax_26': {
                'sequence': 1,
                'name': 'RteFte Servicio de Vigilancia y Aseo (Sobre AIU) 2%',
                'amount': -2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652535',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652535',
                    }),
                ],
            },
            'l10n_co_tax_27': {
                'sequence': 1,
                'name': 'RteFte Honorarios Servicios Licencias Software 3.5%',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651515',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651515',
                    }),
                ],
            },
            'l10n_co_tax_28': {
                'sequence': 1,
                'name': 'RteFte Contratos de Obra Inmuebles 2%',
                'amount': -2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652550',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652550',
                    }),
                ],
            },
            'l10n_co_tax_29': {
                'sequence': 1,
                'name': 'RteFte Arrendamientos Bienes Muebles 4%',
                'amount': -4.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_4',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23653005',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23653005',
                    }),
                ],
            },
            'l10n_co_tax_30': {
                'sequence': 1,
                'name': 'RteFte Arrendamientos Bienes Inmuebles 3.5%',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23653010',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23653010',
                    }),
                ],
            },
            'l10n_co_tax_31': {
                'sequence': 1,
                'name': 'RteFte Rendimientos Financieros Generales 7%',
                'amount': -7.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23653510',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23653510',
                    }),
                ],
            },
            'l10n_co_tax_32': {
                'sequence': 1,
                'name': 'RteFte Honorarios Persona Natural 10%',
                'amount': -10.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651505',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651505',
                    }),
                ],
            },
            'l10n_co_tax_33': {
                'sequence': 1,
                'name': 'RteFte Honorarios Diseno Web y Consultoria Informatica 3.5%',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651520',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651520',
                    }),
                ],
            },
            'l10n_co_tax_34': {
                'sequence': 1,
                'name': 'RteFte Adquisicion de Bienes Raices Comerciales 2.5%',
                'amount': -2.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654035',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654035',
                    }),
                ],
            },
            'l10n_co_tax_35': {
                'sequence': 1,
                'name': 'RteFte Compras No Declarantes 3.5%',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654010',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654010',
                    }),
                ],
            },
            'l10n_co_tax_36': {
                'sequence': 1,
                'name': 'RteFte Comisiones Persona Juridica 11%',
                'amount': -11.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_11',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652010',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652010',
                    }),
                ],
            },
            'l10n_co_tax_37': {
                'sequence': 1,
                'name': 'RteFte Compras Bienes Agricolas 1.5%',
                'amount': -1.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654015',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23654015',
                    }),
                ],
            },
            'l10n_co_tax_38': {
                'sequence': 1,
                'name': 'RteFte Servicio Transporte Terrestre Nacional Pasajeros 3.5%',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652520',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652520',
                    }),
                ],
            },
            'l10n_co_tax_39': {
                'sequence': 1,
                'name': 'RteFte Servicio Temporales de Empleo (Sobre AIU) 1%',
                'amount': -1.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_11',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652530',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652530',
                    }),
                ],
            },
            'l10n_co_tax_40': {
                'sequence': 1,
                'name': 'RteFte Honorarios Persona Juridica 11%',
                'amount': -11.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_11',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651510',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23651510',
                    }),
                ],
            },
            'l10n_co_tax_41': {
                'sequence': 1,
                'name': 'RteFte Servicio Integrales de Salud 2%',
                'amount': -2.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_2',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652540',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652540',
                    }),
                ],
            },
            'l10n_co_tax_42': {
                'sequence': 1,
                'name': 'RteFte Servicio de Hoteles y Restaurantes 3.5%',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652545',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_23652545',
                    }),
                ],
            },
            'l10n_co_tax_43': {
                'sequence': 1,
                'name': 'RteICA',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ica_0',
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
            'l10n_co_tax_44': {
                'sequence': 1,
                'name': 'RteICA 0.69%',
                'amount': -0.69,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ica_069',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
            },
            'l10n_co_tax_45': {
                'sequence': 1,
                'name': 'RteICA 1.104%',
                'amount': -1.104,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ica_1104',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
            },
            'l10n_co_tax_46': {
                'sequence': 1,
                'name': 'RteICA 0.414%',
                'amount': -0.414,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ica_0414',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
            },
            'l10n_co_tax_47': {
                'sequence': 1,
                'name': 'RteICA 1.38%',
                'amount': -1.38,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ica_138',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
            },
            'l10n_co_tax_48': {
                'sequence': 1,
                'name': 'RteICA 0.966%',
                'amount': -0.966,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_r_ica_0966',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_236805',
                    }),
                ],
            },
            'l10n_co_tax_49': {
                'sequence': 1,
                'name': 'IVA Compra 19% RC',
                'amount': 19.0,
                'amount_type': 'group',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_19',
                'children_tax_ids': [
                    Command.set([
                        'l10n_co_tax_1',
                        'l10n_co_tax_12',
                    ]),
                ],
            },
            'l10n_co_tax_50': {
                'sequence': 1,
                'name': 'IVA Compra 19% RS',
                'amount': 19.0,
                'amount_type': 'group',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_19',
                'children_tax_ids': [
                    Command.set([
                        'l10n_co_tax_12',
                        'l10n_co_tax_15',
                    ]),
                ],
            },
            'l10n_co_tax_51': {
                'sequence': 1,
                'name': 'IVA Compra 5% RS',
                'amount': 5.0,
                'amount_type': 'group',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_5',
                'children_tax_ids': [
                    Command.set([
                        'l10n_co_tax_13',
                        'l10n_co_tax_14',
                    ]),
                ],
            },
            'l10n_co_tax_52': {
                'sequence': 1,
                'name': 'IVA Compra 5% RC',
                'amount': 5.0,
                'amount_type': 'group',
                'type_tax_use': 'purchase',
                'tax_group_id': 'tax_group_iva_5',
                'children_tax_ids': [
                    Command.set([
                        'l10n_co_tax_0',
                        'l10n_co_tax_13',
                    ]),
                ],
            },
            'l10n_co_tax_53': {
                'sequence': 1,
                'name': 'RteFte -2.50% Ventas',
                'amount': -2.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_r_ren_25',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135515',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135515',
                    }),
                ],
            },
            'l10n_co_tax_54': {
                'sequence': 1,
                'name': 'RteFte -3.50% Ventas',
                'amount': -3.5,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_r_ren_35',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135515',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135515',
                    }),
                ],
            },
            'l10n_co_tax_55': {
                'sequence': 1,
                'name': 'RteIVA 15% sobre el 5% IVA Ventas',
                'amount': -0.75,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_r_iva_075',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135517',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135517',
                    }),
                ],
            },
            'l10n_co_tax_56': {
                'sequence': 1,
                'name': 'RteIVA 15% sobre el 19% IVA Ventas',
                'amount': -2.85,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_r_iva_285',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135517',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135517',
                    }),
                ],
            },
            'l10n_co_tax_57': {
                'sequence': 1,
                'name': 'RteICA 0.414% Ventas',
                'amount': -0.414,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_r_ica_0414',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135518',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135518',
                    }),
                ],
            },
            'l10n_co_tax_58': {
                'sequence': 1,
                'name': 'RteICA 0.966% Ventas',
                'amount': -0.966,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_r_ica_0966',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135518',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'co_puc_135518',
                    }),
                ],
            },
            'l10n_co_tax_covered_goods': {
                'sequence': 1,
                'name': 'Bienes Cubiertos',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'tax_group_id': 'tax_group_covered_goods',
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
        }
