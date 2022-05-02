# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class MailComposerMixin(models.AbstractModel):
    """ Mixin used to edit and render some fields used when sending emails or
    notifications based on a mail template.

    Main current purpose is to hide details related to subject and body computation
    and rendering based on a mail.template. It also give the base tools to control
    who is allowed to edit body, notably when dealing with templating language
    like inline_template or qweb.

    It is meant to evolve in a near future with upcoming support of qweb and fine
    grain control of rendering access.
    """
    _name = 'mail.composer.mixin'
    _inherit = 'mail.render.mixin'
    _description = 'Mail Composer Mixin'

    # Content
    subject = fields.Char('Subject', compute='_compute_subject', readonly=False, store=True)
    body = fields.Html('Contents', compute='_compute_body', render_engine='qweb', store=True, readonly=False, sanitize=False)
    template_id = fields.Many2one('mail.template', 'Mail Template',
        domain="[('model', '=', render_model), ('is_system_template', '=', False)]")

    @api.depends('template_id')
    def _compute_subject(self):
        for composer_mixin in self:
            if composer_mixin.template_id:
                composer_mixin.subject = composer_mixin.template_id.subject
            elif not composer_mixin.subject:
                composer_mixin.subject = False

    @api.depends('template_id')
    def _compute_body(self):
        for composer_mixin in self:
            if composer_mixin.template_id:
                composer_mixin.body = composer_mixin.template_id.body_html
            elif not composer_mixin.body:
                composer_mixin.body = False
