# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ma_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'pcg_34211',
            'property_account_payable_id': 'pcg_4411',
            'property_account_income_categ_id': 'pcg_7111',
            'property_account_expense_categ_id': 'pcg_6111',
            'code_digits': '6',
            'bank_account_code_prefix': '5141',
            'cash_account_code_prefix': '5161',
            'transfer_account_code_prefix': '5115',
        }

    def _get_ma_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ma',
                'account_default_pos_receivable_account_id': 'pcg_3489',
                'income_currency_exchange_account_id': 'pcg_733',
                'expense_currency_exchange_account_id': 'pcg_633',
            },
        }

    def _get_ma_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tva_exo': {
                'name': 'Exonere de TVA VENTES',
                'description': 'Exonere de TVA VENTES',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_0',
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
            'tva_exo1': {
                'name': 'Exonere de TVA ACHATS',
                'description': 'Exonere de TVA ACHATS',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_0',
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
            'tva_vt20': {
                'name': 'TVA 20% VENTES',
                'description': 'TVA 20% VENTES',
                'type_tax_use': 'sale',
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+TAUX NORMAL DE 20% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445520',
                        'tag_ids': tags('+TAUX NORMAL DE 20% (TVA exigible)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-TAUX NORMAL DE 20% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445520',
                        'tag_ids': tags('-TAUX NORMAL DE 20% (TVA exigible)'),
                    }),
                ],
            },
            'tva_vt14': {
                'name': 'TVA 14% VENTES',
                'description': 'TVA 14% VENTES',
                'type_tax_use': 'sale',
                'amount': 14.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+TAUX REDUIT DE 14% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445514',
                        'tag_ids': tags('+TAUX REDUIT DE 14% (TVA exigible)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-TAUX REDUIT DE 14% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445514',
                        'tag_ids': tags('-TAUX REDUIT DE 14% (TVA exigible)'),
                    }),
                ],
            },
            'tva_vt10': {
                'name': 'TVA 10% VENTES',
                'description': 'TVA 10% VENTES',
                'type_tax_use': 'sale',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+TAUX REDUIT DE 1O% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445510',
                        'tag_ids': tags('+TAUX REDUIT DE 1O% (TVA exigible)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-TAUX REDUIT DE 1O% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445510',
                        'tag_ids': tags('-TAUX REDUIT DE 1O% (TVA exigible)'),
                    }),
                ],
            },
            'tva_vt07': {
                'name': 'TVA 7% VENTES',
                'description': 'TVA 7% VENTES',
                'type_tax_use': 'sale',
                'amount': 7.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+TAUX REDUIT DE 7% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445507',
                        'tag_ids': tags('+TAUX REDUIT DE 7% (TVA exigible)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-TAUX REDUIT DE 7% (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_445507',
                        'tag_ids': tags('-TAUX REDUIT DE 7% (TVA exigible)'),
                    }),
                ],
            },
            'tva_ac20': {
                'name': 'TVA 20% ACHATS',
                'description': 'TVA 20% ACHATS',
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Achats à l\'importation (20%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455220',
                        'tag_ids': tags('+Achats à l\'importation (20%) (TVA)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Achats à l\'importation (20%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455220',
                        'tag_ids': tags('-Achats à l\'importation (20%) (TVA)'),
                    }),
                ],
            },
            'tva_acim': {
                'name': 'TVA 20% ACHATS (immobilisation)',
                'description': 'TVA 20% ACHATS (immobilisation)',
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_20',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Immobilisations (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_34551',
                        'tag_ids': tags('+Immobilisations (TVA déductible)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Immobilisations (Base HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_34551',
                        'tag_ids': tags('-Immobilisations (TVA déductible)'),
                    }),
                ],
            },
            'tva_ac14': {
                'name': 'TVA 14% ACHATS',
                'description': 'TVA 14% ACHATS',
                'type_tax_use': 'purchase',
                'amount': 14.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_14',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Achats à l\'importation (14%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455214',
                        'tag_ids': tags('+Achats à l\'importation (14%) (TVA)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Achats à l\'importation (14%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455214',
                        'tag_ids': tags('-Achats à l\'importation (14%) (TVA)'),
                    }),
                ],
            },
            'tva_ac10': {
                'name': 'TVA 10% ACHATS',
                'description': 'TVA 10% ACHATS',
                'type_tax_use': 'purchase',
                'amount': 10.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_10',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Achats à l\'importation (10%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455210',
                        'tag_ids': tags('+Achats à l\'importation (10%) (TVA)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Achats à l\'importation (10%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455210',
                        'tag_ids': tags('-Achats à l\'importation (10%) (TVA)'),
                    }),
                ],
            },
            'tva_ac07': {
                'name': 'TVA 7% ACHATS',
                'description': 'TVA 7% ACHATS',
                'type_tax_use': 'purchase',
                'amount': 7.0,
                'amount_type': 'percent',
                'tax_group_id': 'tax_group_tva_7',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Achat à l\'importation (7%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455207',
                        'tag_ids': tags('+Achat à l\'importation (7%) (TVA)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Achat à l\'importation (7%) (HT)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'pcg_3455207',
                        'tag_ids': tags('-Achat à l\'importation (7%) (TVA)'),
                    }),
                ],
            },
        }
