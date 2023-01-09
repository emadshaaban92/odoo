# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Portugal - Stock',
    'icon': '/l10n_pt/static/description/icon.png',
    'version': '1.0',
    'description': """Stock module for Portugal which allows hash and QR code on delivery notes""",
    'category': 'Accounting/Localizations/Stock',
    'depends': [
        'stock',
        'base_hash',
        'l10n_pt',
    ],
    'data': [
        'views/l10n_pt_stock_inalterability_menuitem.xml',
        'report/l10n_pt_stock_hash_integrity.xml',
    ],
    'installable': True,
    'auto_install': [
        'stock',
        'l10n_pt'
    ],
    'license': 'LGPL-3',
}
