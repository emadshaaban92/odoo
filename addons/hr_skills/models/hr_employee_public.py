# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    resume_line_ids = fields.One2many('hr.resume.line', 'employee_id', string="Resumé lines")
    employee_skill_ids = fields.One2many('hr.employee.skill', 'employee_id', string="Skills")
    resume_interest_ids = fields.Many2many('hr.resume.interest', string="Interests")

    personal_description = fields.Char(readonly=True)
    social_website = fields.Char(readonly=True)
    social_twitter = fields.Char(readonly=True)
    social_facebook = fields.Char(readonly=True)
    social_github = fields.Char(readonly=True)
    social_linkedin = fields.Char(readonly=True)
    social_youtube = fields.Char(readonly=True)
    social_instagram = fields.Char(readonly=True)
