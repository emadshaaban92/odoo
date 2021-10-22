from odoo import models


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_account_journal(self, template_code):
        """ If EGYPT chart, we add 2 new journals TA and IFRS"""
        journal_data = super()._get_account_journal(template_code)
        if template_code == 'eg':
            journal_data.update({
                "tax_adjustment": {
                    "name": "Tax Adjustments",
                    "code": "TA",
                    "type": "general",
                    "sequence": 1,
                    "show_on_dashboard": True,
                },
                "ifrs": {
                    "name": "IFRS 16",
                    "code": "IFRS",
                    "type": "general",
                    "show_on_dashboard": True,
                    "sequence": 10,
                }
            })
        return journal_data
