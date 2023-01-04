# -*- coding: utf-8 -*-

from odoo import models


class AccountMove(models.Model):
    _inherit = ['account.move']

    def _create_document_from_attachment(self, ocr_results, force_write=False):
        moves = super()._create_document_from_attachment(ocr_results, force_write)
        for move in moves:
            if move.move_type == 'in_invoice':
                references = [move.invoice_origin] if move.invoice_origin else []
                move._find_and_set_purchase_orders(references, move.partner_id.id, move.amount_total, timeout=4)
        return moves
