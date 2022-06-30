# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models


class AuthTotpDevice(models.Model):
    _inherit = "auth_totp.device"

    def unlink(self):
        """ Notify users when trusted devices are removed from their account. """
        removed_devices_by_user = self._classify_by_user()
        for user, removed_devices in removed_devices_by_user.items():
            user._notify_security_setting_update(
                _('Security Update: Device Removed'),
                _(
                    "A trusted device has been removed from your account: %s",
                    ', '.join([device.name for device in removed_devices])
                ),
            )

        return super().unlink()

    def _generate(self, scope, name):
        """ Notify users when trusted devices are added onto their account.
        We override this method instead of 'create' as those records are inserted directly into the
        database using raw SQL. """

        res = super()._generate(scope, name)

        self.env.user._notify_security_setting_update(
            _('Security Update: Device Added'),
            _(
                "A trusted device has been added on your account: %s",
                name
            ),
        )

        return res

    def _classify_by_user(self):
        devices_by_user = {}
        for device in self:
            if device.user_id not in devices_by_user:
                devices_by_user[device.user_id] = self.env['auth_totp.device']

            devices_by_user[device.user_id] |= device

        return devices_by_user
