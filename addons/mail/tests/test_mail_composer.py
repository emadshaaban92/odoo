# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import re

from odoo.addons.mail.tests.common import MailCommon
from odoo.tests import tagged, users


@tagged('mail_composer')
class TestMailComposer(MailCommon):

    @classmethod
    def setUpClass(cls):
        super(TestMailComposer, cls).setUpClass()
        cls.env['ir.config_parameter'].set_param('mail.restrict.template.rendering', True)
        cls.user_employee.groups_id -= cls.env.ref('mail.group_mail_template_editor')
        cls.test_record = cls.env['res.partner'].with_context(cls._test_context).create({
            'name': 'Test',
        })
        cls.body_html = """<div>
    <h1>Hello sir!</h1>
    <p>Here! <a href="https://www.example.com">
        <!--[if mso]>
            <i style="letter-spacing: 25px; mso-font-width: -100%; mso-text-raise: 30pt;">&nbsp;</i>
        <![endif]-->
        A link for you! <!-- my favorite example -->
        <!--[if mso]>
            <i style="letter-spacing: 25px; mso-font-width: -100%;">&nbsp;</i>
        <![endif]-->
    </a> Make good use of it.</p>
</div>"""

        cls.mail_template = cls.env['mail.template'].create({
            'name': 'Test template with mso conditionals',
            'subject': 'MSO FTW',
            'body_html': cls.body_html,
            'lang': '{{ object.lang }}',
            'auto_delete': True,
            'model_id': cls.env.ref('base.model_res_partner').id,
        })

    @users('employee')
    def test_mail_mass_mode_template_with_mso(self):
        mail_compose_message = self.env['mail.compose.message'].create({
            'composition_mode': 'mass_mail',
            'model': 'res.partner',
            'template_id': self.mail_template.id,
            'subject': 'MSO FTW',
        })

        values = mail_compose_message.get_mail_values(self.partner_employee.ids)

        self.assertIn(
            self.body_html,
            values[self.partner_employee.id]['body_html'],
            'We must preserve (mso) comments in email html'
        )

    @users('employee')
    def test_mail_mass_mode_compose_with_mso(self):
        composer = self.env['mail.compose.message'].with_context({
            'default_model': self.test_record._name,
            'default_composition_mode': 'mass_mail',
            'active_ids': [self.test_record.id],
            'active_model': self.test_record._name,
            'active_id': self.test_record.id
        }).create({
            'body': self.body_html,
            'partner_ids': [(4, self.partner_employee.id)],
            'composition_mode': 'mass_mail',
        })
        with self.mock_mail_gateway(mail_unlink_sent=True):
            composer._action_send_mail()

        values = composer.get_mail_values(self.partner_employee.ids)

        self.assertIn(
            self.body_html,
            values[self.partner_employee.id]['body_html'],
            'We must preserve (mso) comments in email html'
        )

    @users('employee')
    def test_mail_attachment_to_download_link(self):
        """ Test that when mail size exceed the max email size limit, attachment are turned into download links added
        at the end of the email content. """
        attachment_size_in_bytes = 1024 * 128
        datas = base64.b64encode((''.join('.' for _ in range(0, attachment_size_in_bytes))).encode())
        attachment1_name = 'attachment1'
        attachment2_name = 'attachment2'
        attachments = self.env['ir.attachment'].sudo().create([{
            'name': attachment1_name,
            'res_name': 'test',
            'res_model': self.test_record._name,
            'res_id': self.test_record.id,
            'datas': datas,
        }, {
            'name': attachment2_name,
            'res_name': 'test',
            'res_model': self.test_record._name,
            'res_id': self.test_record.id,
            'datas': datas,
        }])
        match_download_links = [re.compile(fr'.*<a.*href.*/web/content/([^?]*)\?.*access_token.*>.*{attachment_name}.*</a>', re.DOTALL)
                                for attachment_name in [attachment1_name, attachment2_name]]

        def send_mail(max_email_size):
            self.mail_server_global.max_email_size = max_email_size
            self.mail_server_domain.max_email_size = max_email_size
            composer = self.env['mail.compose.message'].with_context({
                'default_model': self.test_record._name,
                'default_composition_mode': 'mass_mail',
                'active_ids': [self.test_record.id],
                'active_model': self.test_record._name,
                'active_id': self.test_record.id
            }).create({
                'body': self.body_html,
                'partner_ids': [(4, self.partner_employee.id)],
                'composition_mode': 'mass_mail',
                'attachment_ids': attachments,
            })
            with self.mock_smtplib_connection():
                composer._action_send_mail()

        send_mail(1)
        # To match links, we need to remove LR and "=" due to the mail encoder that breaks line at 80 chars and add "="
        message = re.sub(r'[\s=]', '', self.emails[0]['message'])
        self.assertGreater(len(message), attachment_size_in_bytes * 2,
                           'All attachments are present')
        self.assertFalse(any(pattern.match(message) for pattern in match_download_links),
                         'Attachment are not turned into download links')
        self.assertTrue(all(not attachment.access_token for attachment in attachments),
                        'Original attachment not modified (access_token not added)')
        send_mail(0.25)
        message = re.sub(r'[\s=]', '', self.emails[0]['message'])
        self.assertLess(len(message), attachment_size_in_bytes,
                        'Attachment have been removed (replaced by download links)')
        self.assertTrue(all(pattern.match(message) for pattern in match_download_links),
                        'All attachment are turned into download links')
        self.assertTrue(all(self.env['ir.attachment'].browse(int(pattern.findall(message)[0])).access_token
                            for pattern in match_download_links),
                        'All download links target attachment with access token')
        self.assertTrue(all(not attachment.access_token for attachment in attachments),
                        'Original attachment not modified (access_token not added)')
