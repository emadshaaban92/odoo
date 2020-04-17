# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.crm.tests.common import TestCrmCommon, INCOMING_EMAIL
from odoo.tests.common import users
from odoo.tools import mute_logger
from odoo.tests import Form


class TestCRMLead(TestCrmCommon):

    @users('user_sales_manager')
    def test_crm_lead_creation_partner(self):
        lead = self.env['crm.lead'].create({
            'name': 'TestLead',
            'contact_name': 'Raoulette TestContact',
            'email_from': '"Raoulette TestContact" <raoulette@test.example.com>',
        })
        self.assertEqual(lead.type, 'lead')
        self.assertEqual(lead.user_id, self.user_sales_manager)
        self.assertEqual(lead.team_id, self.sales_team_1)
        self.assertEqual(lead.stage_id, self.stage_team1_1)
        self.assertEqual(lead.contact_name, 'Raoulette TestContact')
        self.assertEqual(lead.email_from, '"Raoulette TestContact" <raoulette@test.example.com>')

        # update to a partner, should udpate address
        lead.write({'partner_id': self.contact_1.id})
        # self.assertEqual(lead.partner_name, self.contact_company_1.name)
        # self.assertEqual(lead.contact_name, self.contact_1.name)
        # self.assertEqual(lead.email_from, self.contact_1.email)
        # self.assertEqual(lead.street, self.contact_1.street)
        # self.assertEqual(lead.city, self.contact_1.city)
        # self.assertEqual(lead.zip, self.contact_1.zip)
        # self.assertEqual(lead.country_id, self.contact_1.country_id)

    @users('user_sales_manager')
    def test_crm_lead_stages(self):
        lead = self.lead_1.with_user(self.env.user)
        self.assertEqual(lead.team_id, self.sales_team_1)

        lead.convert_opportunity(self.contact_1.id)
        self.assertEqual(lead.team_id, self.sales_team_1)

        lead.action_set_won()
        self.assertEqual(lead.probability, 100.0)
        self.assertEqual(lead.stage_id, self.stage_gen_won)  # generic won stage has lower sequence than team won stage

    @users('user_sales_manager')
    def test_crm_team_alias(self):
        new_team = self.env['crm.team'].create({
            'name': 'TestAlias',
            'use_leads': True,
            'use_opportunities': True,
            'alias_name': 'test.alias'
        })
        self.assertEqual(new_team.alias_id.alias_name, 'test.alias')
        self.assertEqual(new_team.alias_name, 'test.alias')

        new_team.write({
            'use_leads': False,
            'use_opportunities': False,
        })
        # self.assertFalse(new_team.alias_id.alias_name)
        # self.assertFalse(new_team.alias_name)

    def test_mailgateway(self):
        new_lead = self.format_and_process(
            INCOMING_EMAIL,
            'unknown.sender@test.example.com',
            '%s@%s' % (self.sales_team_1.alias_name, self.alias_domain),
            subject='Delivery cost inquiry',
            target_model='crm.lead',
        )
        self.assertEqual(new_lead.email_from, 'unknown.sender@test.example.com')
        self.assertFalse(new_lead.partner_id)
        self.assertEqual(new_lead.name, 'Delivery cost inquiry')

        message = new_lead.with_user(self.user_sales_manager).message_post(
            body='Here is my offer !',
            subtype_xmlid='mail.mt_comment')
        self.assertEqual(message.author_id, self.user_sales_manager.partner_id)

        new_lead.handle_partner_assignment(create_missing=True)
        self.assertEqual(new_lead.partner_id.email, 'unknown.sender@test.example.com')
        self.assertEqual(new_lead.partner_id.team_id, self.sales_team_1)

    @mute_logger('odoo.addons.phone_validation.tools.phone_validation')
    def test_field_email_and_phone(self):
        lead, partner = self.lead_1, self.contact_2
        lead.partner_id = partner

        # email & phone must be automatically set on the lead
        lead_form = Form(lead)
        lead_form.partner_id = partner
        lead = lead_form.save()
        self.assertEqual(lead.email_from, partner.email)
        self.assertEqual(lead.phone, partner.phone)

        # writing on the lead field must change the partner field
        lead_form = Form(lead)
        lead_form.email_from = 'new@email.com'
        lead_form.phone = '+32499999999'
        lead = lead_form.save()
        self.assertEqual(lead.email_from, partner.email)
        self.assertEqual(lead.phone, partner.phone)
        self.assertEqual(lead.phone, '+32 499 99 99 99')

        # writing on the partner must change the lead values
        partner_form = Form(partner)
        partner_form.email = 'new_super@email.com'
        partner_form.phone = '+32488888888'
        partner = partner_form.save()

        self.assertEqual('new_super@email.com', lead.email_from)
        self.assertEqual('+32 488 88 88 88', lead.phone)
