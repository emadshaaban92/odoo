# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Ireland - Accounting",
    "version": "1.0",
    "category": "Accounting/Localizations/Account Charts",
    "description": """
    This is the base module to manage the accounting for Republic of Ireland in Odoo. 
    """,
    "author": "Odoo SA",
    "depends": [
        "account",
        "base_vat",
    ],
    "data": [
        "data/account_chart_template_data.xml",
        "data/account.account.template.csv",
        "data/account.group.template.csv",
        "data/l10n_ie_chart_data.xml",
        "data/tax_report.xml",
        "data/account_tax_group_data.xml",
        "data/account_tax_template_data.xml",
        "data/account_fiscal_position_template.xml",
        "data/account_chart_template_try_loading.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ],
    "license": "LGPL-3",
}
