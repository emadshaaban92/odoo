# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_account_journal(self, template_code):
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'in':
            for journal in journal_data.values():
                if journal.get('code') == 'INV':
                    journal['name'] = _('Tax Invoices')
        return journal_data

    def _get_template_data(self, template_code):
        template_data = super()._get_template_data(template_code)
        if template_code == 'in':
            template_data['fiscalyear_last_month'] = '3'
        return template_data
