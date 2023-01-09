# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import uuid

from collections import defaultdict
from dateutil.relativedelta import relativedelta
import ast

from odoo import api, fields, models, tools, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.exceptions import AccessError
from odoo.osv import expression
from odoo.tools import is_html_empty

_logger = logging.getLogger(__name__)


class ChannelUsersRelation(models.Model):
    _name = 'slide.channel.partner'
    _description = 'Channel / Partners (Members)'
    _table = 'slide_channel_partner'

    channel_id = fields.Many2one('slide.channel', string='Course', index=True, required=True, ondelete='cascade')
    completion = fields.Integer('% Completed Contents', default=0, group_operator="avg")
    completed_slides_count = fields.Integer('# Completed Contents')
    partner_id = fields.Many2one('res.partner', index=True, required=True, ondelete='cascade')
    partner_email = fields.Char(related='partner_id.email', readonly=True)
    # channel-related information (for UX purpose)
    channel_user_id = fields.Many2one('res.users', string='Responsible', related='channel_id.user_id')
    channel_type = fields.Selection(related='channel_id.channel_type')
    channel_visibility = fields.Selection(related='channel_id.visibility')
    channel_enroll = fields.Selection(related='channel_id.enroll')
    channel_website_id = fields.Many2one('website', string='Website', related='channel_id.website_id')
    # Member and enrollment status
    member_status = fields.Selection([
        ('invited', 'Invite Sent'),
        ('joined', 'Joined'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Finished')],
        string='Member Status', readonly=True, store=True, default='joined')
    # Invitation
    invitation_link_with_hash = fields.Char('Invitation Link', compute="_compute_invitation_link_with_hash")
    last_invitation_date = fields.Datetime('Last Invitation')

    _sql_constraints = [
        ('channel_partner_uniq',
         'unique(channel_id, partner_id)',
         'A partner membership to a channel must be unique!'
        ),
        ('check_completion',
         'check(completion >= 0 and completion <= 100)',
         'The completion of a channel is a percentage and should be between 0% and 100.'
        )
    ]

    def _recompute_completion(self):
        read_group_res = self.env['slide.slide.partner'].sudo()._read_group(
            ['&', '&', ('channel_id', 'in', self.mapped('channel_id').ids),
             ('partner_id', 'in', self.mapped('partner_id').ids),
             ('completed', '=', True),
             ('slide_id.is_published', '=', True),
             ('slide_id.active', '=', True)],
            ['channel_id', 'partner_id'],
            groupby=['channel_id', 'partner_id'], lazy=False)
        mapped_data = dict()
        for item in read_group_res:
            mapped_data.setdefault(item['channel_id'][0], dict())
            mapped_data[item['channel_id'][0]][item['partner_id'][0]] = item['__count']

        completed_records = self.env['slide.channel.partner']
        uncompleted_records = self.env['slide.channel.partner']
        for record in self:
            if record.member_status == 'invited':
                record.completed_slides_count = 0
                record.completion = 0.0
                continue
            record.completed_slides_count = mapped_data.get(record.channel_id.id, dict()).get(record.partner_id.id, 0)
            record.completion = 100.0 if record.member_status == 'completed' else round(100.0 * record.completed_slides_count / (record.channel_id.total_slides or 1))

            if not record.channel_id.active:
                continue
            elif not record.member_status == 'completed' and record.completed_slides_count >= record.channel_id.total_slides:
                completed_records += record
            elif record.member_status == 'completed' and record.completed_slides_count < record.channel_id.total_slides:
                uncompleted_records += record

            if record.completion == 100.0:
                record.member_status = 'completed'
            elif record.completion == 0.0:
                record.member_status = 'joined'
            else:
                record.member_status = 'ongoing'

        if completed_records:
            completed_records._set_as_completed(completed=True)
            completed_records._send_completed_mail()

        if uncompleted_records:
            uncompleted_records._set_as_completed(completed=False)

    @api.model_create_multi
    def create(self, vals_list):
        """ If an attendee is created as enrolled, subscribe its partner to the channel. """
        channel_partners = super(ChannelUsersRelation, self).create(vals_list)
        subtype = self.env.ref('website_slides.mt_channel_slide_published', raise_if_not_found=False)

        for channel_partner in channel_partners.filtered(
                lambda channel_partner: channel_partner.member_status in ['joined', 'ongoing', 'completed']):
            channel_partner.channel_id.message_subscribe(
                partner_ids=channel_partner.partner_id.ids,
                subtype_ids=[subtype.id] if subtype else []
            )

        return channel_partners

    def unlink(self):
        """
        Override unlink method :
        Remove attendee from a channel, then also remove slide.slide.partner related to.
        """
        removed_slide_partner_domain = []
        for channel_partner in self:
            # find all slide link to the channel and the partner
            removed_slide_partner_domain = expression.OR([
                removed_slide_partner_domain,
                [('partner_id', '=', channel_partner.partner_id.id),
                 ('slide_id', 'in', channel_partner.channel_id.slide_ids.ids)]
            ])
        if removed_slide_partner_domain:
            self.env['slide.slide.partner'].search(removed_slide_partner_domain).unlink()
        return super(ChannelUsersRelation, self).unlink()

    @api.depends('channel_id', 'partner_id')
    def _compute_invitation_link_with_hash(self):
        ''' This will return the url used as hyperlink in the channel invitation email in template mail_notification_channel_invite.
        The partner_id is given in the url, as well as a hash based on the partner and channel ids.

        :return: channel invitation url with hash.
        '''
        for record in self:
            partner_sudo = record.partner_id.sudo()
            channel = record.channel_id
            token = (partner_sudo.id, channel.id)
            partner_hash = tools.hmac(record.env(su=True), 'website_slides-channel-invite', token)
            record.invitation_link_with_hash = '%s/slides/%s/invite?partner_id=%s&invite_hash=%s' % (channel.get_base_url(), channel.id, partner_sudo.id, partner_hash)

    def _set_as_completed(self, completed=True):
        """ Set record as completed and compute karma gains

        :param completed:
            True if we make the slide as completed
            False if we remove user completion
        """
        partner_karma = dict.fromkeys(self.mapped('partner_id').ids, 0)
        for record in self:
            record.member_status = 'completed' if completed else 'ongoing' if record.completion > 0 else 'joined'
            partner_karma[record.partner_id.id] += record.channel_id.karma_gen_channel_finish

        partner_karma = {
            partner_id: karma_to_add
            for partner_id, karma_to_add in partner_karma.items() if karma_to_add > 0
        }

        if partner_karma:
            users = self.env['res.users'].sudo().search([('partner_id', 'in', list(partner_karma.keys()))])
            for user in users:
                karma = partner_karma[user.partner_id.id]
                if not completed:
                    # Mark the channel as not-completed, we remove the gained karma
                    karma *= -1
                users.add_karma(karma)

    def _send_completed_mail(self):
        """ Send an email to the attendee when they have successfully completed a course. """
        template_to_records = dict()
        for record in self:
            template = record.channel_id.completed_template_id
            if template:
                template_to_records.setdefault(template, self.env['slide.channel.partner'])
                template_to_records[template] += record

        record_email_values = dict()
        for template, records in template_to_records.items():
            record_email_values.update(
                template.generate_email(
                    records.ids,
                    ['body_html',
                     'email_from',
                     'partner_to',
                     'subject',
                    ]
                )
            )

        mail_mail_values = []
        for record in self:
            email_values = record_email_values.get(record.id)
            if not email_values or not email_values.get('partner_ids'):
                continue

            email_values.update(
                author_id=record.channel_id.user_id.partner_id.id or self.env.company.partner_id.id,
                auto_delete=True,
                recipient_ids=[(4, pid) for pid in email_values['partner_ids']],
            )
            email_values['body_html'] = template._render_encapsulate(
                'mail.mail_notification_light', email_values['body_html'],
                add_context={
                    'message': self.env['mail.message'].sudo().new(dict(body=email_values['body_html'], record_name=record.channel_id.name)),
                    'model_description': _('Completed Course')  # tde fixme: translate into partner lang
                }
            )
            mail_mail_values.append(email_values)

        if mail_mail_values:
            self.env['mail.mail'].sudo().create(mail_mail_values)

    @api.autovacuum
    def _gc_slide_channel_partner(self):
        # The invitation of members is only valid 3 months after their invitation
        limit_dt = fields.Datetime.subtract(fields.Datetime.now(), months=3)
        invited_members = self.env['slide.channel.partner'].search([('last_invitation_date', '<', limit_dt), ('member_status', '=', 'invited')])
        invited_members.unlink()


class Channel(models.Model):
    """ A channel is a container of slides. """
    _name = 'slide.channel'
    _description = 'Course'
    _inherit = [
        'mail.thread', 'rating.mixin',
        'mail.activity.mixin',
        'image.mixin',
        'website.cover_properties.mixin',
        'website.seo.metadata',
        'website.published.multi.mixin',
        'website.searchable.mixin',
    ]
    _order = 'sequence, id'

    def _default_cover_properties(self):
        """ Cover properties defaults are overridden to keep a consistent look for the slides
        channels headers across Odoo versions (pre-customization, with purple gradient fitting the
        homepage images, etc). Furthermore, as adding padding to the cover would not look great,
        its height is set to fit to content (snippet option to change this also disabled on the view)."""
        res = super()._default_cover_properties()
        res.update({
            "background_color_class": "o_cc3",
            'background_color_style': (
                'background-color: rgba(0, 0, 0, 0); '
                'background-image: linear-gradient(120deg, #875A7B, #78516F);'
            ),
            'opacity': '0',
            'resize_class': 'cover_auto'
        })
        return res

    def _default_access_token(self):
        return str(uuid.uuid4())

    def _get_default_enroll_msg(self):
        return _('Contact Responsible')

    # description
    name = fields.Char('Name', translate=True, required=True)
    active = fields.Boolean(default=True, tracking=100)
    description = fields.Html('Description', translate=True, sanitize_attributes=False, sanitize_form=False, help="The description that is displayed on top of the course page, just below the title")
    description_short = fields.Html('Short Description', translate=True, sanitize_attributes=False, sanitize_form=False, help="The description that is displayed on the course card")
    description_html = fields.Html('Detailed Description', translate=tools.html_translate, sanitize_attributes=False, sanitize_form=False)
    channel_type = fields.Selection([
        ('training', 'Training'), ('documentation', 'Documentation')],
        string="Course type", default="training", required=True)
    sequence = fields.Integer(default=10)
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.uid)
    color = fields.Integer('Color Index', default=0, help='Used to decorate kanban view')
    tag_ids = fields.Many2many(
        'slide.channel.tag', 'slide_channel_tag_rel', 'channel_id', 'tag_id',
        string='Tags', help='Used to categorize and filter displayed channels/courses')
    # slides: promote, statistics
    slide_ids = fields.One2many('slide.slide', 'channel_id', string="Slides and categories", copy=True)
    slide_content_ids = fields.One2many('slide.slide', string='Content', compute="_compute_category_and_slide_ids")
    slide_category_ids = fields.One2many('slide.slide', string='Categories', compute="_compute_category_and_slide_ids")
    slide_last_update = fields.Date('Last Update', compute='_compute_slide_last_update', store=True)
    slide_partner_ids = fields.One2many(
        'slide.slide.partner', 'channel_id', string="Slide User Data",
        copy=False, groups='website_slides.group_website_slides_officer')
    promote_strategy = fields.Selection([
        ('latest', 'Latest Created'),
        ('most_voted', 'Most Voted'),
        ('most_viewed', 'Most Viewed'),
        ('specific', 'Select Manually'),
        ('none', 'None')],
        string="Featured Content", default='latest', required=False,
        help='Defines the content that will be promoted on the course home page',
        copy=False,
    )
    promoted_slide_id = fields.Many2one('slide.slide', string='Promoted Slide', copy=False)
    access_token = fields.Char("Security Token", copy=False, default=_default_access_token)
    nbr_document = fields.Integer('Documents', compute='_compute_slides_statistics', store=True)
    nbr_video = fields.Integer('Videos', compute='_compute_slides_statistics', store=True)
    nbr_infographic = fields.Integer('Infographics', compute='_compute_slides_statistics', store=True)
    nbr_article = fields.Integer("Articles", compute='_compute_slides_statistics', store=True)
    nbr_quiz = fields.Integer("Number of Quizs", compute='_compute_slides_statistics', store=True)
    total_slides = fields.Integer('Number of Contents', compute='_compute_slides_statistics', store=True)
    total_views = fields.Integer('Visits', compute='_compute_slides_statistics', store=True)
    total_votes = fields.Integer('Votes', compute='_compute_slides_statistics', store=True)
    total_time = fields.Float('Duration', compute='_compute_slides_statistics', digits=(10, 2), store=True)
    rating_avg_stars = fields.Float("Rating Average (Stars)", compute='_compute_rating_stats', digits=(16, 1), compute_sudo=True)
    # configuration
    allow_comment = fields.Boolean(
        "Allow rating on Course", default=True,
        help="Allow Attendees to like and comment your content and to submit reviews on your course.")
    publish_template_id = fields.Many2one(
        'mail.template', string='New Content Notification',
        help="Defines the email your Attendees will receive each time you upload new content.",
        default=lambda self: self.env['ir.model.data']._xmlid_to_res_id('website_slides.slide_template_published'),
        domain=[('model', '=', 'slide.slide')])
    share_channel_template_id = fields.Many2one(
        'mail.template', string='Channel Share Template',
        help='Email template used when sharing a channel',
        default=lambda self: self.env['ir.model.data']._xmlid_to_res_id('website_slides.mail_template_channel_shared'))
    share_slide_template_id = fields.Many2one(
        'mail.template', string='Share Template',
        help="Email template used when sharing a slide",
        default=lambda self: self.env['ir.model.data']._xmlid_to_res_id('website_slides.slide_template_shared'))
    completed_template_id = fields.Many2one(
        'mail.template', string='Completion Notification', help="Defines the email your Attendees will receive once they reach the end of your course.",
        default=lambda self: self.env['ir.model.data']._xmlid_to_res_id('website_slides.mail_template_channel_completed'),
        domain=[('model', '=', 'slide.channel.partner')])
    enroll = fields.Selection([
        ('public', 'Public'), ('invite', 'On Invitation')],
        default='public', string='Enroll Policy', required=True,
        help='Defines how people can enroll to your Course.', copy=False)
    enroll_msg = fields.Html(
        'Enroll Message', help="Message explaining the enroll process",
        default=_get_default_enroll_msg, translate=tools.html_translate, sanitize_attributes=False)
    enroll_group_ids = fields.Many2many('res.groups', string='Auto Enroll Groups', help="Members of those groups are automatically added as members of the channel.")
    visibility = fields.Selection([
        ('public', 'Open To All'), ('members', 'Members Only')],
        default='public', string='Visibility', required=True,
        help='Defines who can access your courses and their content.')
    partner_ids = fields.Many2many(
        'res.partner', string='Attendees', help="All enrolled partners in channel",
        compute="_compute_partner_ids", search="_search_partner_ids")
    partner_all_ids = fields.Many2many(
        'res.partner', 'slide_channel_partner', 'channel_id', 'partner_id',
        string='All Attendees', help="All partners in the channel (both enrolled and invited)",
        context={'active_test': False}, copy=False, depends=['channel_partner_all_ids'])
    members_count = fields.Integer('Members Count', compute='_compute_members_counts')
    members_active_count = fields.Integer(
        '# Attendees Active', help="Active members include both 'joined' and 'ongoing' members.",
        compute='_compute_members_counts')
    members_done_count = fields.Integer('# Attendees Done', compute='_compute_members_counts')
    members_invited_count = fields.Integer('# Attendees Invited', compute='_compute_members_counts')
    members_all_count = fields.Integer('All Attendees count', compute='_compute_members_counts')
    has_requested_access = fields.Boolean(string='Access Requested', compute='_compute_has_requested_access', compute_sudo=False)
    is_member = fields.Boolean(
        string='Is Member', help='Has the member accepted the invitation / is actively enrolled.',
        compute='_compute_membership_values', compute_sudo=False)
    is_member_invited = fields.Boolean(
        string='Is Invitation Pending', help='Is the invitation for this member pending.',
        compute='_compute_membership_values', compute_sudo=False)
    channel_partner_ids = fields.One2many('slide.channel.partner', 'channel_id', string='Enrolled Members Information', groups='website_slides.group_website_slides_officer', domain=[('member_status', '!=', 'invited')])
    channel_partner_all_ids = fields.One2many('slide.channel.partner', 'channel_id', string='All Members Information', groups='website_slides.group_website_slides_officer')
    upload_group_ids = fields.Many2many(
        'res.groups', 'rel_upload_groups', 'channel_id', 'group_id', string='Upload Groups',
        help="Group of users allowed to publish contents on a documentation course.")
    website_background_image_url = fields.Char('Background image URL', compute='_compute_website_background_image_url')
    # not stored access fields, depending on each user
    completed = fields.Boolean('Done', compute='_compute_user_statistics', compute_sudo=False)
    completion = fields.Integer('Completion', compute='_compute_user_statistics', compute_sudo=False)
    can_upload = fields.Boolean('Can Upload', compute='_compute_can_upload', compute_sudo=False)
    partner_has_new_content = fields.Boolean(compute='_compute_partner_has_new_content', compute_sudo=False)
    # karma generation
    karma_gen_slide_vote = fields.Integer(string='Lesson voted', default=1)
    karma_gen_channel_rank = fields.Integer(string='Course ranked', default=5)
    karma_gen_channel_finish = fields.Integer(string='Course finished', default=10)
    # Karma based actions
    karma_review = fields.Integer('Add Review', default=10, help="Karma needed to add a review on the course")
    karma_slide_comment = fields.Integer('Add Comment', default=3, help="Karma needed to add a comment on a slide of this course")
    karma_slide_vote = fields.Integer('Vote', default=3, help="Karma needed to like/dislike a slide of this course.")
    can_review = fields.Boolean('Can Review', compute='_compute_action_rights', compute_sudo=False)
    can_comment = fields.Boolean('Can Comment', compute='_compute_action_rights', compute_sudo=False)
    can_vote = fields.Boolean('Can Vote', compute='_compute_action_rights', compute_sudo=False)

    @api.depends('channel_partner_all_ids', 'channel_partner_all_ids.member_status')
    def _compute_partner_ids(self):
        for record in self:
            enrolled_partner_ids = record.channel_partner_ids.partner_id.ids or []
            record.partner_ids = record.partner_all_ids.filtered(lambda partner: partner.id in enrolled_partner_ids)

    def _search_partner_ids(self, operator, value):
        if isinstance(value, int) and operator == 'in':
            value = [value]
        enrolled_channel_partner_ids = self.env['slide.channel.partner'].sudo().search([
            ('member_status', '!=', 'invited'),
            ('partner_id', operator, value),
        ])
        return [('id', 'in', enrolled_channel_partner_ids.channel_id.ids)]

    @api.depends('slide_ids.is_published')
    def _compute_slide_last_update(self):
        for record in self:
            record.slide_last_update = fields.Date.today()

    @api.depends('channel_partner_all_ids.channel_id', 'channel_partner_all_ids.member_status')
    def _compute_members_counts(self):
        read_group_res = self.env['slide.channel.partner'].sudo()._read_group(
            [('channel_id', 'in', self.ids)],
            ['channel_id'],
            ['channel_id', 'member_status'],
            lazy=False)
        data_invited = {res['channel_id'][0]: res['__count'] for res in read_group_res if res.get('member_status') == 'invited'}
        data_joined = {res['channel_id'][0]: res['__count'] for res in read_group_res if res.get('member_status') == 'joined'}
        data_ongoing = {res['channel_id'][0]: res['__count'] for res in read_group_res if res.get('member_status') == 'ongoing'}
        data_completed = {res['channel_id'][0]: res['__count'] for res in read_group_res if res.get('member_status') == 'completed'}
        for channel in self:
            channel.members_invited_count = data_invited.get(channel.id, 0)
            channel.members_active_count = data_joined.get(channel.id, 0) + data_ongoing.get(channel.id, 0)
            channel.members_done_count = data_completed.get(channel.id, 0)
            channel.members_all_count = channel.members_invited_count + channel.members_active_count + channel.members_done_count
            channel.members_count = channel.members_active_count + channel.members_done_count

    @api.depends('activity_ids.request_partner_id')
    @api.depends_context('uid')
    @api.model
    def _compute_has_requested_access(self):
        requested_cids = self.sudo().activity_search(
            ['website_slides.mail_activity_data_access_request'],
            additional_domain=[('request_partner_id', '=', self.env.user.partner_id.id)]
        ).mapped('res_id')
        for channel in self:
            channel.has_requested_access = channel.id in requested_cids

    @api.depends('channel_partner_all_ids.partner_id', 'channel_partner_all_ids.member_status')
    @api.depends_context('uid')
    @api.model
    def _compute_membership_values(self):
        channel_partners = self.env['slide.channel.partner'].sudo().search([
            ('channel_id', 'in', self.ids),
            ('partner_id', '=', self.env.user.partner_id.id),
        ])
        result = defaultdict(set)
        for cp in channel_partners:
            result[cp.channel_id.id].add(cp.partner_id.id)
        active_channel_partners = channel_partners.filtered(
            lambda channel_partner: channel_partner.member_status != 'invited')
        invitation_pending_channels = (channel_partners - active_channel_partners).channel_id
        active_channels = active_channel_partners.channel_id
        for channel in self:
            channel.is_member = channel in active_channels
            channel.is_member_invited = channel in invitation_pending_channels

    @api.depends('slide_ids.is_category')
    def _compute_category_and_slide_ids(self):
        for channel in self:
            channel.slide_category_ids = channel.slide_ids.filtered(lambda slide: slide.is_category)
            channel.slide_content_ids = channel.slide_ids - channel.slide_category_ids

    @api.depends('slide_ids.slide_category', 'slide_ids.is_published', 'slide_ids.completion_time',
                 'slide_ids.likes', 'slide_ids.dislikes', 'slide_ids.total_views', 'slide_ids.is_category', 'slide_ids.active')
    def _compute_slides_statistics(self):
        default_vals = dict(total_views=0, total_votes=0, total_time=0, total_slides=0)
        keys = ['nbr_%s' % slide_category for slide_category in self.env['slide.slide']._fields['slide_category'].get_values(self.env)]
        default_vals.update(dict((key, 0) for key in keys))

        result = dict((cid, dict(default_vals)) for cid in self.ids)
        read_group_res = self.env['slide.slide']._read_group(
            [('active', '=', True), ('is_published', '=', True), ('channel_id', 'in', self.ids), ('is_category', '=', False)],
            ['channel_id', 'slide_category', 'likes', 'dislikes', 'total_views', 'completion_time'],
            groupby=['channel_id', 'slide_category'],
            lazy=False)
        for res_group in read_group_res:
            cid = res_group['channel_id'][0]
            result[cid]['total_views'] += res_group.get('total_views', 0)
            result[cid]['total_votes'] += res_group.get('likes', 0)
            result[cid]['total_votes'] -= res_group.get('dislikes', 0)
            result[cid]['total_time'] += res_group.get('completion_time', 0)

        category_stats = self._compute_slides_statistics_category(read_group_res)
        for cid, cdata in category_stats.items():
            result[cid].update(cdata)

        for record in self:
            record.update(result.get(record.id, default_vals))

    def _compute_slides_statistics_category(self, read_group_res):
        """ Compute statistics based on all existing slide categories """
        slide_categories = self.env['slide.slide']._fields['slide_category'].get_values(self.env)
        keys = ['nbr_%s' % slide_category for slide_category in slide_categories]
        result = dict((cid, dict((key, 0) for key in keys + ['total_slides'])) for cid in self.ids)
        for res_group in read_group_res:
            cid = res_group['channel_id'][0]
            slide_category = res_group.get('slide_category')
            if slide_category:
                slide_category_count = res_group.get('__count', 0)
                result[cid]['nbr_%s' % slide_category] = slide_category_count
                result[cid]['total_slides'] += slide_category_count
        return result

    def _compute_rating_stats(self):
        super(Channel, self)._compute_rating_stats()
        for record in self:
            record.rating_avg_stars = record.rating_avg

    @api.depends('slide_partner_ids', 'slide_partner_ids.completed', 'total_slides')
    @api.depends_context('uid')
    def _compute_user_statistics(self):
        current_user_info = self.env['slide.channel.partner'].sudo().search(
            [('channel_id', 'in', self.ids), ('partner_id', '=', self.env.user.partner_id.id)]
        )
        mapped_data = dict((info.channel_id.id, (info.member_status == 'completed', info.completed_slides_count)) for info in current_user_info)
        for record in self:
            completed, completed_slides_count = mapped_data.get(record.id, (False, 0))
            record.completed = completed
            record.completion = 100.0 if completed else round(100.0 * completed_slides_count / (record.total_slides or 1))

    @api.depends('upload_group_ids', 'user_id')
    @api.depends_context('uid')
    def _compute_can_upload(self):
        for record in self:
            if record.user_id == self.env.user or self.env.user._is_admin():
                record.can_upload = True
            elif record.upload_group_ids:
                record.can_upload = bool(record.upload_group_ids & self.env.user.groups_id)
            else:
                record.can_upload = self.env.user.has_group('website_slides.group_website_slides_manager')

    @api.depends('channel_type', 'user_id', 'can_upload')
    @api.depends_context('uid')
    def _compute_can_publish(self):
        """ For channels of type 'training', only the responsible (see user_id field) can publish slides.
        The 'sudo' user needs to be handled because they are the one used for uploads done on the front-end when the
        logged in user is not publisher but fulfills the upload_group_ids condition. """
        for record in self:
            if not record.can_upload:
                record.can_publish = False
            elif record.user_id == self.env.user or self.env.user._is_admin():
                record.can_publish = True
            else:
                record.can_publish = self.env.user.has_group('website_slides.group_website_slides_manager')

    def _get_placeholder_filename(self, field):
        image_fields = ['image_%s' % size for size in [1920, 1024, 512, 256, 128]]
        if field in image_fields:
            return 'website_slides/static/src/img/channel-%s-default.jpg' % ('training' if self.channel_type == 'training' else 'documentation')
        return super()._get_placeholder_filename(field)

    @api.model
    def _get_can_publish_error_message(self):
        return _("Publishing is restricted to the responsible of training courses or members of the publisher group for documentation courses")

    @api.depends('slide_partner_ids')
    @api.depends_context('uid')
    def _compute_partner_has_new_content(self):
        new_published_slides = self.env['slide.slide'].sudo().search([
            ('is_published', '=', True),
            ('date_published', '>', fields.Datetime.now() - relativedelta(days=7)),
            ('channel_id', 'in', self.ids),
            ('is_category', '=', False)
        ])
        slide_partner_completed = self.env['slide.slide.partner'].sudo().search([
            ('channel_id', 'in', self.ids),
            ('partner_id', '=', self.env.user.partner_id.id),
            ('slide_id', 'in', new_published_slides.ids),
            ('completed', '=', True)
        ]).mapped('slide_id')
        for channel in self:
            new_slides = new_published_slides.filtered(lambda slide: slide.channel_id == channel)
            channel.partner_has_new_content = any(slide not in slide_partner_completed for slide in new_slides)

    @api.depends('image_1920', 'channel_type')
    def _compute_website_background_image_url(self):
        for channel in self:
            channel.website_background_image_url = (
                channel.website_id.image_url(channel, 'image_256') if channel.image_1920
                else '/website_slides/static/src/img/channel-%s-default.jpg'
                     % ('training' if channel.channel_type == 'training' else 'documentation')
            )

    @api.depends('name', 'website_id.domain')
    def _compute_website_url(self):
        super(Channel, self)._compute_website_url()
        for channel in self:
            if channel.id:  # avoid to perform a slug on a not yet saved record in case of an onchange.
                base_url = channel.get_base_url()
                channel.website_url = '%s/slides/%s' % (base_url, slug(channel))

    @api.depends('can_publish', 'is_member', 'karma_review', 'karma_slide_comment', 'karma_slide_vote')
    @api.depends_context('uid')
    def _compute_action_rights(self):
        user_karma = self.env.user.karma
        for channel in self:
            if channel.can_publish:
                channel.can_vote = channel.can_comment = channel.can_review = True
            elif not channel.is_member:
                channel.can_vote = channel.can_comment = channel.can_review = False
            else:
                channel.can_review = user_karma >= channel.karma_review
                channel.can_comment = user_karma >= channel.karma_slide_comment
                channel.can_vote = user_karma >= channel.karma_slide_vote

    # ---------------------------------------------------------
    # ORM Overrides
    # ---------------------------------------------------------

    def _init_column(self, column_name):
        """ Initialize the value of the given column for existing rows.
            Overridden here because we need to generate different access tokens
            and by default _init_column calls the default method once and applies
            it for every record.
        """
        if column_name != 'access_token':
            super(Channel, self)._init_column(column_name)
        else:
            query = """
                UPDATE %(table_name)s
                SET access_token = md5(md5(random()::varchar || id::varchar) || clock_timestamp()::varchar)::uuid::varchar
                WHERE access_token IS NULL
            """ % {'table_name': self._table}
            self.env.cr.execute(query)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Ensure creator is member of its channel it is easier for them to manage it (unless it is odoobot)
            if not vals.get('channel_partner_ids') and not self.env.is_superuser():
                vals['channel_partner_ids'] = [(0, 0, {
                    'partner_id': self.env.user.partner_id.id
                })]
            if not is_html_empty(vals.get('description')) and is_html_empty(vals.get('description_short')):
                vals['description_short'] = vals['description']

        channels = super(Channel, self.with_context(mail_create_nosubscribe=True)).create(vals_list)

        for channel in channels:
            if channel.user_id:
                channel._action_add_members(channel.user_id.partner_id)
            if channel.enroll_group_ids:
                channel._add_groups_members()

        return channels

    def copy_data(self, default=None):
        self.ensure_one()
        default = default or {}
        if 'name' not in default:
            default['name'] = f"{self.name} ({_('copy')})"

        return super().copy_data(default)

    def write(self, vals):
        # If description_short wasn't manually modified, there is an implicit link between this field and description.
        if not is_html_empty(vals.get('description')) and is_html_empty(vals.get('description_short')) and self.description == self.description_short:
            vals['description_short'] = vals.get('description')

        res = super(Channel, self).write(vals)

        if vals.get('user_id'):
            self._action_add_members(self.env['res.users'].sudo().browse(vals['user_id']).partner_id)
            self.activity_reschedule(['website_slides.mail_activity_data_access_request'], new_user_id=vals.get('user_id'))
        if 'enroll_group_ids' in vals:
            self._add_groups_members()

        return res

    def toggle_active(self):
        """ Archiving/unarchiving a channel does it on its slides, too.
        1. When archiving
        We want to be archiving the channel FIRST.
        So that when slides are archived and the recompute is triggered,
        it does not try to mark the channel as "completed".
        That happens because it counts slide_done / slide_total, but slide_total
        will be 0 since all the slides for the course have been archived as well.

        2. When un-archiving
        We want to archive the channel LAST.
        So that when it recomputes stats for the channel and completion, it correctly
        counts the slides_total by counting slides that are already un-archived. """

        to_archive = self.filtered(lambda channel: channel.active)
        to_activate = self.filtered(lambda channel: not channel.active)
        if to_archive:
            super(Channel, to_archive).toggle_active()
            to_archive.is_published = False
            to_archive.mapped('slide_ids').action_archive()
        if to_activate:
            to_activate.with_context(active_test=False).mapped('slide_ids').action_unarchive()
            super(Channel, to_activate).toggle_active()

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *, parent_id=False, subtype_id=False, **kwargs):
        """ Temporary workaround to avoid spam. If someone replies on a channel
        through the 'Presentation Published' email, it should be considered as a
        note as we don't want all channel followers to be notified of this answer. """
        self.ensure_one()
        if kwargs.get('message_type') == 'comment' and not self.can_review:
            raise AccessError(_('Not enough karma to review'))
        if parent_id:
            parent_message = self.env['mail.message'].sudo().browse(parent_id)
            if parent_message.subtype_id and parent_message.subtype_id == self.env.ref('website_slides.mt_channel_slide_published'):
                subtype_id = self.env.ref('mail.mt_note').id
        return super(Channel, self).message_post(parent_id=parent_id, subtype_id=subtype_id, **kwargs)

    # ---------------------------------------------------------
    # Business / Actions
    # ---------------------------------------------------------

    def action_redirect_to_members(self, member_status=''):
        """ Redirects to attendees of the course. If member_status is set to 'invited' /
        'active' ('joined' + 'ongoing') / 'completed', attendees being filtered accordingly."""
        action_ctx = {'active_test': False}
        action = self.env["ir.actions.actions"]._for_xml_id("website_slides.slide_channel_partner_action")
        if member_status:
            if member_status == 'active':
                action_ctx['search_default_filter_joined'] = 1
                action_ctx['search_default_filter_ongoing'] = 1
            else:
                action_ctx['search_default_filter_%s' % member_status] = 1
        action['domain'] = [('channel_id', 'in', self.ids)]
        action['sample'] = 1
        if member_status == 'completed':
            help_message = {'header_message': _("No Attendee has completed this course yet!"), 'body_message': ""}
        else:
            help_message = {
                'header_message': _("No Attendees Yet!"),
                'body_message': _("From here you'll be able to monitor attendees and to track their progress.")
            }
        action['help'] = """<p class="o_view_nocontent_smiling_face">%(header_message)s</p><p>%(body_message)s</p>""" % help_message
        if len(self) == 1:
            action['display_name'] = _('Attendees of %s', self.name)
            action_ctx['search_default_channel_id'] = self.id
        action['context'] = action_ctx
        return action

    def action_redirect_to_completed_members(self):
        return self.action_redirect_to_members('completed')

    def action_redirect_to_active_members(self):
        return self.action_redirect_to_members('active')

    def action_redirect_to_invited_members(self):
        return self.action_redirect_to_members('invited')

    def action_channel_enroll_invite(self):
        return self.action_channel_invite(with_enrollment=True)

    def action_channel_invite(self, channel_id=False, with_enrollment=False):
        template = self.env.ref('website_slides.mail_template_slide_channel_invite', raise_if_not_found=False) if with_enrollment else \
            self.env.ref('website_slides.mail_template_slide_channel_share', raise_if_not_found=False)
        course_name = self.env['slide.channel'].sudo().browse(channel_id).name if channel_id else self.name if len(self) == 1 else ''

        local_context = dict(
            self.env.context,
            default_channel_id=channel_id or (self.id if len(self) == 1 else False),
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_email_layout_xmlid='website_slides.mail_notification_channel_invite',
            default_with_enrollment=with_enrollment,
        )
        title_text = _('Invite Members to ') if with_enrollment and course_name else _('Invite Members to a course') if with_enrollment else _('Share ') if course_name else _('Share a Course')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'res_model': 'slide.channel.invite',
            'target': 'new',
            'context': local_context,
            'name': f'{title_text}{course_name}' if course_name else title_text,
        }

    def action_add_member(self, **member_values):
        """ Enroll the logged in user in the course. (see '_action_add_members' for more info)
        This method is called when a user press the 'Join the course' button in front-end,
        through '/enroll' route.

        If the logged in user has been invited, then we sudo the add_members method
        since we consider he has been granted access to the course.

        Returns True if added and enrolled successfully, False otherwise."""
        invited_res = False
        courses_invited = self.filtered(lambda course: course.is_member_invited)
        if courses_invited:
            invited_res = bool(courses_invited.sudo()._action_add_members(self.env.user.partner_id, **member_values))

        return invited_res or bool((self - courses_invited)._action_add_members(self.env.user.partner_id, **member_values))

    def _action_add_members(self, target_partners, **member_values):
        """ Adds the target_partners as members of the channel(s). If member_values contains
        member_status, then according to its value partners are added as follows:
            1) Not in member_values / 'joined' : This is default value and behaviour.
                   The partners will be added as enrolled members. This will make the
                   content (slides) of the channel available to that partner.
            2) 'invited' : This is used when inviting partners. The partners are added as invited
                           members (member_status = 'invited') This will make the channel
                           accessible but not the slides until they enroll themselves.
        Uses:
            - Back-end:
                1) On course access request approval: enroll partner
                2) On inviting member by email: add partner to attendees, set member_status to 'invited'
            - Front-End:
                3) When a partner not in attendees joins the course: enroll partner
                4) When partner in attendees with pending invitation joins the course: enroll partner

        Returns the union of new partners if any and of the invited partners having
        enrolled themselves to courses if any."""
        is_invite = member_values.get('member_status', 'joined') == 'invited'

        # Channels on which the current user has the rights to write.
        channels_to_join = self._filter_add_members(target_partners, **member_values)

        # Existing channel partners
        existing_channel_partners = self.env['slide.channel.partner'].sudo().search([
            ('channel_id', 'in', channels_to_join.ids),
            ('partner_id', 'in', target_partners.ids)
        ])
        existing_channel_partners_map = dict((cid, list()) for cid in self.ids)
        for channel_partner in existing_channel_partners:
            existing_channel_partners_map[channel_partner.channel_id.id].append(channel_partner.partner_id.id)

        # Invited partners confirming their invitation by enrolling to the course.
        confirmed_invitation_partners_sudo = self.env['slide.channel.partner'].sudo()
        to_create_partners_values = []

        for channel in channels_to_join:
            for partner in target_partners:
                if partner.id not in existing_channel_partners_map[channel.id]:
                    to_create_partners_values.append(dict(channel_id=channel.id, partner_id=partner.id, **member_values))
                elif not is_invite:
                    existing_partner = existing_channel_partners.filtered(lambda cp: cp.partner_id.id == partner.id and cp.channel_id.id == channel.id)
                    if existing_partner.member_status == 'invited':
                        confirmed_invitation_partners_sudo |= existing_partner

        # Chatter subscription is done in create function override, if member_status is not 'invited'.
        new_slide_channel_partners = self.env['slide.channel.partner'].sudo().create(to_create_partners_values)
        confirmed_invitation_partners_sudo.write({'member_status': 'joined'})

        # Subscribe invited partners enrolling to the course to the chatter.
        for channel_partner in confirmed_invitation_partners_sudo:
            channel_partner.channel_id.sudo().message_subscribe(
                partner_ids=[channel_partner.partner_id.id],
                subtype_ids=[self.env.ref('website_slides.mt_channel_slide_published').id]
            )

        return confirmed_invitation_partners_sudo | new_slide_channel_partners

    def _filter_add_members(self, target_partners, **member_values):
        allowed = self.filtered(lambda channel: channel.enroll == 'public')
        on_invite = self.filtered(lambda channel: channel.enroll == 'invite')
        if on_invite:
            try:
                on_invite.check_access_rights('write')
                on_invite.check_access_rule('write')
            except:
                pass
            else:
                allowed |= on_invite
        return allowed

    def _add_groups_members(self):
        for channel in self:
            channel._action_add_members(channel.mapped('enroll_group_ids.users.partner_id'))

    def _get_earned_karma(self, partner_ids):
        """ Compute the number of karma earned by partners on a channel
        Warning: this count will not be accurate if the configuration has been
        modified after the completion of a course!
        """
        total_karma = defaultdict(int)

        slide_completed = self.env['slide.slide.partner'].sudo().search([
            ('partner_id', 'in', partner_ids),
            ('channel_id', 'in', self.ids),
            ('completed', '=', True),
            ('quiz_attempts_count', '>', 0)
        ])
        for partner_slide in slide_completed:
            slide = partner_slide.slide_id
            if not slide.question_ids:
                continue
            gains = [slide.quiz_first_attempt_reward,
                     slide.quiz_second_attempt_reward,
                     slide.quiz_third_attempt_reward,
                     slide.quiz_fourth_attempt_reward]
            attempts = min(partner_slide.quiz_attempts_count - 1, 3)
            total_karma[partner_slide.partner_id.id] += gains[attempts]

        channel_completed = self.env['slide.channel.partner'].sudo().search([
            ('partner_id', 'in', partner_ids),
            ('channel_id', 'in', self.ids),
            ('member_status', '=', 'completed')
        ])
        for partner_channel in channel_completed:
            channel = partner_channel.channel_id
            total_karma[partner_channel.partner_id.id] += channel.karma_gen_channel_finish

        return total_karma

    def _remove_membership(self, partner_ids):
        """ Unlink (!!!) the relationships between the passed partner_ids
        and the channels and their slides (done in the unlink of slide.channel.partner model).
        Remove earned karma when completed quizz """
        if not partner_ids:
            raise ValueError("Do not use this method with an empty partner_id recordset")

        earned_karma = self._get_earned_karma(partner_ids)
        users = self.env['res.users'].sudo().search([
            ('partner_id', 'in', list(earned_karma)),
        ])
        for user in users:
            if earned_karma[user.partner_id.id]:
                user.add_karma(-1 * earned_karma[user.partner_id.id])

        removed_channel_partner_domain = []
        for channel in self:
            removed_channel_partner_domain = expression.OR([
                removed_channel_partner_domain,
                [('partner_id', 'in', partner_ids),
                 ('channel_id', '=', channel.id)]
            ])
        self.message_unsubscribe(partner_ids=partner_ids)

        if removed_channel_partner_domain:
            self.env['slide.channel.partner'].sudo().search(removed_channel_partner_domain).unlink()

    def _send_share_email(self, emails):
        """ Share channel through emails."""
        mail_ids = []
        for record in self:
            template = record.share_channel_template_id.with_context(
                user=self.env.user,
                email=emails,
                base_url=record.get_base_url(),
            )
            email_values = {'email_to': emails}
            if self.env.user.has_group('base.group_portal'):
                template = template.sudo()
                email_values['email_from'] = self.env.company.catchall_formatted or self.env.company.email_formatted

            mail_ids.append(template.send_mail(record.id, email_layout_xmlid='mail.mail_notification_light', email_values=email_values))
        return mail_ids

    def action_view_slides(self):
        action = self.env["ir.actions.actions"]._for_xml_id("website_slides.slide_slide_action")
        action['context'] = {
            'search_default_published': 1,
            'default_channel_id': self.id
        }
        action['domain'] = [('channel_id', "=", self.id), ('is_category', '=', False)]
        return action

    def action_view_ratings(self):
        action = self.env["ir.actions.actions"]._for_xml_id("website_slides.rating_rating_action_slide_channel")
        action['name'] = _('Rating of %s') % (self.name)
        action['domain'] = expression.AND([ast.literal_eval(action.get('domain', '[]')), [('res_id', 'in', self.ids)]])
        return action

    def action_request_access(self):
        """ Request access to the channel. Returns a dict with keys being either 'error'
        (specific error raised) or 'done' (request done or not). """
        if self.env.user.has_group('base.group_public'):
            return {'error': _('You have to sign in before')}
        if not self.is_published:
            return {'error': _('Course not published yet')}
        if self.is_member:
            return {'error': _('Already member')}
        if self.enroll == 'invite':
            activities = self.sudo()._action_request_access(self.env.user.partner_id)
            if activities:
                return {'done': True}
            return {'error': _('Already Requested')}
        return {'done': False}

    def action_grant_access(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id).exists()
        if partner:
            if self._action_add_members(partner):
                self.activity_search(
                    ['website_slides.mail_activity_data_access_request'],
                    user_id=self.user_id.id, additional_domain=[('request_partner_id', '=', partner.id)]
                ).action_feedback(feedback=_('Access Granted'))

    def action_refuse_access(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id).exists()
        if partner:
            self.activity_search(
                ['website_slides.mail_activity_data_access_request'],
                user_id=self.user_id.id, additional_domain=[('request_partner_id', '=', partner.id)]
            ).action_feedback(feedback=_('Access Refused'))

    # ---------------------------------------------------------
    # Mailing Mixin API
    # ---------------------------------------------------------

    def _rating_domain(self):
        """ Only take the published rating into account to compute avg and count """
        domain = super(Channel, self)._rating_domain()
        return expression.AND([domain, [('is_internal', '=', False)]])

    def _action_request_access(self, partner):
        activities = self.env['mail.activity']
        requested_cids = self.sudo().activity_search(
            ['website_slides.mail_activity_data_access_request'],
            additional_domain=[('request_partner_id', '=', partner.id)]
        ).mapped('res_id')
        for channel in self:
            if channel.id not in requested_cids:
                activities += channel.activity_schedule(
                    'website_slides.mail_activity_data_access_request',
                    note=_('<b>%s</b> is requesting access to this course.') % partner.name,
                    user_id=channel.user_id.id,
                    request_partner_id=partner.id
                )
        return activities

    # ---------------------------------------------------------
    # Data / Misc
    # ---------------------------------------------------------

    def _get_categorized_slides(self, base_domain, order, force_void=True, limit=False, offset=False):
        """ Return an ordered structure of slides by categories within a given
        base_domain that must fulfill slides. As a course structure is based on
        its slides sequences, uncategorized slides must have the lowest sequences.

        Example
          * category 1 (sequence 1), category 2 (sequence 3)
          * slide 1 (sequence 0), slide 2 (sequence 2)
          * course structure is: slide 1, category 1, slide 2, category 2
            * slide 1 is uncategorized,
            * category 1 has one slide : Slide 2
            * category 2 is empty.

        Backend and frontend ordering is the same, uncategorized first. It
        eases resequencing based on DOM / displayed order, notably when
        drag n drop is involved. """
        self.ensure_one()
        all_categories = self.env['slide.slide'].sudo().search([('channel_id', '=', self.id), ('is_category', '=', True)])
        all_slides = self.env['slide.slide'].sudo().search(base_domain, order=order)
        category_data = []

        # Prepare all categories by natural order
        for category in all_categories:
            category_slides = all_slides.filtered(lambda slide: slide.category_id == category)
            if not category_slides and not force_void:
                continue
            category_data.append({
                'category': category, 'id': category.id,
                'name': category.name, 'slug_name': slug(category),
                'total_slides': len(category_slides),
                'slides': category_slides[(offset or 0):(limit + offset or len(category_slides))],
            })

        # Add uncategorized slides in first position
        uncategorized_slides = all_slides.filtered(lambda slide: not slide.category_id)
        if uncategorized_slides or force_void:
            category_data.insert(0, {
                'category': False, 'id': False,
                'name': _('Uncategorized'), 'slug_name': _('Uncategorized'),
                'total_slides': len(uncategorized_slides),
                'slides': uncategorized_slides[(offset or 0):(offset + limit or len(uncategorized_slides))],
            })

        return category_data

    def _move_category_slides(self, category, new_category):
        if not category.slide_ids:
            return
        truncated_slide_ids = [slide_id for slide_id in self.slide_ids.ids if slide_id not in category.slide_ids.ids]
        if new_category:
            place_idx = truncated_slide_ids.index(new_category.id)
            ordered_slide_ids = truncated_slide_ids[:place_idx] + category.slide_ids.ids + truncated_slide_ids[place_idx]
        else:
            ordered_slide_ids = category.slide_ids.ids + truncated_slide_ids
        for index, slide_id in enumerate(ordered_slide_ids):
            self.env['slide.slide'].browse([slide_id]).sequence = index + 1

    def _resequence_slides(self, slide, force_category=False):
        ids_to_resequence = self.slide_ids.ids
        index_of_added_slide = ids_to_resequence.index(slide.id)
        next_category_id = None
        if self.slide_category_ids:
            force_category_id = force_category.id if force_category else slide.category_id.id
            index_of_category = self.slide_category_ids.ids.index(force_category_id) if force_category_id else None
            if index_of_category is None:
                next_category_id = self.slide_category_ids.ids[0]
            elif index_of_category < len(self.slide_category_ids.ids) - 1:
                next_category_id = self.slide_category_ids.ids[index_of_category + 1]

        if next_category_id:
            added_slide_id = ids_to_resequence.pop(index_of_added_slide)
            index_of_next_category = ids_to_resequence.index(next_category_id)
            ids_to_resequence.insert(index_of_next_category, added_slide_id)
            for i, record in enumerate(self.env['slide.slide'].browse(ids_to_resequence)):
                record.write({'sequence': i + 1})  # start at 1 to make people scream
        else:
            slide.write({
                'sequence': self.env['slide.slide'].browse(ids_to_resequence[-1]).sequence + 1
            })

    def get_backend_menu_id(self):
        return self.env.ref('website_slides.website_slides_menu_root').id

    @api.model
    def _search_get_detail(self, website, order, options):
        with_description = options['displayDescription']
        with_date = options['displayDetail']
        my = options.get('my')
        search_tags = options.get('tag')
        slide_category = options.get('slide_category')
        domain = [website.website_domain()]
        if my:
            domain.append([('partner_ids', '=', self.env.user.partner_id.id)])
        if search_tags:
            ChannelTag = self.env['slide.channel.tag']
            try:
                tag_ids = list(filter(None, [unslug(tag)[1] for tag in search_tags.split(',')]))
                tags = ChannelTag.search([('id', 'in', tag_ids)]) if tag_ids else ChannelTag
            except Exception:
                tags = ChannelTag
            # Group by group_id
            # OR inside a group, AND between groups.
            for tags in tags.grouped('group_id').values():
                domain.append([('tag_ids', 'in', tags.ids)])
        if slide_category and 'nbr_%s' % slide_category in self:
            domain.append([('nbr_%s' % slide_category, '>', 0)])
        search_fields = ['name']
        fetch_fields = ['name', 'website_url']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'website_url', 'type': 'text', 'truncate': False},
        }
        if with_description:
            search_fields.append('description_short')
            fetch_fields.append('description_short')
            mapping['description'] = {'name': 'description_short', 'type': 'text', 'html': True, 'match': True}
        if with_date:
            fetch_fields.append('slide_last_update')
            mapping['detail'] = {'name': 'slide_last_update', 'type': 'date'}
        return {
            'model': 'slide.channel',
            'base_domain': domain,
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-graduation-cap',
        }
