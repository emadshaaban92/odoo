import base64
import logging
import random
import re
from base64 import b64encode
from datetime import datetime
from lxml import etree
from unittest.mock import patch

from freezegun import freeze_time

from odoo import Command
from odoo.addons.account_edi.tests.common import AccountEdiTestCommon
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tools import file_open, safe_eval

_logger = logging.getLogger(__name__)

@tagged('post_install_l10n', 'post_install', '-at_install')
class TestEdiFaceXmls(AccountEdiTestCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref='l10n_es.account_chart_template_full',
                   edi_format_ref='l10n_es_edi_facturae.edi_es_face'):
        super().setUpClass(chart_template_ref=chart_template_ref, edi_format_ref=edi_format_ref)
        cls.frozen_past = datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
        cls.frozen_today = datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0)
        cls.frozen_future = datetime(year=5000, month=1, day=1, hour=0, minute=0, second=0)

        # ==== Company ====

        cls.company_data['company'].write({ # -> PersonTypeCode 'J'
            'country_id': cls.env.ref('base.es').id, # -> ResidenceTypeCode 'R'
            'street': "C. de Embajadores, 68-116",
            'state_id': cls.env.ref('base.state_es_m').id,
            'city': "Madrid",
            'zip': "12345",
            'vat': 'ES59962470K',
        })

        # ==== Business ====

        cls.partner_a.write({ # -> PersonTypeCode 'F'
            'country_id': cls.env.ref('base.be').id, # -> ResidenceTypeCode 'U'
            'vat': 'BE0477472701',
            'city': "Namur",
            'street': "Rue de Bruxelles, 15000",
            'zip': "5000",
        })

        cls.product_t = cls.env["product.product"].create({"name": "Test product"})
        cls.partner_t = cls.env["res.partner"].create({"name": "Test partner", "vat": "ESF35999705"})
        cls.password = "test"
        cls.certificate = cls.env["l10n_es_edi_facturae.certificate"].create({
            "content": b64encode(file_open('l10n_es_edi_facturae/tests/data/certificate_test.pfx', 'rb').read()),
            "password": "test",
            'company_id': cls.company_data['company'].id,
        })
        cls.tax = cls.env['account.tax'].create({
                'name': "IVA 21% (Bienes)",
                'company_id': cls.company_data['company'].id,
                'amount': 21.0,
                'price_include': False,
                'l10n_es_edi_facturae_tax_type': '01'
            })[0]

        cls.nsmap = {
            'ds': "http://www.w3.org/2000/09/xmldsig#", 'fe': "http://www.facturae.es/Facturae/2007/v3.1/Facturae",
            'xades': "http://uri.etsi.org/01903/v1.3.2#", 'xd': "http://www.w3.org/2000/09/xmldsig#",
        }

        cls.maxDiff = None

    @classmethod
    def create_invoice(cls, **kwargs):
        return cls.env['account.move'].with_context(edi_test_mode=True).create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner_a.id,
            'invoice_date': cls.frozen_today.isoformat(),
            'date': cls.frozen_today.isoformat(),
            **kwargs,
            'invoice_line_ids': [Command.create({'product_id': cls.product_a.id, 'price_unit': 1000.0, **line_vals, })
                                 for line_vals in kwargs.get('invoice_line_ids', [])],

        })

    def test_generate_signed_xml(self, date=None):
        random.seed(42)
        date = date or self.frozen_today
        ids = [f"id-{''.join(str(random.randint(0, 10)) for v in range(15))}" for i in range(10)]
        with freeze_time(date), patch('xades.utils.get_unique_id', ids.pop), patch('datetime.datetime.now', lambda: date):
            invoice = self.create_invoice(
                    partner_id=self.partner_a.id,
                    invoice_line_ids=[
                        {'price_unit': 100.0, 'tax_ids': [self.tax.id]},
                        {'price_unit': 100.0, 'tax_ids': [self.tax.id]},
                        {'price_unit': 200.0, 'tax_ids': [self.tax.id]},
                    ],
            )
            invoice.action_post()

            invoice.edi_document_ids._process_documents_no_web_services()
            generated_files = []
            attachment_ids = invoice.edi_document_ids.with_context(bin_size=False).filtered(lambda x: x.edi_format_id.code == 'es_face').attachment_id
            for attachment in attachment_ids:
                generated_files.append(base64.decodebytes(attachment.datas))
            self.assertTrue(generated_files)

            with file_open("l10n_es_edi_facturae/tests/data/expected_signed_data.json", 'rb') as exp_f:
                expected_data = safe_eval.json.loads(exp_f.read())

            actual_data = self.env['account.edi.format'].l10n_es_edi_facturae_export_facturae(invoice)
            self.assertDictEqual(expected_data, {**actual_data[0], **actual_data[1]})

            expected_signature = re.sub(r'\s*', '', """K1syTL8Fep5gMU/5yJziRAGLQgsKfu/w9Hzg2VG9GBODaRF9j8v5pXyoaQ0XLIuG4
                3v4aCQa1odyxyZXh/8MivxffTn94KEs5seLM2jR96mFOPEuqMnxwqgdn6v14VBKs1CzvaA9/5a36UXqOF80rlq4rfLiCwQn8FMkqK7u3
                WmcJntVOQWrfu8pv3QnLZiXb/dBW+WqvNAj1OyHOJKZiG3eLOvNI203oEZjpNjXI44TjXzJ5UyBiIKKxYn3VR+SG2n1wr34FJHtbuTPv
                vR/fYGz0vM9fL1n+j/87oZgNyF8cPZXypX6Mul15voX11QWu1POvsDHu8odIVT9kpuQQA==""")
            actual_signature = etree.fromstring(generated_files[0]).xpath('//xd:SignatureValue', namespaces=self.nsmap)[0].text
            actual_signature = re.sub(r'\s*', '', actual_signature)
            self.assertEqual(expected_signature, actual_signature)  # If the signature is valid, all the sub-hashes must be valid

    def test_cannot_generate_unsigned_xml(self):
        """
        Test that a certificate is required to generate an xml
        """
        self.certificate.unlink()
        random.seed(42)
        ids = [f"id-{''.join(str(random.randint(0, 10)) for v in range(15))}" for i in range(10)]
        with freeze_time(self.frozen_today), patch('xades.utils.get_unique_id', ids.pop), patch('datetime.datetime.now', lambda: self.frozen_today):
            invoice = self.create_invoice(partner_id=self.partner_a.id, invoice_line_ids=[{'price_unit': 100.0, 'tax_ids': [self.tax.id]}, ], )
            invoice.action_post()

            invoice.edi_document_ids._process_documents_no_web_services()
            generated_files = []
            attachment_ids = invoice.edi_document_ids.with_context(bin_size=False).filtered(lambda x: x.edi_format_id.code == 'es_face').attachment_id
            for attachment in attachment_ids:
                generated_files.append(base64.decodebytes(attachment.datas))
            self.assertFalse(generated_files)

    def test_certificate_validity(self):
        """
        Test that the signature will not be done if the current date is out of the certificate validity boundaries
        """
        with self.assertRaises(UserError):
            self.test_generate_signed_xml(self.frozen_past)
        with self.assertRaises(UserError):
            self.test_generate_signed_xml(self.frozen_future)
