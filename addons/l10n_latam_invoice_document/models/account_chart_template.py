# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_account_journal(self, template_code):
        """ We add use_documents or not depending on the context"""
        journal_data = super()._get_account_journal(template_code)

        # if chart has localization, then we use documents by default
        if self.env.company._localization_use_documents():
            for vals_journal in journal_data.values():
                if vals_journal['type'] in ['sale', 'purchase']:
                    vals_journal['l10n_latam_use_documents'] = True
        return journal_data
