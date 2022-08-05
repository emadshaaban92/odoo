# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo.addons.mail.controllers.discuss as discuss
from odoo.osv.expression import AND, OR


class DiscussController(discuss.DiscussController):
    def _mail_thread_messages_filter(self):
        return AND([
            super()._mail_thread_messages_filter(),
            # Exclude sms not sent because of a permanent failure: blacklisted, duplicated or opted out
            OR([
                [('sms_ids', '=', False)],  # Not all mail.message have a related sms.sms
                [('sms_ids.failure_type', 'not in', ('sms_blacklist', 'sms_optout', 'sms_duplicate'))],
            ])
        ])
