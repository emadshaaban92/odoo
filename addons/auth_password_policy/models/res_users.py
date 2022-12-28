# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_password_policy(self):
        params = self.env['ir.config_parameter'].sudo()
        return {
            'minlength': int(params.get_param('auth_password_policy.minlength', default=0)),
        }

    def _set_password(self):
        self._check_password_policy(self.mapped('password'))

        super(ResUsers, self)._set_password()

    def _check_password_policy(self, passwords):
        failures = []
        params = self.env['ir.config_parameter'].sudo()

        minlength = int(params.get_param('auth_password_policy.minlength', default=0))
        for password in passwords:
            if not password:
                continue
            if len(password) < minlength:
                failures.append(_(u"Passwords must have at least %d characters, got %d.") % (minlength, len(password)))

        if failures:
            raise UserError(u'\n\n '.join(failures))

class ChangePasswordUser(models.TransientModel):
    _inherit = 'change.password.user'

    passwd_strength = fields.Integer("Password Strength", compute='_compute_passwd_strength')

    @api.depends('new_passwd')
    def _compute_passwd_strength(self):
        params = self.env['ir.config_parameter'].sudo()
        minlength = int(params.get_param('auth_password_policy.minlength', default=0))
        for password in self:
            strength = len(password.new_passwd) / minlength * 100
            password.passwd_strength = strength if strength < 100 else 100
