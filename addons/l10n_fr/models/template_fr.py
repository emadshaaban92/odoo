# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_fr_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_fr_fiscal_position(template_code),
            'account.reconcile.model': self._get_fr_reconcile_model(template_code),
        }

    def _get_fr_template_data(self, template_code):
        return {
            'code_digits': 6,
            'bank_account_code_prefix': '512',
            'cash_account_code_prefix': '53',
            'transfer_account_code_prefix': '58',
            'property_account_receivable_id': 'fr_pcg_recv',
            'property_account_payable_id': 'fr_pcg_pay',
            'property_account_expense_categ_id': 'pcg_6071',
            'property_account_income_categ_id': 'pcg_7071',
            'property_tax_payable_account_id': 'pcg_44551',
            'property_tax_receivable_account_id': 'pcg_44567',
        }

    def _get_fr_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.fr',
                'account_default_pos_receivable_account_id': 'fr_pcg_recv_pos',
                'income_currency_exchange_account_id': 'pcg_766',
                'expense_currency_exchange_account_id': 'pcg_666',
                'account_journal_early_pay_discount_loss_account_id': 'pcg_665',
                'account_journal_early_pay_discount_gain_account_id': 'pcg_765',
            },
        }

    def _get_fr_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tva_acq_normale': {
                'name': 'VAT 20%',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 9,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_specifique': {
                'name': 'VAT 8.5%',
                'description': 'VAT 8.5%',
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_intermediaire': {
                'name': 'VAT 10%',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_reduite': {
                'name': 'VAT 5.5%',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_super_reduite': {
                'name': 'VAT 2.1%',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_purchase_good_fuel': {
                'name': 'VAT 20% Fuels',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 9,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 80,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': 20,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 80,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': 20,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_purchase_good_fuel_TTC': {
                'name': 'VAT 20% fuel tax incl.',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 9,
                'price_include': True,
                'include_base_amount': 1,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 80,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': 20,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 80,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': 20,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_acq_normale_TTC': {
                'name': 'VAT 20% tax incl.',
                'description': 'VAT 20%',
                'price_include': True,
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_specifique_TTC': {
                'name': 'VAT 8.5% tax incl.',
                'description': 'VAT 8.5%',
                'price_include': True,
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_intermediaire_TTC': {
                'name': 'VAT 10% tax incl.',
                'description': 'VAT 10%',
                'price_include': True,
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_reduite_TTC': {
                'name': 'VAT 5.5% tax incl.',
                'description': 'VAT 5.5%',
                'price_include': True,
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_super_reduite_TTC': {
                'name': 'VAT 2.1% tax incl.',
                'description': 'VAT 2.1%',
                'price_include': True,
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_imm_normale': {
                'name': 'VAT 20% real estate',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('+19'),
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
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('-19'),
                    }),
                ],
            },
            'tva_imm_specifique': {
                'name': 'VAT 8.5% real estate',
                'description': 'VAT 8.5%',
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('+19'),
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
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('-19'),
                    }),
                ],
            },
            'tva_imm_intermediaire': {
                'name': 'VAT 10% real estate',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('+19'),
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
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('-19'),
                    }),
                ],
            },
            'tva_imm_reduite': {
                'name': 'VAT 5.5% real estate',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('+19'),
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
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('-19'),
                    }),
                ],
            },
            'tva_imm_super_reduite': {
                'name': 'VAT 2.1% real estate',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('+19'),
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
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('-19'),
                    }),
                ],
            },
            'tva_import_outside_eu_20': {
                'name': 'VAT 20% import',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 11,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A4', '+I1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('+20', '+24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('-I1_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A4', '-I1_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('-20', '-24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('+I1_taxe'),
                    }),
                ],
            },
            'tva_import_outside_eu_10': {
                'name': 'VAT 10% import',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 11,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A4', '+I2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('+20', '+24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('-I2_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A4', '-I2_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('-20', '-24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('+I2_taxe'),
                    }),
                ],
            },
            'tva_import_outside_eu_8_5': {
                'name': 'VAT 8.5% import',
                'description': 'VAT 8.5%',
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 11,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A4', '+I3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('+20', '+24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('-I3_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A4', '-I3_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('-20', '-24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('+I3_taxe'),
                    }),
                ],
            },
            'tva_import_outside_eu_5_5': {
                'name': 'VAT 5.5% import',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 11,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A4', '+I4_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('+20', '+24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('-I4_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A4', '-I4_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('-20', '-24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('+I4_taxe'),
                    }),
                ],
            },
            'tva_import_outside_eu_2_1': {
                'name': 'VAT 2.1% import',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 11,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A4', '+I5_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('+20', '+24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('-I5_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A4', '-I5_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('-20', '-24'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4453',
                        'tag_ids': tags('+I5_taxe'),
                    }),
                ],
            },
            'tva_intra_normale_biens': {
                'name': 'VAT 20% EU G',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+B2', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('-08_taxe', '-17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-B2', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('+08_taxe', '+17'),
                    }),
                ],
            },
            'tva_intra_normale_services': {
                'name': 'VAT 20% EU S',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A3', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('-08_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A3', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('+08_taxe'),
                    }),
                ],
            },
            'tva_purchase_service_20_import': {
                'name': 'VAT 20% IMPORT',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+B4', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44531',
                        'tag_ids': tags('-08_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-B4', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445663',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44531',
                        'tag_ids': tags('+08_taxe'),
                    }),
                ],
            },
            'tva_purchase_service_0': {
                'name': 'VAT 0% EXO',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_exigibility': 'on_invoice',
                'cash_basis_transition_account_id': 'pcg_44574',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
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
                    }),
                ],
            },
            'tva_acq_encaissement': {
                'name': 'VAT 20%',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_20',
                'include_base_amount': 1,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_intermediaire_encaissement': {
                'name': 'VAT 10%',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_10',
                'include_base_amount': 1,
                'active': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_encaissement_reduite': {
                'name': 'VAT 5.5%',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_55',
                'include_base_amount': 1,
                'active': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_encaissement_super_reduite': {
                'name': 'VAT 2.1%',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_21',
                'include_base_amount': 1,
                'active': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_encaissement_TTC': {
                'name': 'VAT 20% tax incl.',
                'description': 'VAT 20%',
                'price_include': True,
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_intermediaire_encaissement_TTC': {
                'name': 'VAT 10% tax incl.',
                'description': 'VAT 10%',
                'price_include': True,
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_encaissement_reduite_TTC': {
                'name': 'VAT 5.5% tax incl.',
                'description': 'VAT 5.5%',
                'price_include': True,
                'amount': 5.5,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_acq_encaissement_super_reduite_TTC': {
                'name': 'VAT 2.1% tax incl.',
                'description': 'VAT 2.1%',
                'price_include': True,
                'amount': 2.1,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'active': 0,
                'cash_basis_transition_account_id': 'pcg_44564',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('+20'),
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
                        'account_id': 'pcg_44566',
                        'tag_ids': tags('-20'),
                    }),
                ],
            },
            'tva_purchase_imm_normale': {
                'name': 'VAT 20% real estate',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44564',
                'tax_scope': 'service',
                'tax_group_id': 'tax_group_tva_20',
                'include_base_amount': 1,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('+19'),
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
                        'account_id': 'pcg_44562',
                        'tag_ids': tags('-19'),
                    }),
                ],
            },
            'tva_normale': {
                'name': 'VAT 20%',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+08_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-08_taxe'),
                    }),
                ],
            },
            'tva_intermediaire': {
                'name': 'VAT 10%',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'active': 0,
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+9B_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-9B_taxe'),
                    }),
                ],
            },
            'tva_reduite': {
                'name': 'VAT 5.5%',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'active': 0,
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+09_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-09_taxe'),
                    }),
                ],
            },
            'tva_specifique': {
                'name': 'VAT 8.5%',
                'description': 'VAT 8.5%',
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+10_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-10_taxe'),
                    }),
                ],
            },
            'tva_super_reduite': {
                'name': 'VAT 2.1%',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+11_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-11_taxe'),
                    }),
                ],
            },
            'tva_normale_ttc': {
                'name': 'VAT 20% tax incl.',
                'description': 'VAT 20%',
                'price_include': True,
                'amount': 20.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'tax_group_id': 'tax_group_tva_20',
                'active': 0,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+08_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-08_taxe'),
                    }),
                ],
            },
            'tva_intermediaire_ttc': {
                'name': 'VAT 10% tax incl.',
                'description': 'VAT 10%',
                'price_include': True,
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+9B_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-9B_taxe'),
                    }),
                ],
            },
            'tva_specifique_ttc': {
                'name': 'VAT 8.5% tax incl.',
                'description': 'VAT 8.5%',
                'price_include': True,
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'active': 0,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+10_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-10_taxe'),
                    }),
                ],
            },
            'tva_reduite_ttc': {
                'name': 'VAT 5.5% tax incl.',
                'description': 'VAT 5.5%',
                'price_include': True,
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+09_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-09_taxe'),
                    }),
                ],
            },
            'tva_super_reduite_ttc': {
                'name': 'VAT 2.1% tax incl.',
                'description': 'VAT 2.1%',
                'price_include': True,
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+11_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-11_taxe'),
                    }),
                ],
            },
            'tva_sale_good_0': {
                'name': 'VAT 0% EXO',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_sale_good_export_0': {
                'name': 'VAT 0% EXPORT',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+E1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-E1'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_sale_good_intra_0': {
                'name': 'VAT 0% EU G',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+F2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-F2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_normale_encaissement': {
                'name': 'VAT 20%',
                'description': 'VAT 20%',
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44574',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+08_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-08_taxe'),
                    }),
                ],
            },
            'tva_intermediaire_encaissement': {
                'name': 'VAT 10%',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44574',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'include_base_amount': 1,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+9B_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-9B_taxe'),
                    }),
                ],
            },
            'tva_reduite_encaissement': {
                'name': 'VAT 5.5%',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44574',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+09_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-09_taxe'),
                    }),
                ],
            },
            'tva_super_reduite_encaissement': {
                'name': 'VAT 2.1%',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44574',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+11_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-11_taxe'),
                    }),
                ],
            },
            'tva_normale_encaissement_ttc': {
                'name': 'VAT 20% tax incl.',
                'description': 'VAT 20%',
                'price_include': True,
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_445800',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+08_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-08_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-08_taxe'),
                    }),
                ],
            },
            'tva_intermediaire_encaissement_ttc': {
                'name': 'VAT 10% tax incl.',
                'description': 'VAT 10%',
                'price_include': True,
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_445800',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+9B_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-9B_taxe'),
                    }),
                ],
            },
            'tva_reduite_encaissement_ttc': {
                'name': 'VAT 5.5% tax incl.',
                'description': 'VAT 5.5%',
                'price_include': True,
                'amount': 5.5,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_445800',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+09_taxe'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-09_taxe'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_super_reduite_encaissement_ttc': {
                'name': 'VAT 2.1% tax incl.',
                'description': 'VAT 2.1%',
                'price_include': True,
                'amount': 2.1,
                'amount_type': 'percent',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_445800',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A1', '+11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('+11_taxe'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A1', '-11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44571',
                        'tag_ids': tags('-11_taxe'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_sale_service_0': {
                'name': 'VAT 0% EXO',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44574',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_sale_service_export_0': {
                'name': 'VAT 0% EXPORT',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'cash_basis_transition_account_id': 'pcg_44574',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_sale_service_intra_0': {
                'name': 'VAT 0% EU S',
                'description': 'VAT 0%',
                'amount': 0.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'sale',
                'tax_scope': 'service',
                'tax_exigibility': 'on_payment',
                'cash_basis_transition_account_id': 'pcg_44574',
                'include_base_amount': 1,
                'tax_group_id': 'tax_group_tva_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-E2'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tva_intra_specifique_biens': {
                'name': 'VAT 8.5% EU M',
                'description': 'VAT 8.5%',
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+B2', '+10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('-10_taxe', '-17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-B2', '-10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('+10_taxe', '+17'),
                    }),
                ],
            },
            'tva_intra_specifique_services': {
                'name': 'VAT 8.5% EU S',
                'description': 'VAT 8.5%',
                'amount': 8.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_85',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A3', '+10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+17', '+10_taxe'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('-20'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A3', '-10_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-17', '-10_taxe'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('+20'),
                    }),
                ],
            },
            'tva_intra_intermediaire_biens': {
                'name': 'VAT 10% EU M',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+B2', '+9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('-9B_taxe', '-17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-B2', '-9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('+9B_taxe', '+17'),
                    }),
                ],
            },
            'tva_intra_intermediaire_services': {
                'name': 'VAT 10% EU S',
                'description': 'VAT 10%',
                'amount': 10.0,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A3', '+9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('-9B_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A3', '-9B_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('+9B_taxe'),
                    }),
                ],
            },
            'tva_intra_reduite_biens': {
                'name': 'VAT 5.5% EU M',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+B2', '+09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('-09_taxe', '-17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-B2', '-09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('+09_taxe', '+17'),
                    }),
                ],
            },
            'tva_intra_reduite_services': {
                'name': 'VAT 5.5% EU S',
                'description': 'VAT 5.5%',
                'amount': 5.5,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_55',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A3', '+09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('-09_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A3', '-09_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('+09_taxe'),
                    }),
                ],
            },
            'tva_intra_super_reduite_biens': {
                'name': 'VAT 2.1% EU M',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'consu',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+B2', '+11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('-11_taxe', '-17'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-B2', '-11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_4452',
                        'tag_ids': tags('+11_taxe', '+17'),
                    }),
                ],
            },
            'tva_intra_super_reduite_services': {
                'name': 'VAT 2.1% EU S',
                'description': 'VAT 2.1%',
                'amount': 2.1,
                'amount_type': 'percent',
                'sequence': 10,
                'type_tax_use': 'purchase',
                'tax_scope': 'service',
                'include_base_amount': 1,
                'active': 0,
                'tax_group_id': 'tax_group_tva_21',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('+A3', '+11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('+20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('-11_taxe'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'base',
                        'tag_ids': tags('-A3', '-11_base'),
                    }),
                    Command.create({
                        'factor_percent': 100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445662',
                        'tag_ids': tags('-20'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'pcg_44521',
                        'tag_ids': tags('+11_taxe'),
                    }),
                ],
            },
        }

    def _get_fr_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_domestic': {
                'sequence': 1,
                'name': 'Domestic - France',
                'auto_apply': 1,
                'vat_required': 1,
                'country_id': 'base.fr',
            },
            'fiscal_position_template_intraeub2c': {
                'sequence': 2,
                'name': 'EU private',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_intraeub2b': {
                'sequence': 3,
                'name': 'Intra-EU B2B',
                'auto_apply': 1,
                'country_group_id': 'base.europe',
                'vat_required': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tva_normale',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_normale_ttc',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire_encaissement',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_normale_encaissement',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_normale_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_specifique',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_specifique_ttc',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire_ttc',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite_ttc',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite_encaissement',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite_ttc',
                        'tax_dest_id': 'tva_sale_good_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite_encaissement',
                        'tax_dest_id': 'tva_sale_service_intra_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_normale',
                        'tax_dest_id': 'tva_intra_normale_biens',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_specifique',
                        'tax_dest_id': 'tva_intra_specifique_biens',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_encaissement',
                        'tax_dest_id': 'tva_intra_normale_services',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_intermediaire_encaissement',
                        'tax_dest_id': 'tva_intra_intermediaire_services',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_intermediaire',
                        'tax_dest_id': 'tva_intra_intermediaire_biens',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_reduite',
                        'tax_dest_id': 'tva_intra_reduite_biens',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_encaissement_reduite',
                        'tax_dest_id': 'tva_intra_reduite_services',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_super_reduite',
                        'tax_dest_id': 'tva_intra_super_reduite_biens',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_encaissement_super_reduite',
                        'tax_dest_id': 'tva_intra_super_reduite_services',
                    }),
                ],
            },
            'fiscal_position_template_import_export': {
                'sequence': 50,
                'name': 'Import/Export Outside Europe + DOM-TOM',
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tva_normale',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_normale_ttc',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_normale_encaissement',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire_encaissement',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_normale_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_specifique',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_specifique_ttc',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_intermediaire_ttc',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite_ttc',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_reduite_encaissement',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite_ttc',
                        'tax_dest_id': 'tva_sale_good_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite_encaissement_ttc',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_super_reduite_encaissement',
                        'tax_dest_id': 'tva_sale_service_export_0',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_normale',
                        'tax_dest_id': 'tva_import_outside_eu_20',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_specifique',
                        'tax_dest_id': 'tva_import_outside_eu_8_5',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_intermediaire',
                        'tax_dest_id': 'tva_import_outside_eu_10',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_reduite',
                        'tax_dest_id': 'tva_import_outside_eu_5_5',
                    }),
                    Command.create({
                        'tax_src_id': 'tva_acq_super_reduite',
                        'tax_dest_id': 'tva_import_outside_eu_2_1',
                    }),
                ],
            },
        }

    def _get_fr_reconcile_model(self, template_code):
        return {
            'bank_charges_reconcile_model': {
                'name': 'Bank fees',
                'line_ids': [
                    Command.create({
                        'account_id': 'pcg_6278',
                        'amount_type': 'percentage',
                        'amount_string': '100',
                    }),
                ],
            },
        }
