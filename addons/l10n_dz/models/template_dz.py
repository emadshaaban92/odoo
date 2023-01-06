# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_dz_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_dz_fiscal_position(template_code),
        }

    def _get_dz_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'dz_pcg_recv',
            'property_account_payable_id': 'dz_pcg_pay',
            'property_account_expense_categ_id': 'pcg_6001',
            'property_account_income_categ_id': 'pcg_7001',
            'code_digits': 6,
            'bank_account_code_prefix': '512',
            'cash_account_code_prefix': '53',
            'transfer_account_code_prefix': '58',
        }

    def _get_dz_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.dz',
                'account_default_pos_receivable_account_id': 'dz_pcg_recv_pos',
                'income_currency_exchange_account_id': 'pcg_766',
                'expense_currency_exchange_account_id': 'pcg_666',
            },
        }

    def _get_dz_account_tax(self, template_code):
        return {
            'tva_acq_normale19': {
                'name': 'TVA (achat) 19,0%',
                'description': 'ACH-19.0',
                'amount': 19.0,
                'amount_type': 'percent',
                'sequence': 9,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                    }),
                ],
            },
            'tva_normale19': {
                'name': 'TVA (vente) 19,0%',
                'description': '19.0',
                'amount': 19.0,
                'amount_type': 'percent',
                'sequence': 9,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                    }),
                ],
            },
            'tva_acq_specifique9': {
                'name': 'TVA (achat) 9,0%',
                'description': 'ACH-9.0',
                'amount': 9.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                    }),
                ],
            },
            'tva_specifique9': {
                'name': 'TVA (vente) 9,0%',
                'description': '9.0',
                'amount': 9.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                    }),
                ],
            },
            'tva_imm_normale19': {
                'name': 'TVA immobilisation (achat) 19,0%',
                'description': 'IMMO-19.0',
                'amount': 19.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                    }),
                ],
            },
            'tva_imm_specifique9': {
                'name': 'TVA immobilisation (achat) 9,0%',
                'description': 'IMMO-9.0',
                'amount': 9.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                    }),
                ],
            },
            'tva_exo_0': {
                'name': 'TVA 0% EXO (achat)',
                'description': 'ACHAT-0',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
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
            'tva_purchase_0': {
                'name': 'TVA 0% (achat)',
                'description': 'ACHAT-0',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
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
            'tva_0': {
                'name': 'TVA 0% (vente)',
                'description': 'EXO-0',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
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
            'tva_export_0': {
                'name': 'TVA 0% export (vente)',
                'description': 'EXPORT-0',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
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
            'tva_import_0': {
                'name': 'TVA 0% import (achat)',
                'description': 'IMPORT-0',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
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

    def _get_dz_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_national': {
                'sequence': 1,
                'name': 'Régime National',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.dz',
            },
            'fiscal_position_template_exo': {
                'name': 'EXO',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tva_normale19',
                        'tax_dest_id': 'tva_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_specifique9',
                        'tax_dest_id': 'tva_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_normale19',
                        'tax_dest_id': 'tva_exo_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_specifique9',
                        'tax_dest_id': 'tva_exo_0',
                    }),
                ],
            },
            'fiscal_position_template_import_export': {
                'name': 'Import/Export',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tva_normale19',
                        'tax_dest_id': 'tva_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_specifique9',
                        'tax_dest_id': 'tva_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_normale19',
                        'tax_dest_id': 'tva_import_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_specifique9',
                        'tax_dest_id': 'tva_import_0',
                    }),
                ],
            },
        }
