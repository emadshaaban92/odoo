# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    def _get_account_journal(self, template_code):
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'kz':
            journal_data['cash']['default_account_id'] = 'kz1010'
            journal_data['bank']['default_account_id'] = 'kz1030'
        return journal_data
