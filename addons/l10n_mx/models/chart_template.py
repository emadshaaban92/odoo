# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, _


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    def _get_account_journal(self, template_code):
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'mx':
            journal_data.update({
                "cbmx": {
                    'type': 'general',
                    'name': _('Effectively Paid'),
                    'code': 'CBMX',
                    'default_account_id': "cuenta118_01",
                    'show_on_dashboard': True,
                },
            })
        return journal_data

    def _get_template_data(self, template_code):
        template_data = super()._get_template_data(template_code)
        if template_code == 'mx':
            template_data['tax_cash_basis_journal_id'] = "cbmx"
        return template_data
