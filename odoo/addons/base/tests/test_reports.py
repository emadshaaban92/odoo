# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import PyPDF2
import io

import odoo
from odoo.tests import TransactionCase, HttpCase, tagged


_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install', 'post_install_l10n', 'reports')
class TestReports(TransactionCase):
    def test_reports(self):
        invoice_domain = [('move_type', 'in', ('out_invoice', 'out_refund', 'out_receipt', 'in_invoice', 'in_refund', 'in_receipt'))]
        specific_model_domains = {
            'account.report_original_vendor_bill': [('move_type', 'in', ('in_invoice', 'in_receipt'))],
            'account.report_invoice_with_payments': invoice_domain,
            'account.report_invoice': invoice_domain,
        }
        Report = self.env['ir.actions.report']
        for report in Report.search([('report_type', 'like', 'qweb')]):
            report_model = 'report.%s' % report.report_name
            try:
                self.env[report_model]
            except KeyError:
                # Only test the generic reports here
                _logger.info("testing report %s", report.report_name)
                report_model_domain = specific_model_domains.get(report.report_name, [])
                report_records = self.env[report.model].search(report_model_domain, limit=10)
                if not report_records:
                    _logger.info("no record found skipping report %s", report.report_name)

                # Test report generation
                if not report.multi:
                    for record in report_records:
                        Report._render_qweb_html(report.id, record.ids)
                else:
                    Report._render_qweb_html(report.id, report_records.ids)
            else:
                continue


@tagged('post_install', '-at_install', 'post_install_l10n', 'reports')
class TestReportsPDF(HttpCase):
    def test_report_pdf(self):
        IrAsset = self.env['ir.asset']
        IrUiView = self.env['ir.ui.view']
        IrActionsReport = self.env['ir.actions.report'].with_context(force_report_rendering=True)

        IrAsset.create({
            'bundle': 'base.assets_dummy',
            'name': '/base/tests/test_reports.css',
            'path': '/base/tests/test_reports.css',
        })
        IrAsset.create({
            'bundle': 'base.assets_dummy',
            'name': '/base/tests/test_reports.js',
            'path': '/base/tests/test_reports.js',
        })

        view = IrUiView.create({
            'name': "dummy",
            'type': 'qweb',
            'arch': """
                <t t-name="base.dummy">
                    <html>
                        <body>
                            <main>
                                <style>section {color: yellow;}</style>
                                <t t-call-assets="base.assets_dummy"/>
                                <custom_header style="display: none;"/>
                                <section>
                                    <div t-foreach="[10, 20, 30]" t-as="o">Bidule<t t-out="o"/></div>
                                </section>
                                <custom_footer style="display: none;"/>
                            </main>
                        </body>
                    </html>
                </t>"""
        })

        action = IrActionsReport.create({
            'name': 'test_reports',
            'model': 'res.company',
            'binding_model_id': self.env['ir.model'].search([('model', '=', 'res.company')]).id,
            'binding_type': 'report',
            'report_type': 'qweb-pdf',
            'report_name': view.id,
            'report_file': 'dummy',
        })

        # check html content
        content_html, report_type = IrActionsReport._render_qweb_html(action, self.env.company.ids)
        self.assertEqual(report_type, 'html')
        self.assertIn(b'Bidule10', content_html)
        self.assertIn(b'/base.assets_dummy.min.css', content_html)
        self.assertIn(b'/base.assets_dummy.min.js', content_html)

        # check pdf
        content_pdf, report_type = IrActionsReport._render(action, self.env.company.ids)
        self.assertEqual(report_type, 'pdf')
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(content_pdf))
        self.assertEqual(pdf_reader.numPages, 4, 'The css file add 2 pages from header + js file add 1 page from footer')
