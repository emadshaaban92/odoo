# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import ast
import base64
import logging

from odoo import _, api, fields, models, tools, Command
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import email_re

_logger = logging.getLogger(__name__)


def _reopen(self, res_id, model, context=None):
    # save original model in context, because selecting the list of available
    # templates requires a model in context
    context = dict(context or {}, default_model=model)
    return {'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': res_id,
            'res_model': self._name,
            'target': 'new',
            'context': context,
            }


class MailComposer(models.TransientModel):
    """ Generic message composition wizard. You may inherit from this wizard
        at model and view levels to provide specific features.

        The behavior of the wizard depends on the composition_mode field:
        - 'comment': post on a record. The wizard is pre-populated via ``get_record_data``
        - 'mass_mail': wizard in mass mailing mode where the mail details can
            contain template placeholders that will be merged with actual data
            before being sent to each recipient.
    """
    _name = 'mail.compose.message'
    _inherit = 'mail.composer.mixin'
    _description = 'Email composition wizard'
    _log_access = True
    _batch_size = 500

    @api.model
    def default_get(self, fields_list):
        """ Handle composition mode and contextual computation, until moving
        to computed fields. Support active_model / active_id(s) as valid default
        values, as this comes from standard web client usage.

        Note that supporting active_ids through composer is still done, as we
        may have to give a huge list of IDs that won't fit into res_ids field.
        """
        # support subtype xmlid, like ``message_post``, when easier than using ``ref``
        if self.env.context.get('default_subtype_xmlid'):
            self = self.with_context(
                default_subtype_id=self.env['ir.model.data']._xmlid_to_res_id(
                    self.env.context['default_subtype_xmlid']
                )
            )
        # deprecated record context management
        if 'default_res_id' in self.env.context:
            raise ValueError(_("Deprecated usage of 'default_res_id', should use 'default_res_ids'."))

        result = super().default_get(fields_list)

        # record context management
        if 'model' in fields_list and 'model' not in result:
            result['model'] = self.env.context.get('active_model')
        if 'res_ids' in fields_list and 'res_ids' not in result:
            if self.env.context.get('active_ids'):
                active_res_ids = self._parse_res_ids(self.env.context['active_ids'])
                # beware, field is limited in storage, usage of active_ids in context still required
                if active_res_ids and len(active_res_ids) <= self._batch_size:
                    result['res_ids'] = self.env.context['active_ids']
            elif self.env.context.get('active_id'):
                result['res_ids'] = [self.env.context['active_id']]
            else:
                result['res_ids'] = False
        # record / parent based computation
        if result.get('composition_mode') == 'comment' and (set(fields_list) & {'model', 'res_ids', 'partner_ids'}):
            result.update(self.get_record_data(result))

        # when being in new mode, create_uid is not granted -> ACLs issue may arise
        if 'create_uid' in fields_list and 'create_uid' not in result:
            result['create_uid'] = self.env.uid

        return {
            fname: result[fname]
            for fname in result if fname in fields_list
        }

    # content
    subject = fields.Char('Subject', compute='_compute_subject', readonly=False, store=True)
    body = fields.Html(
        'Contents', render_engine='qweb', render_options={'post_process': True}, sanitize_style=True,
        compute='_compute_body', readonly=False, store=True)
    parent_id = fields.Many2one(
        'mail.message', 'Parent Message', ondelete='set null')
    template_id = fields.Many2one('mail.template', 'Use template', domain="[('model', '=', model)]")
    attachment_ids = fields.Many2many(
        'ir.attachment', 'mail_compose_message_ir_attachments_rel',
        'wizard_id', 'attachment_id', 'Attachments')
    email_layout_xmlid = fields.Char('Email Notification Layout', copy=False)
    email_add_signature = fields.Boolean(default=True)
    # origin
    email_from = fields.Char(
        'From', compute='_compute_email_from', readonly=False, store=True,
        help="Email address of the sender. This field is set when no matching partner is found and replaces the author_id field in the chatter.")
    author_id = fields.Many2one(
        'res.partner', string='Author',
        compute='_compute_author_id', readonly=False, store=True,
        help="Author of the message. If not set, email_from may hold an email address that did not match any partner.")
    # composition
    composition_mode = fields.Selection(
        selection=[('comment', 'Post on a document'),
                   ('mass_mail', 'Email Mass Mailing')],
        string='Composition mode', default='comment')
    composition_batch = fields.Boolean(
        'Batch composition', compute='_compute_composition_batch')  # more than 1 record (raw source)
    model = fields.Char('Related Document Model')
    res_ids = fields.Text('Related Document IDs')
    res_domain = fields.Text('Active domain')
    res_domain_user_id = fields.Many2one(
        'res.users', string='Responsible',
        help='Used as context used to evaluate composer domain')
    record_name = fields.Char(
        'Record Name',
        compute='_compute_record_name', readonly=False, store=True)  # useful only in monorecord comment mode
    # characteristics
    message_type = fields.Selection([
        ('comment', 'Comment'),
        ('notification', 'System notification')],
        'Type', required=True, default='comment',
        help="Message type: email for email message, notification for system "
             "message, comment for other messages such as user replies")
    subtype_id = fields.Many2one(
        'mail.message.subtype', 'Subtype', ondelete='set null',
        default=lambda self: self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment'))
    mail_activity_type_id = fields.Many2one('mail.activity.type', 'Mail Activity Type', ondelete='set null')
    # destination
    reply_to = fields.Char(
        'Reply To', compute='_compute_reply_to', readonly=False, store=True,
        help='Reply email address. Setting the reply_to bypasses the automatic thread creation.')
    reply_to_force_new = fields.Boolean(
        string='Considers answers as new thread',
        compute='_compute_reply_to_force_new', readonly=False, store=True,
        help='Manage answers as new incoming emails instead of replies going to the same thread.')
    reply_to_mode = fields.Selection([
        ('update', 'Store email and replies in the chatter of each record'),
        ('new', 'Collect replies on a specific email address')],
        string='Replies', compute='_compute_reply_to_mode', inverse='_inverse_reply_to_mode',
        help="Original Discussion: Answers go in the original document discussion thread. \n Another Email Address: Answers go to the email address mentioned in the tracking message-id instead of original document discussion thread. \n This has an impact on the generated message-id.")
    # recipients
    partner_ids = fields.Many2many(
        'res.partner', 'mail_compose_message_res_partner_rel',
        'wizard_id', 'partner_id', 'Additional Contacts',
        domain=[('type', '!=', 'private')])
    # sending
    auto_delete = fields.Boolean(
        'Delete Emails',
        compute="_compute_auto_delete", readonly=False, store=True,
        help='This option permanently removes any track of email after it\'s been sent, including from the Technical menu in the Settings, in order to preserve storage space of your Odoo database.')
    auto_delete_keep_log = fields.Boolean(
        'Keep Message Copy', default=True,
        help='Do not keep a copy of the email in the document communication history (mass mailing only)')
    mail_server_id = fields.Many2one('ir.mail_server', 'Outgoing mail server')
    scheduled_date = fields.Char(
        'Scheduled Date',
        help="In comment mode: if set, postpone notifications sending. "
             "In mass mail mode: if sent, send emails after that date. "
             "This date is considered as being in UTC timezone.")

    @api.constrains('res_ids')
    def _check_res_ids(self):
        """ Check res_ids is a valid list of integers (or Falsy). """
        for composer in self:
            composer._evaluate_res_ids()

    @api.constrains('res_domain')
    def _check_res_domain(self):
        """ Check domain is a valid domain if set (otherwise it is considered
        as a Falsy leaf. """
        for composer in self:
            composer._evaluate_res_domain()

    @api.depends('composition_mode', 'model', 'parent_id', 'res_ids',
                 'template_id')
    def _compute_subject(self):
        for composer in self:
            if composer.template_id.subject:
                composer._set_value_from_template('subject')
            elif (not composer.template_id or not composer.subject):
                if composer.composition_mode == 'mass_mail':
                    composer.subject = False
                    continue
                subject = composer.parent_id.subject
                if not subject:
                    res_ids = composer._evaluate_res_ids()
                    if len(res_ids) == 1:
                        subject = self.env[composer.model].browse(res_ids)._message_compute_subject()
                composer.subject = subject

    @api.depends('composition_mode', 'model', 'res_ids', 'template_id')
    def _compute_body(self):
        """ When changing template, update body (rendered in comment or raw in
        mass mode). When removing template, reset body otherwise mail content
        may not be complete. """
        for composer in self:
            if composer.template_id.body_html:
                composer._set_value_from_template('body_html', 'body')
            elif not composer.template_id or not composer.body:
                composer.body = False

    @api.depends('author_id', 'composition_mode', 'model', 'res_ids', 'template_id')
    def _compute_email_from(self):
        for composer in self:
            if composer.template_id.email_from:
                composer._set_value_from_template('email_from')
            elif not composer.template_id:
                composer.email_from = self.env.user.partner_id.email_formatted
                # directly update author_id, fields are inter dependent
                composer.author_id = self.env.user.partner_id
            elif not composer.email_from and composer.author_id:
                composer.email_from = composer.author_id.email_formatted

    @api.depends('composition_mode', 'email_from', 'model', 'res_ids')
    def _compute_author_id(self):
        for composer in self.filtered(lambda composer: not composer.author_id):
            if (composer.email_from and composer.composition_mode == 'comment'
                and not composer.composition_batch
                # the next condition is added to match pre-compute field behavior
                # to improve and tweak in an upcoming task/commit/PR
                and not composer.template_id):
                author = self.env['mail.thread']._mail_find_partner_from_emails(
                    [composer.email_from],
                    force_create=False,
                )[0]
            else:
                author = self.env.user.partner_id
            composer.author_id = author.id
            # ensure email_from is set (inter dependent fields are hard to model
            # in a compute)
            if not composer.email_from and author:
                composer.email_from = author.email_formatted

    @api.depends('res_ids')
    def _compute_composition_batch(self):
        """ Determine if batch mode is activated:

          * using res_domain: always batch (even if result is singleton at a
            given time, it is user and time dependent, hence batch);
          * res_ids: if more than one item in the list (void and singleton are
            not batch);
        """
        for composer in self:
            if composer.res_domain:
                composer.composition_batch = True
                continue
            res_ids = composer._evaluate_res_ids()
            composer.composition_batch = len(res_ids) > 1 if res_ids else False

    @api.depends('composition_mode', 'model', 'parent_id', 'res_ids')
    def _compute_record_name(self):
        for composer in self.filtered(lambda comp: not comp.record_name
                                                   and comp.composition_mode == 'comment'
                                                   and not comp.composition_batch):
            res_ids = composer._evaluate_res_ids()
            if composer.parent_id.record_name:
                composer.record_name = composer.parent_id.record_name
            elif composer.model and len(res_ids) == 1:
                composer.record_name = self.env[composer.model].browse(res_ids).display_name

    @api.depends('composition_mode', 'model', 'res_ids', 'template_id')
    def _compute_reply_to(self):
        for composer in self:
            if composer.template_id.reply_to:
                composer._set_value_from_template('reply_to')

    @api.depends('model')
    def _compute_reply_to_force_new(self):
        for composer in self:
            if not composer.model or not hasattr(self.env[composer.model], 'message_post'):
                composer.reply_to_force_new = True

    @api.depends('reply_to_force_new')
    def _compute_reply_to_mode(self):
        for composer in self:
            composer.reply_to_mode = 'new' if composer.reply_to_force_new else 'update'

    def _inverse_reply_to_mode(self):
        for composer in self:
            composer.reply_to_force_new = composer.reply_to_mode == 'new'

    @api.depends('composition_mode', 'template_id')
    def _compute_auto_delete(self):
        """ Comes either from template, either is True in comment mode (remove
        notification emails), False in email mode (keep emails, backward
        compatibility mode). """
        for composer in self:
            if composer.template_id:
                composer.auto_delete = composer.template_id.auto_delete
            else:
                composer.auto_delete = composer.composition_mode == 'comment'

    # Overrides of mail.render.mixin
    @api.depends('model')
    def _compute_render_model(self):
        for composer in self:
            composer.render_model = composer.model

    def _compute_can_edit_body(self):
        """Can edit the body if we are not in "mass_mail" mode because the template is
        rendered before it's modified.
        """
        non_mass_mail = self.filtered(lambda m: m.composition_mode != 'mass_mail')
        non_mass_mail.can_edit_body = True
        super(MailComposer, self - non_mass_mail)._compute_can_edit_body()

    # Onchanges

    @api.onchange('template_id')
    def _onchange_template_id_wrapper(self):
        self.ensure_one()
        values = self._onchange_template_id(self.template_id.id, self.composition_mode, self.model, self._evaluate_res_ids())['value']
        for fname, value in values.items():
            setattr(self, fname, value)

    def _onchange_template_id(self, template_id, composition_mode, model, res_ids):
        """ Perform the onchange.

          * mass_mailing or comment in batch: we cannot render, so return the
            template values
          * normal mode: return rendered values
            -> for x2many field, this onchange return command instead of ids
        """
        if template_id and (composition_mode == 'mass_mail' or len(res_ids) > 1):
            # copy raw template values (not rendered due to mass mode)
            template = self.env['mail.template'].browse(template_id)
            values = dict(
                (field, template[field])
                for field in ('scheduled_date',
                             )
                if template[field]
            )
            if template.attachment_ids:
                values['attachment_ids'] = [att.id for att in template.attachment_ids]
            if template.mail_server_id:
                values['mail_server_id'] = template.mail_server_id.id
        elif template_id and len(res_ids) <= 1:
            # render template (mono record, comment mode) and set it as composer values
            # trick to evaluate qweb even when having no records
            template_res_ids = res_ids if res_ids else [0]
            values = self._generate_template_for_composer(
                self.env['mail.template'].browse(template_id),
                template_res_ids,
                ('attachment_ids',
                 'email_cc',
                 'email_to',
                 'mail_server_id',
                 'partner_ids',
                 'report_template_ids',
                 'scheduled_date',
                )
            )[template_res_ids[0]]
            # transform attachments into attachment_ids; not attached to the document because this will
            # be done further in the posting process, allowing to clean database if email not send
            attachment_ids = []
            Attachment = self.env['ir.attachment']
            for attach_fname, attach_datas in values.pop('attachments', []):
                data_attach = {
                    'name': attach_fname,
                    'datas': attach_datas,
                    'res_model': 'mail.compose.message',
                    'res_id': 0,
                    'type': 'binary',  # override default_type from context, possibly meant for another model!
                }
                attachment_ids.append(Attachment.create(data_attach).id)
            if values.get('attachment_ids', []) or attachment_ids:
                values['attachment_ids'] = [Command.set(values.get('attachment_ids', []) + attachment_ids)]
        else:
            default_values = self.with_context(
                default_composition_mode=composition_mode,
                default_model=model,
                default_res_ids=res_ids
            ).default_get(['attachment_ids',
                           'composition_mode',
                           'mail_server_id',
                           'model',
                           'parent_id',
                           'partner_ids',
                           'res_ids',
                           'scheduled_date',
                          ])
            values = dict(
                (key, default_values[key])
                for key in ('attachment_ids',
                            'mail_server_id',
                            'partner_ids',
                            'scheduled_date',
                           ) if key in default_values)

        # This onchange should return command instead of ids for x2many field.
        values = self._convert_to_write(values)

        return {'value': values}

    @api.model
    def get_record_data(self, values):
        """ Returns a defaults-like dict with initial values for the composition
        wizard when sending an email related a previous email (parent_id) or
        a document (model, res_id). This is based on previously computed default
        values. """
        result = {}
        model = values.get('model')
        res_ids = self._parse_res_ids(values['res_ids']) if values.get('res_ids') else []
        if values.get('parent_id'):
            parent = self.env['mail.message'].browse(values.get('parent_id'))
            if not model:
                model = parent.model
                result['model'] = model
            if not res_ids:
                res_ids = [parent.res_id]
                result['res_ids'] = res_ids
            result['partner_ids'] = values.get('partner_ids', list()) + parent.partner_ids.ids

        return result

    # ------------------------------------------------------------
    # CRUD / ORM
    # ------------------------------------------------------------

    @api.autovacuum
    def _gc_lost_attachments(self):
        """ Garbage collect lost mail attachments. Those are attachments
            - linked to res_model 'mail.compose.message', the composer wizard
            - with res_id 0, because they were created outside of an existing
                wizard (typically user input through Chatter or reports
                created on-the-fly by the templates)
            - unused since at least one day (create_date and write_date)
        """
        limit_date = fields.Datetime.subtract(fields.Datetime.now(), days=1)
        self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', 0),
            ('create_date', '<', limit_date),
            ('write_date', '<', limit_date)]
        ).unlink()

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_send_mail(self):
        """ Used for action button that do not accept arguments. """
        self._action_send_mail(auto_commit=False)
        return {'type': 'ir.actions.act_window_close'}

    def _action_send_mail(self, auto_commit=False):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed.

        :return tuple: (
            result_mails_su: in mass mode, sent emails (as sudo),
            result_messages: in comment mode, posted messages
        )
        """
        result_mails_su, result_messages = self.env['mail.mail'].sudo(), self.env['mail.message']

        for wizard in self:
            # Duplicate attachments linked to the email.template.
            # Indeed, basic mail.compose.message wizard duplicates attachments in mass
            # mailing mode. But in 'single post' mode, attachments of an email template
            # also have to be duplicated to avoid changing their ownership.
            if wizard.attachment_ids and wizard.composition_mode != 'mass_mail' and wizard.template_id:
                new_attachment_ids = []
                for attachment in wizard.attachment_ids:
                    if attachment in wizard.template_id.attachment_ids:
                        new_attachment_ids.append(attachment.copy({'res_model': 'mail.compose.message', 'res_id': wizard.id}).id)
                    else:
                        new_attachment_ids.append(attachment.id)
                new_attachment_ids.reverse()
                wizard.write({'attachment_ids': [Command.set(new_attachment_ids)]})

            if wizard.res_domain:
                search_domain = wizard._evaluate_res_domain()
                search_user = wizard.res_domain_user_id or self.env.user
                res_ids = self.env[wizard.model].with_user(search_user).search(search_domain).ids
            else:
                res_ids = wizard._evaluate_res_ids()
            # in comment mode: raise here as anyway message_post will raise.
            if not res_ids and wizard.composition_mode == 'comment':
                raise ValueError(
                    _('Mail composer in comment mode should run on at least one record. No records found (model %(model_name)s).',
                      model_name=wizard.model)
                )

            if wizard.composition_mode == 'mass_mail':
                result_mails_su += wizard._action_send_mail_mass_mail(res_ids, auto_commit=auto_commit)
            else:
                result_messages += wizard._action_send_mail_comment(res_ids)

        return result_mails_su, result_messages

    def _action_send_mail_comment(self, res_ids):
        """ Send in comment mode. It calls message_post on model, or the generic
        implementation of it if not available (as message_notify). """
        self.ensure_one()
        post_values_all = self._prepare_mail_values(res_ids)
        ActiveModel = self.env[self.model] if self.model and hasattr(self.env[self.model], 'message_post') else self.env['mail.thread']
        if self.composition_mode == 'mass_post':
            # do not send emails directly but use the queue instead
            # add context key to avoid subscribing the author
            ActiveModel = ActiveModel.with_context(
                mail_notify_force_send=False,
                mail_create_nosubscribe=True,
            )

        messages = self.env['mail.message']
        for res_id, post_values in post_values_all.items():
            if ActiveModel._name == 'mail.thread':
                if self.model:
                    post_values['model'] = self.model
                    post_values['res_id'] = res_id
                message = ActiveModel.message_notify(**post_values)
                if not message:
                    # if message_notify returns an empty record set, no recipients where found.
                    raise UserError(_("No recipient found."))
                messages += message
            else:
                messages += ActiveModel.browse(res_id).message_post(**post_values)
        return messages

    def _action_send_mail_mass_mail(self, res_ids, auto_commit=False):
        """ Send in mass mail mode. Mails are sudo-ed, as when going through
        _prepare_mail_values standard access rights on related records will be
        checked when browsing them to compute mail values. If people have
        access to the records they have rights to create lots of emails in
        sudo as it is considered as a technical model. """
        mails_sudo = self.env['mail.mail'].sudo()

        batch_size = int(self.env['ir.config_parameter'].sudo().get_param('mail.batch_size')) or self._batch_size
        sliced_res_ids = [res_ids[i:i + batch_size] for i in range(0, len(res_ids), batch_size)]

        for res_ids_iter in sliced_res_ids:
            mail_values_all = self._prepare_mail_values(res_ids_iter)

            iter_mails_sudo = self.env['mail.mail'].sudo()
            for _res_id, mail_values in mail_values_all.items():
                iter_mails_sudo += mails_sudo.create(mail_values)
            mails_sudo += iter_mails_sudo

            records = self.env[self.model].browse(res_ids_iter) if self.model and hasattr(self.env[self.model], 'message_post') else False
            if records:
                records._message_mail_after_hook(iter_mails_sudo)
            iter_mails_sudo.send(auto_commit=auto_commit)

        return mails_sudo

    def action_save_as_template(self):
        """ hit save as template button: current form value will be a new
            template attached to the current document. """
        for record in self:
            model = self.env['ir.model']._get(record.model or 'mail.message')
            model_name = model.name or ''
            template_name = "%s: %s" % (model_name, tools.ustr(record.subject))
            values = {
                'name': template_name,
                'subject': record.subject or False,
                'body_html': record.body or False,
                'model_id': model.id or False,
                'use_default_to': True,
            }
            template = self.env['mail.template'].create(values)

            if record.attachment_ids:
                attachments = self.env['ir.attachment'].sudo().browse(record.attachment_ids.ids).filtered(
                    lambda a: a.res_model == 'mail.compose.message' and a.create_uid.id == self._uid)
                if attachments:
                    attachments.write({'res_model': template._name, 'res_id': template.id})
                template.attachment_ids |= record.attachment_ids

            # generate the saved template
            record.write({'template_id': template.id})
            record._onchange_template_id_wrapper()
            return _reopen(self, record.id, record.model, context=self.env.context)

    # ------------------------------------------------------------
    # RENDERING / VALUES GENERATION
    # ------------------------------------------------------------

    def _prepare_mail_values(self, res_ids):
        """Generate the values that will be used by send_mail to create either
         mail_messages or mail_mails depending on composition mode. """
        self.ensure_one()
        email_mode = self.composition_mode == 'mass_mail'
        rendering_mode = email_mode or self.composition_batch

        base_values = self._prepare_mail_values_common()

        additional_values_all = {}
        if rendering_mode and self.model:
            additional_values_all = self._prepare_mail_values_dynamic(res_ids)
        elif not rendering_mode:
            additional_values_all = self._prepare_mail_values_static(res_ids)

        mail_values_all = {
            res_id: dict(base_values, **additional_values_all.get(res_id, {}))
            for res_id in res_ids
        }

        if email_mode:
            mail_values_all = self._process_mail_values_state(mail_values_all)
        return mail_values_all

    def _prepare_mail_values_common(self):
        """Prepare values always valid, not rendered or dynamic whatever the
        composition mode and related records. """
        self.ensure_one()
        email_mode = self.composition_mode == 'mass_mail'

        if email_mode:
            subtype_id = False
        elif self.subtype_id:
            subtype_id = self.subtype_id.id
        else:
            subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')

        values = {
            'author_id': self.author_id.id,
            'mail_activity_type_id': self.mail_activity_type_id.id,
            'message_type': 'email' if email_mode else self.message_type,
            'parent_id': self.parent_id.id,
            'reply_to_force_new': self.reply_to_force_new,
            'subtype_id': subtype_id,
        }
        if self.composition_mode == 'comment':
            # Several custom layouts make use of the model description at rendering, e.g. in the
            # 'View <document>' button. Some models are used for different business concepts, such as
            # 'purchase.order' which is used for a RFQ and and PO. To avoid confusion, we must use a
            # different wording depending on the state of the object.
            # Therefore, we can set the description in the context from the beginning to avoid falling
            # back on the regular display_name retrieved in ``_notify_by_email_prepare_rendering_context()``.
            model_description = self.env.context.get('model_description')
            values.update(
                email_add_signature=not bool(self.template_id) and self.email_add_signature,
                email_layout_xmlid=self.email_layout_xmlid,
                mail_auto_delete=self.auto_delete,
                model_description=model_description,
            )
        else:
            values.update(
                auto_delete=self.auto_delete,
            )
        return values

    def _prepare_mail_values_dynamic(self, res_ids):
        """Generate values based on composer content as well as its template
        based on records given by res_ids.

        Part of the advanced rendering is delegated to template, notably
        recipients or attachments dynamic generation. See sub methods for
        more details.

        :param list res_ids: list of record IDs on which composer runs;

        :return dict results: for each res_id, the generated values available
          to create mail.mail or mail.message;
        """
        self.ensure_one()
        email_mode = self.composition_mode == 'mass_mail'
        records_sudo = None

        subjects = self._render_field('subject', res_ids)
        bodies = self._render_field(
            'body', res_ids,
            # We want to preserve comments in emails so as to keep mso conditionals
            options={'preserve_comments': email_mode},
        )
        emails_from = self._render_field('email_from', res_ids)

        mail_values_all = {
            res_id: {
                'body': bodies[res_id],  # should be void
                'body_html': bodies[res_id] if email_mode else False,
                'email_from': emails_from[res_id],
                'is_notification': self.auto_delete_keep_log,
                'mail_server_id': self.mail_server_id.id,
                'model': self.model,
                'record_name': False,
                'res_id': res_id,
                'subject': subjects[res_id],
            }
            for res_id in res_ids
        }

        # generate template-based values
        if self.template_id:
            template_values = self._generate_template_for_composer(
                self.template_id,
                res_ids,
                ('attachment_ids',
                 'email_to',
                 'email_cc',
                 'mail_server_id',
                 'partner_ids',
                 'report_template_ids',
                 'scheduled_date',
                )
            )
            for res_id in res_ids:
                # remove attachments from template values as they should not be rendered
                template_values[res_id].pop('attachment_ids', None)
                mail_values_all[res_id].update(template_values[res_id])
        # without template, update recipients using default recipients if no recipients given
        elif not self.partner_ids:
            if not records_sudo:
                records_sudo = self.env[self.model].browse(res_ids).sudo()
            default_recipients = records_sudo._message_get_default_recipients()
            for res_id in res_ids:
                mail_values_all[res_id].update(default_recipients.get(res_id, {}))

        if not self.reply_to_force_new:
            # compute alias-based reply-to in batch
            if not records_sudo:
                records_sudo = self.env[self.model].browse(res_ids)
            reply_to_values = records_sudo._notify_get_reply_to(default=False)
        else:
            reply_to_values = self._render_field('reply_to', res_ids)
            for res_id in res_ids:
                reply_to = reply_to_values.get(res_id)
                if not reply_to:
                    reply_to = mail_values_all[res_id].get('email_from', False)

        for res_id, mail_values in mail_values_all.items():
            record = self.env[self.model].browse(res_id)

            # attachments: process, should not be encoded before being processed
            # by message_post / mail_mail create
            mail_values['attachments'] = [(name, base64.b64decode(enc_cont)) for name, enc_cont in mail_values.pop('attachments', list())]
            attachment_ids = [
                attachment.copy({'res_model': self._name, 'res_id': self.id}).id
                for attachment in self.attachment_ids
            ]
            attachment_ids.reverse()
            mail_values['attachment_ids'] = record._process_attachments_for_post(
                mail_values.pop('attachments', []),
                attachment_ids,
                {'model': 'mail.message', 'res_id': 0}
            )['attachment_ids']

            # headers
            mail_values['headers'] = repr(record._notify_by_email_get_headers())

            # transform partner_ids (field used in mail_message) into recipient_ids, used by mail_mail
            mail_values['recipient_ids'] = [
                Command.link(id) for id in (
                    mail_values.pop('partner_ids', []) + self.partner_ids.ids
                )
            ]

            # when having no specific reply_to -> fetch rendered email_from
            reply_to = reply_to_values.get(res_id)
            if not reply_to:
                reply_to = mail_values.get('email_from', False)
            mail_values['reply_to'] = reply_to

        return mail_values_all

    def _prepare_mail_values_static(self, res_ids):
        """Generate values that are static, aka already rendered.

        :param list res_ids: list of record IDs on which composer runs;

        :return dict results: for each res_id, the generated values available
          to create mail.mail or mail.message;
        """
        self.ensure_one()
        return {
            res_id: {
                'attachment_ids': [attach.id for attach in self.attachment_ids],
                'body': self.body or '',
                'email_from': self.email_from,
                'mail_server_id': self.mail_server_id.id,
                'partner_ids': self.partner_ids.ids,
                'record_name': self.record_name,
                'scheduled_date': self.scheduled_date,
                'subject': self.subject or '',
            }
            for res_id in res_ids
        }

    def _process_mail_values_state(self, mail_values_dict):
        """ When being in mass mailing, avoid sending emails to void or invalid
        emails. For that purpose a processing of generated values allows to
        give a state and a failure type to mail.mail records that will be
        created at sending time.

        :param dict mail_values_dict: as generated by '_prepare_mail_values';

        :return: updated mail_values_dict
        """
        recipients_info = self._get_recipients_data(mail_values_dict)
        blacklist_ids = self._get_blacklist_record_ids(mail_values_dict)
        optout_emails = self._get_optout_emails(mail_values_dict)
        done_emails = self._get_done_emails(mail_values_dict)
        # in case of an invoice e.g.
        mailing_document_based = self.env.context.get('mailing_document_based')

        for record_id, mail_values in mail_values_dict.items():
            recipients = recipients_info[record_id]
            # when having more than 1 recipient: we cannot really decide when a single
            # email is linked to several to -> skip that part. Mass mailing should
            # anyway always have a single recipient per record as this is default behavior.
            if len(recipients['mail_to']) > 1:
                continue

            mail_to = recipients['mail_to'][0] if recipients['mail_to'] else ''
            mail_to_normalized = recipients['mail_to_normalized'][0] if recipients['mail_to_normalized'] else ''

            # prevent sending to blocked addresses that were included by mistake
            # blacklisted or optout or duplicate -> cancel
            if record_id in blacklist_ids:
                mail_values['state'] = 'cancel'
                mail_values['failure_type'] = 'mail_bl'
                # Do not post the mail into the recipient's chatter
                mail_values['is_notification'] = False
            elif optout_emails and mail_to in optout_emails:
                mail_values['state'] = 'cancel'
                mail_values['failure_type'] = 'mail_optout'
            elif done_emails and mail_to in done_emails and not mailing_document_based:
                mail_values['state'] = 'cancel'
                mail_values['failure_type'] = 'mail_dup'
            # void of falsy values -> error
            elif not mail_to:
                mail_values['state'] = 'cancel'
                mail_values['failure_type'] = 'mail_email_missing'
            elif not mail_to_normalized or not email_re.findall(mail_to):
                mail_values['state'] = 'cancel'
                mail_values['failure_type'] = 'mail_email_invalid'
            elif done_emails is not None and not mailing_document_based:
                done_emails.append(mail_to)

        return mail_values_dict

    def _generate_template_for_composer(self, template, res_ids, render_fields,
                                        find_or_create_partners=True):
        """ Generate values based on template and relevant values for the
        mail.compose.message wizard.

        :param record template: a mail template, as during onchange mode it
          may not be set on self (to remove when removing the onchange);
        :param list res_ids: list of record IDs on which template is rendered;
        :param list render_fields: list of fields to render on template;
        :param boolean find_or_create_partners: transform emails into partners
          (see ``Template._generate_template_recipients``);

        :returns: a dict containing all asked fields for each record ID given by
          res_ids. Note that

          * 'body' comes from template 'body_html' generation;
          * 'attachments' is an additional key coming with 'attachment_ids' due
            to report generation (in the format [(report_name, data)] where data
            is base64 encoded);
          * 'partner_ids' is returned due to recipients generation that gives
            partner ids coming from default computation as well as from email
            to partner convert (see ``find_or_create_partners``);
        """
        self.ensure_one()

        # some fields behave / are named differently on template model
        mapping = {
            'attachments': 'report_template_ids',
            'body': 'body_html',
            'partner_ids': 'partner_to',
        }
        template_fields = {mapping.get(fname, fname) for fname in render_fields}
        template_values = template._generate_template(
            res_ids,
            template_fields,
            find_or_create_partners=True
        )

        exclusion_list = ('email_cc', 'email_to') if find_or_create_partners else ()
        mapping = {'body_html': 'body'}
        render_results = {}
        for res_id in res_ids:
            render_results[res_id] = {
                mapping.get(fname, fname): value
                for fname, value in template_values[res_id].items()
                if fname not in exclusion_list and value
            }

        return render_results

    # ----------------------------------------------------------------------
    # EMAIL MANAGEMENT
    # ---------------------------------------------------------------------

    def _get_blacklist_record_ids(self, mail_values_dict):
        blacklisted_rec_ids = set()
        if self.composition_mode == 'mass_mail' and issubclass(type(self.env[self.model]), self.pool['mail.thread.blacklist']):
            self.env['mail.blacklist'].flush_model(['email', 'active'])
            self._cr.execute("SELECT email FROM mail_blacklist WHERE active=true")
            blacklist = {x[0] for x in self._cr.fetchall()}
            if blacklist:
                targets = self.env[self.model].browse(mail_values_dict.keys()).read(['email_normalized'])
                # First extract email from recipient before comparing with blacklist
                blacklisted_rec_ids.update(target['id'] for target in targets
                                           if target['email_normalized'] in blacklist)
        return blacklisted_rec_ids

    def _get_done_emails(self, mail_values_dict):
        return []

    def _get_optout_emails(self, mail_values_dict):
        return []

    def _get_recipients_data(self, mail_values_dict):
        # Preprocess res.partners to batch-fetch from db if recipient_ids is present
        # it means they are partners (the only object to fill get_default_recipient this way)
        recipient_pids = [
            recipient_command[1]
            for mail_values in mail_values_dict.values()
            # recipient_ids is a list of x2m command tuples at this point
            for recipient_command in mail_values.get('recipient_ids') or []
            if recipient_command[1]
        ]
        recipient_emails = {
            p.id: p.email
            for p in self.env['res.partner'].browse(set(recipient_pids))
        } if recipient_pids else {}

        recipients_info = {}
        for record_id, mail_values in mail_values_dict.items():
            mail_to = []
            if mail_values.get('email_to'):
                mail_to += email_re.findall(mail_values['email_to'])
                # if unrecognized email in email_to -> keep it as used for further processing
                if not mail_to:
                    mail_to.append(mail_values['email_to'])
            # add email from recipients (res.partner)
            mail_to += [
                recipient_emails[recipient_command[1]]
                for recipient_command in mail_values.get('recipient_ids') or []
                if recipient_command[1]
            ]
            mail_to = list(set(mail_to))
            recipients_info[record_id] = {
                'mail_to': mail_to,
                'mail_to_normalized': [
                    tools.email_normalize(mail)
                    for mail in mail_to
                    if tools.email_normalize(mail)
                ]
            }
        return recipients_info

    # ----------------------------------------------------------------------
    # MISC UTILS
    # ----------------------------------------------------------------------

    def _evaluate_res_domain(self):
        """ Parse composer domain, which can be: an already valid list or
        tuple (generally in code), a list or tuple as a string (coming from
        actions). Void strings are considered as a falsy domain.

        :return: an Odoo domain (list of leaves) """
        self.ensure_one()
        if isinstance(self.res_domain, (str, bool)) and not self.res_domain:
            return expression.FALSE_DOMAIN
        try:
            domain = self.res_domain
            if isinstance(self.res_domain, str):
                domain = ast.literal_eval(domain)

            expression.expression(
                domain,
                self.env[self.model],
            )
        except (ValueError, AssertionError) as e:
            raise ValidationError(
                _("Invalid domain %(domain)r (type %(domain_type)s)",
                    domain=self.res_domain,
                    domain_type=type(self.res_domain))
            ) from e

        return domain

    def _evaluate_res_ids(self):
        """ Parse composer res_ids, which can be: an already valid list or
        tuple (generally in code), a list or tuple as a string (coming from
        actions). Void strings / missing values are evaluated as an empty list.

        Note that 'active_ids' context key is supported at this point as mailing
        on big ID list would create issues if stored in database.

        :return: a list of IDs (empty list in case of falsy strings)"""
        self.ensure_one()
        return self._parse_res_ids(
            self.res_ids or self.env.context.get('active_ids')
        ) or []

    @api.model
    def _parse_res_ids(self, res_ids):
        if tools.is_list_of(res_ids, int) or not res_ids:
            return res_ids
        error_msg = _("Invalid res_ids %(res_ids_str)s (type %(res_ids_type)s)",
                      res_ids_str=res_ids,
                      res_ids_type=type(res_ids))
        try:
            res_ids = ast.literal_eval(res_ids)
        except Exception as e:
            raise ValidationError(error_msg) from e
        if not tools.is_list_of(res_ids, int):
            raise ValidationError(error_msg)
        return res_ids

    def _set_value_from_template(self, template_fname, composer_fname=False, force_void=False):
        """ Get composer value from its template counterpart. In monorecord
        comment mode, we get directly the rendered value, giving the real
        value to the user. Otherwise we get the raw (unrendered) value from
        template, as it will be rendered at send time (for mass mail, whatever
        the number of contextual records to mail) or before posting on records
        (for comment in batch).

        :param str template_fname: name of field on template model, used to
          fetch the value (and maybe render it);
        :param str composer_fname: name of field on composer model, when field
          names do not match (e.g. body_html on template used to populate body
          on composer);
        :param bool force_void: if False, do not propagate a falsy template
          value on composer, allowing to keep the previous composer value
          instead of voiding it with template falsy value;
        """
        self.ensure_one()
        composer_fname = composer_fname or template_fname
        if self.template_id and (self.template_id[template_fname] or force_void):
            if self.composition_mode == 'comment' and not self.composition_batch:
                res_ids = self._evaluate_res_ids()
                rendering_res_ids = res_ids or [False]
                self[composer_fname] = self.template_id._generate_template(
                    rendering_res_ids,
                    {template_fname},
                )[rendering_res_ids[0]][template_fname]
            else:
                self[composer_fname] = self.template_id[template_fname]
