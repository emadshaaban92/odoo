# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ae_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ae_fiscal_position(template_code),
        }

    def _get_ae_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'uae_account_102011',
            'property_account_payable_id': 'uae_account_201002',
            'property_account_expense_categ_id': 'uae_account_400001',
            'property_account_income_categ_id': 'uae_account_500001',
            'property_tax_payable_account_id': 'uae_account_202003',
            'property_tax_receivable_account_id': 'uae_account_100103',
            'code_digits': '6',
            'bank_account_code_prefix': '101',
            'cash_account_code_prefix': '105',
            'transfer_account_code_prefix': '100',
        }

    def _get_ae_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ae',
                'account_default_pos_receivable_account_id': 'uae_account_102012',
                'income_currency_exchange_account_id': 'uae_account_500011',
                'expense_currency_exchange_account_id': 'uae_account_400053',
                'account_journal_early_pay_discount_loss_account_id': 'uae_account_400071',
                'account_journal_early_pay_discount_gain_account_id': 'uae_account_500014',
            },
        }

    def _get_ae_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'uae_sale_tax_5_dubai': {
                'name': 'VAT 5% (Dubai)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+b. Dubai (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+b. Dubai (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-b. Dubai (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-b. Dubai (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_5_abu_dhabi': {
                'name': 'VAT 5% (Abu Dhabi)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+a. Abu Dhabi (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+a. Abu Dhabi (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-a. Abu Dhabi (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-a. Abu Dhabi (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_5_sharjah': {
                'name': 'VAT 5% (Sharjah)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+c. Sharjah (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+c. Sharjah (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-c. Sharjah (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-c. Sharjah (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_5_ajman': {
                'name': 'VAT 5% (Ajman)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+d. Ajman (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+d. Ajman (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-d. Ajman (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-d. Ajman (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_5_umm_al_quwain': {
                'name': 'VAT 5% (Umm Al Quwain)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+e. Umm Al Quwain (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+e. Umm Al Quwain (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-e. Umm Al Quwain (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-e. Umm Al Quwain (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_5_ras_al_khaima': {
                'name': 'VAT 5% (Ras Al-Khaima)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+f. Ras Al-Khaima (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+f. Ras Al-Khaima (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-f. Ras Al-Khaima (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-f. Ras Al-Khaima (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_5_fujairah': {
                'name': 'VAT 5% (Fujairah)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+g. Fujairah (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+g. Fujairah (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-g. Fujairah (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-g. Fujairah (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_exempted': {
                'name': 'Exempted Tax',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Exempted',
                'tax_group_id': 'ae_tax_group_exempted',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+5. Exempt supplies (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-5. Exempt supplies (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'uae_sale_tax_0': {
                'name': 'VAT 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'VAT 0%',
                'tax_group_id': 'ae_tax_group_0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4. Zero rated supplies (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4. Zero rated supplies (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'uae_export_tax': {
                'name': 'Export Tax 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Export Tax',
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
            'uae_sale_tax_reverse_charge_dubai': {
                'name': 'Reverse Charge Provision (Dubai)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_reverse_charge_abu_dhabi': {
                'name': 'Reverse Charge Provision (Abu Dhabi)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_reverse_charge_sharjah': {
                'name': 'Reverse Charge Provision (Sharjah)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_reverse_charge_ajman': {
                'name': 'Reverse Charge Provision (Ajman)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_reverse_charge_umm_al_quwain': {
                'name': 'Reverse Charge Provision (Umm Al Quwain)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_reverse_charge_ras_al_khaima': {
                'name': 'Reverse Charge Provision (Ras Al-Khaima)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_reverse_charge_fujairah': {
                'name': 'Reverse Charge Provision (Fujairah)',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
            'uae_sale_tax_tourist_refund': {
                'name': 'Tourist Refund scheme 5%',
                'type_tax_use': 'sale',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Tax Refunds provided to Tourists under the Tax Refunds for Tourists Scheme',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+2. Tax Refunds provided to Tourists under the Tax Refunds for Tourists Scheme (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+2. Tax Refunds provided to Tourists under the Tax Refunds for Tourists Scheme (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-2. Tax Refunds provided to Tourists under the Tax Refunds for Tourists Scheme (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-2. Tax Refunds provided to Tourists under the Tax Refunds for Tourists Scheme (Tax)'),
                    }),
                ],
            },
            'uae_purchase_tax_5': {
                'name': 'VAT 5%',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'VAT 5%',
                'tax_group_id': 'ae_tax_group_5',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+10. Standard rated expenses (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+10. Standard rated expenses (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-10. Standard rated expenses (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-10. Standard rated expenses (Tax)'),
                    }),
                ],
            },
            'uae_purchase_tax_exempted': {
                'name': 'Exempted Tax',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Exempted Tax',
                'tax_group_id': 'ae_tax_group_exempted',
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
            'uae_purchase_tax_0': {
                'name': 'VAT 0%',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'VAT 0%',
                'tax_group_id': 'ae_tax_group_0',
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
            'uae_import_tax': {
                'name': 'Import Tax 5%',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Import Tax',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7. Goods imported into the UAE (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+7. Goods imported into the UAE (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7. Goods imported into the UAE (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-7. Goods imported into the UAE (Tax)'),
                    }),
                ],
            },
            'uae_purchase_tax_reverse_charge': {
                'name': 'Reverse Charge Provision',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'description': 'Supplies subject to reverse charge provisions',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Base)', '+3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('+11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('-3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Base)', '-3. Supplies subject to reverse charge provisions (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_104041',
                        'tag_ids': tags('-11. Supplies subject to the reverse charge provisions (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'uae_account_201017',
                        'tag_ids': tags('+3. Supplies subject to reverse charge provisions (Tax)'),
                    }),
                ],
            },
        }

    def _get_ae_fiscal_position(self, template_code):
        return {
            'account_fiscal_position_dubai': {
                'name': 'Dubai',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_du',
                    ]),
                ],
            },
            'account_fiscal_position_abu_dhabi': {
                'name': 'Abu Dhabi',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_az',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_5_abu_dhabi',
                    }),
                ],
            },
            'account_fiscal_position_sharjah': {
                'name': 'Sharjah',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_sh',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_5_sharjah',
                    }),
                ],
            },
            'account_fiscal_position_ajman': {
                'name': 'Ajman',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_aj',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_5_ajman',
                    }),
                ],
            },
            'account_fiscal_position_umm_al_quwain': {
                'name': 'Umm Al Quwain',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_uq',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_5_umm_al_quwain',
                    }),
                ],
            },
            'account_fiscal_position_ras_al_khaima': {
                'name': 'Ras Al-Khaima',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_rk',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_5_ras_al_khaima',
                    }),
                ],
            },
            'account_fiscal_position_fujairah': {
                'name': 'Fujairah',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.ae',
                'state_ids': [
                    Command.set([
                        'base.state_ae_fu',
                    ]),
                ],
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_5_fujairah',
                    }),
                ],
            },
            'account_fiscal_position_non_uae_countries': {
                'name': 'Non-UAE',
                'sequence': 20,
                'auto_apply': 1,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'uae_sale_tax_5_dubai',
                        'tax_dest_id': 'uae_sale_tax_0',
                    }),
                    Command.create({
                        'tax_src_id': 'uae_purchase_tax_5',
                        'tax_dest_id': 'uae_purchase_tax_reverse_charge',
                    }),
                ],
            },
        }
