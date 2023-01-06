# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Poland - Accounting',
    'version': '2.0',
    'author': 'Grzegorz Grzelak (OpenGLOBE)',
    'website': 'http://www.openglobe.pl',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
This is the module to manage the accounting chart and taxes for Poland in Odoo.
==================================================================================

To jest moduł do tworzenia wzorcowego planu kont, podatków, obszarów podatkowych i
rejestrów podatkowych. Moduł ustawia też konta do kupna i sprzedaży towarów
zakładając, że wszystkie towary są w obrocie hurtowym.

Niniejszy moduł jest przeznaczony dla odoo 8.0.
Wewnętrzny numer wersji OpenGLOBE 1.02
    """,
    'depends': [
        'account',
        'base_iban',
        'base_vat',
    ],
    'data': [
        'data/res.country.state.csv',
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'post_init_hook': '_preserve_tag_on_taxes',
    'license': 'LGPL-3',
}
