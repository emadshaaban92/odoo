# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_pe_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_pe_fiscal_position(template_code),
        }

    def _get_pe_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'chart1213',
            'property_account_payable_id': 'chart4212',
            'property_account_expense_categ_id': 'chart6329',
            'property_account_expense_id': 'chart6011',
            'property_account_income_categ_id': 'chart70121',
            'property_stock_account_input_categ_id': 'chart6111',
            'property_stock_account_output_categ_id': 'chart69111',
            'property_stock_valuation_account_id': 'chart20111',
            'bank_account_code_prefix': '1041',
            'cash_account_code_prefix': '1031',
            'transfer_account_code_prefix': '1051',
            'code_digits': '7',
        }

    def _get_pe_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.pe',
                'account_default_pos_receivable_account_id': 'chart1215',
                'income_currency_exchange_account_id': 'chart676',
                'expense_currency_exchange_account_id': 'chart776',
                'account_journal_early_pay_discount_loss_account_id': 'chart675',
                'account_journal_early_pay_discount_gain_account_id': 'chart775',
            },
        }

    def _get_pe_account_tax(self, template_code):
        return {
            'sale_tax_igv_18': {
                'name': '18%',
                'description': 'IGV',
                'l10n_pe_edi_tax_code': '1000',
                'l10n_pe_edi_unece_category': 'S',
                'amount': 18.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_igv',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'sale_tax_igv_18_included': {
                'name': '18% (Included in price)',
                'description': 'IGV',
                'l10n_pe_edi_tax_code': '1000',
                'l10n_pe_edi_unece_category': 'S',
                'amount': 18.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'price_include': True,
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_igv',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'sale_tax_exo': {
                'name': '0% Exonerated',
                'description': 'EXO',
                'l10n_pe_edi_tax_code': '9997',
                'l10n_pe_edi_unece_category': 'E',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'tax_group_id': 'tax_group_exo',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'sale_tax_ina': {
                'name': '0% Unaffected',
                'description': 'INA',
                'l10n_pe_edi_tax_code': '9998',
                'l10n_pe_edi_unece_category': 'Z',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'tax_group_id': 'tax_group_ina',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'sale_tax_gra': {
                'name': '0% Free',
                'description': 'GRA',
                'l10n_pe_edi_tax_code': '9996',
                'l10n_pe_edi_unece_category': 'E',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'tax_group_id': 'tax_group_gra',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'sale_tax_ics_0': {
                'name': '0% ISC',
                'description': 'ISC',
                'l10n_pe_edi_tax_code': '2000',
                'l10n_pe_edi_unece_category': 'S',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_isc',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart4012',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'chart4012',
                    }),
                ],
            },
            'purchase_tax_igv_18': {
                'name': '18%',
                'description': 'IGV',
                'l10n_pe_edi_tax_code': '1000',
                'l10n_pe_edi_unece_category': 'S',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'sequence': 1,
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_igv',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'purchase_tax_igv_18_included': {
                'name': '18% (Included in price)',
                'description': 'IGV',
                'l10n_pe_edi_tax_code': '1000',
                'l10n_pe_edi_unece_category': 'S',
                'amount': 18.0,
                'type_tax_use': 'purchase',
                'sequence': 1,
                'price_include': True,
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_igv',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'purchase_tax_exo': {
                'name': '0% Exonerated',
                'description': 'EXO',
                'l10n_pe_edi_tax_code': '9997',
                'l10n_pe_edi_unece_category': 'E',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'sequence': 1,
                'tax_group_id': 'tax_group_exo',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'purchase_tax_ina': {
                'name': '0% Unaffected',
                'description': 'INA',
                'l10n_pe_edi_tax_code': '9998',
                'l10n_pe_edi_unece_category': 'Z',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'sequence': 1,
                'tax_group_id': 'tax_group_ina',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'purchase_tax_gra': {
                'name': '0% Free',
                'description': 'GRA',
                'l10n_pe_edi_tax_code': '9996',
                'l10n_pe_edi_unece_category': 'E',
                'amount': 0.0,
                'type_tax_use': 'purchase',
                'sequence': 1,
                'tax_group_id': 'tax_group_gra',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
            'sale_tax_exp': {
                'name': '0% EXP',
                'description': 'EXP',
                'l10n_pe_edi_tax_code': '9995',
                'l10n_pe_edi_unece_category': 'S',
                'amount': 0.0,
                'type_tax_use': 'sale',
                'sequence': 1,
                'include_base_amount': '1',
                'tax_group_id': 'tax_group_exp',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 0,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 0,
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 0,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 0,
                        'repartition_type': 'tax',
                        'account_id': 'chart40111',
                    }),
                ],
            },
        }

    def _get_pe_fiscal_position(self, template_code):
        return {
            'local_peru': {
                'name': 'LOCAL PERU',
                'auto_apply': 1,
                'country_id': 'base.pe',
                'sequence': 15,
            },
            'exportation': {
                'name': 'FOREIGN - EXPORT',
                'auto_apply': 1,
                'sequence': 10,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'sale_tax_igv_18',
                        'tax_dest_id': 'sale_tax_exp',
                    }),
                    Command.create({
                        'tax_src_id': 'sale_tax_igv_18_included',
                        'tax_dest_id': 'sale_tax_exp',
                    }),
                ],
            },
        }
