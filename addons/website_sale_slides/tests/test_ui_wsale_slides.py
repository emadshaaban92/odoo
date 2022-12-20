# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tests
from odoo.addons.website_slides.tests import test_ui_wslides


@tests.common.tagged('post_install', '-at_install')
class TestSaleSlidesUiMemberInvited(test_ui_wslides.TestUICommon):

    def setUp(self):
        super(TestSaleSlidesUiMemberInvited, self).setUp()
        self.course_product = self.env['product.product'].create({
            'name': "Course Product",
            'standard_price': 100,
            'list_price': 150,
            'type': 'service',
            'invoice_policy': 'order',
            'is_published': True,
        })

        self.channel.write({
            'enroll': 'payment',
            'product_id': self.course_product.id,
            'visibility': 'members'
        })

        self.channel_partner_portal = self.env['slide.channel.partner'].create({
            'channel_id': self.channel.id,
            'partner_id': self.user_portal.partner_id.id,
            'member_status': 'invited',
        })
        self.portal_invite_url = self.channel_partner_portal.invitation_link_with_hash

    def test_course_payment_members_only_invited_logged(self):
        self.start_tour(self.portal_invite_url, 'course_payment_members_only_invited_logged', login='portal')

    def test_course_payment_members_only_invited_public(self):
        self.start_tour(self.portal_invite_url, 'course_payment_members_only_invited_public', login=None)
