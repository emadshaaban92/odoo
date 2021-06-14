# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_slides.tests import common
from odoo.tests import tagged, users
from odoo.tests.common import HOST
from odoo.tools import config

@tagged('post_install', '-at_install')
class TestMembership(common.SlidesCase):

    @users('user_officer')
    def test_invite_to_course(self):
        user_portal_partner = self.user_portal.partner_id
        self.assertFalse(user_portal_partner.id in self.channel.partner_ids.ids)

        # Invite partner to course
        self.slide_channel_invite_wizard = self.env['slide.channel.invite'].create({
            'channel_id': self.channel.id,
            'partner_ids': [(6, 0, [self.user_portal.partner_id.id])],
        })
        self.slide_channel_invite_wizard.action_invite()

        # The partner should be in the attendees with invitation pending status
        user_portal_channel_partner = self.channel.channel_partner_all_ids.filtered(lambda p: p.partner_id.id == user_portal_partner.id)
        self.assertTrue(user_portal_channel_partner)
        self.assertTrue(self.channel.with_user(self.user_portal).is_member_invited)
        self.assertFalse(user_portal_channel_partner.id in self.channel.channel_partner_ids.ids)
        self.assertFalse(self.channel.with_user(self.user_portal).is_member)
        self.assertEqual(user_portal_channel_partner.member_status, 'invited')

        # Do not subscribe invited members to the chatter
        self.assertFalse(user_portal_partner.id in self.channel.message_partner_ids.ids)

    @users('user_officer')
    def test_attendee_default_create(self):
        slide_channel_partner = self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': self.user_portal.partner_id.id
        })

        # By default, partner is enrolled and subscribed to chatter
        self.assertTrue(self.user_portal.partner_id.id in self.channel.message_partner_ids.ids)
        self.assertFalse(self.channel.with_user(self.user_portal).is_member_invited)
        self.assertTrue(self.channel.with_user(self.user_portal).is_member)
        self.assertEqual(slide_channel_partner.member_status, 'joined')

    @users('user_officer')
    def test_join_enroll_invite_channel(self):
        self.channel.write({'enroll': 'invite'})
        user_portal_partner = self.user_portal.partner_id

        # Uninvited partner cannot join the course
        self.channel.with_user(self.user_portal).action_add_member()
        self.assertFalse(user_portal_partner.id in self.channel.partner_ids.ids)

        user_portal_channel_partner = self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': user_portal_partner.id,
            'member_status': 'invited'
        })

        self.assertTrue(user_portal_partner.id in self.channel.partner_all_ids.ids)
        self.assertFalse(user_portal_partner.id in self.channel.partner_ids.ids)
        # Invited partner can join the course and enroll itself. It is added in chatter subscribers
        self.channel.with_user(self.user_portal).action_add_member()
        self.assertEqual(user_portal_channel_partner.member_status, 'joined')
        self.assertTrue(user_portal_partner.id in self.channel.partner_ids.ids)
        self.assertTrue(self.user_portal.partner_id.id in self.channel.message_partner_ids.ids)

    @users('user_officer')
    def test_slide_channel_partner_ids_search(self):
        ''' Test the behavior of partner_ids (enrolled partners) vs partner_all_ids (invited + enrolled partners)'''
        invited_cp, joined_cp = self.env['slide.channel.partner'].create([{
            'channel_id': self.channel.id,
            'partner_id': self.user_portal.partner_id.id,
            'member_status': 'invited'
        }, {
            'channel_id': self.channel.id,
            'partner_id': self.user_emp.partner_id.id,
            'member_status': 'joined'
        }])

        # Search on model
        invited_cp_channel_ids = self.env['slide.channel'].search([('partner_ids', '=', invited_cp.partner_id.id)])
        self.assertFalse(self.channel in invited_cp_channel_ids)
        joined_cp_channel_ids = self.env['slide.channel'].search([('partner_ids', '=', joined_cp.partner_id.id)])
        self.assertTrue(self.channel in joined_cp_channel_ids)

        # partner_ids should only contain enrolled channel partners
        partner_ids = self.channel.partner_ids
        self.assertFalse(invited_cp.partner_id in partner_ids)
        self.assertTrue(joined_cp.partner_id in partner_ids)

        # partner_all_ids also contains invited channel partners.
        partner_all_ids = self.channel.partner_all_ids
        self.assertTrue(joined_cp.partner_id in partner_all_ids)
        self.assertTrue(invited_cp.partner_id in partner_all_ids)


@tagged('-at_install', 'post_install')
class TestMembershipCase(HttpCaseWithUserPortal):

    def setUp(self):
        super(TestMembershipCase, self).setUp()
        self.user_admin = self.env.ref('base.user_admin')
        self.user_emp = mail_new_test_user(
            self.env,
            email='employee@example.com',
            groups='base.group_user',
            login='user_emp',
            name='Eglantine Employee',
            notification_type='email',
        )
        self.channel = self.env['slide.channel'].with_user(self.user_admin).create({
            'name': 'All about member status - Members only',
            'channel_type': 'training',
            'enroll': 'public',
            'visibility': 'public',
            'is_published': True,
        })
        self.slide = self.env['slide.slide'].with_user(self.user_admin).create({
            'name': 'How to understand membership',
            'channel_id': self.channel.id,
            'slide_type': 'article',
            'is_published': True,
            'completion_time': 2.0,
            'sequence': 1,
        })
        self.partner_nan = self.env['res.partner'].create({
            'country_id': self.env.ref('base.be').id,
            'email': 'partnerNan@partnerNan.example.com',
            'mobile': '0416001133',
            'name': 'Partner Nan',
        })
        self.common_base_url = "http://%s:%s" % (HOST, config['http_port'])

    def test_direct_invite_route_members_only_course(self):
        ''' Invite route redirects properly the (not) logged user in a course with members-only visibility'''
        self.channel.write({'visibility': 'members'})
        self.env['res.config.settings'].create({'auth_signup_uninvited': 'b2c'})
        # Logged user now has a pending invitation to the course
        channel_partner_emp = self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': self.user_emp.partner_id.id,
            'member_status': 'invited'
        })
        invite_url = channel_partner_emp.invitation_link_with_hash

        # No user logged
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/login' in res.url, "Should redirect to login page if unlogged.")
        self.assertTrue(f'&redirect=/slides/{self.channel.id}/invite?' in res.url, "Login should redirect to the invite route.")

        # Logged user has a pending invitation to the course
        self.authenticate("user_emp", "user_emp")
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'slides/{slug(self.channel)}' in res.url, "Should redirect to the course page")

        # Hash is wrong
        invite_url_false_hash = invite_url + 'abc'
        res = self.url_open(invite_url_false_hash)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=hash_fail' in res.url, "A wrong hash should redirect to the main /slides page")

        # Link is for another user
        self.authenticate("portal", "portal")
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=partner_fail' in res.url, "Using an other user's invitation link should redirect to the course page")

        # Invited partner has been removed from channel partners. Link is expired.
        channel_partner_emp.sudo().unlink()
        self.authenticate("user_emp", "user_emp")
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('slides?invite_state=expired' in res.url, "Using an expired link should redirect to the main /slides page")

    def test_direct_invite_route_public_course(self):
        ''' Invite route redirects properly the (not) logged user in a course with public visibility'''
        self.channel.write({'visibility': 'public'})
        self.env['res.config.settings'].create({'auth_signup_uninvited': 'b2c'})

        # No such channel
        invite_url = "/slides/-1/invite"
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=no_channel' in res.url, "This channel does not exist. Redirect to the main /slides page.")

        channel_partner_portal = self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': self.user_portal.partner_id.id,
            'member_status': 'invited'
        })
        invite_url = channel_partner_portal.invitation_link_with_hash

        # TODO : tests for auth_signup / auth_login
        # TODO : discuss auth_signup / auth_login (accept that?) / redirect + ACL's (new or modify) vs simple redirect and fetch_possible on different routes (~appointment)
        # TODO : discuss publish (invite / share)

        # No logged user but possible to login -> Login page
        # TODO: write 2 tests without allow_redirect = false to check auth_login and auth_token??
        # Invited without user but can create an account, auth_signup_token in url

        channel_partner_nan = self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': self.partner_nan.id,
            'member_status': 'invited'
        })
        invite_url = channel_partner_nan.invitation_link_with_hash

        # Invited without user and cannot create an account. The invitation link generates and redirects to an account creation link.
        self.env['res.config.settings'].create({'auth_signup_uninvited': 'b2b'})
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        signup_url = self.partner_nan.signup_url
        self.assertTrue(signup_url in res.url, "Should redirect to the course page")

    def test_generic_invite_route_members_only_course(self):
        ''' Invite route redirects properly the (not) logged user when using the generic link'''
        invite_url = "/slides/%s/invite" % self.channel.id
        self.channel.write({'visibility': 'members'})

        # No user logged
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=no_rights' in res.url, "The public user has no access to members-only courses.")

        # User logged but not invited nor enrolled
        self.authenticate("portal", "portal")
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, f'{self.common_base_url}/slides?invite_state=no_rights', "An external user has no access to members-only courses.")

        # Logged user now has a pending invitation to the course
        self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': self.user_portal.partner_id.id,
            'member_status': 'invited'
        })

        # User logged and invited
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'slides/{slug(self.channel)}' in res.url, "Invited partner should be redirected to the course page")

    def test_generic_invite_route_public_course(self):
        ''' Invite route redirects properly the (not) logged user when using the generic link'''
        invite_url = "/slides/%s/invite" % self.channel.id

        # No user logged
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'slides/{slug(self.channel)}' in res.url, "Should redirect to the course page")
