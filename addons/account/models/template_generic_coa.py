from odoo import Command, _, models


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    def _get_generic_coa_template_data(self, template_code):
        return {
            'anglo_saxon_accounting': True,
            'bank_account_code_prefix': '1014',
            'cash_account_code_prefix': '1015',
            'transfer_account_code_prefix': '1017',
            'default_pos_receivable_account_id': 'pos_receivable',
            'property_account_receivable_id': 'receivable',
            'property_account_payable_id': 'payable',
            'property_account_expense_id': 'expense',
            'property_account_income_id': 'income',
            'property_account_expense_categ_id': 'expense',
            'property_account_income_categ_id': 'income',
            'property_tax_payable_account_id': 'tax_payable',
            'property_tax_receivable_account_id': 'tax_receivable',
            'property_stock_account_input_categ_id': 'stock_in',
            'property_stock_account_output_categ_id': 'stock_out',
            'property_stock_valuation_account_id': 'stock_valuation',
        }

    def _get_generic_coa_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.us',
                'account_default_pos_receivable_account_id': 'pos_receivable',
                'income_currency_exchange_account_id': 'income_currency_exchange',
                'expense_currency_exchange_account_id': 'expense_currency_exchange',
                'default_cash_difference_income_account_id': 'cash_diff_income',
                'default_cash_difference_expense_account_id': 'cash_diff_expense',
                'account_journal_early_pay_discount_loss_account_id': 'cash_discount_loss',
                'account_journal_early_pay_discount_gain_account_id': 'cash_discount_gain',
                # TODO only MX ?? -- 'account_cash_basis_base_account_id': f'',
            }
        }

    def _get_generic_coa_account_tax(self, template_code):
        tax_repartition_lines = [
            Command.create({
                'factor_percent': 100,
                'repartition_type': 'base',
            }),
            Command.create({
                'factor_percent': 100,
                'repartition_type': 'tax',
                'account_id': 'tax_received',
            }),
        ]
        return {
            f"{kind}_tax_template": {
                "name": name,
                "amount": 15,
                "type_tax_use": kind,
                "tax_group_id": 'tax_group_15',
                "invoice_repartition_line_ids": tax_repartition_lines,
                "refund_repartition_line_ids": tax_repartition_lines.copy(),
            } for kind, name in (
                ('sale', _('Tax 15%')),
                ('purchase', _('Purchase Tax 15%'))
            )
        }
