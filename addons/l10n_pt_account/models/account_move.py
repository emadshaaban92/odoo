# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'l10n_pt.mixin']

    @api.depends('move_type', 'sequence_prefix', 'sequence_number')
    def _compute_l10n_pt_document_number(self):
        for move in self.filtered(lambda m: m.company_id.account_fiscal_country_id.code == 'PT'):
            move.l10n_pt_document_number = f"{move.move_type} {move.sequence_prefix.replace('/', '.', 1)}{str(move.sequence_number)}"

    # Override hash.mixin
    def _get_previous_record_domain(self):
        self.ensure_one()
        if self.company_id.account_fiscal_country_id.code != 'PT':
            return super()._get_previous_record_domain()

        # We should only hash invoices and refunds
        if self.move_type not in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund'):
            return self.env['account.move']

        # Different from account.move because in Portugal the previous record is not the
        # latest posted account.move but the latest posted account.move with the same move_type
        return [
            ('state', '=', 'posted'),
            ('move_type', '=', self.move_type),
            ('company_id', '=', self.company_id.id),
            ('id', '!=', self.id),
            ('secure_sequence_number', '<', self.secure_sequence_number),
            ('secure_sequence_number', '!=', 0)
        ]

    # Override hash.mixin
    def _get_inalterable_hash_fields(self):
        if self.company_id.account_fiscal_country_id.code != 'PT':
            return super()._get_inalterable_hash_fields()
        return 'invoice_date', 'create_date', 'l10n_pt_document_number', 'amount_total'

    # Override hash.mixin
    def _create_hash_string(self, previous_hash=None):
        self.ensure_one()
        if self.company_id.account_fiscal_country_id.code != 'PT':
            return super()._create_hash_string(previous_hash)
        return self._l10n_pt_create_hash_string(self.invoice_date, self.amount_total, previous_hash)
