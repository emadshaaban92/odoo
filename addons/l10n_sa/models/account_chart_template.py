# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_account_journal(self, template_code):
        """ If Saudi Arabia chart, we add 3 new journals Tax Adjustments, IFRS 16 and Zakat"""
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'sa':
            journal_data.update({
                "tax_adjustment": {
                    'name': 'Tax Adjustments',
                    'code': 'TA',
                    'type': 'general',
                    'show_on_dashboard': True,
                    'sequence': 1,
                },
                "ifrs16": {
                    'name': 'IFRS 16 Right of Use Asset',
                    'code': 'IFRS',
                    'type': 'general',
                    'show_on_dashboard': True,
                    'sequence': 10,
                },
                "zakat": {
                    'name': 'Zakat',
                    'code': 'ZAKAT',
                    'type': 'general',
                    'show_on_dashboard': True,
                    'sequence': 10,
                }
            })
        return journal_data

    def _get_account_account(self, template_code):
        account_data = super()._get_account_account(template_code)
        if template_code == 'ae':
            for accountxml in [
                "sa_account_100101",
                "sa_account_100102",
                "sa_account_400070",
            ]:
                account_data[accountxml]['allowed_journal_ids'] = [Command.link("ifrs16")]
            for accountxml in [
                "sa_account_201019",
                "sa_account_400072",
            ]:
                account_data[accountxml]['allowed_journal_ids'] = [Command.link("zakat")]
        return account_data
