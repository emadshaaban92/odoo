# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class Event(models.Model):
    _inherit = 'event.event'

    def _get_visitor_events(self, current_visitor):
        events = super()._get_visitor_events(current_visitor)
        registration_not_payed = events.registration_ids.filtered_domain([
            ('visitor_id', '=', current_visitor.id),
            ('payment_status', '=', 'to_pay'),
        ])
        events -= registration_not_payed.event_id
        return events
