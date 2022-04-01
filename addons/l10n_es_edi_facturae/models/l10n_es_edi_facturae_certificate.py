# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
from base64 import b64decode
from copy import deepcopy
import logging
from unittest.mock import patch

from cryptography.hazmat.primitives.serialization import pkcs12
from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import file_open, ormcache

__logger = logging.getLogger(__name__)
try:
    import xmlsig
    import xades
except ImportError as err:
    __logger.debug(err)

class Certificate(models.Model):
    _name = 'l10n_es_edi_facturae.certificate'
    _description = 'Facturae Digital Certificate'
    _order = 'date_start desc, id desc'
    _rec_name = 'serial_number'

    content = fields.Binary(string="PFX Certificate", required=True, help="PFX Certificate")
    password = fields.Char(help="Passphrase for the PFX certificate")
    serial_number = fields.Char(readonly=True, index=True, help="The serial number to add to electronic documents")
    date_start = fields.Datetime(readonly=True, help="The date on which the certificate starts to be valid")
    date_end = fields.Datetime(readonly=True, help="The date on which the certificate expires")
    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company, required=True, readonly=True)
    is_valid = fields.Boolean(string="is the certificate date valid", compute='_compute_is_valid', store=False, readonly=True)

    @api.depends('date_start', 'date_end')
    def _compute_is_valid(self):
        for certificate in self:
            certificate.is_valid = certificate.date_start < fields.Datetime.now() < certificate.date_end

    @ormcache('self.content', 'self.password')
    def _decode_certificate(self):
        """
        Return some certificate data concerning its validity
        :return tuple: encoded certificate, private key, decrypted certificate
        """
        self.ensure_one()
        _unused, certificate, *_unused = pkcs12.load_key_and_certificates(b64decode(self.content), self.password.encode())
        return certificate.not_valid_before, certificate.not_valid_after, certificate.serial_number

    # -------------------------------------------------------------------------
    # LOW-LEVEL METHODS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        certificates = super().create(vals_list)
        for certificate in certificates:
            try:
                cert_date_start, cert_date_end, serial_number = certificate._decode_certificate()
            except ValueError:
                raise UserError(_('There has been a problem with the certificate, some usual problems can be:\n'
                                        '\t- The password given or the certificate are not valid.\n'
                                        '\t- The certificate content is invalid.'))
            if datetime.datetime.now() > cert_date_end:
                raise UserError(_('The certificate is expired since %s') % certificate.date_end)
            # Assign extracted values from the certificate
            certificate.write({'serial_number': serial_number, 'date_start': cert_date_start, 'date_end': cert_date_end,})
        return certificates

    # -------------------------------------------------------------------------
    # BUSINESS METHODS
    # -------------------------------------------------------------------------
    def sign_xml(self, edi_data, sig_data):
        """
        Signs the given XML data with the certificate and private key.
        :param str edi_data: The XML data to sign.
        :param dict sig_data: The signature data to use.
        :return str: The signed XML data as a sting.
        """
        self.ensure_one()
        if not self.is_valid:
            raise UserError(_('This certificate date is not valid, its validity has probably expired'))
        nspaces = {
            'xd': 'http://www.w3.org/2000/09/xmldsig#', 'xades': 'http://uri.etsi.org/01903/v1.3.2#',
            'fac': "http://www.facturae.es/Facturae/2007/v3.1/Facturae"
        }
        root = etree.fromstring(deepcopy(edi_data).encode("utf-8"))
        root.remove(root.xpath('//xd:Signature', namespaces=nspaces)[0])

        signature = xmlsig.template.create(xmlsig.constants.TransformInclC14N, xmlsig.constants.TransformRsaSha1, "Signature", ns="xd")
        signature_id = "Signature-SignedProperties"
        ref = xmlsig.template.add_reference(signature, xmlsig.constants.TransformSha1, uri="", name="REF")
        xmlsig.template.add_transform(ref, xmlsig.constants.TransformEnveloped)
        xmlsig.template.add_reference(signature, xmlsig.constants.TransformSha1, uri="#KI")
        xmlsig.template.add_reference(signature, xmlsig.constants.TransformSha1, uri="#" + signature_id)
        ki = xmlsig.template.ensure_key_info(signature, name="KI")
        data = xmlsig.template.add_x509_data(ki)
        xmlsig.template.x509_data_add_certificate(data)
        serial = xmlsig.template.x509_data_add_issuer_serial(data)
        xmlsig.template.x509_issuer_serial_add_issuer_name(serial)
        xmlsig.template.x509_issuer_serial_add_serial_number(serial)
        xmlsig.template.add_key_value(ki)
        qualifying = xades.template.create_qualifying_properties(signature, etsi='xades',)
        props = xades.template.create_signed_properties(qualifying, name=signature_id,)
        xades.template.add_claimed_role(props, sig_data["SignerRole"])
        pol_id = "http://www.facturae.gob.es/politica_de_firma_formato_facturae/politica_de_firma_formato_facturae_v3_1.pdf"
        pol_desc = "Politica de firma Facturae v3.1"
        policy = xades.policy.GenericPolicyId(pol_id, pol_desc, xmlsig.constants.TransformSha1)
        root.append(signature)
        cert_bundled = pkcs12.load_key_and_certificates(b64decode(self.content), self.password.encode(),)
        ctx = xades.XAdESContext(policy, [cert_bundled[1]])
        ctx.load_pkcs12(cert_bundled)

        # We don't want to access the policy with urllib as we have a local copy of said policy
        with file_open('l10n_es_edi_facturae/data/politica_de_firma_formato_facturae_v3_1.pdf', 'rb') as f:
            pol_data = f.read()
        with patch('xades.policy.BasePolicy._resolve_policy', lambda s, x: pol_data):
            ctx.sign(signature)
            ctx.verify(signature)

        return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True, pretty_print=True)
