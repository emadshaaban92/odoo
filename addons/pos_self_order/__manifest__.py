# -*- coding: utf-8 -*-
{
    'name': "pos_self_order",

    'summary': """
        Addon for the POS App that allows customers to order from their smartphone or kiosk""",

    'description': """
    
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/index.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'assets': {

        'pos_self_order.assets_self_order': [
            'web/static/tests/legacy/legacy_setup.js',
            'pos_self_order/static/src/**/*',
        ],

    }

}
