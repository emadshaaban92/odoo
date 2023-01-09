# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools import float_repr


class L10nPtMixin(models.AbstractModel):
    _name = 'l10n_pt.mixin'
    _description = "Portugal Mixin - Contains common things between Portuguese apps"

    l10n_pt_document_number = fields.Char(string='Document number', compute='_compute_l10n_pt_document_number', store=True)

    def _compute_l10n_pt_document_number(self):
        raise NotImplementedError("'_compute_l10n_pt_document_number' must be overriden by the inheriting class"
                                  "that uses the following '_l10n_pt_create_hash_string' method")

    def _l10n_pt_create_hash_string(self, date, gross_total, previous_hash=None):
        self.ensure_one()
        date = date.strftime('%Y-%m-%d')
        system_entry_date = self.create_date.strftime("%Y-%m-%dT%H:%M:%S")
        gross_total = float_repr(gross_total, 2)
        if previous_hash is None:
            previous_hash = self._get_previous_hash()
        message = f"{date};{system_entry_date};{self.l10n_pt_document_number};{gross_total};{previous_hash}"
        return self._l10n_pt_generate_hash_from_message(message)

    def _l10n_pt_generate_hash_from_message(self, message):
        """
        This method's purpose is only to test that the hash is correctly
        computed as we have multilple hash chains: one per move_type.
        In each chain, we simply add one 1 to the previous hash value of that chain.
        This method will be overriden in SaaS which will provide the real hash
        """
        self.ensure_one()
        hash_string = int(message[message.rfind(';')+1:]) + 1 if message[-1].isdigit() else 0
        return str(hash_string)
