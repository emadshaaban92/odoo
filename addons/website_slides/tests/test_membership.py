# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_slides.tests import common
from odoo.tests import tagged, users
from odoo.tests.common import HOST
from odoo.tools import config

from werkzeug.urls import url_decode

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
        self.partner_no_user = self.env['res.partner'].create({
            'country_id': self.env.ref('base.be').id,
            'email': 'partner_no_user@example.com',
            'name': 'Partner Without User',
        })
        self.channel_partner_emp, self.channel_partner_no_user = self.env['slide.channel.partner'].create([{
            'channel_id': self.channel.id,
            'partner_id': self.user_emp.partner_id.id
        }, {
            'channel_id': self.channel.id,
            'partner_id': self.partner_no_user.id
        }])
        self.common_base_url = "http://%s:%s" % (HOST, config['http_port'])

    def test_direct_invite_members_invitation_expiration(self):
        ''' When sharing a course with members visibility to a partner, they are 'invited'. They access a the course as if it were public,
        but only for three months. Afterwards, they will be removed by garbage collector.'''
        # Logged user has been invited more than three months ago.
        self.channel_partner_emp.write({
            'member_status': 'invited',
            'last_invitation_date': fields.Datetime.subtract(fields.Datetime.now(), months=4)
        })
        self.channel.visibility = 'members'
        self.authenticate("user_emp", "user_emp")
        res = self.url_open(self.channel_partner_emp.invitation_link_with_hash)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=expired' in res.url, "Using an expired link should redirect to the main /slides page")

        # Clean outdated records
        invited_member_id = self.channel_partner_emp.id
        self.env['slide.channel.partner']._gc_slide_channel_partner()
        self.assertFalse(self.env['slide.channel.partner'].search([('id', '=', invited_member_id)]))

    def test_direct_invite_public_or_members_visibility(self):
        ''' Invite route redirects properly the (not) logged user in a course with public visibility.
        As the direct invitation enrolls the partner in the course, we always redirect them to the login / signup,
        no matter the enroll policy.'''
        # Logged user now has a pending invitation to the course
        invite_url_emp = self.channel_partner_emp.invitation_link_with_hash
        invite_url_no_user = self.channel_partner_no_user.invitation_link_with_hash

        # No user logged. Partner has a user. Redirects to login.
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/login' in res.url, "Should redirect to login page if unlogged.")
        self.assertTrue('auth_login=user_emp' in res.url, "The login should correspond to the invited partner.")
        self.assertTrue(f'redirect=/slides/{self.channel.id}' in res.url, "Login should redirect to the course.")

        # No user logged. Partner has no user. Redirects to a prepared signup. Decode used because of signup prepare.
        res = self.url_open(invite_url_no_user)
        decoded_url = url_decode(res.url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/signup' in res.url, "Should redirect to signup page if unlogged and no user.")
        self.assertEqual(self.partner_no_user.signup_token, decoded_url['token'], "Signup should correspond to the invited partner.")
        self.assertEqual(f'/slides/{self.channel.id}', decoded_url['redirect'], "Signup should redirect to the course.")

        # Hash is wrong
        invite_url_false_hash = invite_url_emp + 'abc'
        res = self.url_open(invite_url_false_hash)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=hash_fail' in res.url, "A wrong hash should redirect to the main /slides page")

        # Logged user is a member of the course
        self.authenticate("user_emp", "user_emp")
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'slides/{slug(self.channel)}' in res.url, "Should redirect to the course page")

        # Link is for another user
        res = self.url_open(invite_url_no_user)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=partner_fail' in res.url, "Using an other user's invitation link should redirect to the course page")

        # Invited partner has been removed from channel partners. Link is expired. As it is a public course, redirects to the course.
        self.channel_partner_emp.sudo().unlink()
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'slides/{slug(self.channel)}' in res.url, "Using an expired link should still redirect to the public course page")

        # Members only course. Link is expired. Redirects to the main slides page.
        self.channel.visibility = 'members'
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=expired' in res.url, "Using an expired link should redirect to the main /slides page")

    def test_direct_share_members_visibility(self):
        ''' When sharing a course with members visibility to a partner, they are 'invited'. They access a the course as if it were public.
        However, they only access a preview of it. (But none of slides)'''
        self.channel.write({'visibility': 'members'})
        # Logged user now has a pending invitation to the course
        self.channel_partner_emp.member_status = 'invited'
        invite_url_emp = self.channel_partner_emp.invitation_link_with_hash

        # No user logged, but access via valid hash.
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'/slides/{self.channel.id}' in res.url, "Partners being shared the course can access the course page")

        # Error if course not published
        self.channel.sudo().is_published = False
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=no_rights' in res.url)

        # If removed from invited attendees, the hash is not valid.
        self.channel.sudo().is_published = True
        self.channel_partner_emp.sudo().unlink()
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=expired' in res.url, "Using an expired link should redirect to the main /slides page")

    def test_direct_share_public_visibility(self):
        ''' Shared link will redirect properly the user to the course with a public visibility'''
        self.channel_partner_emp.member_status = 'invited'
        invite_url_emp = self.channel_partner_emp.invitation_link_with_hash

        # No user logged.
        res = self.url_open(invite_url_emp)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'/slides/{self.channel.id}' in res.url, "Partners being shared the course can access the public course page")

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
        # No such channel
        invite_url = "/slides/-1/invite"
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('/slides?invite_state=no_channel' in res.url, "This channel does not exist. Redirect to the main /slides page.")

        # No user logged
        invite_url = "/slides/%s/invite" % self.channel.id
        res = self.url_open(invite_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(f'slides/{slug(self.channel)}' in res.url, "Should redirect to the course page")
