# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval
from datetime import timedelta
from freezegun import freeze_time
from unittest.mock import DEFAULT, patch

from odoo.addons.base.tests.test_ir_cron import CronMixinCase
from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.addons.mail.wizard.mail_compose_message import MailComposer
from odoo.addons.test_mail.models.test_mail_models import MailTestTicket
from odoo.addons.test_mail.tests.common import TestMailCommon, TestRecipients
from odoo.fields import Datetime as FieldDatetime
from odoo.exceptions import AccessError
from odoo.tests import tagged
from odoo.tests.common import users, Form
from odoo.tools import mute_logger, formataddr


@tagged('mail_composer')
class TestMailComposer(TestMailCommon, TestRecipients):
    """ Test Composer internals """

    @classmethod
    def setUpClass(cls):
        super(TestMailComposer, cls).setUpClass()
        cls.reference_now = FieldDatetime.from_string('2022-12-24 12:00:00')
        cls.env.cr._now = cls.reference_now  # force create_date to check schedulers

        # ensure employee can create partners, necessary for templates
        cls.user_employee.write({
            'groups_id': [(4, cls.env.ref('base.group_partner_manager').id)],
        })

        cls.user_employee_2 = mail_new_test_user(
            cls.env, login='employee2', groups='base.group_user',
            notification_type='email', email='eglantine@example.com',
            name='Eglantine Employee', signature='--\nEglantine')
        cls.partner_employee_2 = cls.user_employee_2.partner_id

        # User without the group "mail.group_mail_template_editor"
        cls.user_rendering_restricted = mail_new_test_user(
            cls.env, login='user_rendering_restricted',
            groups='base.group_user',
            company_id=cls.company_admin.id,
            name='Code Template Restricted User',
            notification_type='inbox',
            signature='--\nErnest'
        )
        cls.env.ref('mail.group_mail_template_editor').users -= cls.user_rendering_restricted

        cls.test_record = cls.env['mail.test.ticket'].with_context(cls._test_context).create({
            'name': 'TestRecord',
            'customer_id': cls.partner_1.id,
            'user_id': cls.user_employee_2.id,
        })
        cls.test_records, cls.test_partners = cls._create_records_for_batch(
            'mail.test.ticket', 2,
            additional_values={'user_id': cls.user_employee_2.id}
        )

        cls.test_report, cls.test_report_2 = cls.env['ir.actions.report'].create([
            {
                'name': 'Test Report on Mail Test Ticket',
                'model': 'mail.test.ticket',
                'print_report_name': "'TestReport for %s' % object.name",
                'report_type': 'qweb-pdf',
                'report_name': 'test_mail.mail_test_ticket_test_template',
            }, {
                'name': 'Test Report 2 on Mail Test Ticket',
                'model': 'mail.test.ticket',
                'print_report_name': "'TestReport2 for %s' % object.name",
                'report_type': 'qweb-pdf',
                'report_name': 'test_mail.mail_test_ticket_test_template_2',
            }
        ])

        cls.test_from = '"John Doe" <john@example.com>'

        cls.template = cls.env['mail.template'].create({
            'auto_delete': True,
            'name': 'TestTemplate',
            'subject': 'TemplateSubject {{ object.name }}',
            'body_html': '<p>TemplateBody <t t-esc="object.name"></t></p>',
            'partner_to': '{{ object.customer_id.id if object.customer_id else "" }}',
            'email_to': '{{ (object.email_from if not object.customer_id else "") }}',
            'email_from': '{{ (object.user_id.email_formatted or user.email_formatted) }}',
            'mail_server_id': cls.mail_server_domain.id,
            'model_id': cls.env['ir.model']._get('mail.test.ticket').id,
            'reply_to': '{{ ctx.get("custom_reply_to") or "info@test.example.com" }}',
            'scheduled_date': '{{ (object.create_date or datetime.datetime(2022, 12, 26, 18, 0, 0)) + datetime.timedelta(days=2) }}',
        })

    def _get_web_context(self, records, add_web=True, **values):
        """ Helper to generate composer context. Will make tests a bit less
        verbose.

        :param add_web: add web context, generally making noise especially in
          mass mail mode (active_id/ids both present in context)
        """
        base_context = {
            'default_model': records._name,
            'default_res_ids': records.ids,
        }
        if len(records) == 1:
            base_context['default_composition_mode'] = 'comment'
        else:
            base_context['default_composition_mode'] = 'mass_mail'
        if add_web:
            base_context['active_model'] = records._name
            base_context['active_id'] = records[0].id
            base_context['active_ids'] = records.ids
        if values:
            base_context.update(**values)
        return base_context


@tagged('mail_composer')
class TestComposerForm(TestMailComposer):

    @users('employee')
    def test_mail_composer_comment(self):
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=True)
        ))
        self.assertTrue(composer_form.auto_delete, 'MailComposer: comment mode should remove notification emails by default')
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertFalse(composer_form.body)
        self.assertFalse(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'comment')
        self.assertEqual(composer_form.email_from, self.env.user.email_formatted)
        self.assertFalse(composer_form.mail_server_id)
        self.assertEqual(composer_form.model, self.test_record._name)
        self.assertFalse(composer_form.partner_ids)
        self.assertEqual(composer_form.record_name, self.test_record.name, 'MailComposer: comment mode should compute record name')
        self.assertFalse(composer_form.reply_to)
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertFalse(composer_form.scheduled_date)
        self.assertEqual(literal_eval(composer_form.res_ids), self.test_record.ids)
        self.assertEqual(composer_form.subject, self.test_record._message_compute_subject())
        self.assertIn(f'Ticket for {self.test_record.name}', composer_form.subject,
                      'Check effective content')
        self.assertEqual(composer_form.subtype_id, self.env.ref('mail.mt_comment'))

    @users('employee')
    def test_mail_composer_comment_attachments(self):
        """Tests that all attachments are added to the composer, static attachments
        are not duplicated and while reports are re-generated, and that intermediary
        attachments are dropped."""
        attachment_data = self._generate_attachments_data(2, self.template._name, self.template.id)
        template_1 = self.template.copy({
            'attachment_ids': [(0, 0, a) for a in attachment_data],
            'report_template_ids': [(6, 0, (self.test_report + self.test_report_2).ids)],
        })
        template_1_attachments = template_1.attachment_ids
        self.assertEqual(len(template_1_attachments), 2)
        template_2 = self.template.copy({
            'attachment_ids': False,
            'report_template_ids': [(6, 0, self.test_report.ids)],
        })

        # begins without attachments
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=True, default_attachment_ids=[])
        ))
        self.assertEqual(len(composer_form.attachment_ids), 0)

        # change template: 2 static (attachment_ids) and 2 dynamic (reports)
        composer_form.template_id = template_1
        self.assertEqual(len(composer_form.attachment_ids), 4)
        report_attachments = [att for att in composer_form.attachment_ids if att not in template_1_attachments]
        self.assertEqual(len(report_attachments), 2)
        tpl_attachments = composer_form.attachment_ids[:] - self.env['ir.attachment'].concat(*report_attachments)
        self.assertEqual(tpl_attachments, template_1_attachments)

        # change template: 0 static (attachment_ids) and 1 dynamic (report)
        composer_form.template_id = template_2
        self.assertEqual(len(composer_form.attachment_ids), 1)
        report_attachments = [att for att in composer_form.attachment_ids if att not in template_1_attachments]
        self.assertEqual(len(report_attachments), 1)
        tpl_attachments = composer_form.attachment_ids[:] - self.env['ir.attachment'].concat(*report_attachments)
        self.assertFalse(tpl_attachments)

        # change back to template 1
        composer_form.template_id = template_1
        self.assertEqual(len(composer_form.attachment_ids), 4)
        report_attachments = [att for att in composer_form.attachment_ids if att not in template_1_attachments]
        self.assertEqual(len(report_attachments), 2)
        tpl_attachments = composer_form.attachment_ids[:] - self.env['ir.attachment'].concat(*report_attachments)
        self.assertEqual(tpl_attachments, template_1_attachments)

        # reset template
        composer_form.template_id = self.env['mail.template']
        self.assertEqual(len(composer_form.attachment_ids), 0)

    @users('employee')
    def test_mail_composer_comment_wtpl(self):
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=True, default_template_id=self.template.id)
        ))
        self.assertTrue(composer_form.auto_delete, 'Should take template value')
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertEqual(composer_form.body, '<p>TemplateBody %s</p>' % self.test_record.name)
        self.assertFalse(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'comment')
        self.assertEqual(composer_form.email_from, self.user_employee_2.email_formatted)
        self.assertEqual(composer_form.mail_server_id, self.mail_server_domain)
        self.assertEqual(composer_form.model, self.test_record._name)
        self.assertEqual(composer_form.partner_ids[:], self.partner_1)
        self.assertEqual(composer_form.record_name, self.test_record.name, 'MailComposer: comment mode should compute record name')
        self.assertEqual(composer_form.reply_to, 'info@test.example.com')
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertEqual(literal_eval(composer_form.res_ids), self.test_record.ids)
        self.assertEqual(composer_form.scheduled_date, FieldDatetime.to_string(self.reference_now + timedelta(days=2)))
        self.assertEqual(composer_form.subject, 'TemplateSubject %s' % self.test_record.name)
        self.assertEqual(composer_form.subtype_id, self.env.ref('mail.mt_comment'))

    @users('employee')
    def test_mail_composer_comment_wtpl_batch(self):
        """ Batch mode of composer in comment mode. """
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(
                self.test_records,
                add_web=True,
                default_composition_mode='comment',
                default_template_id=self.template.id),
        ))
        self.assertTrue(composer_form.auto_delete, 'Should take composer value')
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertEqual(composer_form.body, self.template.body_html,
                         'MailComposer: comment in batch mode should have template raw body if template')
        self.assertTrue(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'comment')
        self.assertEqual(composer_form.email_from, self.template.email_from,
                         'MailComposer: comment in batch mode should have template raw email_from if template')
        self.assertEqual(composer_form.mail_server_id, self.mail_server_domain)
        self.assertEqual(composer_form.model, self.test_record._name)
        self.assertFalse(composer_form.record_name, 'MailComposer: comment in batch mode should have void record name')
        self.assertEqual(composer_form.reply_to, self.template.reply_to)
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertEqual(literal_eval(composer_form.res_ids), self.test_records.ids)
        self.assertEqual(composer_form.scheduled_date, self.template.scheduled_date)
        self.assertEqual(composer_form.subject, self.template.subject,
                         'MailComposer: comment in batch mode should have template raw subject if template')

    @users('employee')
    def test_mail_composer_comment_wtpl_norecords(self):
        """ Test specific case when running without records, to see the rendering
        when nothing is given as context. """
        composer_form = Form(self.env['mail.compose.message'].with_context(
            default_composition_mode='comment',
            default_model='mail.test.ticket',
            default_template_id=self.template.id,
        ))
        self.assertTrue(composer_form.auto_delete, 'Should take composer value')
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertEqual(composer_form.body, '<p>TemplateBody </p>')
        self.assertFalse(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'comment')
        self.assertEqual(composer_form.email_from, self.env.user.partner_id.email_formatted)
        self.assertEqual(composer_form.mail_server_id, self.mail_server_domain)
        self.assertEqual(composer_form.model, self.test_record._name)
        self.assertFalse(composer_form.partner_ids[:])
        self.assertFalse(composer_form.record_name)
        self.assertEqual(composer_form.reply_to, 'info@test.example.com')
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertFalse(composer_form.res_ids)
        self.assertEqual(composer_form.scheduled_date,
                         '2022-12-28 18:00:00',
                         'No record but rendered, see expression in template')
        self.assertEqual(composer_form.subject, 'TemplateSubject ')
        self.assertEqual(composer_form.subtype_id, self.env.ref('mail.mt_comment'))

    @users('employee')
    def test_mail_composer_mass(self):
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True)
        ))
        self.assertFalse(composer_form.auto_delete)
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertFalse(composer_form.body)
        self.assertTrue(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'mass_mail')
        self.assertEqual(composer_form.email_from, self.env.user.email_formatted)
        self.assertFalse(composer_form.mail_server_id)
        self.assertEqual(composer_form.model, self.test_records._name)
        self.assertFalse(composer_form.record_name, 'MailComposer: mass mode should have void record name')
        self.assertFalse(composer_form.reply_to)
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertEqual(sorted(literal_eval(composer_form.res_ids)), sorted(self.test_records.ids))
        self.assertFalse(composer_form.scheduled_date)
        self.assertFalse(composer_form.subject, 'MailComposer: mass mode should have void default subject if no template')
        self.assertEqual(composer_form.subtype_id, self.env.ref('mail.mt_comment'))

    @users('employee')
    def test_mail_composer_mass_wtpl(self):
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True, default_template_id=self.template.id)
        ))
        self.assertTrue(composer_form.auto_delete, 'Should take composer value')
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertEqual(composer_form.body, self.template.body_html,
                         'MailComposer: mass mode should have template raw body if template')
        self.assertTrue(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'mass_mail')
        self.assertEqual(composer_form.email_from, self.template.email_from,
                         'MailComposer: mass mode should have template raw email_from if template')
        self.assertEqual(composer_form.mail_server_id, self.mail_server_domain)
        self.assertEqual(composer_form.model, self.test_records._name)
        self.assertFalse(composer_form.record_name, 'MailComposer: mass mode should have void record name')
        self.assertEqual(composer_form.reply_to, self.template.reply_to)
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertEqual(sorted(literal_eval(composer_form.res_ids)), sorted(self.test_records.ids))
        self.assertEqual(composer_form.scheduled_date, self.template.scheduled_date)
        self.assertEqual(composer_form.subject, self.template.subject,
                         'MailComposer: mass mode should have template raw subject if template')
        self.assertEqual(composer_form.subtype_id, self.env.ref('mail.mt_comment'))

    @users('employee')
    def test_mail_composer_mass_wtpl_norecords(self):
        """ Test specific case when running without records, to see the rendering
        when nothing is given as context. """
        composer_form = Form(self.env['mail.compose.message'].with_context(
            default_composition_mode='mass_mail',
            default_model='mail.test.ticket',
            default_template_id=self.template.id,
        ))
        self.assertTrue(composer_form.auto_delete, 'Should take composer value')
        self.assertTrue(composer_form.auto_delete_keep_log)
        self.assertEqual(composer_form.author_id, self.env.user.partner_id)
        self.assertEqual(composer_form.body, self.template.body_html,
                         'MailComposer: mass mode should have template raw body if template')
        self.assertFalse(composer_form.composition_batch)
        self.assertEqual(composer_form.composition_mode, 'mass_mail')
        self.assertEqual(composer_form.email_from, self.template.email_from,
                         'MailComposer: mass mode should have template raw email_from if template')
        self.assertEqual(composer_form.mail_server_id, self.mail_server_domain)
        self.assertEqual(composer_form.model, self.test_records._name)
        self.assertFalse(composer_form.record_name, 'MailComposer: mass mode should have void record name')
        self.assertEqual(composer_form.reply_to, self.template.reply_to)
        self.assertFalse(composer_form.reply_to_force_new)
        self.assertFalse(composer_form.res_ids)
        self.assertEqual(composer_form.scheduled_date, self.template.scheduled_date)
        self.assertEqual(composer_form.subject, self.template.subject,
                         'MailComposer: mass mode should have template raw subject if template')
        self.assertEqual(composer_form.subtype_id, self.env.ref('mail.mt_comment'))


@tagged('mail_composer')
class TestComposerInternals(TestMailComposer):

    @users('employee')
    @mute_logger('odoo.addons.mail.models.mail_mail')
    def test_mail_composer_attachments_comment(self):
        """ Test attachments management in comment mode. """
        attachment_data = self._generate_attachments_data(3, self.template._name, self.template.id)
        self.template.write({
            'attachment_ids': [(0, 0, a) for a in attachment_data],
            'report_template_ids': [(6, 0, self.test_report.ids)],
        })
        template_void = self.template.copy(default={
            'attachment_ids': False,
            'report_template_ids': False,
        })
        attachs = self.env['ir.attachment'].search([('name', 'in', [a['name'] for a in attachment_data])])
        self.assertEqual(len(attachs), 3)

        composer = self.env['mail.compose.message'].with_context({
            'default_composition_mode': 'comment',
            'default_model': self.test_record._name,
            'default_res_ids': self.test_record.ids,
            'default_template_id': self.template.id,
        }).create({
            'body': '<p>Test Body</p>',
        })
        # currently onchange necessary
        composer._onchange_template_id_wrapper()

        # values coming from template
        self.assertEqual(len(composer.attachment_ids), 4)
        for attach in attachs:
            self.assertIn(attach, composer.attachment_ids)
        generated = composer.attachment_ids - attachs
        self.assertEqual(len(generated), 1, 'MailComposer: should have 1 additional attachment for report')
        self.assertEqual(generated.name, 'TestReport for %s.html' % self.test_record.name)
        self.assertEqual(generated.res_model, 'mail.compose.message')
        self.assertEqual(generated.res_id, 0)

        # update with template with void values: values are kept
        composer.write({'template_id': template_void.id})
        # currently onchange necessary
        composer._onchange_template_id_wrapper()
        self.assertEqual(composer.attachment_ids, attachs + generated)

        # reset template: values are kept
        composer.write({'template_id': False})
        # currently onchange necessary
        composer._onchange_template_id_wrapper()
        self.assertEqual(composer.attachment_ids, attachs + generated)

    @users('employee')
    @mute_logger('odoo.addons.mail.models.mail_mail')
    def test_mail_composer_author(self):
        """ Test author_id / email_from synchronization, in both comment and mass mail
        modes. """
        template_void = self.template.copy(default={
            'email_from': False,
        })

        for composition_mode, batch in (('comment', False), ('comment', True),
                                        ('mass_mail', False), ('mass_mail', True)):
            with self.subTest(composition_mode=composition_mode, batch=batch):
                test_records = self.test_records if batch else self.test_record
                ctx = self._get_web_context(test_records, add_web=False, default_composition_mode=composition_mode)

                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'body': '<p>Test Body</p>',
                })

                # default values are current user
                self.assertEqual(composer.author_id, self.env.user.partner_id)
                self.assertEqual(composer.composition_mode, composition_mode)
                self.assertEqual(composer.email_from, self.env.user.email_formatted)

                # author values reset email (FIXME: currently not synchronized)
                composer.write({'author_id': self.partner_1})
                self.assertEqual(composer.author_id, self.partner_1)
                self.assertEqual(composer.email_from, self.env.user.email_formatted)
                # self.assertEqual(composer.email_from, self.partner_1.email_formatted)

                # changing template should update its email_from
                composer.write({'template_id': self.template.id, 'author_id': self.env.user.partner_id})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()
                self.assertEqual(composer.author_id, self.env.user.partner_id,
                                 'MailComposer: should take value given by user')
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.email_from, self.test_record.user_id.email_formatted,
                                     f'MailComposer: should take email_from rendered from template ({composition_mode}-{batch})')
                else:
                    self.assertEqual(composer.email_from, self.template.email_from,
                                     f'MailComposer: should take email_from raw from template ({composition_mode}-{batch})')

                # manual values are kept over template values
                composer.write({'email_from': self.test_from})
                self.assertEqual(composer.author_id, self.env.user.partner_id)
                self.assertEqual(composer.email_from, self.test_from)

                # update with template with void values: void value is not forced in
                # rendering mode as well as when copying template values
                composer.write({'template_id': template_void.id})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.author_id, self.env.user.partner_id)
                    self.assertEqual(composer.email_from, self.test_from)
                else:
                    self.assertEqual(composer.author_id, self.env.user.partner_id)
                    self.assertEqual(composer.email_from, self.test_from)

                # reset template: values are reset due to call to default_get
                composer.write({'template_id': False})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.author_id, self.env.user.partner_id)
                    self.assertEqual(composer.email_from, self.env.user.email_formatted)
                else:
                    self.assertEqual(composer.author_id, self.env.user.partner_id)
                    self.assertEqual(composer.email_from, self.env.user.email_formatted)

    @users('employee')
    def test_mail_composer_content(self):
        """ Test content management (subject, body, server) in both comment and
        mass mailing mode. Template update is also tested. """
        template_void = self.template.copy(default={
            'body_html': False,
            'subject': False,
            'mail_server_id': False,
        })

        for composition_mode, batch in (('comment', False), ('comment', True),
                                        ('mass_mail', False), ('mass_mail', True)):
            with self.subTest(composition_mode=composition_mode, batch=batch):
                test_records = self.test_records if batch else self.test_record
                ctx = self._get_web_context(test_records, add_web=False, default_composition_mode=composition_mode)

                # 1. check without template + template update
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'subject': 'My amazing subject',
                    'body': '<p>Test Body</p>',
                })

                # creation values are taken
                self.assertEqual(composer.subject, 'My amazing subject')
                self.assertEqual(composer.body, '<p>Test Body</p>')
                self.assertEqual(composer.mail_server_id.id, False)
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.record_name, self.test_record.name)
                else:
                    self.assertFalse(composer.record_name)

                # changing template should update its content
                composer.write({'template_id': self.template.id})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values come from template
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.subject, 'TemplateSubject %s' % self.test_record.name)
                    self.assertEqual(composer.body, '<p>TemplateBody %s</p>' % self.test_record.name)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertEqual(composer.record_name, self.test_record.name)
                    self.assertEqual(FieldDatetime.from_string(composer.scheduled_date), self.reference_now + timedelta(days=2))
                else:
                    self.assertEqual(composer.subject, self.template.subject)
                    self.assertEqual(composer.body, self.template.body_html)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertFalse(composer.record_name)
                    self.assertEqual(composer.scheduled_date, self.template.scheduled_date)

                # manual values is kept over template
                composer.write({
                    'body': 'Back to my amazing body',
                    'subject': 'Back to my amazing subject',
                })
                self.assertEqual(composer.body, 'Back to my amazing body')
                self.assertEqual(composer.subject, 'Back to my amazing subject')

                # update with template with void values: void value is not forced in
                # rendering mode as well as when copying template values
                composer.write({'template_id': template_void.id})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.body, 'Back to my amazing body')
                    self.assertEqual(composer.subject, 'Back to my amazing subject')
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                else:
                    self.assertEqual(composer.body, 'Back to my amazing body')
                    self.assertEqual(composer.subject, 'Back to my amazing subject')
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)

                # reset template should reset values
                composer.write({'body': 'Back to my amazing body'})
                composer.write({'template_id': False})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values are reset with default_get call, if it returns value
                # (aka subject for comment mode)
                if composition_mode == 'comment' and not batch:
                    self.assertFalse(composer.body)
                    self.assertEqual(composer.subject, self.test_record._message_compute_subject())
                    self.assertIn(f'Ticket for {self.test_record.name}', composer.subject,
                                  'Check effective content')
                    # TDE FIXME: server id is kept, not sure why
                    # self.assertFalse(composer.mail_server_id.id)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertEqual(composer.record_name, self.test_record.name)
                    # TDE FIXME: scheduled date is kept, not sure why
                    self.assertEqual(FieldDatetime.from_string(composer.scheduled_date), self.reference_now + timedelta(days=2))
                else:
                    self.assertFalse(composer.body)
                    # values are reset TDE FIXME: strange for subject
                    self.assertEqual(composer.subject, 'Back to my amazing subject')
                    # TDE FIXME: server id is kept, not sure why
                    # self.assertFalse(composer.mail_server_id.id)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertFalse(composer.record_name)
                    # TDE FIXME: scheduled_Date is kept, not sure why
                    self.assertEqual(composer.scheduled_date, self.template.scheduled_date)

                # 2. check with default
                ctx['default_template_id'] = self.template.id
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'template_id': self.template.id,
                })
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values come from template
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.subject, 'TemplateSubject %s' % self.test_record.name)
                    self.assertEqual(composer.body, '<p>TemplateBody %s</p>' % self.test_record.name)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertEqual(composer.record_name, self.test_record.name)
                    self.assertEqual(FieldDatetime.from_string(composer.scheduled_date), self.reference_now + timedelta(days=2))
                else:
                    self.assertEqual(composer.subject, self.template.subject)
                    self.assertEqual(composer.body, self.template.body_html)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertFalse(composer.record_name)
                    self.assertEqual(composer.scheduled_date, self.template.scheduled_date)

                # 3. check at create
                ctx.pop('default_template_id')
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'template_id': self.template.id,
                })
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values come from template
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.subject, 'TemplateSubject %s' % self.test_record.name)
                    self.assertEqual(composer.body, '<p>TemplateBody %s</p>' % self.test_record.name)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertEqual(composer.record_name, self.test_record.name)
                    self.assertEqual(FieldDatetime.from_string(composer.scheduled_date), self.reference_now + timedelta(days=2))
                else:
                    self.assertEqual(composer.subject, self.template.subject)
                    self.assertEqual(composer.body, self.template.body_html)
                    self.assertEqual(composer.mail_server_id, self.template.mail_server_id)
                    self.assertFalse(composer.record_name)
                    self.assertEqual(composer.scheduled_date, self.template.scheduled_date)

                # 4. template + user input
                ctx['default_template_id'] = self.template.id
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'subject': 'My amazing subject',
                    'body': '<p>Test Body</p>',
                    'mail_server_id': False,
                    'record_name': 'CustomName',
                })

                # creation values are taken
                self.assertEqual(composer.subject, 'My amazing subject')
                self.assertEqual(composer.body, '<p>Test Body</p>')
                self.assertEqual(composer.mail_server_id.id, False)
                self.assertEqual(composer.record_name, 'CustomName')
                self.assertFalse(composer.scheduled_date)

    @users('employee')
    @mute_logger('odoo.models.unlink')
    def test_mail_composer_recipients(self):
        """ Test content management (partner_ids, reply_to) in both comment and
        mass mailing mode. Template update is also tested. Add some tests for
        partner creation based on unknown emails as this is part of the process. """
        base_recipients = self.partner_1 + self.partner_2
        self.template.write({
            'email_cc': 'test.cc.1@test.example.com, test.cc.2@test.example.com'
        })
        template_void = self.template.copy(default={
            'email_cc': False,
            'email_to': False,
            'partner_to': False,
            'reply_to': False,
        })

        for composition_mode, batch in (('comment', False), ('comment', True),
                                        ('mass_mail', False), ('mass_mail', True)):
            with self.subTest(composition_mode=composition_mode, batch=batch):
                self.assertFalse(
                    self.env['res.partner'].search([
                        ('email_normalized', 'in', ['test.cc.1@test.example.com',
                                                    'test.cc.2@test.example.com'])
                    ])
                )

                test_records = self.test_records if batch else self.test_record
                ctx = self._get_web_context(test_records, add_web=False, default_composition_mode=composition_mode)

                # 1. check without template + template update
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'body': '<p>Test Body</p>',
                    'partner_ids': base_recipients.ids,
                    'reply_to': 'my_reply_to@test.example.com',
                    'subject': 'My amazing subject',
                })

                # creation values are taken
                self.assertEqual(composer.partner_ids, base_recipients)
                self.assertEqual(composer.reply_to, 'my_reply_to@test.example.com')
                self.assertFalse(composer.reply_to_force_new)
                self.assertEqual(composer.reply_to_mode, 'update')

                # update with template with void values: void value is not forced in
                # rendering mode as well as when copying template values (and recipients
                # are not computed until sending in rendering mode)
                composer.write({'template_id': template_void.id})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()
                if composition_mode == 'comment':
                    self.assertEqual(composer.partner_ids, base_recipients)
                    self.assertEqual(composer.reply_to, 'my_reply_to@test.example.com')
                    self.assertFalse(composer.reply_to_force_new)
                else:
                    self.assertEqual(composer.partner_ids, base_recipients)
                    self.assertEqual(composer.reply_to, 'my_reply_to@test.example.com')
                    self.assertFalse(composer.reply_to_force_new)

                # changing template should update its content
                composer.write({'template_id': self.template.id})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()
                new_partners = self.env['res.partner'].search(
                    [('email_normalized', 'in', ['test.cc.1@test.example.com',
                                                 'test.cc.2@test.example.com'])
                    ]
                )

                # values come from template
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(len(new_partners), 2)
                    self.assertEqual(composer.partner_ids, self.partner_1 + new_partners, 'Template took customer_id as set on record')
                    self.assertEqual(composer.reply_to, 'info@test.example.com', 'Template was rendered')
                    self.assertFalse(composer.reply_to_force_new)  # should not change in comment mode
                else:
                    self.assertEqual(len(new_partners), 0)
                    self.assertEqual(composer.partner_ids, base_recipients, 'Mass mode: kept original values')
                    self.assertEqual(composer.reply_to, self.template.reply_to, 'Mass mode: raw template value')
                    self.assertFalse(composer.reply_to_force_new)  # should probably become True, not supported currently

                # manual values is kept over template
                composer.write({'partner_ids': [(5, 0), (4, self.partner_admin.id)]})
                self.assertEqual(composer.partner_ids, self.partner_admin)

                # reset template should reset values
                composer.write({'template_id': False})
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values are kepts, not sure why
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.partner_ids, self.partner_admin, 'Values are kept, not sure why')
                    self.assertEqual(composer.reply_to, 'info@test.example.com', 'Values are kept')
                    self.assertFalse(composer.reply_to_force_new)
                else:
                    self.assertEqual(composer.partner_ids, self.partner_admin, 'Mass mode: kept current value')
                    self.assertEqual(composer.reply_to, '{{ ctx.get("custom_reply_to") or "info@test.example.com" }}', 'Mass mode: kept current value')
                    self.assertFalse(composer.reply_to_force_new)

                # 2. check with default
                ctx['default_template_id'] = self.template.id
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'template_id': self.template.id,
                })
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values come from template
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.partner_ids, self.partner_1 + new_partners)
                else:
                    self.assertFalse(composer.partner_ids)
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.reply_to, "info@test.example.com")
                else:
                    self.assertEqual(composer.reply_to, self.template.reply_to)
                self.assertFalse(composer.reply_to_force_new)  # note: this should be updated with reply-to
                self.assertEqual(composer.reply_to_mode, 'update')  # note: this should be updated with reply-to

                # 3. check at create
                ctx.pop('default_template_id')
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'template_id': self.template.id,
                })
                # currently onchange necessary
                composer._onchange_template_id_wrapper()

                # values come from template
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.partner_ids, self.partner_1 + new_partners)
                else:
                    self.assertFalse(composer.partner_ids)
                if composition_mode == 'comment' and not batch:
                    self.assertEqual(composer.reply_to, "info@test.example.com")
                else:
                    self.assertEqual(composer.reply_to, self.template.reply_to)
                self.assertFalse(composer.reply_to_force_new)
                self.assertEqual(composer.reply_to_mode, 'update')

                # 4. template + user input
                ctx['default_template_id'] = self.template.id
                composer = self.env['mail.compose.message'].with_context(ctx).create({
                    'body': '<p>Test Body</p>',
                    'partner_ids': base_recipients.ids,
                    'subject': 'My amazing subject',
                    'reply_to': False,
                })

                # creation values are taken
                self.assertEqual(composer.partner_ids, base_recipients)
                self.assertFalse(composer.reply_to)
                self.assertFalse(composer.reply_to_force_new)
                self.assertEqual(composer.reply_to_mode, 'update')

                self.env['res.partner'].search([
                    ('email_normalized', 'in', ['test.cc.1@test.example.com',
                                                'test.cc.2@test.example.com'])
                ]).unlink()

    @users('employee')
    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_parent(self):
        """ Test specific management in comment mode when having parent_id set:
        record_name, subject, parent's partners. """
        parent_subject = "Parent Subject"
        parent = self.test_record.message_post(
            body='Test',
            partner_ids=(self.partner_1 + self.partner_2).ids,
            subject=parent_subject,
        )

        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=False, default_parent_id=parent.id)
        ).create({
            'body': '<p>Test Body</p>',
        })

        # creation values taken from parent
        self.assertEqual(composer.body, '<p>Test Body</p>')
        self.assertEqual(composer.parent_id, parent)
        self.assertEqual(composer.partner_ids, self.partner_1 + self.partner_2)
        self.assertEqual(composer.record_name, self.test_record.name)
        self.assertEqual(composer.subject, parent_subject)

    @users('user_rendering_restricted')
    @mute_logger('odoo.tests', 'odoo.addons.base.models.ir_rule', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_rights_attachments(self):
        """ Ensure a user without write access to a template can send an email"""
        template_1 = self.template.copy({
            'report_template_ids': [(6, 0, self.test_report.ids)],
        })
        attachment_data = self._generate_attachments_data(2, self.template._name, self.template.id)
        template_1.write({
            'attachment_ids': [(0, 0, dict(a, res_model="mail.template", res_id=template_1.id)) for a in attachment_data]
        })
        with self.assertRaises(AccessError):
            # ensure user_rendering_restricted has no write access
            template_1.with_user(self.env.user).write({'name': 'New Name'})

        template_1_attachments = template_1.attachment_ids
        self.assertEqual(len(template_1_attachments), 2)
        template_1_attachment_name = list(template_1_attachments.mapped('name')) + [f"TestReport for {self.test_record.name}.html"]

        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record)
        ).create({
            'subject': 'Template Subject',
            'body': '<p>Template Body</p>',
            'template_id': template_1.id,
            'attachment_ids': template_1_attachments.ids,
            'partner_ids': [self.partner_employee_2.id],
        })
        composer._onchange_template_id_wrapper()
        composer._action_send_mail()

        self.assertEqual(self.test_record.message_ids[0].subject, 'TemplateSubject TestRecord')
        self.assertEqual(
            sorted(self.test_record.message_ids[0].attachment_ids.mapped('name')),
            sorted(template_1_attachment_name))

    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_rights_portal(self):
        portal_user = self._create_portal_user()
        # give read access to the record to portal (for check access rule)
        self.test_record.message_subscribe(partner_ids=portal_user.partner_id.ids)

        # patch check access rights for write access, required to post a message by default
        with patch.object(MailTestTicket, 'check_access_rights', return_value=True):
            self.env['mail.compose.message'].with_user(portal_user).with_context(
                self._get_web_context(self.test_record)
            ).create({
                'subject': 'Subject',
                'body': '<p>Body text</p>',
                'partner_ids': []
            })._action_send_mail()

            self.assertEqual(self.test_record.message_ids[0].body, '<p>Body text</p>')
            self.assertEqual(self.test_record.message_ids[0].author_id, portal_user.partner_id)

            self.env['mail.compose.message'].with_user(portal_user).with_context({
                'default_composition_mode': 'comment',
                'default_parent_id': self.test_record.message_ids.ids[0],
            }).create({
                'subject': 'Subject',
                'body': '<p>Body text 2</p>'
            })._action_send_mail()

            self.assertEqual(self.test_record.message_ids[0].body, '<p>Body text 2</p>')
            self.assertEqual(self.test_record.message_ids[0].author_id, portal_user.partner_id)

    @users('employee')
    def test_mail_composer_save_template(self):
        self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=False)
        ).create({
            'subject': 'Template Subject',
            'body': '<p>Template Body</p>',
        }).action_save_as_template()

        # Test: email_template subject, body_html, model
        template = self.env['mail.template'].search([
            ('model', '=', self.test_record._name),
            ('subject', '=', 'Template Subject')
        ], limit=1)
        self.assertEqual(template.name, "%s: %s" % (self.env['ir.model']._get(self.test_record._name).name, 'Template Subject'))
        self.assertEqual(template.body_html, '<p>Template Body</p>', 'email_template incorrect body_html')


@tagged('mail_composer')
class TestComposerResultsComment(TestMailComposer, CronMixinCase):
    """ Test global output of composer used in comment mode. Test notably
    notification and emails generated during this process. """

    @users('employee')
    def test_mail_composer_default_subject(self):
        """ Make sure the default subject is applied in the composer. """
        simple_record = self.env['mail.test.simple'].create({'name': 'TestSimple'})
        ticket_record = self.env['mail.test.ticket'].create({'name': 'TestTicket'})

        # default behavior: use record name
        _, message = self.env['mail.compose.message'].with_context(
            self._get_web_context(simple_record, add_web=False, composition_mode='comment')
        ).create({
            'body': '<p>Test Body</p>',
        })._action_send_mail()
        self.assertEqual(message.subject, simple_record.name)

        # overridden in model
        _, message = self.env['mail.compose.message'].with_context(
            self._get_web_context(ticket_record, add_web=False, composition_mode='comment')
        ).create({
            'body': '<p>Test Body</p>',
        })._action_send_mail()
        self.assertEqual(message.subject, ticket_record._message_compute_subject())
        self.assertIn(f'Ticket for {ticket_record.name}', message.subject)

        # forced value
        _, message = self.env['mail.compose.message'].with_context(
            self._get_web_context(ticket_record, add_web=False, composition_mode='comment')
        ).create({
            'body': '<p>Test Body</p>',
            'subject': 'Forced Subject',
        })._action_send_mail()
        self.assertEqual(message.subject, 'Forced Subject',)

    @users('employee')
    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_notifications_delete(self):
        """ Notifications are correctly deleted once sent """
        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record)
        ).create({
            'body': '<p>Test Body</p>',
            'partner_ids': [(4, self.partner_1.id), (4, self.partner_2.id)]
        })
        self.assertTrue(composer.auto_delete, 'Comment mode removes notification emails by default')
        self.assertTrue(composer.auto_delete_keep_log)
        with self.mock_mail_gateway(mail_unlink_sent=True):
            composer._action_send_mail()

        # notifications
        message = self.test_record.message_ids[0]
        self.assertEqual(message.notified_partner_ids, self.partner_employee_2 + self.partner_1 + self.partner_2)

        # global outgoing
        self.assertEqual(len(self._mails), 3, 'Should have sent an email each recipient')
        self.assertEqual(len(self._new_mails), 2, 'Should have created 2 mail.mail (1 for users, 1 for customers)')
        self.assertFalse(self._new_mails.exists(), 'Should have deleted mail.mail records')

        # Check ``auto_delete`` field usage (note: currently not correctly managed)
        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record),
        ).create({
            'auto_delete': False,
            'body': '<p>Test Body</p>',
            'partner_ids': [(4, self.partner_1.id), (4, self.partner_2.id)]
        })
        self.assertFalse(composer.auto_delete)
        self.assertTrue(composer.auto_delete_keep_log)
        with self.mock_mail_gateway(mail_unlink_sent=True):
            composer._action_send_mail()

        # notifications
        message = self.test_record.message_ids[0]
        self.assertEqual(message.notified_partner_ids, self.partner_employee_2 + self.partner_1 + self.partner_2)

        # global outgoing
        self.assertEqual(len(self._mails), 3, 'Should have sent an email each recipient')
        self.assertEqual(len(self._new_mails), 2, 'Should have created 2 mail.mail (1 for users, 1 for customers)')
        self.assertEqual(len(self._new_mails.exists()), 2, 'Should not have deleted mail.mail records')

    @users('employee')
    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_post_parameters(self):
        """ Test various fields and tweaks in comment mode used for message_post
        parameters and process.. """
        # default behavior
        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record)
        ).create({
            'body': '<p>Test Body</p>',
        })
        _mail, message = composer._action_send_mail()
        self.assertEqual(message.body, '<p>Test Body</p>')
        self.assertTrue(message.email_add_signature)
        self.assertFalse(message.email_layout_xmlid)
        self.assertEqual(message.message_type, 'comment', 'Mail: default message type with composer is user comment')
        self.assertEqual(message.record_name, self.test_record.name)
        self.assertEqual(message.subtype_id, self.env.ref('mail.mt_comment', 'Mail: default subtype is comment'))

        # tweaks
        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record)
        ).create({
            'body': '<p>Test Body 2</p>',
            'email_add_signature': False,
            'email_layout_xmlid': 'mail.mail_notification_light',
            'message_type': 'notification',
            'subtype_id': self.env.ref('mail.mt_note').id,
            'partner_ids': [(4, self.partner_1.id), (4, self.partner_2.id)],
            'record_name': 'Custom record name',
        })
        _mail, message = composer._action_send_mail()
        self.assertEqual(message.body, '<p>Test Body 2</p>')
        self.assertFalse(message.email_add_signature)
        self.assertEqual(message.email_layout_xmlid, 'mail.mail_notification_light')
        self.assertEqual(message.message_type, 'notification')
        self.assertEqual(message.record_name, 'Custom record name')
        self.assertEqual(message.subtype_id, self.env.ref('mail.mt_note'))

        # subtype through xml id
        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record),
            default_subtype_xmlid='mail.mt_note',
        ).create({
            'body': '<p>Default subtype through xml id</p>',
        })
        _mail, message = composer._action_send_mail()
        self.assertEqual(message.subtype_id, self.env.ref('mail.mt_note'))

    @users('employee')
    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_recipients(self):
        """ Test partner_ids given to composer are given to the final message. """
        composer = self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record)
        ).create({
            'body': '<p>Test Body</p>',
            'partner_ids': [(4, self.partner_1.id), (4, self.partner_2.id)]
        })
        composer._action_send_mail()

        message = self.test_record.message_ids[0]
        self.assertEqual(message.author_id, self.user_employee.partner_id)
        self.assertEqual(message.body, '<p>Test Body</p>')
        self.assertEqual(message.subject, self.test_record._message_compute_subject())
        self.assertEqual(message.subtype_id, self.env.ref('mail.mt_comment'))
        self.assertEqual(message.partner_ids, self.partner_1 | self.partner_2)

    @users('employee')
    @mute_logger('odoo.models.unlink', 'odoo.addons.mail.models.mail_mail')
    def test_mail_composer_wtpl_complete(self):
        """ Test a posting process using a complex template, holding several
        additional recipients and attachments.

        This tests notifies: 2 new email_to (+ 1 duplicated), 1 email_cc,
        test_record followers and partner_admin added in partner_to."""
        attachment_data = self._generate_attachments_data(2, self.template._name, self.template.id)
        email_to_1 = 'test.to.1@test.example.com'
        email_to_2 = 'test.to.2@test.example.com'
        email_to_3 = 'test.to.1@test.example.com'  # duplicate: should not sent twice the email
        email_cc_1 = 'test.cc.1@test.example.com'
        self.template.write({
            'auto_delete': False,  # keep sent emails to check content
            'attachment_ids': [(0, 0, a) for a in attachment_data],
            'email_to': '%s, %s, %s' % (email_to_1, email_to_2, email_to_3),
            'email_cc': email_cc_1,
            'partner_to': '%s, {{ object.customer_id.id if object.customer_id else "" }}' % self.partner_admin.id,
            'report_template_ids': [(6, 0, self.test_report.ids)],
        })
        attachs = self.env['ir.attachment'].search([('name', 'in', [a['name'] for a in attachment_data])])
        self.assertEqual(len(attachs), 2)

        # ensure initial data
        self.assertEqual(self.test_record.user_id, self.user_employee_2)
        self.assertEqual(self.test_record.message_partner_ids, self.partner_employee_2)

        # open a composer and run it in comment mode
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        self.assertFalse(composer.reply_to_force_new, 'Mail: thread-enabled models should use auto thread by default')

        # due to scheduled_date, cron for sending notifciation will be used
        schedule_cron_id = self.env.ref('mail.ir_cron_send_scheduled_message').id
        with self.mock_mail_gateway(mail_unlink_sent=False), \
             self.mock_mail_app(), \
             freeze_time(self.reference_now), \
             self.capture_triggers(schedule_cron_id) as capt:
            composer._action_send_mail()

        # notification process should not have been sent
        self.assertEqual(capt.records.call_at, self.reference_now + timedelta(days=2),
                         msg='Should have created a cron trigger for the scheduled sending')
        self.assertFalse(self._new_mails)
        self.assertFalse(self._mails)

        # check new partners have been created based on emails given
        new_partners = self.env['res.partner'].search([
            ('email', 'in', [email_to_1, email_to_2, email_to_3, email_cc_1])
        ])
        self.assertEqual(len(new_partners), 3)
        self.assertEqual(set(new_partners.mapped('email')),
                         set(['test.to.1@test.example.com', 'test.to.2@test.example.com', 'test.cc.1@test.example.com'])
                        )

        # Send the scheduled message from the CRON
        with self.mock_mail_gateway(mail_unlink_sent=False), \
             self.mock_mail_app(), \
             freeze_time(self.reference_now + timedelta(days=3)):
            self.env['mail.message.schedule'].sudo()._send_notifications_cron()

        # global outgoing: one mail.mail (all customer recipients, then all employee recipients)
        # and 5 emails, and 1 inbox notification (admin)
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per group')
        self.assertEqual(len(self._mails), 5, 'Should have sent 5 emails, one per recipient')

        # template is sent only to partners (email_to are transformed)
        message = self.test_record.message_ids[0]
        self.assertMailMail(self.partner_employee_2, 'sent',
                            mail_message=message,
                            author=self.partner_employee,  # author != email_from (template sets only email_from)
                            email_values={
                                'body_content': 'TemplateBody %s' % self.test_record.name,
                                'email_from': self.test_record.user_id.email_formatted,  # set by template
                                'subject': 'TemplateSubject %s' % self.test_record.name,
                                'attachments_info': [
                                    {'name': 'AttFileName_00.txt', 'raw': b'AttContent_00', 'type': 'text/plain'},
                                    {'name': 'AttFileName_01.txt', 'raw': b'AttContent_01', 'type': 'text/plain'},
                                    {'name': 'TestReport for %s.html' % self.test_record.name, 'type': 'text/plain'},
                                ]
                            },
                            fields_values={
                                'mail_server_id': self.mail_server_domain,
                            },
                           )
        self.assertMailMail(self.test_record.customer_id + new_partners, 'sent',
                            mail_message=message,
                            author=self.partner_employee,  # author != email_from (template sets only email_from)
                            email_values={
                                'body_content': 'TemplateBody %s' % self.test_record.name,
                                'email_from': self.test_record.user_id.email_formatted,  # set by template
                                'subject': 'TemplateSubject %s' % self.test_record.name,
                                'attachments_info': [
                                    {'name': 'AttFileName_00.txt', 'raw': b'AttContent_00', 'type': 'text/plain'},
                                    {'name': 'AttFileName_01.txt', 'raw': b'AttContent_01', 'type': 'text/plain'},
                                    {'name': 'TestReport for %s.html' % self.test_record.name, 'type': 'text/plain'},
                                ]
                            },
                            fields_values={
                                'mail_server_id': self.mail_server_domain,
                            },
                           )

        # message is posted and notified admin
        self.assertEqual(message.subtype_id, self.env.ref('mail.mt_comment'))
        self.assertNotified(message, [{'partner': self.partner_admin, 'is_read': False, 'type': 'inbox'}])
        # attachments are copied on message and linked to document
        self.assertEqual(
            set(message.attachment_ids.mapped('name')),
            set(['AttFileName_00.txt', 'AttFileName_01.txt', 'TestReport for %s.html' % self.test_record.name])
        )
        self.assertEqual(set(message.attachment_ids.mapped('res_model')), set([self.test_record._name]))
        self.assertEqual(set(message.attachment_ids.mapped('res_id')), set(self.test_record.ids))
        self.assertTrue(all(attach not in message.attachment_ids for attach in attachs), 'Should have copied attachments')


@tagged('mail_composer')
class TestComposerResultsMass(TestMailComposer):

    @classmethod
    def setUpClass(cls):
        super(TestComposerResultsMass, cls).setUpClass()
        # ensure employee can create partners, necessary for templates
        cls.user_employee.write({
            'groups_id': [(4, cls.env.ref('base.group_partner_manager').id)],
        })

    @users('employee')
    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_delete(self):
        """ Check mail / msg delete support """
        # ensure initial data
        self.assertTrue(self.template.auto_delete)
        self.assertEqual(self.test_records.user_id, self.user_employee_2)
        self.assertEqual(self.test_records.message_partner_ids, self.partner_employee_2)

        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        self.assertTrue(composer.auto_delete, 'Should take composer value')
        self.assertTrue(composer.auto_delete_keep_log)
        with self.mock_mail_gateway(mail_unlink_sent=True), self.mock_mail_app():
            composer._action_send_mail()

        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record')
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record')
        self.assertFalse(self._new_mails.exists(), 'Should have deleted mail.mail records')
        self.assertEqual(len(self._new_msgs), 2, 'Should have created 1 mail.mail per record')
        self.assertEqual(self._new_msgs.exists(), self._new_msgs, 'Should not have deleted mail.message records')

        # force composer auto_delete field
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        composer.auto_delete = False
        with self.mock_mail_gateway(mail_unlink_sent=True), self.mock_mail_app():
            composer._action_send_mail()

        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record')
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record')
        self.assertEqual(self._new_mails.exists(), self._new_mails, 'Should not have deleted mail.mail records')
        self.assertEqual(len(self._new_msgs), 2, 'Should have created 1 mail.mail per record')
        self.assertEqual(self._new_msgs.exists(), self._new_msgs, 'Should not have deleted mail.message records')

        # check composer auto_delete_keep_log
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        composer.auto_delete_keep_log = False
        with self.mock_mail_gateway(mail_unlink_sent=True), self.mock_mail_app():
            composer._action_send_mail()

        # global outgoing
        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record')
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record')
        self.assertFalse(self._new_mails.exists(), 'Should have deleted mail.mail records')
        self.assertEqual(len(self._new_msgs), 2, 'Should have created 1 mail.mail per record')
        self.assertFalse(self._new_msgs.exists(), 'Should have deleted mail.message records')

    @users('employee')
    @mute_logger('odoo.tests', 'odoo.addons.mail.models.mail_mail', 'odoo.models.unlink')
    def test_mail_composer_document_based(self):
        """ Tests a document-based mass mailing with the same address mails
        This should be allowed and not considered as duplicate in this context
        """
        self.test_records.write({
            'customer_id': False,
            'email_from': 'duplicate.email@test.example.com',
        })
        self.template.write({
            'auto_delete': False,  # keep sent emails to check content
            'email_to': '{{ object.email_from }}',
            'partner_to': '',
        })
        # launch composer in mass mode
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        with self.mock_mail_gateway(mail_unlink_sent=False), self.mock_mail_app():
            composer.with_context(mailing_document_based=False)._action_send_mail()
        self.assertEqual(len(self._mails), 1, 'Should have sent 1 email, and skipped a duplicate.')

        with self.mock_mail_gateway(mail_unlink_sent=False), self.mock_mail_app():
            composer.with_context(mailing_document_based=True)._action_send_mail()
        self.assertEqual(len(self._mails), 2, 'Should have sent 2 emails.')

    @users('employee')
    @mute_logger('odoo.models.unlink', 'odoo.addons.mail.models.mail_mail')
    def test_mail_composer_wtpl(self):
        self.template.auto_delete = False  # keep sent emails to check content

        # ensure initial data
        self.assertEqual(self.test_records.user_id, self.user_employee_2)
        self.assertEqual(self.test_records.message_partner_ids, self.partner_employee_2)

        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        self.assertFalse(composer.reply_to_force_new, 'Mail: thread-enabled models should use auto thread by default')
        with self.mock_mail_gateway(mail_unlink_sent=True):
            composer._action_send_mail()

        # global outgoing
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record')
        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record')

        for record in self.test_records:
            # message copy is kept
            message = record.message_ids[0]

            # template is sent directly using customer field, meaning we have recipients
            self.assertMailMail(record.customer_id, 'sent',
                                mail_message=message,
                                author=self.partner_employee,
                                email_values={
                                    'email_from': self.partner_employee_2.email_formatted,
                                })

            # message content
            self.assertEqual(message.subject, 'TemplateSubject %s' % record.name)
            self.assertEqual(message.body, '<p>TemplateBody %s</p>' % record.name)
            self.assertEqual(message.author_id, self.user_employee.partner_id)
            # post-related fields are void
            self.assertFalse(message.subtype_id)
            self.assertFalse(message.partner_ids)

    @users('employee')
    @mute_logger('odoo.models.unlink', 'odoo.addons.mail.models.mail_mail')
    def test_mail_composer_wtpl_complete(self):
        """ Test a composer in mass mode with a quite complete template, containing
        notably email-based recipients and attachments. """
        attachment_data = self._generate_attachments_data(2, self.template._name, self.template.id)
        email_to_1 = 'test.to.1@test.example.com'
        email_to_2 = 'test.to.2@test.example.com'
        email_to_3 = 'test.to.1@test.example.com'  # duplicate: should not sent twice the email
        email_cc_1 = 'test.cc.1@test.example.com'
        self.template.write({
            'auto_delete': False,  # keep sent emails to check content
            'attachment_ids': [(0, 0, a) for a in attachment_data],
            'email_to': '%s, %s, %s' % (email_to_1, email_to_2, email_to_3),
            'email_cc': email_cc_1,
            'partner_to': '%s, {{ object.customer_id.id if object.customer_id else "" }}' % self.partner_admin.id,
            'report_template_ids': [(6, 0, self.test_report.ids)],
        })
        attachs = self.env['ir.attachment'].search([('name', 'in', [a['name'] for a in attachment_data])])
        self.assertEqual(len(attachs), 2)

        # ensure initial data
        self.assertEqual(self.test_records.user_id, self.user_employee_2)
        self.assertEqual(self.test_records.message_partner_ids, self.partner_employee_2)

        # launch composer in mass mode
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        with self.mock_mail_gateway(mail_unlink_sent=False):
            composer._action_send_mail()

        new_partners = self.env['res.partner'].search([
            ('email', 'in', [email_to_1, email_to_2, email_to_3, email_cc_1])
        ])
        self.assertEqual(len(new_partners), 3)

        # global outgoing
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record')
        self.assertEqual(len(self._mails), 10, 'Should have sent 5 emails per record')

        # hack to use assertEmails: filtering on from/to only is not sufficient to distinguish emails
        _mails_records = [
            [mail for mail in self._mails if '%s-%s' % (record.id, record._name) in mail['message_id']]
            for record in self.test_records
        ]

        for record, _mails in zip(self.test_records, _mails_records):
            # message copy is kept
            message = record.message_ids[0]

            # template is sent only to partners (email_to are transformed)
            self._mails = _mails
            self.assertMailMail(record.customer_id + new_partners + self.partner_admin,
                                'sent',
                                mail_message=message,
                                author=self.partner_employee,
                                email_values={
                                    'attachments_info': [
                                        {'name': 'AttFileName_00.txt', 'raw': b'AttContent_00', 'type': 'text/plain'},
                                        {'name': 'AttFileName_01.txt', 'raw': b'AttContent_01', 'type': 'text/plain'},
                                        {'name': 'TestReport for %s.html' % record.name, 'type': 'text/plain'},
                                    ],
                                    'body_content': 'TemplateBody %s' % record.name,
                                    'email_from': self.partner_employee_2.email_formatted,
                                    'subject': 'TemplateSubject %s' % record.name,
                                },
                                fields_values={
                                    'email_from': self.partner_employee_2.email_formatted,
                                    'mail_server_id': self.mail_server_domain,
                                    'reply_to': formataddr((
                                        f'{self.env.user.company_id.name} {record.name}',
                                        f'{self.alias_catchall}@{self.alias_domain}'
                                    )),
                                    'subject': 'TemplateSubject %s' % record.name,
                                },
                               )

        # test without catchall filling reply-to
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer = composer_form.save()
        with self.mock_mail_gateway(mail_unlink_sent=True):
            # remove alias so that _notify_get_reply_to will return the default value instead of alias
            self.env['ir.config_parameter'].sudo().set_param("mail.catchall.domain", None)
            composer.action_send_mail()

        # hack to use assertEmails: filtering on from/to only is not sufficient to distinguish emails
        _mails_records = [
            [mail for mail in self._mails if '%s-%s' % (record.id, record._name) in mail['message_id']]
            for record in self.test_records
        ]

        for record, _mails in zip(self.test_records, _mails_records):
            # template is sent only to partners (email_to are transformed)
            self._mails = _mails
            self.assertMailMail(record.customer_id + new_partners + self.partner_admin,
                                'sent',
                                mail_message=record.message_ids[0],
                                author=self.partner_employee,
                                email_values={
                                    'email_from': self.partner_employee_2.email_formatted,
                                    'reply_to': self.partner_employee_2.email_formatted,
                                },
                                fields_values={
                                    'email_from': self.partner_employee_2.email_formatted,
                                    'reply_to': self.partner_employee_2.email_formatted,
                                },
                               )

    @users('employee')
    @mute_logger('odoo.models.unlink', 'odoo.addons.mail.models.mail_mail')
    def test_mail_composer_wtpl_recipients(self):
        """ Test various combinations of recipients: res_domain, active_id,
        active_ids, ... to ensure fallback behavior are working. """
        # 1: active ids
        composer_form = Form(self.env['mail.compose.message'].with_context(
            active_ids=self.test_records.ids,
            default_composition_mode='mass_mail',
            default_model=self.test_records._name,
            default_template_id=self.template.id,
        ))
        composer = composer_form.save()
        self.assertEqual(sorted(literal_eval(composer.res_ids)), sorted(self.test_records.ids))

        with self.mock_mail_gateway(mail_unlink_sent=True):
            composer._action_send_mail()

        # should create emails in a single batch
        self.assertEqual(self.build_email_mocked.call_count, 2, 'One build email per outgoing email')
        self.assertEqual(self.mail_mail_create_mocked.call_count, 2, 'Emails are anyway created in a singleton loop')
        # global outgoing
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record based on active_ids')
        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record based on  on active_ids')

        for record in self.test_records:
            # template is sent directly using customer field, even if author is partner_employee
            self.assertSentEmail(self.partner_employee_2.email_formatted,
                                 record.customer_id)

        # 2: default_res_ids + active_ids -> res_ids takes lead
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_record, add_web=False,
                                  default_composition_mode='mass_mail',
                                  default_res_ids=self.test_record.ids,
                                  default_template_id=self.template.id,
                                  active_ids=self.test_records.ids,
                                 )
        ))
        composer = composer_form.save()
        self.assertEqual(literal_eval(composer.res_ids), self.test_record.ids)

        with self.mock_mail_gateway(mail_unlink_sent=True):
            composer._action_send_mail()

        # global outgoing
        self.assertEqual(len(self._new_mails), 1, 'Should have taken default_res_ids (1 record)')
        self.assertEqual(len(self._mails), 1, 'Should have taken default_res_ids (1 record)')

        # template is sent directly using customer field, even if author is partner_employee
        self.assertSentEmail(self.partner_employee_2.email_formatted,
                             self.test_record.customer_id)

        # 3: fallback on active_id if not active_ids
        composer_form = Form(self.env['mail.compose.message'].with_context(
            active_id=self.test_record.id,
            default_composition_mode='mass_mail',
            default_model=self.test_records._name,
            default_template_id=self.template.id,
        ))
        composer = composer_form.save()
        self.assertEqual(literal_eval(composer.res_ids), self.test_record.ids)

        with self.mock_mail_gateway(mail_unlink_sent=False):
            composer._action_send_mail()

        # global outgoing
        self.assertEqual(len(self._new_mails), 1, 'Should have created 1 mail.mail per record')
        self.assertEqual(len(self._mails), 1, 'Should have sent 1 email per record')

        # 4: _batch_size limit for active_ids
        with patch.object(MailComposer, '_batch_size', new=1):
            composer_form = Form(self.env['mail.compose.message'].with_context(
                active_ids=self.test_records.ids,
                default_composition_mode='mass_mail',
                default_model=self.test_records._name,
                default_template_id=self.template.id,
            ))
            composer = composer_form.save()
            self.assertTrue(composer.composition_batch)
            self.assertEqual(composer.composition_mode, 'mass_mail')
            self.assertFalse(composer.res_ids)

            with self.mock_mail_gateway(mail_unlink_sent=True):
                composer._action_send_mail()

        # should create emails in 2 batches of 1
        self.assertEqual(self.build_email_mocked.call_count, 2)
        self.assertEqual(self.mail_mail_create_mocked.call_count, 2)
        # global outgoing
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record based on active_ids')
        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record based on  on active_ids')

        # 5: mail.batch_size config parameter support, for sending only
        self.env['ir.config_parameter'].sudo().set_param('mail.batch_size', 1)
        with patch.object(MailComposer, '_batch_size', new=50):
            composer_form = Form(self.env['mail.compose.message'].with_context(
                active_ids=self.test_records.ids,
                default_composition_mode='mass_mail',
                default_model=self.test_records._name,
                default_template_id=self.template.id,
            ))
            composer = composer_form.save()
            self.assertTrue(composer.composition_batch)
            self.assertEqual(composer.composition_mode, 'mass_mail')
            self.assertEqual(sorted(literal_eval(composer.res_ids)), sorted(self.test_records.ids))

            with self.mock_mail_gateway(mail_unlink_sent=True):
                composer._action_send_mail()

        # should create emails in 2 batches of 1
        self.assertEqual(self.build_email_mocked.call_count, 2)
        self.assertEqual(self.mail_mail_create_mocked.call_count, 2)
        # global outgoing
        self.assertEqual(len(self._new_mails), 2, 'Should have created 1 mail.mail per record based on active_ids')
        self.assertEqual(len(self._mails), 2, 'Should have sent 1 email per record based on  on active_ids')

        # 6: void is void: raise in comment mode, just don't send anything in mass mail mode
        composer_form = Form(self.env['mail.compose.message'].with_context(
            default_model='mail.test.ticket',
            default_template_id=self.template.id
        ))
        composer = composer_form.save()
        self.assertEqual(composer.composition_mode, 'comment')
        with self.mock_mail_gateway(mail_unlink_sent=False), self.assertRaises(ValueError):
            composer._action_send_mail()
        self.assertNotSentEmail()

        composer_form = Form(self.env['mail.compose.message'].with_context(
            default_composition_mode='mass_mail',
            default_model='mail.test.ticket',
            default_template_id=self.template.id
        ))
        composer = composer_form.save()
        self.assertEqual(composer.composition_mode, 'mass_mail')
        with self.mock_mail_gateway(mail_unlink_sent=False):
            composer._action_send_mail()
        self.assertNotSentEmail()

    @users('employee')
    @mute_logger('odoo.models.unlink', 'odoo.addons.mail.models.mail_mail')
    def test_mail_composer_wtpl_recipients_res_domain(self):
        """ Test specific use case of res_domain usage, in combination with
        res_domain_user_id allowing to set the evaluation environment for
        the domain. """
        def _search_as_employee_2(recordset, *args, **kwargs):
            """ Mock to return only one record, simulating a specific ir.rule """
            if recordset.env.uid == self.user_employee_2.id:
                return self.test_records[0]
            return DEFAULT

        composer_form = Form(self.env['mail.compose.message'].with_context(
            default_composition_mode='mass_mail',
            default_model=self.test_records._name,
            default_res_domain=[('id', 'in', self.test_records.ids)],
            default_res_domain_user_id=self.user_employee_2.id,
            default_template_id=self.template.id,
        ))
        composer = composer_form.save()
        self.assertEqual(literal_eval(composer.res_domain), [('id', 'in', self.test_records.ids)])
        self.assertEqual(composer.res_domain_user_id, self.user_employee_2)

        with self.mock_mail_gateway(mail_unlink_sent=True), \
            patch.object(MailTestTicket, 'search', autospec=True, side_effect=_search_as_employee_2):
            composer._action_send_mail()

        # global outgoing
        self.assertEqual(len(self._new_mails), 1, 'Should have created 1 mail.mail, search done by employee 2')
        self.assertEqual(len(self._mails), 1, 'Should have sent 1 email, search done by employee 2')

        # template is sent directly using customer field, whatever the author
        self.assertSentEmail(self.partner_employee_2.email_formatted,
                             self.test_records[0].customer_id)

    @users('employee')
    @mute_logger('odoo.models.unlink', 'odoo.addons.mail.models.mail_mail')
    def test_mail_composer_wtpl_reply_to_force_new(self):
        """ Test no auto thread behavior, notably with reply-to. """
        # launch composer in mass mode
        composer_form = Form(self.env['mail.compose.message'].with_context(
            self._get_web_context(self.test_records, add_web=True,
                                  default_template_id=self.template.id)
        ))
        composer_form.reply_to_mode = 'new'
        composer_form.reply_to = "{{ '\"' + object.name + '\" <%s>' % 'dynamic.reply.to@test.com' }}"
        composer = composer_form.save()
        self.assertTrue(composer.reply_to_force_new)
        with self.mock_mail_gateway(mail_unlink_sent=False):
            composer.action_send_mail()

        for record in self.test_records:
            self.assertMailMail(record.customer_id,
                                'sent',
                                mail_message=record.message_ids[0],
                                author=self.partner_employee,
                                email_values={
                                    'body_content': 'TemplateBody %s' % record.name,
                                    'email_from': self.partner_employee_2.email_formatted,
                                    'reply_to': formataddr((
                                        f'{record.name}',
                                        'dynamic.reply.to@test.com'
                                    )),
                                    'subject': 'TemplateSubject %s' % record.name,
                                },
                                fields_values={
                                    'email_from': self.partner_employee_2.email_formatted,
                                    'reply_to': formataddr((
                                        f'{record.name}',
                                        'dynamic.reply.to@test.com'
                                    )),
                                },
                               )
