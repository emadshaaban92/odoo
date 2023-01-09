{
    'name': 'Portugal - Accounting',
    'version': '1.0',
    'author': 'Odoo',
    'icon': '/l10n_pt/static/description/icon.png',
    'category': 'Accounting/Localizations/Account Charts',
    'description': 'Portugal - Accounting',
    'depends': [
        'account',
        'base_vat',
        'l10n_multilang',
        'l10n_pt',
    ],
    'data': [
       'data/l10n_pt_account_chart_data.xml',
       'data/account.account.template.csv',
       'data/account.group.template.csv',
       'data/account_chart_template_data.xml',
       'data/account_tax_group_data.xml',
       'data/account_tax_report.xml',
       'data/account_tax_data.xml',
       'data/account_fiscal_position_template_data.xml',
       'data/account_chart_template_configure_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'installable': True,
    'auto_install': [
        'l10n_pt',
        'account'
    ],
    'license': 'LGPL-3',
}
