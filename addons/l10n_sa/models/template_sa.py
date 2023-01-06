# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_sa_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_sa_fiscal_position(template_code),
        }

    def _get_sa_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'sa_account_102011',
            'property_account_payable_id': 'sa_account_201002',
            'property_account_expense_categ_id': 'sa_account_400001',
            'property_account_income_categ_id': 'sa_account_500001',
            'bank_account_code_prefix': '101',
            'cash_account_code_prefix': '105',
            'transfer_account_code_prefix': '100',
            'code_digits': '6',
        }

    def _get_sa_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.sa',
                'account_default_pos_receivable_account_id': 'sa_account_102012',
                'income_currency_exchange_account_id': 'sa_account_400053',
                'expense_currency_exchange_account_id': 'sa_account_500011',
            },
        }

    def _get_sa_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'sa_sales_tax_15': {
                'name': 'Sales Tax 15%',
                'type_tax_use': 'sale',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Sales Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+1. Standard Rates 15% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_201017',
                        'tag_ids': tags('+1. Standard Rates 15% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-1. Standard Rates 15% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_201017',
                        'tag_ids': tags('-1. Standard Rates 15% (Tax)'),
                    }),
                ],
            },
            'sa_local_sales_tax_0': {
                'name': 'Local Sales 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Local Sales 0%',
                'tax_group_id': 'sa_tax_group_taxes_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3. Local Sales Subject to 0% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+3. Local Sales Subject to 0% (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3. Local Sales Subject to 0% (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-3. Local Sales Subject to 0% (Tax)'),
                    }),
                ],
            },
            'sa_export_sales_tax_0': {
                'name': 'Export Sales 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Export Sales 0%',
                'tax_group_id': 'sa_tax_group_taxes_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+4. Export Sales (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+4. Export Sales (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-4. Export Sales (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-4. Export Sales (Tax)'),
                    }),
                ],
            },
            'sa_exempt_sales_tax_0': {
                'name': 'Exempt Sales Tax 0%',
                'type_tax_use': 'sale',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Exempt Sales Tax 0%',
                'tax_group_id': 'sa_tax_group_taxes_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+5. Exempt Sales (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+5. Exempt Sales (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-5. Exempt Sales (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-5. Exempt Sales (Tax)'),
                    }),
                ],
            },
            'sa_purchase_tax_15': {
                'name': 'Purchase Tax 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Purchase Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+7. Standard rated 15% Purchases (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_104041',
                        'tag_ids': tags('+7. Standard rated 15% Purchases (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-7. Standard rated 15% Purchases (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_104041',
                        'tag_ids': tags('-7. Standard rated 15% Purchases (Tax)'),
                    }),
                ],
            },
            'sa_rcp_tax_15': {
                'name': 'Reverse charge provision Tax 15%',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Reverse charge provision Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_15',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+9. Imports subject to reverse charge mechanism (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_104041',
                        'tag_ids': tags('+9. Imports subject to reverse charge mechanism (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-9. Imports subject to reverse charge mechanism (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_104041',
                        'tag_ids': tags('-9. Imports subject to reverse charge mechanism (Tax)'),
                    }),
                ],
            },
            'sa_import_tax_paid_15_paid_to_customs': {
                'name': 'Import tax 15% Paid to customs',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'description': 'Import tax 15% Paid to customs',
                'tax_group_id': 'sa_tax_group_taxes_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+8. Taxable Imports 15% Paid to Customs (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_101060',
                        'tag_ids': tags('+8. Taxable Imports 15% Paid to Customs (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-8. Taxable Imports 15% Paid to Customs (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_101060',
                        'tag_ids': tags('-8. Taxable Imports 15% Paid to Customs (Tax)'),
                    }),
                ],
            },
            'sa_purchases_tax_0': {
                'name': 'Purchases 0%',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Purchases 0%',
                'tax_group_id': 'sa_tax_group_taxes_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+10. Zero Rated Purchases (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+10. Zero Rated Purchases (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-10. Zero Rated Purchases (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-10. Zero Rated Purchases (Tax)'),
                    }),
                ],
            },
            'sa_exempt_purchases_tax': {
                'name': 'Exempt Purchases',
                'type_tax_use': 'purchase',
                'amount': 0.0,
                'amount_type': 'percent',
                'description': 'Exempt Purchases',
                'tax_group_id': 'sa_tax_group_taxes_other',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+11. Exempt Purchases (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+11. Exempt Purchases (Tax)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-11. Exempt Purchases (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-11. Exempt Purchases (Tax)'),
                    }),
                ],
            },
            'sa_withholding_tax_5_rental': {
                'name': 'Withholding Tax 5% (Rental)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Rental) (Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Rental) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Rental) (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Rental) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_tickets_or_air_freight': {
                'name': 'Withholding Tax 5% (Tickets or Air Freight)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Tickets or Air Freight) (Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Tickets or Air Freight) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Tickets or Air Freight) (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Tickets or Air Freight) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_tickets_or_sea_freight': {
                'name': 'Withholding Tax 5% (Tickets or Sea Freight)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Tickets or Sea Freight)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Tickets or Sea Freight)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Tickets or Sea Freight)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Tickets or Sea Freight)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_international_telecommunication': {
                'name': 'Withholding Tax 5% (International Telecommunication)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (International Telecommunication)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (International Telecommunication)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (International Telecommunication)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (International Telecommunication)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_distributed_profits': {
                'name': 'Withholding Tax 5% (Distributed Profits)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Distributed Profits) (Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Distributed Profits) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Distributed Profits) (Tax)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Distributed Profits) (Base)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_consulting_and_technical': {
                'name': 'Withholding Tax 5% (Consulting and Technical)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Consulting and Technical) (Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Consulting and Technical) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Consulting and Technical) (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Consulting and Technical) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_return_from_loans': {
                'name': 'Withholding Tax 5% (Return from Loans)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Return from Loans) (Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Return from Loans) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Return from Loans) (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Return from Loans) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_5_insurance_amd_reinsurance': {
                'name': 'Withholding Tax 5% (Insurance & Reinsurance)',
                'type_tax_use': 'purchase',
                'amount': 5.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 5%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 5% (Insurance & Reinsurance) (Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 5% (Insurance & Reinsurance) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 5% (Insurance & Reinsurance) (Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 5% (Insurance & Reinsurance) (Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_15_royalties': {
                'name': 'Withholding Tax 15% (Royalties)',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 15% (Royalties)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 15% (Royalties)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 15% (Royalties)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 15% (Royalties)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_15_paid_services_from_main_branch': {
                'name': 'Withholding Tax 15% (Paid Services from Main Branch)',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 15% (Paid Services from Main Branch)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 15% (Paid Services from Main Branch)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 15% (Paid Services from Main Branch)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 15% (Paid Services from Main Branch)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_15_paid_services_from_another_branch': {
                'name': 'Withholding Tax 15% (Paid Services from another branch)',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 15% (Paid Services from another branch)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 15% (Paid Services from another branch)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 15% (Paid Services from another branch)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 15% (Paid Services from another branch)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_15_others': {
                'name': 'Withholding Tax 15% (Others)',
                'type_tax_use': 'purchase',
                'amount': 15.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 15%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 15% (Others)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 15% (Others)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 15% (Others)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 15% (Others)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'sa_withholding_tax_20_managerial': {
                'name': 'Withholding Tax 20% (Managerial)',
                'type_tax_use': 'purchase',
                'amount': 20.0,
                'amount_type': 'percent',
                'tax_scope': 'service',
                'description': 'Withholding Tax 20%',
                'tax_group_id': 'sa_tax_group_taxes_withholding',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+Withholding Tax 20% (Managerial)(Base)'),
                    }),
                    Command.create({
                        'account_id': 'sa_account_400073',
                        'repartition_type': 'tax',
                        'tag_ids': tags('+Withholding Tax 20% (Managerial)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-Withholding Tax 20% (Managerial)(Base)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'sa_account_400073',
                        'tag_ids': tags('-Withholding Tax 20% (Managerial)(Tax)'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'account_id': 'sa_account_201020',
                        'repartition_type': 'tax',
                    }),
                ],
            },
        }

    def _get_sa_fiscal_position(self, template_code):
        return {
            'l10n_sa_account_fiscal_position_ksa': {
                'name': 'KSA',
                'auto_apply': 1,
                'sequence': 16,
                'country_id': 'base.sa',
            },
            'l10n_sa_account_fiscal_position_gcc': {
                'name': 'GCC',
                'auto_apply': 1,
                'sequence': 16,
                'country_group_id': 'base.gulf_cooperation_council',
            },
            'l10n_sa_account_fiscal_position_non_gcc': {
                'name': 'Non-GCC',
                'sequence': 16,
            },
        }
