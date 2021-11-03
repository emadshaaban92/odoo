# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def _generate_template_attachments(self, res_ids, render_fields, render_results=None):
        """ Method overridden in order to add an attachment containing the ISR
        to the draft message when opening the 'send by mail' wizard on an invoice.
        This attachment generation will only occur if all the required data are
        present on the invoice. Otherwise, no ISR attachment will be created, and
        the mail will only contain the invoice (as defined in the mother method).
        """
        render_res = super(MailTemplate, self)._generate_template_attachments(res_ids, render_fields, render_results=render_results)

        if self.model != 'account.move':
            return render_res
        if 'attachments' not in render_fields:
            return render_res

        for record in self.env[self.model].browse(res_ids):
            inv_print_name = self._render_field('report_name', record.ids, compute_lang=True)[record.id]
            new_attachments = []

            if record.l10n_ch_isr_valid:
                # We add an attachment containing the ISR
                isr_report_name = 'ISR-' + inv_print_name + '.pdf'
                isr_pdf = self.env.ref('l10n_ch.l10n_ch_isr_report')._render_qweb_pdf(record.ids)[0]
                isr_pdf = base64.b64encode(isr_pdf)
                new_attachments.append((isr_report_name, isr_pdf))

            if record.partner_bank_id._eligible_for_qr_code('ch_qr', record.partner_id, record.currency_id):
                # We add an attachment containing the QR-bill
                qr_report_name = 'QR-bill-' + inv_print_name + '.pdf'
                qr_pdf = self.env.ref('l10n_ch.l10n_ch_qr_report')._render_qweb_pdf(record.ids)[0]
                qr_pdf = base64.b64encode(qr_pdf)
                new_attachments.append((qr_report_name, qr_pdf))

            render_res[record.id]['attachments'] += new_attachments

        return render_res
