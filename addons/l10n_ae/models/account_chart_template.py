# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_account_journal(self, template_code):
        """ If UAE chart, we add 2 new journals TA and IFRS"""
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'ae':
            journal_data.update({
                "tax_adjustment":{
                    "name": "Tax Adjustments",
                    "code": "TA",
                    "type": "general",
                    "show_on_dashboard": True,
                    "sequence": 1,
                },
                "ifrs16": {
                    "name": "IFRS 16",
                    "code": "IFRS",
                    "type": "general",
                    "show_on_dashboard": True,
                    "sequence": 10,
                }
            })
        return journal_data

    def _get_account_account(self, template_code):
        account_data = super()._get_account_account(template_code)
        if template_code == 'ae':
            for accountxml in [
                "uae_account_100101",
                "uae_account_100102",
                "uae_account_400070",
            ]:
                account_data[accountxml]['allowed_journal_ids'] = [Command.link("ifrs16")]
        return account_data
