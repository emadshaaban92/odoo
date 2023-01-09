from odoo import api, _, models
from odoo.exceptions import UserError


class ReportL10nPtStockHashIntegrity(models.AbstractModel):
    _name = 'report.l10n_pt_stock.report_stock_hash_integrity'
    _inherit = 'report.base_hash.report_hash_integrity'
    _description = 'Get Portuguese stock hash integrity result as PDF.'

    @api.model
    def _get_report_values(self, docids, data=None):
        if self.env.company.country_id != self.env.ref('base.pt'):
            raise UserError(_('This report is only available for Portuguese companies.'))
        if data:
            data.update(self.env.company._l10n_pt_stock_check_hash_integrity())
        else:
            data = self.env.company._l10n_pt_stock_check_hash_integrity()
        return {
            'doc_ids': docids,
            'doc_model': self.env['res.company'],
            'data': data,
            'docs': self.env['res.company'].browse(self.env.company.id),
        }
