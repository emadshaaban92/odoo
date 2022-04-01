# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict

from odoo import SUPERUSER_ID, api
from . import models


def _set_tax_code(env):
    tax_templates_data = defaultdict(lambda x: '01')
    tax_templates_data.update({
        (tax.name, tax.type_tax_use, tax.tax_scope, tax.amount): tax.l10n_es_edi_facturae_tax_type
        for tax in env['account.tax.template'].search([('chart_template_id.country_id', '=', env.ref('base.es').id)])
    })
    for tax in env['account.tax'].with_context(active_test=False).search([('country_id', '=', env.ref('base.es').id)]):
        key = (tax.name, tax.type_tax_use, tax.tax_scope, tax.amount)
        tax.write({'l10n_es_edi_facturae_tax_type': tax_templates_data[key]})


def _l10n_es_edi_facturae_post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _set_tax_code(env)
