# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from stdnum.it import codicefiscale, iva

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import re


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    l10n_it_pec_email = fields.Char(string="PEC e-mail")
    l10n_it_codice_fiscale = fields.Char(string="Codice Fiscale", size=16)
    l10n_it_pa_index = fields.Char(string="PA index",
        size=7,
        help="Must contain the 6-character (or 7) code, present in the PA\
              Index in the information relative to the electronic invoicing service,\
              associated with the office which, within the addressee administration, deals\
              with receiving (and processing) the invoice.")

    def _l10n_it_edi_in_eu(self):
        self.ensure_one()
        europe = self.env.ref('base.europe', raise_if_not_found=False)
        country = self.country_id
        return not europe or not country or country in europe.country_ids

    def _l10n_it_edi_normalized_vat(self):
        self.ensure_one()
        normalized_vat = self.vat
        if self.vat:
            normalized_vat = self.vat.replace(' ', '')
            in_eu = self._l10n_it_edi_in_eu()
            # If the partner is from the EU, the country-code prefix of the VAT must be taken away
            if in_eu and not normalized_vat[:2].isdecimal():
                normalized_vat = normalized_vat[2:]
            # The Tax Agency arbitrarily decided that non-EU VAT are not interesting,
            # so this default code is used instead
            elif not in_eu:
                normalized_vat = 'OO99999999999'
        elif not self.vat and (not self.country_id or self.country_id.code != 'IT'):
            normalized_vat = '0000000'
        return normalized_vat

    def _l10n_it_edi_normalized_country(self):
        self.ensure_one()
        normalized_country = False
        # Detect the country code from VAT, useful for VAT numbers in EU
        if self.vat:
            if self._l10n_it_edi_in_eu():
                if self.vat[:2].isdecimal():
                    normalized_country = 'IT'
                else:
                    normalized_country = self.vat[:2].upper()
        if not normalized_country:
            # If not found, detect the country code from the partner country instead
            if self.country_id:
                normalized_country = self.country_id.code
            # If it has a codice fiscale (and no country), it's an Italian partner
            elif self.l10n_it_codice_fiscale:
                normalized_country = 'IT'
        return normalized_country

    def _l10n_it_edi_normalized_codice_fiscale(self):
        self.ensure_one()
        return self._l10n_it_normalize_codice_fiscale(self.l10n_it_codice_fiscale)

    def _l10n_it_edi_normalized_pa_index(self):
        self.ensure_one()
        if (self._l10n_it_edi_normalized_country() or '') == 'IT':
            return (self.l10n_it_pa_index or '0000000').upper()
        else:
            return 'XXXXXXX'

    _sql_constraints = [
        ('l10n_it_codice_fiscale',
            "CHECK(l10n_it_codice_fiscale IS NULL OR l10n_it_codice_fiscale = '' OR LENGTH(l10n_it_codice_fiscale) >= 11)",
            "Codice fiscale must have between 11 and 16 characters."),

        ('l10n_it_pa_index',
            "CHECK(l10n_it_pa_index IS NULL OR l10n_it_pa_index = '' OR LENGTH(l10n_it_pa_index) >= 6)",
            "PA index must have between 6 and 7 characters."),
    ]

    @api.model
    def _l10n_it_normalize_codice_fiscale(self, codice):
        if codice and re.match(r'^IT[0-9]{11}$', codice):
            return codice[2:13]
        return codice

    @api.onchange('vat', 'country_id')
    def _l10n_it_onchange_vat(self):
        if not self.l10n_it_codice_fiscale and self.vat and (self.country_id.code == "IT" or self.vat.startswith("IT")):
            self.l10n_it_codice_fiscale = self._l10n_it_normalize_codice_fiscale(self.vat)
        elif self.country_id.code not in [False, "IT"]:
            self.l10n_it_codice_fiscale = ""

    @api.constrains('l10n_it_codice_fiscale')
    def validate_codice_fiscale(self):
        for record in self:
            if record.l10n_it_codice_fiscale and (not codicefiscale.is_valid(record.l10n_it_codice_fiscale) and not iva.is_valid(record.l10n_it_codice_fiscale)):
                raise UserError(_("Invalid Codice Fiscale '%s': should be like 'MRTMTT91D08F205J' for physical person and '12345670546' or 'IT12345670546' for businesses.", record.l10n_it_codice_fiscale))
