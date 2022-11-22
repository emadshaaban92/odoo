# -*- coding: utf-8 -*-
import base64
import io
from PyPDF2 import PdfFileReader, PdfFileWriter

from odoo import _, api, fields, models, tools, Command
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang


class AccountMoveSend(models.TransientModel):
    _name = 'account.move.send'
    _description = "Account Move Send"

    company_id = fields.Many2one(comodel_name='res.company')
    move_ids = fields.Many2many(comodel_name='account.move')
    mode = fields.Selection(
        selection=[
            ('invoice_single', "Invoice Single"),
            ('invoice_multi', "Invoice Multi"),
        ],
        compute='_compute_mode',
    )
    button_name = fields.Char(compute='_compute_button_name')

    # == PRINT ==
    enable_download = fields.Boolean(compute='_compute_enable_download')
    download = fields.Boolean(
        string="Download",
        compute='_compute_download',
        store=True,
        readonly=False,
    )

    # == MAIL ==
    display_mail_composer = fields.Boolean(compute='_compute_send_mail_extra_fields')
    enable_send_mail = fields.Boolean(compute='_compute_send_mail_extra_fields')
    send_mail_warning_message = fields.Text(compute='_compute_send_mail_extra_fields')
    send_mail_readonly = fields.Boolean(compute='_compute_send_mail_extra_fields')
    send_mail = fields.Boolean(
        string="Email",
        compute='_compute_send_mail',
        store=True,
        readonly=False,
    )

    mail_template_id = fields.Many2one(
        comodel_name='mail.template',
        string="Use template",
        domain="[('model', '=', 'account.move')]",
    )
    mail_lang = fields.Char(
        string="Lang",
        compute='_compute_mail_lang',
    )
    mail_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Recipients",
        domain=[('type', '!=', 'private')],
        compute='_compute_mail_partner_ids',
        store=True,
        readonly=False,
    )
    mail_subject = fields.Char(
        string="Subject",
        compute='_compute_mail_subject',
        store=True,
        readonly=False,
    )
    mail_body = fields.Html(
        string="Contents",
        sanitize_style=True,
        compute='_compute_mail_body',
        store=True,
        readonly=False,
    )

    allow_pdf_needed = fields.Boolean(
        compute='_compute_allow_pdf_needed',
        store=True,
        readonly=False,
    )
    pdf_needed = fields.Boolean(default=True)
    pdf_needed_message = fields.Text(compute='_compute_pdf_needed_message')
    mail_attachments_widget = fields.Json(
        compute='_compute_mail_attachments_widget',
        store=True,
        readonly=False,
    )

    def _get_mail_default_field_value_from_template(self, move, field, **kwargs):
        self.ensure_one()
        return self.mail_template_id\
            .with_context(lang=self.mail_lang)\
            ._render_field(field, move.ids, **kwargs)[move._origin.id]

    @api.model
    def default_get(self, fields_list):
        # EXTENDS 'base'
        results = super().default_get(fields_list)

        if 'move_ids' in fields_list and 'move_ids' not in results:
            results['move_ids'] = [Command.set(self._context.get('active_ids', []))]

        if 'move_ids' in results:
            moves = self.env['account.move'].browse(results['move_ids'][0][2])
            if len(moves.company_id) > 1:
                raise UserError(_("You can only send from the same company."))
            results['company_id'] = moves.company_id.id

        return results

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.model
    def _get_mode_from_moves(self, moves):
        self.ensure_one()
        if all(x.is_invoice(include_receipts=True) for x in moves):
            return 'invoice_single' if len(moves) == 1 else 'invoice_multi'
        return None

    @api.depends('move_ids')
    def _compute_mode(self):
        for wizard in self:
            if wizard.move_ids:
                wizard.mode = wizard._get_mode_from_moves(wizard.move_ids)
            else:
                raise UserError(_("You can only send invoices."))

    @api.depends('enable_download', 'download', 'enable_send_mail', 'send_mail')
    def _compute_button_name(self):
        for wizard in self:
            actions = []
            if wizard.enable_send_mail and wizard.send_mail:
                actions.append(_("Send"))
            if wizard.enable_download and wizard.download:
                actions.append(_("Print"))
            wizard.button_name = " & ".join(actions) if actions else None

    @api.depends('mode')
    def _compute_enable_download(self):
        for wizard in self:
            wizard.enable_download = wizard.mode in ('invoice_single', 'invoice_multi')

    @api.depends('enable_download')
    def _compute_download(self):
        for wizard in self:
            wizard.download = wizard.company_id.invoice_is_print

    @api.depends('mode')
    def _compute_send_mail_extra_fields(self):
        for wizard in self:
            wizard.enable_send_mail = wizard.mode in ('invoice_single', 'invoice_multi')
            wizard.display_mail_composer = wizard.mode == 'invoice_single'
            send_mail_readonly = False

            display_messages = []
            if wizard.enable_send_mail:
                invoices_without_mail_data = wizard.move_ids.filtered(lambda x: not x.partner_id.email)
                if invoices_without_mail_data:
                    if wizard.mode == 'invoice_multi':
                        display_messages.append(_(
                            "The following invoice(s) will not be sent by email, because the customers don't have email "
                            "address: "
                        ))
                        display_messages.append(", ".join(invoices_without_mail_data.mapped('name')))
                        send_mail_readonly = True
                    else:
                        display_messages.append(_("Please add an email address for your partner"))

            wizard.send_mail_readonly = send_mail_readonly
            wizard.send_mail_warning_message = "".join(display_messages) if display_messages else None

    @api.depends('mode')
    def _compute_send_mail(self):
        for wizard in self:
            wizard.send_mail = wizard.company_id.invoice_is_email and not wizard.send_mail_readonly

    @api.depends('mail_template_id')
    def _compute_mail_lang(self):
        for wizard in self:
            if wizard.mail_template_id:
                wizard.mail_lang = wizard.mail_template_id._render_lang([0])[0]
            else:
                wizard.mail_lang = get_lang(self.env).code

    def _get_invoice_mail_partner_ids(self, invoice):
        self.ensure_one()
        template = self.mail_template_id
        partners = self.env['res.partner'].with_company(invoice.company_id)
        if template.email_to:
            for mail_data in tools.email_split(template.email_to):
                partners |= partners.find_or_create(mail_data)
        if template.email_cc:
            for mail_data in tools.email_split(template.email_cc):
                partners |= partners.find_or_create(mail_data)
        if template.partner_to:
            partner_to = self._get_mail_default_field_value_from_template(invoice, 'partner_to')
            partner_ids = [int(pid) for pid in partner_to.split(',') if pid]
            partners |= self.env['res.partner'].sudo().browse(partner_ids).exists()
        return partners

    @api.depends('company_id', 'mail_template_id')
    def _compute_mail_partner_ids(self):
        for wizard in self:
            template = wizard.mail_template_id
            if template and wizard.mode == 'invoice_single':
                wizard.mail_partner_ids = wizard._get_invoice_mail_partner_ids(wizard.move_ids)
            else:
                wizard.mail_partner_ids = []

    def _get_invoice_mail_subject(self, invoice):
        self.ensure_one()
        return self._get_mail_default_field_value_from_template(invoice, 'subject')

    @api.depends('mail_template_id', 'mail_lang')
    def _compute_mail_subject(self):
        for wizard in self:
            if wizard.mail_template_id and wizard.mode == 'invoice_single':
                wizard.mail_subject = wizard._get_invoice_mail_subject(wizard.move_ids)
            else:
                wizard.mail_subject = None

    def _get_invoice_mail_body(self, invoice):
        self.ensure_one()
        return self._get_mail_default_field_value_from_template(invoice, 'body_html', options={'post_process': True})

    @api.depends('mail_template_id', 'mail_lang')
    def _compute_mail_body(self):
        for wizard in self:
            if wizard.mail_template_id and wizard.mode == 'invoice_single':
                wizard.mail_body = wizard._get_invoice_mail_body(wizard.move_ids)
            else:
                wizard.mail_body = None

    def _get_invoice_mail_attachments_data(self, invoice):
        self.ensure_one()
        results = []
        report = self.mail_template_id.report_template

        if report and invoice.pdf_report_id:
            attachment = invoice.pdf_report_id
            results.append({
                'id': attachment.id,
                'name': attachment.name,
                'mimetype': attachment.mimetype,
            })

        for attachment in self.mail_template_id.attachment_ids:
            results.append({
                'id': attachment.id,
                'name': attachment.name,
                'mimetype': attachment.mimetype,
            })

        return results

    @api.depends('mail_template_id', 'mail_lang')
    def _compute_mail_attachments_widget(self):
        for wizard in self:
            if wizard.mode == 'invoice_single':
                wizard.mail_attachments_widget = wizard._get_invoice_mail_attachments_data(wizard.move_ids)
            else:
                wizard.mail_attachments_widget = []

    @api.depends('move_ids')
    def _compute_allow_pdf_needed(self):
        for wizard in self:
            wizard.allow_pdf_needed = wizard.mode == 'invoice_single' and \
                                      not wizard.move_ids.pdf_report_id \
                                      and wizard.move_ids.state == 'posted'

    def _get_invoice_pdf_messages(self):
        self.ensure_one()
        return [_("Generate the invoice PDF document")]

    @api.depends('move_ids')
    def _compute_pdf_needed_message(self):
        for wizard in self:
            if wizard.mode == 'invoice_single':
                wizard.pdf_needed_message = "".join(wizard._get_invoice_pdf_messages())
            else:
                wizard.pdf_needed_message = None

    # -------------------------------------------------------------------------
    # BUSINESS ACTIONS
    # -------------------------------------------------------------------------

    @api.model
    def _create_invoice_pdf_report_attachment(self, invoice):
        self.ensure_one()

        result, _report_format = self.env['ir.actions.report']._render(
            'account.account_invoices_without_payment',
            invoice.ids,
        )

        filename = f"{invoice.name.replace('/', '_')}.pdf"
        return self.env['ir.attachment'].create({
            'name': filename,
            'raw': result,
            'res_model': invoice._name,
            'res_id': invoice.id,
        })

    def action_send_and_print(self):
        self.ensure_one()

        # Ensure the invoice report is generated.
        for move in self.move_ids:
            if self.mode == 'invoice_multi' \
                or (self.mode == 'invoice_single' and self.allow_pdf_needed and self.pdf_needed):
                pdf_report = self._create_invoice_pdf_report_attachment(move)
                move._set_pdf_report(pdf_report)

        # Send mail.
        if self.enable_send_mail and self.send_mail:
            subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')

            for move in self.move_ids:

                if self.mode == 'invoice_single':
                    attachment_ids = [
                        attachment_vals['id']
                        for attachment_vals in self.mail_attachments_widget or []
                    ]
                    partners = self.mail_partner_ids
                    body = self.mail_body
                    subject = self.mail_subject
                else:
                    attachment_ids = [
                        attachment_vals['id']
                        for attachment_vals in self._get_invoice_mail_attachments_data(move)
                    ]
                    partners = self._get_invoice_mail_partner_ids(move)
                    body = self._get_invoice_mail_body(move)
                    subject = self._get_invoice_mail_subject(move)
                attachment_ids.append(move.pdf_report_id.id)

                email_from = self._get_mail_default_field_value_from_template(move, 'email_from')

                move\
                    .with_context({
                        'no_new_invoice': True,
                        'mail_notify_author': self.env.user.partner_id in partners,
                        'mailing_document_based': True,
                    })\
                    .message_post(
                        body=body or '',
                        subject=subject,
                        message_type='comment',
                        email_from=email_from,
                        subtype_id=subtype_id,
                        partner_ids=partners.ids,
                        attachment_ids=attachment_ids,
                        **{
                            'email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
                            'email_add_signature': not self.mail_template_id,
                            'mail_auto_delete': self.mail_template_id.auto_delete,
                            'mail_server_id': self.mail_template_id.mail_server_id.id,
                            'reply_to_force_new': False,
                        },
                    )

            self.move_ids.write({'is_move_sent': True})

        # Print.
        if self.enable_download and self.download:
            attachments = self.move_ids.pdf_report_id

            if len(attachments) == 1:
                attachment = self.move_ids.pdf_report_id
            else:
                writer = PdfFileWriter()
                for attachment in attachments:
                    reader = PdfFileReader(io.BytesIO(base64.decodebytes(attachment.datas)), strict=False)
                    writer.appendPagesFromReader(reader)

                with io.BytesIO() as buffer:
                    writer.write(buffer)
                    data = buffer.getvalue()

                attachment = self.env['ir.attachment'].create({
                    'name': _("Invoices"),
                    'raw': data,
                })

            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'close_on_report_download': True,
            }

        return {'type': 'ir.actions.act_window_close'}

    def action_save_as_template(self):
        self.ensure_one()

        model = self.env['ir.model']._get('account.move')
        template_name = _("Invoice: %s", tools.ustr(self.mail_subject))
        attachment_ids = [attachment_vals['id'] for attachment_vals in self.mail_attachments_widget]

        self.mail_template_id = self.env['mail.template'].create({
            'name': template_name,
            'subject': self.mail_subject,
            'body_html': self.mail_body,
            'model_id': model.id,
            'attachment_ids': [Command.set(attachment_ids)],
            'use_default_to': True,
        })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': self._name,
            'target': 'new',
            'context': self._context,
        }
