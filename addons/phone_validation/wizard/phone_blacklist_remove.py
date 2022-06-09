# -*- coding: utf-8 -*-

from markupsafe import Markup
from odoo import fields, models, _


class PhoneBlacklistRemove(models.TransientModel):
    _name = 'phone.blacklist.remove'
    _description = 'Remove phone from blacklist'

    phone = fields.Char(string="Phone Number", readonly=True, required=True)
    reason = fields.Char(name="Reason")

    def action_unblacklist_apply(self):
        return self.env['phone.blacklist']._remove(
            self.phone,
            message=Markup('<p>%s</p>') % _("Unblock Reason: %(reason)s", reason=self.reason) if self.reason else None,
        )
