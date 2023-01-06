# Part of Odoo. See LICENSE file for full copyright and licensing details.
from . import models
from . import report
from . import wizard
from odoo import api, SUPERUSER_ID

def init_settings(env):
    """If the company is localized in Switzerland, activate the cash rounding by default.
    """
    for company in env['res.company'].search([('partner_id.country_id.code', 'in', ['CH', 'LI'])]):
        res_config_id = env['res.config.settings'].create({'company_id': company.id, 'group_cash_rounding': True})
        res_config_id.execute()

def post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    init_settings(env)
