# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.http import request


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_template_data(self, template_code):
        """ Set tax calculation rounding method required in Chilean localization"""
        template_data = super()._get_template_data(template_code)
        if template_code == 'cl':
            template_data['tax_calculation_rounding_method'] = 'round_globally'
        return template_data
