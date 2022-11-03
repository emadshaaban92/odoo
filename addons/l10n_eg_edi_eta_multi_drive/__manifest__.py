# -*- coding: utf-8 -*-
{
    'name': "Egyptian ETA Multi drive",
    'summary': """
            Allow the use of multiple thumb drives for the Egyptian Tax Authority Invoice Integration
        """,
    'description': """
       Allow the use of multiple thumb drives for the Egyptian Tax Authority Invoice Integration
    """,
    'author': 'odoo',
    'website': 'https://www.odoo.com',
    'category': 'account',
    'version': '0.3',
    'license': 'LGPL-3',
    'depends': ['l10n_eg_edi_eta'],
    'data': [
        'views/eta_thumb_drive.xml',
    ],
}
