# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Requisition Sale Stock',
    'description': "Add relation information between Sale Orders and Alternative Purchase Orders if Make to Order (MTO) is activated on one sold product.",
    'version': '1.0',
    'category': 'Inventory/Purchase',
    'depends': ['purchase_requisition', 'sale_purchase_stock'],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
