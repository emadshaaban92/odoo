# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

emails_split = re.compile(r"[;,\n\r]+")


class SlideChannelInvite(models.TransientModel):
    _name = 'slide.channel.invite'
    _inherit = 'mail.composer.mixin'
    _description = 'Channel Invitation Wizard'

    # composer content
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    # recipients
    partner_ids = fields.Many2many('res.partner', string='Recipients')
    # slide channel
    channel_id = fields.Many2one('slide.channel', string='Course', required=True)
    channel_invite_url = fields.Char('Course Invitation URL', compute='_compute_channel_invite_url')
    channel_visibility = fields.Selection(related="channel_id.visibility", string='Course Visibility')
    channel_published = fields.Boolean('Course Published', compute="_compute_channel_published", readonly=False, store=True)
    channel_can_publish = fields.Boolean(compute="_compute_channel_can_publish")
    # membership
    with_enrollment = fields.Boolean(
        'Enroll partners', readonly=True,
        help="Whether invited partners will be added as enrolled or just invited partners")
    signup_allowed = fields.Boolean('Signup Allowed', readonly=True, default=lambda self: self.env['res.users']._get_signup_invitation_scope() == 'b2c')

    @api.depends('channel_id')
    @api.depends_context('uid')
    def _compute_channel_can_publish(self):
        for invite in self:
            invite.channel_can_publish = invite.channel_id and invite.channel_id.can_publish

    @api.depends('channel_id', 'channel_id.is_published')
    def _compute_channel_published(self):
        for invite in self:
            invite.channel_published = invite.channel_id.is_published

    @api.onchange('channel_published')
    def _onchange_channel_published(self):
        for invite in self:
            channel = invite.channel_id
            if invite.channel_can_publish and channel and channel.is_published != invite.channel_published:
                channel.write({'is_published': not channel.is_published})

    @api.depends('channel_id')
    def _compute_channel_invite_url(self):
        for invite in self:
            channel = invite.channel_id
            invite.channel_invite_url = '%s/slides/%s/invite?' % (channel.get_base_url(), channel.id)

    # Overrides of mail.composer.mixin
    @api.depends('channel_id')  # fake trigger otherwise not computed in new mode
    def _compute_render_model(self):
        self.render_model = 'slide.channel.partner'

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('template_id') and not (values.get('body') or values.get('subject')):
                template = self.env['mail.template'].browse(values['template_id'])
                if not values.get('subject'):
                    values['subject'] = template.subject
                if not values.get('body'):
                    values['body'] = template.body_html
        return super(SlideChannelInvite, self).create(vals_list)

    def action_invite(self):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed.
            This method is used both to add members as 'joined' (on invitation)
            and as 'invited' (on share), depending on the value of with_enrollment.
            Invited members can be reinvited, or enrolled depending on that value. """
        self.ensure_one()

        if not self.env.user.email:
            raise UserError(_("Unable to post message, please configure the sender's email address."))
        if not self.partner_ids:
            raise UserError(_("Please select at least one recipient."))

        mail_values = []

        # Resend invitations to 'invited' members and refresh their last invitation date
        attendees_to_reinvite = self.env['slide.channel.partner']
        if not self.with_enrollment:
            attendees_to_reinvite = self.env['slide.channel.partner'].search([
                ('member_status', '=', 'invited'),
                ('channel_id', '=', self.channel_id.id),
                ('partner_id', 'in', self.partner_ids.ids)
            ])
            for attendee in attendees_to_reinvite:
                attendee.last_invitation_date = fields.Datetime.now()
                mail_values.append(self._prepare_mail_values(attendee))

        for partner_id in (self.partner_ids - attendees_to_reinvite.partner_id):
            slide_channel_partner = self.channel_id._action_add_members(partner_id, member_status='joined' if self.with_enrollment else 'invited')
            # New (invited) member or member upgraded from 'invited' to 'joined'
            if slide_channel_partner:
                mail_values.append(self._prepare_mail_values(slide_channel_partner))
                if not self.with_enrollment:
                    slide_channel_partner.last_invitation_date = fields.Datetime.now()

        self.env['mail.mail'].sudo().create(mail_values)

        return {'type': 'ir.actions.act_window_close'}

    def _prepare_mail_values(self, slide_channel_partner):
        """ Create mail specific for recipient """
        subject = self._render_field('subject', slide_channel_partner.ids)[slide_channel_partner.id]
        body = self._render_field('body', slide_channel_partner.ids)[slide_channel_partner.id]
        # post the message
        mail_values = {
            'email_from': self.env.user.email_formatted,
            'author_id': self.env.user.partner_id.id,
            'model': None,
            'res_id': None,
            'subject': subject,
            'body_html': body,
            'attachment_ids': [(4, att.id) for att in self.attachment_ids],
            'auto_delete': True,
            'recipient_ids': [(4, slide_channel_partner.partner_id.id)]
        }

        # optional support of default_email_layout_xmlid in context
        email_layout_xmlid = self.env.context.get('default_email_layout_xmlid', self.env.context.get('notif_layout'))
        if email_layout_xmlid:
            # could be great to use ``_notify_by_email_prepare_rendering_context`` someday
            template_ctx = {
                'message': self.env['mail.message'].sudo().new({'body': mail_values['body_html'], 'record_name': self.channel_id.name}),
                'model_description': self.env['ir.model']._get('slide.channel').display_name,
                'record': slide_channel_partner,
                'company': self.env.company,
                'signature': self.channel_id.user_id.signature,
            }
            body = self.env['ir.qweb']._render(email_layout_xmlid, template_ctx, engine='ir.qweb', minimal_qcontext=True, raise_if_not_found=False)
            if body:
                mail_values['body_html'] = self.env['mail.render.mixin']._replace_local_links(body)
            else:
                _logger.warning('QWeb template %s not found when sending slide channel mails. Sending without layout.', email_layout_xmlid)

        return mail_values
