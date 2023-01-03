# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.exceptions import UserError
from odoo.tools.misc import file_open
from odoo.tests import tagged
from contextlib import contextmanager
from .common import TestSaEdiCommon, mocked_l10n_sa_post_zatca_edi
from unittest.mock import patch
import base64
import logging
import re

_logger = logging.getLogger(__name__)

@tagged('post_install_l10n', '-at_install', 'post_install')
class TestEdiZatca(TestSaEdiCommon):

    def testInvoiceStandard(self):

        # with self.frozen_date,\
        # patch('odoo.addons.l10n_sa_edi.models.account_edi_format.AccountEdiFormat._l10n_sa_post_zatca_edi',
        #     new=mocked_l10n_sa_post_zatca_edi):

        move = self._create_invoice()
        move.action_post()

        self.assertTrue(generated_files)

        current_tree = None
        expected_tree = self.expected_xml_invoice_value
        self.assertXmlTreeEqual(current_tree, expected_tree)
