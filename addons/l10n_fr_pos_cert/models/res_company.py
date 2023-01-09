# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields
from odoo.tools.misc import format_date


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_fr_pos_cert_sequence_id = fields.Many2one('ir.sequence')

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company in companies:
            #when creating a new french company, create the securisation sequence as well
            if company._is_accounting_unalterable():
                self.env['hash.mixin']._create_secure_sequence(company, company.id, "l10n_fr_pos_cert_sequence_id")
        return companies

    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        #if country changed to fr, create the securisation sequence
        for company in self:
            if company._is_accounting_unalterable():
                self.env['hash.mixin']._create_secure_sequence(company, company.id, "l10n_fr_pos_cert_sequence_id")
        return res

    def _action_check_pos_hash_integrity(self):
        return self.env.ref('l10n_fr_pos_cert.action_report_pos_hash_integrity').report_action(self.id)

    def _check_pos_hash_integrity(self):
        """Checks that all posted or invoiced pos orders have still the same data as when they were posted
        and raises an error with the result.
        """
        orders = self.env['pos.order'].search([
            ('state', 'in', ['paid', 'done', 'invoiced']),
            ('company_id', '=', self.id),
            ('secure_sequence_number', '!=', 0),
        ])
        result = self.env['report.l10n_fr_pos_cert.report_pos_hash_integrity']._check_hash_integrity(self._is_accounting_unalterable(), orders, 'date_order')
        return {
            'results': [result],
            'printing_date': format_date(self.env, fields.Date.context_today(self))
        }
