# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    l10n_es_edi_facturae_person_type = fields.Char(string='Facturae EDI Person Type Code',
            compute='_compute_l10n_es_edi_facturae_person_type', store=False, readonly=True,)
    l10n_es_edi_facturae_residence_type = fields.Char(string='Facturae EDI Residency Type Code',
            compute='_compute_l10n_es_edi_facturae_residence_type', store=False, readonly=True,)
    l10n_es_edi_facturae_cif_nif_nie = fields.Char(string='Facturae EDI Non-VAT Tax Identifier (CIF/NIF/NIE)')
    l10n_es_edi_facturae_tax_identifier = fields.Char(string='Facturae EDI Tax Identifier',
            compute='_compute_l10n_es_edi_facturae_tax_identifier', store=False, readonly=True,)

    @api.depends('is_company')
    def _compute_l10n_es_edi_facturae_person_type(self):
        for partner in self:
            partner.l10n_es_edi_facturae_person_type = 'J' if partner.is_company else 'F'

    @api.depends('country_id')
    def _compute_l10n_es_edi_facturae_residence_type(self):
        eu_country_ids = self.env['res.country.group'].search([('name', '=', 'European Union')]).country_ids.ids
        for partner in self:
            country = partner.country_id
            if country.code == 'ES':
                partner.l10n_es_edi_facturae_residence_type = 'R'
            elif country.id in eu_country_ids:
                partner.l10n_es_edi_facturae_residence_type = 'U'
            else:
                partner.l10n_es_edi_facturae_residence_type = 'E'

    @api.depends('vat', 'l10n_es_edi_facturae_cif_nif_nie')
    def _compute_l10n_es_edi_facturae_tax_identifier(self):
        for partner in self:
            partner.l10n_es_edi_facturae_tax_identifier = partner.vat or partner.l10n_es_edi_facturae_cif_nif_nie
