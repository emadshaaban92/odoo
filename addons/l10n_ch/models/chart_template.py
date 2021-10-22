# -*- coding: utf-8 -*-
from odoo import models


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    # Write paperformat and report template used on company
    def _load(self, template_code, company, install_demo):
        res = super()._load(template_code, company, install_demo)
        if template_code == 'ch':
            company.write({
                'external_report_layout_id': self.env.ref('l10n_din5008.external_layout_din5008').id,
                'paperformat_id': self.env.ref('l10n_din5008.paperformat_euro_din').id
            })
        return res
