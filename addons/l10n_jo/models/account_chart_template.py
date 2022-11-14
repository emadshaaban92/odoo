from odoo import models


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        """ If JORDAN chart, we add 3 new journals TA, Purchase and Invoice"""
        if self == self.env.ref('l10n_jo.jordan_chart_template_standard'):
            if not journals_dict:
                journals_dict = []
            journals_dict.extend(
                [{"name": "Tax Adjustments", "company_id": company.id, "code": "TA", "type": "general", "sequence": 1,
                  "favorite": True}])
        return super()._prepare_all_journals(acc_template_ref, company, journals_dict=journals_dict)
