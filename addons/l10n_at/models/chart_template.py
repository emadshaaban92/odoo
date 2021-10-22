# -*- coding: utf-8 -*-
from odoo import models


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    # Write paperformat and report template used on company
    def _get_template_data(self, template_code):
        template_data = super()._get_template_data(template_code)
        if template_code == 'at':
            template_data.update({
                'external_report_layout_id': 'l10n_din5008.external_layout_din5008',
                'paperformat_id': 'l10n_din5008.paperformat_euro_din',
            })
        return template_data
