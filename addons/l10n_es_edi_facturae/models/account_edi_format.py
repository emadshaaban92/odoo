# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from collections import namedtuple

from lxml import etree

from odoo import  api, models, _
from odoo.exceptions import UserError
from odoo.tools import file_open, float_repr
from odoo.tools.xml_utils import _check_with_xsd

COUNTRY_CODE_MAP = {
    "BD": "BGD", "BE": "BEL", "BF": "BFA", "BG": "BGR", "BA": "BIH", "BB": "BRB", "WF": "WLF", "BL": "BLM", "BM": "BMU",
    "BN": "BRN", "BO": "BOL", "BH": "BHR", "BI": "BDI", "BJ": "BEN", "BT": "BTN", "JM": "JAM", "BV": "BVT", "BW": "BWA",
    "WS": "WSM", "BQ": "BES", "BR": "BRA", "BS": "BHS", "JE": "JEY", "BY": "BLR", "BZ": "BLZ", "RU": "RUS", "RW": "RWA",
    "RS": "SRB", "TL": "TLS", "RE": "REU", "TM": "TKM", "TJ": "TJK", "RO": "ROU", "TK": "TKL", "GW": "GNB", "GU": "GUM",
    "GT": "GTM", "GS": "SGS", "GR": "GRC", "GQ": "GNQ", "GP": "GLP", "JP": "JPN", "GY": "GUY", "GG": "GGY", "GF": "GUF",
    "GE": "GEO", "GD": "GRD", "GB": "GBR", "GA": "GAB", "SV": "SLV", "GN": "GIN", "GM": "GMB", "GL": "GRL", "GI": "GIB",
    "GH": "GHA", "OM": "OMN", "TN": "TUN", "JO": "JOR", "HR": "HRV", "HT": "HTI", "HU": "HUN", "HK": "HKG", "HN": "HND",
    "HM": "HMD", "VE": "VEN", "PR": "PRI", "PS": "PSE", "PW": "PLW", "PT": "PRT", "SJ": "SJM", "PY": "PRY", "IQ": "IRQ",
    "PA": "PAN", "PF": "PYF", "PG": "PNG", "PE": "PER", "PK": "PAK", "PH": "PHL", "PN": "PCN", "PL": "POL", "PM": "SPM",
    "ZM": "ZMB", "EH": "ESH", "EE": "EST", "EG": "EGY", "ZA": "ZAF", "EC": "ECU", "IT": "ITA", "VN": "VNM", "SB": "SLB",
    "ET": "ETH", "SO": "SOM", "ZW": "ZWE", "SA": "SAU", "ES": "ESP", "ER": "ERI", "ME": "MNE", "MD": "MDA", "MG": "MDG",
    "MF": "MAF", "MA": "MAR", "MC": "MCO", "UZ": "UZB", "MM": "MMR", "ML": "MLI", "MO": "MAC", "MN": "MNG", "MH": "MHL",
    "MK": "MKD", "MU": "MUS", "MT": "MLT", "MW": "MWI", "MV": "MDV", "MQ": "MTQ", "MP": "MNP", "MS": "MSR", "MR": "MRT",
    "IM": "IMN", "UG": "UGA", "TZ": "TZA", "MY": "MYS", "MX": "MEX", "IL": "ISR", "FR": "FRA", "IO": "IOT", "SH": "SHN",
    "FI": "FIN", "FJ": "FJI", "FK": "FLK", "FM": "FSM", "FO": "FRO", "NI": "NIC", "NL": "NLD", "NO": "NOR", "NA": "NAM",
    "VU": "VUT", "NC": "NCL", "NE": "NER", "NF": "NFK", "NG": "NGA", "NZ": "NZL", "NP": "NPL", "NR": "NRU", "NU": "NIU",
    "CK": "COK", "XK": "XKX", "CI": "CIV", "CH": "CHE", "CO": "COL", "CN": "CHN", "CM": "CMR", "CL": "CHL", "CC": "CCK",
    "CA": "CAN", "CG": "COG", "CF": "CAF", "CD": "COD", "CZ": "CZE", "CY": "CYP", "CX": "CXR", "CR": "CRI", "CW": "CUW",
    "CV": "CPV", "CU": "CUB", "SZ": "SWZ", "SY": "SYR", "SX": "SXM", "KG": "KGZ", "KE": "KEN", "SS": "SSD", "SR": "SUR",
    "KI": "KIR", "KH": "KHM", "KN": "KNA", "KM": "COM", "ST": "STP", "SK": "SVK", "KR": "KOR", "SI": "SVN", "KP": "PRK",
    "KW": "KWT", "SN": "SEN", "SM": "SMR", "SL": "SLE", "SC": "SYC", "KZ": "KAZ", "KY": "CYM", "SG": "SGP", "SE": "SWE",
    "SD": "SDN", "DO": "DOM", "DM": "DMA", "DJ": "DJI", "DK": "DNK", "VG": "VGB", "DE": "DEU", "YE": "YEM", "DZ": "DZA",
    "US": "USA", "UY": "URY", "YT": "MYT", "UM": "UMI", "LB": "LBN", "LC": "LCA", "LA": "LAO", "TV": "TUV", "TW": "TWN",
    "TT": "TTO", "TR": "TUR", "LK": "LKA", "LI": "LIE", "LV": "LVA", "TO": "TON", "LT": "LTU", "LU": "LUX", "LR": "LBR",
    "LS": "LSO", "TH": "THA", "TF": "ATF", "TG": "TGO", "TD": "TCD", "TC": "TCA", "LY": "LBY", "VA": "VAT", "VC": "VCT",
    "AE": "ARE", "AD": "AND", "AG": "ATG", "AF": "AFG", "AI": "AIA", "VI": "VIR", "IS": "ISL", "IR": "IRN", "AM": "ARM",
    "AL": "ALB", "AO": "AGO", "AQ": "ATA", "AS": "ASM", "AR": "ARG", "AU": "AUS", "AT": "AUT", "AW": "ABW", "IN": "IND",
    "AX": "ALA", "AZ": "AZE", "IE": "IRL", "ID": "IDN", "UA": "UKR", "QA": "QAT", "MZ": "MOZ"
}
REVERSED_COUNTRY_CODE = {v: k for k, v in COUNTRY_CODE_MAP.items()}

EDI_XML_DICT_TEMPLATES = {
    'business': {'TaxIdentification': {}, 'PartyIdentification': False, 'AdministrativeCentres': [], 'Assignee': {'LegalEntity': False, 'Individual': False, }, },
    'invoice_line': {
        'IssuerContractReference': False,
        'IssuerContractDate': False,
        'IssuerTransactionReference': False,
        'IssuerTransactionDate': False,
        'ReceiverContractReference': False,
        'ReceiverContractDate': False,
        'ReceiverTransactionDate': False,
        'ReceiverTransactionReference': False,
        'FileReference': False,
        'FileDate': False,
        'SequenceNumber': False,
        'DeliveryNotesReferences': [],
        'ItemDescription': '',
        'Quantity': '',
        'UnitOfMeasure': False,
        'UnitPriceWithoutTax': '',
        'TotalCost': '',
        'DiscountsAndRebates': [],
        'Charges': [],
        'GrossAmount': '',
        'TaxesWitheld': [],
        'TaxesOutputs': [],
        'LineItemPeriod': False,
        'TransactionDate': False,
        'AdditionalLineItemInformation': False,
        'SpecialTaxableEvent': False,
        'ArticleCode': False,
        'Extensions': False,
    },
    'facturae': {
        'Modality': '',
        'InvoiceIssuerType': '',
        'ThirdParty': False,
        'BatchIdentifier': '',
        'InvoicesCount': '',
        'TotalInvoicesAmount': {'TotalAmount': '', 'EquivalentInEuros': False, },
        'TotalOutstandingAmount': {'TotalAmount': '', 'EquivalentInEuros': False, },
        'TotalExecutableAmount': {'TotalAmount': '', 'EquivalentInEuros': False, },
        'InvoiceCurrencyCode': '',
        'FactoringAssignmentData': False,
        'SellerParty': '',
        'BuyerParty': '',
        'Invoices': [],
        'Extensions': False,
    },
    'signature': {'SigningTime': '', 'SignerRole': '', },
}


class AccountEdiFaceFormat(models.Model):
    _inherit = 'account.edi.format'

    # ------------------------- #
    #       ES B2G2B EDI        #
    # ------------------------- #

    ################################################
    # Export methods overridden based on EDI Format #
    ################################################

    def _is_compatible_with_journal(self, journal):
        """ Indicate if the EDI format should appear on the journal passed as parameter to be selected by the user.
        If True, this EDI format will appear on the journal.

        :param journal: The journal.
        :returns:       True if this format can appear on the journal, False otherwise.
        """
        # EXTENDS account_edi
        if self.code != 'es_face':
            return super()._is_compatible_with_journal(journal)
        self.ensure_one()
        return journal.type == 'sale' and journal.country_code == 'ES'

    def _get_move_applicability(self, move):
        """ Core function for the EDI processing: it first checks whether the EDI format is applicable on a given
        move, if so, it then returns a dictionary containing the functions to call for this move.

        :return: dict mapping str to function (callable)
        * post:             function called for edi.documents with state 'to_send' (post flow)
        * cancel:           function called for edi.documents with state 'to_cancel' (cancel flow)
        * post_batching:    function returning the batching key for the post flow
        * cancel_batching:  function returning the batching key for the cancel flow
        * edi_content:      function called when computing the edi_content for an edi.document
        """
        # EXTENDS account_edi
        self.ensure_one()
        if self.code != 'es_face':
            return super()._get_move_applicability(move)

        if move.company_id.country_code == 'ES':
            return {
                'post': self._l10n_es_edi_facturae_post_invoices,
                'edi_content': self._l10n_es_edi_facturae_xml_edi_content,
            }

    def _needs_web_services(self):
        # EXTENDS account_edi
        return False if self.code == 'es_face' else super()._needs_web_services()

    #############################
    #   EDI SPECIFIC METHODS    #
    #############################

    def _l10n_es_edi_facturae_xml_edi_content(self, invoice):
        return self.l10n_es_edi_facturae_export_facturae(invoice).encode()
    def _l10n_es_edi_facturae_post_invoices(self, invoices):
        # Ensure a certificate is available.
        certificate = self.env['l10n_es_edi_facturae.certificate'].search([("company_id", 'in', invoices.company_id.ids)])
        if not certificate:
            return {inv: {
                'error': _("Please configure the certificate for Facturae."),
                'blocking_level': 'error',
            } for inv in invoices}

        # Generate the XMLs.
        res = {}
        for inv in invoices:
            xml_name = f'{inv.name.replace("/", "_")}_facturae_signed.xml'
            attachment = self.env['ir.attachment'].create({
                'name': xml_name,
                'raw': self.l10n_es_edi_facturae_render_facturae(inv),
                'res_model': 'account.edi.document',
                'mimetype': 'application/xml'
            })
            res[inv] = {'success': True, 'attachment': attachment}
        return res

    @staticmethod
    def l10n_es_edi_facturae_clean_xml(tree_or_str, as_string=True):
        """
        Remove all the unwanted whitespaces and end of lines from the xml tree.
        :param etree.XML or str tree_or_str: the xml tree in etree or str format
        :return: the cleaned xml tree
        """
        str_tree = tree_or_str if isinstance(tree_or_str, str) else etree.tostring(tree_or_str, encoding=str)
        str_tree = re.sub('\n+', '', str_tree)
        str_tree = re.sub(r'\s{2, }', '', str_tree)
        if as_string:
            return str_tree
        return etree.XML(str_tree)

    @staticmethod
    def l10n_es_edi_facturae_inv_lines_to_items(invoice, conv_rate, needs_equivalency, fmt_in_cur, fmt_in_eur):
        """
        Convert the invoice lines to a list of items required for the Facturae xml generation

        :param account.move invoice:    The invoice containing the invoice lines
        :param float conv_rate:         The conversion rate from the invoice currency to the company currency
        :param bool needs_equivalency:  True if the invoice uses multi-currencies
        :param func fmt_in_cur:         The formatting function to use for the amount in the invoice currency
        :param func fmt_in_eur:         The formatting function to use for the amount in euros
        :return tuple:                  A tuple containing the Face items, the taxes and the invoice totals data.
        """

        def compute_tax_amount(tax, line):
            if tax.amount_type == 'percent':
                return tax.amount * line.price_subtotal / 100
            if tax.amount_type == 'fixed':
                return tax.amount
            if tax.amount_type == 'division':
                if 1 + (tax.amount / 100):
                    return line.price_subtotal - (line.price_subtotal / (1 + (tax.amount / 100)))
                return 0.0

        items = []
        totals = {
            'total_gross_amount': 0.,
            'total_general_discounts': 0.,
            'total_general_surcharges': 0.,
            'total_taxes_withheld': 0.,
            'total_payments_on_account': 0.,
            'amounts_withheld': 0.,
        }
        taxes = []
        for line in invoice.invoice_line_ids:
            invoice_line_values = EDI_XML_DICT_TEMPLATES['invoice_line'].copy()

            total_price = line.quantity * line.price_unit * conv_rate  # This isn't a mistake
            gross_amount = line.price_subtotal / conv_rate
            discount = max(0., line.discount * total_price)
            surcharge = max(0., - line.discount * total_price)  # + line.price_total - line.price_subtotal
            totals['total_gross_amount'] += gross_amount
            totals['total_general_discounts'] += discount
            totals['total_general_surcharges'] += surcharge

            taxes_output = [{
                "TaxTypeCode": tax.l10n_es_edi_facturae_tax_type,
                "TaxRate": f'{tax.amount:.3f}',
                "TaxableBase": {
                    'TotalAmount': fmt_in_cur(gross_amount),
                    'EquivalentInEuros': fmt_in_eur(line.price_subtotal) if needs_equivalency else False,
                },
                "TaxAmount": {
                    "TotalAmount": fmt_in_cur(compute_tax_amount(tax, line) * conv_rate),
                    "EquivalentInEuros": fmt_in_eur(compute_tax_amount(tax, line)),
                },
            } for tax in line.tax_ids]

            invoice_line_values.update({
                'ItemDescription': line.name,
                'Quantity': line.quantity,
                'UnitOfMeasure': line.product_uom_id.l10n_es_edi_facturae_uom_code,
                'UnitPriceWithoutTax': fmt_in_cur(line.price_unit),
                'TotalCost': fmt_in_cur(total_price),
                'DiscountsAndRebates': [
                    {'DiscountReason': '', 'DiscountRate': f'{line.discount:.2f}', 'DiscountAmount': fmt_in_cur(discount)},
                ] if discount != 0. else [],
                'Charges': [
                    {'ChargeReason': '', 'ChargeRate': f'{max(0, -line.discount):.2f}', 'ChargeAmount': fmt_in_cur(surcharge)},
                ] if surcharge != 0. else [],
                'GrossAmount': fmt_in_cur(gross_amount),
                'TaxesOutputs': taxes_output,
            })
            items.append(invoice_line_values)
            taxes += taxes_output
        return items, taxes, totals

    @api.model
    def l10n_es_edi_facturae_export_facturae(self, invoice):
        """
        Produce the Facturae XML data for the invoice.

        :param account.move invoice: The invoice to export.
        :return tuple: (data needed to render the full template, data needed to render the signature template).
        """

        self_company = invoice.company_id
        partner = invoice.partner_id.parent_id or invoice.partner_id

        if not self_company.l10n_es_edi_facturae_tax_identifier:
            raise UserError(_('The company needs a set tax identification number or VAT number'))

        if not partner.l10n_es_edi_facturae_tax_identifier:
            raise UserError(_('The partner needs a set tax identification number or VAT number'))

        def fmt_eur(value):
            # Format the monetary values to avoid trailing decimals (e.g. 90.850...1).
            return float_repr(value, eur_curr.decimal_places)

        def fmt_curr(number):
            # Format the monetary values to avoid trailing decimals (e.g. 90.850...1).
            if inv_curr.name == 'EUR':
                return fmt_eur(number)
            return float_repr(number, inv_curr.decimal_places)

        eur_curr = self.env['res.currency'].search([('name', '=', 'EUR')])
        inv_curr = invoice.currency_id or self_company.currency_id
        IndividualName = namedtuple('IndividualName', ['firstname', 'surname', 'surname2'])
        firstname = surname = surname2 = ''
        phone_clean_table = str.maketrans({" ": None, "-": None, "(": None, ")": None, "+": None})
        legal_literals = invoice.narration.striptags() if invoice.narration else False
        legal_literals = legal_literals.split(";") if legal_literals else False

        if partner.is_company:
            partner_name = IndividualName('', '', '')
        else:
            name_split = [part for part in partner.name.replace(', ', ' ').split(' ') if part]
            if len(name_split) > 2:
                firstname = ' '.join(name_split[:-2])
                surname, surname2 = name_split[-2:]
            elif len(name_split) == 2:
                firstname = ' '.join(name_split[:-1])
                surname = name_split[-1]

            partner_name = IndividualName(firstname, surname, surname2)

        template_values = EDI_XML_DICT_TEMPLATES['facturae'].copy()
        self_party_values = EDI_XML_DICT_TEMPLATES['business'].copy()
        partner_party_values = EDI_XML_DICT_TEMPLATES['business'].copy()
        signature_values = EDI_XML_DICT_TEMPLATES['signature'].copy()

        if invoice.move_type == "entry":
            return False
        invoice_issuer_type = 'EM' if invoice.move_type == 'out_invoice' else 'RE'
        invoice_issuer_signature_type = 'supplier' if invoice.move_type == 'out_invoice' else 'customer'

        company_is_not_euro = self_company.currency_id != eur_curr
        invoice_is_not_euro = inv_curr != eur_curr

        if not (company_is_not_euro or invoice_is_not_euro):
            conv_rate = 1.00
            need_conv = False
        elif not company_is_not_euro and invoice_is_not_euro:
            conv_rate = inv_curr._get_conversion_rate(inv_curr, eur_curr, self_company, invoice.invoice_date)
            need_conv = True
        elif company_is_not_euro and invoice_is_not_euro:
            conv_rate = inv_curr._get_conversion_rate(inv_curr, eur_curr, self_company, invoice.invoice_date)
            need_conv = True
        else:
            conv_rate = 1.00
            need_conv = False

        total_outst_am_in_currency = abs(invoice.amount_total_in_currency_signed)
        total_outst_am = abs(invoice.amount_total_signed)

        total_exec_am_in_currency = abs(invoice.amount_total_in_currency_signed)
        total_exec_am = abs(invoice.amount_total_signed)
        self_party_values.update({
            'TaxIdentification': {
                'PersonTypeCode': self_company.l10n_es_edi_facturae_person_type,
                'ResidenceTypeCode': self_company.l10n_es_edi_facturae_residence_type,
                'TaxIdentificationNumber': self_company.l10n_es_edi_facturae_tax_identifier,
            },
            'Assignee': {
                'LegalEntity': {
                    'CorporateName': self_company.name,
                    'TradeName': self_company.display_name,
                    'address': {
                        'Address': ', '.join([val for val in (partner.street, partner.street2) if val]),
                        'PostCode': self_company.zip,
                        'Town': self_company.city,
                        'Province': self_company.state_id.name if self_company.state_id else self_company.country_id.name,
                        'CountryCode': COUNTRY_CODE_MAP[self_company.country_id.code],
                    },
                    'ContactDetails': {
                        'Telephone': self_company.phone.translate(phone_clean_table) if self_company.phone else False,
                        'WebAdress': self_company.website if self_company.email else False,
                        'ElectronicMail': self_company.email if self_company.email else False,
                    },
                } if self_company.l10n_es_edi_facturae_person_type == 'J' else False,
            },
        })
        partner_party_values.update({
            'TaxIdentification': {
                'PersonTypeCode': partner.l10n_es_edi_facturae_person_type,
                'ResidenceTypeCode': partner.l10n_es_edi_facturae_residence_type,
                'TaxIdentificationNumber': partner.l10n_es_edi_facturae_tax_identifier,
            },
            'Assignee': {
                'LegalEntity': {
                    'CorporateName': partner.name,
                    'TradeName': partner.display_name,
                    'address': {
                        'Address': ', '.join([val for val in (partner.street, partner.street2) if val]),
                        'PostCode': partner.zip,
                        'Town': partner.city,
                        'Province': partner.state_id.name if partner.state_id else partner.country_id.name,
                        'CountryCode': COUNTRY_CODE_MAP[partner.country_id.code],
                    },
                    'ContactDetails': {
                        'Telephone': partner.phone.translate(phone_clean_table) if partner.phone else False,
                        'WebAdress': partner.website if partner.website else False,
                        'ElectronicMail': partner.email if partner.email else False,
                    },
                } if partner.l10n_es_edi_facturae_person_type == 'J' else False,
                'Individual': {
                    'Name': partner_name.firstname,
                    'FirstSurname': partner_name.surname,
                    'SecondSurname': partner_name.surname2,
                    'address': {
                        'Address': ', '.join([val for val in (partner.street, partner.street2) if val]),
                        'PostCode': partner.zip,
                        'Town': partner.city,
                        'Province': partner.state_id.name if partner.state_id else partner.country_id.name,
                        'CountryCode': COUNTRY_CODE_MAP[partner.country_id.code],
                    },
                    'ContactDetails': {
                        'Telephone': partner.phone.translate(phone_clean_table) if partner.phone else False,
                        'WebAdress': partner.website if partner.website else False,
                        'ElectronicMail': partner.email if partner.email else False,
                    },
                } if partner.l10n_es_edi_facturae_person_type == 'F' else False,
            },
        })

        items, taxes, totals = self.l10n_es_edi_facturae_inv_lines_to_items(invoice, conv_rate, need_conv, fmt_curr, fmt_eur)

        template_values.update({
            'Modality': 'I',
            'InvoiceIssuerType': invoice_issuer_type,
            'BatchIdentifier': invoice.name,
            'InvoicesCount': 1,
            'TotalInvoicesAmount': {
                'TotalAmount': fmt_curr(abs(invoice.amount_total_in_currency_signed)),
                'EquivalentInEuros': fmt_eur(invoice.amount_total_signed) if need_conv else False,
            },
            'TotalOutstandingAmount': {
                'TotalAmount': fmt_curr(total_outst_am_in_currency),
                'EquivalentInEuros': fmt_eur(total_outst_am) if need_conv else False,
            },
            'TotalExecutableAmount': {
                'TotalAmount': fmt_curr(total_exec_am_in_currency),
                'EquivalentInEuros': fmt_eur(total_exec_am) if need_conv else False,
            },
            'InvoiceCurrencyCode': inv_curr.name,
            'SellerParty': self_party_values if invoice.move_type == 'out_invoice' else partner_party_values,
            'BuyerParty': self_party_values if invoice.move_type == 'in_invoice' else partner_party_values,
            'Invoices': [{
                'InvoiceNumber': invoice.name,
                'InvoiceDocumentType': 'FC',
                'InvoiceClass': 'OO',
                'InvoiceIssueData': {
                    'IssueDate': invoice.invoice_date.isoformat(),
                    'InvoiceCurrencyCode': inv_curr.name,
                    'ExchangeRateDetails': need_conv,
                    'ExchangeRate': f'{conv_rate:.2f}',
                    'ExchangeRateDate': invoice.date.isoformat(),
                    'TaxCurrencyCode': inv_curr.name,
                    'LanguageName': self._context.get('lang', 'en_US').split('_')[0],
                },
                'TaxOutputs': taxes,
                'TaxesWithheld': [],
                'TotalGrossAmount': fmt_curr(totals['total_gross_amount']),
                'TotalGeneralDiscounts': fmt_curr(totals['total_general_discounts']),
                'TotalGeneralSurcharges': fmt_curr(totals['total_general_surcharges']),
                'TotalGrossAmountBeforeTaxes': fmt_curr(abs(invoice.amount_untaxed_signed) / conv_rate),
                'TotalTaxOutputs': fmt_curr(abs(invoice.amount_total_in_currency_signed - invoice.amount_untaxed_signed) / conv_rate
                ),
                'TotalTaxesWithheld': fmt_curr(totals['total_taxes_withheld']),
                'PaymentsOnAccount': [],
                'TotalOutstandingAmount': fmt_curr(total_outst_am_in_currency),
                'InvoiceTotal': fmt_curr(abs(invoice.amount_total_in_currency_signed)),
                'TotalPaymentsOnAccount': fmt_curr(totals['total_payments_on_account']),
                'AmountsWithheld': {
                    'WithholdingReason': '',
                    'WithholdingRate': False,
                    'WithouldingAmount': fmt_curr(totals['amounts_withheld']),
                } if totals['amounts_withheld'] else False,
                'TotalExecutableAmount': fmt_curr(total_exec_am_in_currency),
                'Items': items,
                'PaymentDetails': [],
                'LegalLiterals': legal_literals,
                'AdditionalData': {'RelatedInvoice': False, 'RelatedDocuments': [], 'Extensions': False, },
            }],
        })
        signature_values.update({'SignerRole': invoice_issuer_signature_type, })
        return template_values, signature_values

    @api.model
    def l10n_es_edi_facturae_render_facturae(self, invoice):
        """
        Produce the Facturae XML file for the invoice.

        :param account.move invoice: The invoice to export.
        :return str: rendered xml file string.
        """
        self_company = invoice.company_id
        template_values, signature_values = self.l10n_es_edi_facturae_export_facturae(invoice)
        xml_content = self.env['ir.qweb']._render('l10n_es_edi_facturae.account_invoice_facturae_export', template_values)
        xml_content = self.l10n_es_edi_facturae_clean_xml(xml_content)
        try:
            certificate = self.env['l10n_es_edi_facturae.certificate'].search([("company_id", '=', self_company.id)], limit=1)
            xml_content = certificate.sign_xml(xml_content, signature_values)
        except IndexError:
            raise UserError(_('No valid certificate found for this company, Facturae EDI file will not be signed.\n'))
        with file_open('l10n_es_edi_facturae/data/Facturaev3_2_1.xsd', 'rb') as xsd:
            # The serial number will fail the xsd check because it is too long for the atomic integer type,
            # this is a bug of the schema, as there should be no boundaries. Hence the hack-fix to still verify the data
            xml_cleaned = xml_content.decode().replace(certificate.serial_number, '1').encode()
            _check_with_xsd(xml_cleaned, xsd)
        return xml_content
