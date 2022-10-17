# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models
from . import report
from . import populate
from . import wizard

from odoo import api, SUPERUSER_ID

def _post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    companies = env['res.company'].search([])
    country_codes = ['US', 'MM', 'LR']

    if all(c.country_id.code in country_codes for c in companies):
        env['ir.config_parameter'].sudo().set_param('product.weight_in_lbs', '1')
        env['ir.config_parameter'].sudo().set_param('product.volume_in_cubic_feet', '1')
