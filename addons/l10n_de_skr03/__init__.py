# Part of Odoo. See LICENSE file for full copyright and licensing details.
from . import models
from odoo import api, SUPERUSER_ID

def load_translations(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref('l10n_de_skr03.l10n_de_chart_template').process_coa_translations()
