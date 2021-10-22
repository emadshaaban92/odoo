# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    # TODO move to template_it.py
    def _get_it_res_company(self, template_code):
        company_vals = super()._get_it_res_company(template_code)
        for vals in company_vals.values():
            vals['tax_calculation_rounding_method'] = 'round_globally'
        return company_vals
