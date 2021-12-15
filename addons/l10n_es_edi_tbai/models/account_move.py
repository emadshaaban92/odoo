# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import io
import zipfile
from datetime import datetime
from re import sub as regex_sub

from lxml import etree
from odoo import api, fields, models
from pytz import timezone

from .crc8 import l10n_es_tbai_crc8


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Stored fields
    l10n_es_tbai_is_required = fields.Boolean(
        string="Is the Bask EDI (TicketBai) needed",
        compute='_compute_l10n_es_tbai_is_required',
        store=True
    )

    # Non-stored fields (TODO registration date needed to find last posted invoice -> store=True ?) (do not mix store=True and store=False in same compute)
    l10n_es_tbai_sequence = fields.Char(string="TicketBai sequence", compute="_compute_l10n_es_tbai_sequence")
    l10n_es_tbai_number = fields.Char(string="TicketBai number", compute="_compute_l10n_es_tbai_number")
    l10n_es_tbai_id = fields.Char(string="TicketBai ID", compute="_compute_l10n_es_tbai_id")
    l10n_es_tbai_signature = fields.Char(string="Signature value of XML", compute="_compute_l10n_es_tbai_values")
    l10n_es_tbai_registration_date = fields.Date(
        string="Registration Date",
        help="Technical field to keep the date the invoice was sent the first time as the date the invoice was "
             "registered into the system.",
        compute="_compute_l10n_es_tbai_values"
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('move_type', 'company_id')
    def _compute_l10n_es_tbai_is_required(self):
        for move in self:
            move.l10n_es_tbai_is_required = move.is_sale_document() \
                and move.country_code == 'ES' \
                and move.company_id.l10n_es_tbai_tax_agency

    @api.depends('l10n_es_tbai_is_required')
    def _compute_edi_show_cancel_button(self):
        # OVERRIDE
        super()._compute_edi_show_cancel_button()
        for move in self.filtered('l10n_es_tbai_is_required'):
            move.edi_show_cancel_button = False

    @api.depends('company_id', 'state')
    def _compute_l10n_es_tbai_id(self):
        for record in self:
            if record.l10n_es_tbai_is_required:
                company = record.company_id
                edi_format = self.env['account.edi.format'].search([('code', '=', 'es_tbai')])
                inv_xml = edi_format._l10n_es_tbai_get_invoice_xml(record)
                signature = edi_format._l10n_es_tbai_sign_invoice(record, inv_xml)
                tbai_id_no_crc = '-'.join([
                    'TBAI',
                    str(company.vat[2:] if company.vat.startswith('ES') else company.vat),
                    datetime.strftime(datetime.now(tz=timezone('Europe/Madrid')), '%d%m%y'),  # TODO needs to match FechaExpedicion and TBAI_ID date
                    signature[:13],
                    ''  # CRC
                ])
                record.l10n_es_tbai_id = tbai_id_no_crc + l10n_es_tbai_crc8(tbai_id_no_crc)
            else:
                record.l10n_es_tbai_id = ''  # record

    def _get_l10n_es_tbai_values_from_zip(self, xpaths, response=False):
        for doc in self.edi_document_ids.filtered(lambda d: d.edi_format_id.code == 'es_tbai'):
            if not doc.attachment_id:
                print("ZIP: NO ATTACHMENT")
                return None
            zip = io.BytesIO(doc.attachment_id.with_context(bin_size=False).raw)  # TODO investigate with_context(bin_size)
            try:
                with zipfile.ZipFile(zip, 'r', compression=zipfile.ZIP_DEFLATED) as zipf:
                    for file in zipf.infolist():
                        if file.filename.endswith('_response.xml') == response:
                            xml = etree.fromstring(zipf.read(file))
                            res = {}
                            for key, value in xpaths.items():
                                res[key] = xml.find(value).text
                            return res
            except zipfile.BadZipFile:
                print("ZIP: BAD FILE")
                return None

    @api.depends('edi_document_ids.attachment_id.raw')
    def _compute_l10n_es_tbai_values(self):
        for record in self:

            vals_response = record._get_l10n_es_tbai_values_from_zip({
                'tbai_id': r'.//IdentificadorTBAI'
            }, response=True)
            print("V1:", vals_response)
            vals = record._get_l10n_es_tbai_values_from_zip({
                'signature': r'.//{http://www.w3.org/2000/09/xmldsig#}SignatureValue',
                'registration_date': r'.//CabeceraFactura//FechaExpedicionFactura'
            })
            print("V2:", vals)
            if not (vals or vals_response):
                record.l10n_es_tbai_signature = ''
                record.l10n_es_tbai_registration_date = None
            else:
                record.l10n_es_tbai_signature = vals['signature']
                record.l10n_es_tbai_registration_date = datetime.strptime(vals['registration_date'], '%d-%m-%Y').replace(tzinfo=timezone('Europe/Madrid'))

    @api.depends('name')
    def _compute_l10n_es_tbai_sequence(self):
        for record in self:
            sequence, _ = record.name.rsplit('/', 1)
            sequence = regex_sub(r"[^0-9A-Za-z.\_\-\/]", "", sequence)  # remove forbidden characters
            sequence = regex_sub(r"[\s]+", " ", sequence)  # no more than once consecutive whitespace allowed
            # TODO (optional) issue warning if sequence uses chars out of ([0123456789ABCDEFGHJKLMNPQRSTUVXYZ.\_\-\/ ])
            print("Sequence: ", sequence)
            record.write({'l10n_es_tbai_sequence': sequence + "TEST"})  # TODO use journal sequences

    @api.depends('name')
    def _compute_l10n_es_tbai_number(self):
        for record in self:
            _, number = record.name.rsplit('/', 1)
            number = regex_sub(r"[^0-9]", "", number)  # remove non-decimal characters
            record.write({'l10n_es_tbai_number': number})
