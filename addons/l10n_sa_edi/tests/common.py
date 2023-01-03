# coding: utf-8
from lxml import etree

from odoo import Command, tools
from odoo.tests import tagged
from odoo.addons.account_edi.tests.common import AccountEdiTestCommon


def mocked_l10n_sa_post_zatca_edi(edi_format, invoice):
    pass
@tagged('post_install_l10n', '-at_install', 'post_install')
class TestSaEdiCommon(AccountEdiTestCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref='l10n_sa.sa_chart_template_standard', edi_format_ref='l10n_sa_edi.edi_sa_zatca'):
        super().setUpClass(chart_template_ref=chart_template_ref, edi_format_ref=edi_format_ref)

        # Setup company
        cls.company = cls.company_data['company']
        cls.company.l10n_sa_api_mode = 'sandbox'
        customer_invoice_journal = cls.env['account.journal'].search([('company_id', '=', cls.company.id), ('name', '=', 'Customer Invoices')])
        customer_invoice_journal.l10n_sa_csr = 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ056Q0NBZDBDQVFBd2daNHhDekFKQmdOVkJBWVRBbE5CTVJNd0VRWURWUVFMREFvek1USXpNVEl6TkRVMgpNUk13RVFZRFZRUUtEQXBUUVNCRGIyMXdZVzU1TVJNd0VRWURWUVFEREFwVFFTQkRiMjF3WVc1NU1SZ3dGZ1lEClZRUmhEQTh6TVRJek1USXpORFUyTkRVMk56TXhEakFNQmdOVkJBZ01CVTFsWTJOaE1TWXdKQVlEVlFRSERCM1kKcDltRTJZWFlyOW1LMlliWXFTRFlwOW1FMllYWmh0bUkyTEhZcVRCV01CQUdCeXFHU000OUFnRUdCU3VCQkFBSwpBMElBQktZejNkNWRCVytzb2NBdHNVR1liLzZiRFNidU9McUFuUU5UNDFnK0I1Si9qZXVzMzhVTTExWU1uS01XCnVxZmJyZ0YvTWhPbEF4Zk5BV3I1VUhZQmN1aWdnZDR3Z2RzR0NTcUdTSWIzRFFFSkRqR0J6VENCeWpBaEJna3IKQmdFRUFZSTNGQUlFRkF3U1drRlVRMEV0UTI5a1pTMVRhV2R1YVc1bk1JR2tCZ05WSFJFRWdad3dnWm1rZ1pZdwpnWk14SURBZUJnTlZCQVFNRnpFdFQyUnZiM3d5TFRFMWZETXRNVEl6TkRVMk56ZzVNUjh3SFFZS0NaSW1pWlB5CkxHUUJBUXdQTXpFeU16RXlNelExTmpRMU5qY3pNUTB3Q3dZRFZRUU1EQVF4TURBd01TOHdMUVlEVlFRYURDWkIKYkNCQmJXbHlJRTF2YUdGdGJXVmtJRUpwYmlCQlltUjFiQ0JCZW1sNklGTjBjbVZsZERFT01Bd0dBMVVFRHd3RgpUM1JvWlhJd0NnWUlLb1pJemowRUF3SURTQUF3UlFJaEFMNWlnNHJLVXY1NGI0VTA1YnU1U3dGU2FKaGFTeTRuCnRxMFRKYittcDJ6aEFpQjhoUjd2TGlVeUhPOHNkRnNYNTBXdDNOemU2M1g0b3RKL1dsN2JKdmpwcEE9PQotLS0tLUVORCBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0K'
        cls.company.street = 'Al Amir Mohammed Bin Abdul Aziz Street'
        cls.company.l10n_sa_edi_building_number = '1234'
        cls.company.l10n_sa_edi_plot_identification = '1234'
        cls.company.l10n_sa_edi_neighborhood = 'Testomania'
        cls.company.zip = '42317'

        # Setup partner
        cls.partner_us = cls.env['res.partner'].create({
            'name': 'Chichi Lboukla',
            'street': '4557 De Silva St',
            'l10n_sa_edi_building_number': '12300',
            'l10n_sa_edi_plot_identification': '2323',
            'l10n_sa_edi_neighborhood': 'Neighbor!',
            'city': 'Fremont',
            'zip': '94538',
            'country_id': cls.env['res.country'].search([('code', '=', 'US')]).id,
            'state_id': cls.env['res.country.state'].search([('name', '=', 'California')]).id,
            'email': 'azure.Interior24@example.com',
            'phone': '(870)-931-0505',
        })

        # 15% tax
        cls.tax_15 = cls.env['account.tax'].search([('company_id', '=', cls.company.id), ('name', '=', 'Sales Tax 15%')])

        # Large cabinet product
        cls.product = cls.env['product.template'].search([('company_id', '=', cls.company.id), ('default_code', '=', 'E-COM07')])

        basis_xml = cls._get_test_file_content('standard/invoice.xml')
        cls.expected_xml_invoice_value = cls.with_applied_xpath(
            etree.fromstring(basis_xml),
            '''
            <xpath expr="//cac:PartyName/cbc:Name[0]" position="replace">
                <cbc:Name>__ignore__</cbc:Name>
            </xpath>
            '''
            )

    @classmethod
    def _get_test_file_content(cls, filename):
        """ Get the content of a test file inside this module """
        path = 'l10n_sa_edi/tests/compliance/' + filename
        with tools.file_open(path, mode='rb') as test_file:
            return test_file.read()

    def _create_invoice(self, **kwargs):
        vals = {
            'name': 'INV/2022/00014',
            'move_type':'out_invoice',
            'partner_id': self.partner_us.id,
            'invoice_date': '2022-09-22',
            'date': '2022-09-22',
            'currency_id': self.company.currency_id,
            'invoice_line_ids': [Command.create({
                'product_id': self.product.id,
                'product_uom_id':self.product.uom_id,
                'price_unit': '320.0',
                'tax_ids':[Command.set(self.tax_15.ids)],
                }),
            ],
        }
        vals.update(kwargs)

        return self.env['account.move'].create(vals)
