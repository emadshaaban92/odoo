# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from ast import literal_eval
from odoo import api, fields, models
from odoo.osv import expression


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    mass_mailing_id = fields.Many2one('mailing.mailing', string='Mass Mailing', ondelete='cascade')
    campaign_id = fields.Many2one('utm.campaign', string='Mass Mailing Campaign', ondelete='set null')
    mass_mailing_name = fields.Char(string='Mass Mailing Name', help='If set, a mass mailing will be created so that you can track its results in the Email Marketing app.')
    mailing_list_ids = fields.Many2many('mailing.list', string='Mailing List')
    model_is_thread = fields.Boolean(compute='_compute_model_is_thread')

    @api.depends('model')
    def _compute_model_is_thread(self):
        for composer in self:
            model = self.env['ir.model']._get(composer.model)
            composer.model_is_thread = model.is_mail_thread

    def get_mail_values(self, res_ids):
        """ Override method that generated the mail content by creating the
        mailing.trace values in the o2m of mail_mail, when doing pure
        email mass mailing. """
        self.ensure_one()
        res = super(MailComposeMessage, self).get_mail_values(res_ids)
        # use only for allowed models in mass mailing
        if self._should_add_traces():
            mass_mailing = self.mass_mailing_id
            if not mass_mailing:
                mass_mailing = self.env['mailing.mailing'].create(
                    self._prepare_mailing_values()
                )
                self.mass_mailing_id = mass_mailing.id

            recipients_info = self._process_recipient_values(res)
            # if not keeping archive, delete messages (consistent with not logging SMS)
            self.auto_delete_message = not mass_mailing.keep_archives
            for res_id in res_ids:
                mail_values = res[res_id]
                if mail_values.get('body_html'):
                    body = self.env['ir.qweb']._render(
                        'mass_mailing.mass_mailing_mail_layout',
                        {'body': mail_values['body_html']},
                        minimal_qcontext=True,
                        raise_if_not_found=False
                    )
                    if body:
                        mail_values['body_html'] = body

                traces_vals = [{
                    'email': email,
                    'mass_mailing_id': mass_mailing.id,
                    'model': self.model,
                    'res_id': res_id,
                } for email in (recipients_info[res_id]['mail_to'] or [''])]  # if mail_to is void, keep falsy values to allow searching / debugging traces

                # propagate failed states to trace when still-born
                for trace_vals in traces_vals:
                    if mail_values.get('state') == 'cancel':
                        trace_vals['trace_status'] = 'cancel'
                    elif mail_values.get('state') == 'exception':
                        trace_vals['trace_status'] = 'error'
                    if mail_values.get('failure_type'):
                        trace_vals['failure_type'] = mail_values['failure_type']

                mail_values.update({
                    'auto_delete': not mass_mailing.keep_archives,
                    # email-mode: keep original message for routing
                    'is_notification': mass_mailing.reply_to_mode == 'update',
                    'mailing_id': mass_mailing.id,
                    'mailing_trace_ids': [(0, 0, trace_vals) for trace_vals in traces_vals],
                })
                # we need to keep mails to link messages to traces with archives
                # we do not need to keep mails if we do not want archives
                mail_values['auto_delete'] = not mass_mailing.keep_archives

        return res

    def _get_mail_values_auto_delete(self):
        if self.mass_mailing_id.keep_archives:
            return False
        return super()._get_mail_values_auto_delete()

    def _should_add_traces(self):
        return self.composition_mode == 'mass_mail' and \
            (self.mass_mailing_name or self.mass_mailing_id) and \
            self.model_is_thread

    def _get_done_emails(self, mail_values_dict):
        seen_list = super(MailComposeMessage, self)._get_done_emails(mail_values_dict)
        if self.mass_mailing_id:
            seen_list += self.mass_mailing_id._get_seen_list()
        return seen_list

    def _get_optout_emails(self, mail_values_dict):
        opt_out_list = super(MailComposeMessage, self)._get_optout_emails(mail_values_dict)
        if self.mass_mailing_id:
            opt_out_list += self.mass_mailing_id._get_opt_out_list()
        return opt_out_list

    def _prepare_mailing_values(self):
        now = fields.Datetime.now()

        active_ids = self._context.get('active_ids')
        # add active_ids to domain so that it doesn't resend on records that were not selected
        if active_ids:
            active_ids_domain = [('id', 'in', active_ids)]
            current_active_domain = literal_eval(self.active_domain) if self.active_domain else []
            enhanced_active_domain = expression.AND([current_active_domain, active_ids_domain])

        return {
            'attachment_ids': [(6, 0, self.attachment_ids.ids)],
            'body_html': self.body,
            'campaign_id': self.campaign_id.id,
            'keep_archives': not self.auto_delete_message,
            'mailing_model_id': self.env['ir.model']._get(self.model).id,
            'mailing_domain': enhanced_active_domain,
            'name': self.mass_mailing_name,
            'reply_to': self.reply_to if self.reply_to_mode == 'new' else False,
            'reply_to_mode': 'new' if self.auto_delete_message else 'update',  # if creating a new mailing and not archiving, reply as mails
            'sent_date': now,
            'state': 'done',
            'subject': self.subject,
            'user_id': next(iter(self.author_id.user_ids.ids), None),
        }

    def _action_send_mail_create_notifications(self, *args):
        # Notifications not needed, information gathered through traces
        if not self._should_add_traces():
            super()._action_send_mail_create_notifications(*args)
