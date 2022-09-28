# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class User(models.Model):
    _inherit = ['res.users']

    resume_line_ids = fields.One2many(related='employee_id.resume_line_ids', readonly=False)
    employee_skill_ids = fields.One2many(related='employee_id.employee_skill_ids', readonly=False)
    resume_interest_ids = fields.Many2many('hr.resume.interest', string="Interests")

    personal_description = fields.Char(related='employee_id.personal_description')
    social_website = fields.Char(related='employee_id.social_website')
    social_twitter = fields.Char(related='employee_id.social_twitter')
    social_facebook = fields.Char(related='employee_id.social_facebook')
    social_github = fields.Char(related='employee_id.social_github')
    social_linkedin = fields.Char(related='employee_id.social_linkedin')
    social_youtube = fields.Char(related='employee_id.social_youtube')
    social_instagram = fields.Char(related='employee_id.social_instagram')

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            'resume_line_ids',
            'employee_skill_ids',
            'resume_interest_ids',
            'personal_description',
            'social_website',
            'social_twitter',
            'social_facebook',
            'social_github',
            'social_linkedin',
            'social_youtube',
            'social_instagram',
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + [
            'resume_line_ids',
            'employee_skill_ids',
            'resume_interest_ids',
            'personal_description',
            'social_website',
            'social_twitter',
            'social_facebook',
            'social_github',
            'social_linkedin',
            'social_youtube',
            'social_instagram',
        ]
