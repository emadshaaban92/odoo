# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @api.model
    def _get_account_journal(self, template_code):
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'fr':
            for journal in journal_data.values():
                if journal['type'] in ('sale', 'purchase'):
                    journal.update({'refund_sequence': True})
        return journal_data
