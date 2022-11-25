# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import json
import re

from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_ke_cu_datetime = fields.Datetime(string='CU Signing Date and Time')
    l10n_ke_cu_serial_number = fields.Char(string='CU Serial Number')
    l10n_ke_cu_invoice_number = fields.Char(string='CU Invoice Number', copy=False)
    l10n_ke_cu_qrcode = fields.Char(string='CU QR Code', copy=False)

    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------

    def _l10n_ke_fmt(self, string, length, ljust=True):
        """ Function for common formatting behaviour

        :param string: string to be formatted/encoded
        :param length: integer length to justify (if enabled), and then truncate the string to
        :param ljust:  boolean representing whether the string should be justified
        :returns:      byte-string justified/truncated, with all non-alphanumeric characters removed
        """
        if not string:
            string = ''
        return re.sub('[^A-Za-z0-9 ]+', '', str(string)).encode('cp1251').ljust(length if ljust else 0)[:length]

    # -------------------------------------------------------------------------
    # CHECKS
    # -------------------------------------------------------------------------

    def _l10n_ke_validate_move(self):
        """ Returns list of misconfigurations on the move that would cause rejection by the KRA """
        self.ensure_one()
        errors = []
        # The credit note / debit note should refer to the control unit number (reciept number)
        # of the original invoice to which it relates.
        if self.move_type == 'out_refund' and not self.reversed_entry_id.l10n_ke_cu_invoice_number:
            errors.append(_("This credit note must reference the previous invoice, and this previous invoice must have already been submitted."))
        return errors

    def _l10n_ke_validate_lines(self):
        """ Returns list of misconfigurations on the lines of the move that would cause rejection by the KRA """
        self.ensure_one()
        errors = []
        for line in self.invoice_line_ids.filtered(lambda l: not l.display_type):
            if not line.tax_ids or len(line.tax_ids) > 1:
                errors.append(_("On line %s, you must select one and only one tax.", line.name))
            else:
                if line.tax_ids[0].amount != 16 and not (line.product_id and line.product_id.l10n_ke_hsn_code and line.product_id.l10n_ke_hsn_name):
                    errors.append(_("On line %s, a product with a HS Code and HS Name must be selected, since the tax is 8%%, 0%% or exempt.", line.name))
        return errors

    def _l10n_ke_validate_taxes(self):
        """ Returns list of misconfigurations on the taxes of the move that would cause rejection by the KRA """
        self.ensure_one()
        errors = []
        for tax in self.invoice_line_ids.tax_ids:
            if tax.amount not in (16, 8, 0):
                errors.append(_("Tax '%s' is used, but only taxes of 16%%, 8%%, 0%% or Exempt can be sent. Please reconfigure or change the tax.", tax.name))
        return errors


    # -------------------------------------------------------------------------
    # SERIALISERS
    # -------------------------------------------------------------------------

    def _l10n_ke_cu_open_invoice_message(self):
        """ Serialise the required fields for opening an invoice

        :returns: a list containing one byte-string representing the <CMD> and
                  <DATA> of the message sent to the fiscal device.
        """
        headquarter_address = (self.commercial_partner_id.street or '') + (self.commercial_partner_id.street2 or '')
        customer_address = (self.partner_id.street or '') + (self.partner_id.street2 or '')
        postcode_and_city = self.partner_id.zip or '' + ' ' +  self.partner_id.city or ''
        invoice_elements = [
            b'1',                                                   # Reserved - 1 symbol with value '1'
            b'     0',                                              # Reserved - 1 symbol with value ‘     0’
            b'0',                                                   # Reserved - 1 symbol with value '0'
            b'1' if self.move_type == 'out_invoice' else b'A',      # 1 symbol with value '1' (new invoice), 'A' (credit note), or '@' (debit note)
            self._l10n_ke_fmt(self.commercial_partner_id.name, 30), # 30 symbols for Company name
            self._l10n_ke_fmt(self.commercial_partner_id.vat, 14),  # 14 Symbols for the client PIN number
            self._l10n_ke_fmt(headquarter_address, 30),             # 30 Symbols for customer headquarters
            self._l10n_ke_fmt(customer_address, 30),                # 30 Symbols for the address
            self._l10n_ke_fmt(postcode_and_city, 30),               # 30 symbols for the customer post code and city
            self._l10n_ke_fmt('', 30),                              # 30 symbols for the exemption number
        ]
        if self.move_type in ('out_refund', 'debit_note'):
            invoice_elements.append(self._l10n_ke_fmt(self.reversed_entry_id.l10n_ke_cu_invoice_number, 19)), # 19 symbols for related invoice number
        invoice_elements.append(self._l10n_ke_fmt(self.name, 15))   # 15 symbols for trader system invoice number

        # CMD_OPEN_FISCAL_RECORD = 0x30
        return [b'\x30' + b';'.join(invoice_elements)]

    def _l10n_ke_cu_lines_messages(self):
        """ Serialise the data of each line on the invoice

        This function transforms the lines in order to handle the differences
        between the KRA expected data and the lines in odoo.

        If a discount line (as a negative line) has been added to the invoice
        lines, find a suitable line/lines to distribute the discount accross

        :returns: List of byte-strings representing each command <CMD> and the
                  <DATA> of the line, which will be sent to the fiscal device
                  in order to add a line to the opened invoice.
        """
        def is_discount_line(line):
            return line.price_unit < 0.0

        def is_candidate(discount_line, other_line):
            """ If the of one line match those of the discount line, the discount can be distributed accross that line """
            discount_taxes = discount_line.tax_ids.flatten_taxes_hierarchy()
            other_line_taxes = other_line.tax_ids.flatten_taxes_hierarchy()
            return set(discount_taxes.ids) == set(other_line_taxes.ids)

        lines = self.invoice_line_ids.filtered(lambda l: not l.display_type and l.quantity and l.price_total)
        discount_dict = {line.id: line.discount for line in lines if line.price_total > 0}
        for line in lines:
            if not is_discount_line(line):
                continue
            # Search for non-discount lines
            candidate_vals_list = [l for l in lines if not is_discount_line(l) and is_candidate(l, line)]
            candidate_vals_list = sorted(candidate_vals_list, key=lambda x: x.price_unit * x.quantity, reverse=True)
            line_to_discount = abs(line.price_unit * line.quantity)
            for candidate in candidate_vals_list:
                still_to_discount = abs(candidate.price_unit * candidate.quantity * (100.0 - discount_dict[candidate.id]) / 100.0)
                if line_to_discount >= still_to_discount:
                    discount_dict[candidate.id] = 100.0
                    line_to_discount -= still_to_discount
                else:
                    rest_to_discount = abs((line_to_discount / (candidate.price_unit * candidate.quantity)) * 100.0)
                    discount_dict[candidate.id] += rest_to_discount
                    break

        vat_class = {16.0: 'A', 8.0: 'B'}
        msgs = []
        for line in self.invoice_line_ids.filtered(lambda l: not l.display_type and l.quantity and l.price_total > 0 and not discount_dict.get(l.id) >= 100):
            # Here we use the original discount of the line, since it the distributed discount has not been applied in the price_total
            price = round(line.price_total / line.quantity * 100 / (100-line.discount), 2)
            percentage = line.tax_ids[0].amount

            # Letter to classify tax, 0% taxes are handled conditionally, as the tax can be zero-rated or exempt
            letter = ''
            if percentage in vat_class:
                letter = vat_class[percentage]
            else:
                report_line_ids = line.tax_ids[0].invoice_repartition_line_ids.filtered(lambda r: r.repartition_type == 'base').tag_ids.tax_report_line_ids.ids
                letter = 'E' if self.env.ref('l10n_ke.tax_report_line_exempt_sales_base', raise_if_not_found=False).id in report_line_ids else 'C'

            uom = line.product_uom_id and line.product_uom_id.name or ''
            if letter != 'A':
                hscode = line.product_id.l10n_ke_hsn_code
                hsname = line.product_id.l10n_ke_hsn_name
            else:
                hscode = ''
                hsname = ''
            line_data = b';'.join([
                self._l10n_ke_fmt(line.name, 36),               # 36 symbols for the article's name
                self._l10n_ke_fmt(letter, 1),                   # 1 symbol for article's vat class ('A', 'B', 'C', 'D', or 'E')
                str(price)[:13].encode('cp1251'),                # 1 to 13 symbols for article's price
                self._l10n_ke_fmt(uom, 3),                      # 3 symbols for unit of measure
                self._l10n_ke_fmt(hscode, 10),                  # 10 symbols for HS code in the format xxxx.xx.xx (can be empty)
                self._l10n_ke_fmt(hsname, 20),                  # 20 symbols for the HS name (can be empty)
                str(percentage).encode('cp1251')[:5]             # up to 5 symbols for vat rate
            ])

            # 1 to 10 symbols for quantity
            line_data += b'*' + str(line.quantity).encode('cp1251')[:10]
            if discount_dict[line.id]:
                # 1 to 7 symbols for percentage of discount/addition
                discount_sign = b'-' if discount_dict[line.id] > 0 else b'+'
                discount = discount_sign + str(abs(discount_dict[line.id])).encode('cp1251')[:6]
                line_data += b',' + discount + b'%'

            # Command: Sale of article (0x31)
            msgs += [b'\x31' + line_data]
        return msgs

    def _l10n_ke_cu_message(self):
        self.ensure_one()
        # Check the configuration of the invoice
        errors = self._l10n_ke_validate_move() + self._l10n_ke_validate_lines() + self._l10n_ke_validate_taxes()
        if errors:
            raise UserError(_("Invalid invoice configuration:\n\n%s") % '\n'.join(errors))

        msgs = self._l10n_ke_cu_open_invoice_message()
        msgs += self._l10n_ke_cu_lines_messages()
        # CMD_CLOSE_FISCAL_RECEIPT = 0x38
        msgs += [b'\x38']
        return msgs

    # -------------------------------------------------------------------------
    # POST COMMANDS / RECEIVE DATA
    # -------------------------------------------------------------------------

    def l10n_ke_action_cu_post(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'post_send',
            'params': {
                'messages': json.dumps([m.decode('cp1251') for m in self._l10n_ke_cu_message()]),
                'move_id': self.id,
                'proxy_address': self.company_id.l10n_ke_cu_proxy_address,
                'company_vat': self.company_id.vat,
            }
        }

    def l10n_ke_cu_response(self, response):
        move = self.browse(response['move_id'])
        replies = [msg for msg in response['replies']]
        move.update({
            'l10n_ke_cu_serial_number': response['serial_number'],
            'l10n_ke_cu_invoice_number': replies[-1].split(';')[0],
            'l10n_ke_cu_qrcode': replies[-1].split(';')[1].strip(),
            'l10n_ke_cu_datetime': fields.Datetime.now(),
        })
