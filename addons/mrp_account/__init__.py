# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from . import models

from odoo import api, SUPERUSER_ID

def _configure_accounts(cr, registry):
    """Setting property field"""
    env = api.Environment(cr, SUPERUSER_ID, {})

    # if we already have a coa installed, create set property field
    company_ids = env['res.company'].search([('chart_template_id', '!=', False)])

    for company_id in company_ids:
        if company_id.property_stock_account_production_cost_id:
            env['ir.property']._set_default(
                'property_stock_account_production_cost_id',
                'product.category',
                company_id.property_stock_account_production_cost_id,
                company_id,
            )
