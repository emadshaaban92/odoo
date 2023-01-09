from odoo import models, fields
from odoo.tools.misc import format_date


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _l10n_pt_stock_action_check_stock_hash_integrity(self):
        return self.env.ref('l10n_pt_stock.l10n_pt_stock_action_report_stock_hash_integrity').report_action(self.id)

    def _l10n_pt_stock_check_hash_integrity(self):
        stock_pickings = self.env['stock.picking'].search([
            ('state', '=', 'done'),
            ('company_id', '=', self.id),
            ('secure_sequence_number', '!=', 0),
        ])
        result = self.env['report.l10n_pt_stock.report_stock_hash_integrity']._check_hash_integrity(True, stock_pickings, 'date_done')
        return {
            'results': [result],
            'printing_date': format_date(self.env, fields.Date.context_today(self))
        }
