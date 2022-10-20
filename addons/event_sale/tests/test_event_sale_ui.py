# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo.fields import Datetime
from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestUi(HttpCase):
    def setUp(self):
        super().setUp()
        self.event = self.env['event.event'].create({
            'name': 'Live Music Festival',
            'date_begin': Datetime.now() + timedelta(days=1),
            'date_end': Datetime.now() + timedelta(days=5),
            'auto_confirm': True,
        })

        self.env['event.event.ticket'].create([{
            'name': 'Standard',
            'event_id': self.event.id,
            'product_id': self.env.ref('event_sale.product_product_event').id,
        }, {
            'name': 'VIP',
            'event_id': self.event.id,
            'product_id': self.env.ref('event_sale.product_product_event').id,
        }])

    def test_event_configurator(self):
        self.start_tour("/web", 'event_configurator_tour', login="admin")

    def test_event_decrease_registration_propagation(self):
        self.start_tour("/web", 'decrease_registration_propagation_tour', login="admin")
        attendee_count = self.event.registration_ids.sale_order_id.attendee_count
        self.assertEqual(self.event.registration_ids.sale_order_line_id.product_uom_qty, attendee_count)
        self.assertEqual(attendee_count, 1)
        self.assertEqual(len(self.event.registration_ids), 2)
        self.assertEqual(len(self.event.registration_ids.filtered(lambda r: r.state == 'cancel')), 1)

    def test_event_increase_registration_propagation(self):
        self.start_tour("/web", 'increase_registration_propagation_tour', login="admin")
        attendee_count = self.event.registration_ids.sale_order_id.attendee_count
        self.assertEqual(self.event.registration_ids.sale_order_line_id.product_uom_qty, attendee_count)
        self.assertEqual(attendee_count, 3)
        self.assertEqual(len(self.event.registration_ids), 3)
        self.assertEqual(len(self.event.registration_ids.filtered(lambda r: r.state == 'open')), 3)
