# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    l10n_es_edi_facturae_person_type = fields.Char(string='Facturae EDI Person Type Code', size=1,
                                               compute='_compute_l10n_es_edi_facturae_person_type', store=False, readonly=True)
    l10n_es_edi_facturae_residence_type = fields.Char(string='Facturae EDI Residency Type Code', related='partner_id.l10n_es_edi_facturae_residence_type')
    l10n_es_edi_facturae_cif_nif_nie = fields.Char(string='Facturae EDI Non-VAT Tax Identifier (CIF/NIF/NIE)')
    l10n_es_edi_facturae_tax_identifier = fields.Char(string='Facturae EDI Tax Identifier',
                                                  compute='_compute_l10n_es_edi_facturae_tax_identifier', store=False, readonly=True)
    l10n_es_edi_facturae_certificate_id = fields.One2many(string='Facturae EDI signing certificate',
                                                      comodel_name='l10n_es_edi_facturae.certificate', inverse_name='company_id')

    def _compute_l10n_es_edi_facturae_person_type(self):
        for company in self:
            company.l10n_es_edi_facturae_person_type = 'J'

    @api.depends('vat', 'l10n_es_edi_facturae_cif_nif_nie')
    def _compute_l10n_es_edi_facturae_tax_identifier(self):
        for company in self:
            company.l10n_es_edi_facturae_tax_identifier = company.vat or company.l10n_es_edi_facturae_cif_nif_nie
