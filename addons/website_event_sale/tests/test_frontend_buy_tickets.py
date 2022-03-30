# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo.tests

from datetime import timedelta
import json

from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.fields import Datetime


class TestUiCommon(HttpCaseWithUserDemo):
    def setUp(self):
        super().setUp()

        if self.env['ir.module.module']._get('payment_custom').state != 'installed':
            self.skipTest("Transfer provider is not installed")

        self.env.ref('payment.payment_provider_transfer').write({
            'state': 'enabled',
            'is_published': True,
        })

        self.event_2 = self.env['event.event'].create({
            'name': 'Conference for Architects TEST',
            'user_id': self.env.ref('base.user_admin').id,
            'date_begin': (Datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d 07:00:00'),
            'date_end': (Datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d 16:30:00'),
            'website_published': True,
        })

        self.event_product = self.env.ref('event_sale.product_product_event')
        self.event_ticket_std, self.event_ticket_vip = self.env['event.event.ticket'].create([{
            'name': 'Standard',
            'event_id': self.event_2.id,
            'product_id': self.event_product.id,
            'start_sale_datetime': (Datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d 07:00:00'),
            'end_sale_datetime': (Datetime.today() + timedelta(90)).strftime('%Y-%m-%d'),
            'price': 1000.0,
        }, {
            'name': 'VIP',
            'event_id': self.event_2.id,
            'product_id': self.event_product.id,
            'end_sale_datetime': (Datetime.today() + timedelta(90)).strftime('%Y-%m-%d'),
            'price': 1500.0,
        }])

        self.event_3 = self.env['event.event'].create({
            'name': 'Last ticket test',
            'user_id': self.env.ref('base.user_admin').id,
            'date_begin': (Datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d 07:00:00'),
            'date_end': (Datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d 16:30:00'),
            'website_published': True,
        })

        self.env['event.event.ticket'].create([{
            'name': 'VIP',
            'event_id': self.event_3.id,
            'product_id': self.env.ref('event_sale.product_product_event').id,
            'end_sale_datetime': (Datetime.today() + timedelta(90)).strftime('%Y-%m-%d'),
            'price': 1500.0,
            'seats_max': 2,
        }])

        # flush event to ensure having tickets available in the tests
        self.env.flush_all()

        (self.env.ref('base.partner_admin') + self.partner_demo).write({
            'street': '215 Vine St',
            'city': 'Scranton',
            'zip': '18503',
            'country_id': self.env.ref('base.us').id,
            'state_id': self.env.ref('base.state_us_39').id,
            'phone': '+1 555-555-5555',
            'email': 'admin@yourcompany.example.com',
        })

        self.env['account.journal'].create({'name': 'Cash - Test', 'type': 'cash', 'code': 'CASH - Test'})

        # Add price list rule on event product on all price list
        # All are modified because some user don't get the default price list (depending on ir_property)
        self.pricelist_currency = self.event_2.company_id.currency_id
        for price_list in self.env['product.pricelist'].search([]):
            price_list.write({
                'discount_policy': 'with_discount',
                'currency_id': self.pricelist_currency,  # Ensure that price list is in event currency to simplify test
            })
            price_list.item_ids += self.env['product.pricelist.item'].create({
                'compute_price': 'percentage',
                'percent_price': 25.0,
                'base': 'list_price',
                'min_quantity': 2,
                'product_id': self.event_product.id,
                'applied_on': '0_product_variant',
            })
        # Add tax on the product
        self.tax = self.env['account.tax'].create({
            'name': "Tax 10",
            'amount': 10,
        })
        self.event_product.write({
            'taxes_id': [self.tax.id],
        })


@odoo.tests.common.tagged('post_install', '-at_install')
class TestUi(TestUiCommon):

    def test_admin(self):
        if self.env['ir.module.module']._get('payment_custom').state != 'installed':
            self.skipTest("Transfer provider is not installed")

        # Seen that:
        # - this test relies on demo data that are entirely in USD (pricelists)
        # - that main demo company is gelocated in US
        # - that this test awaits for hardcoded USDs amount
        # we have to force company currency as USDs only for this test
        self.cr.execute("UPDATE res_company SET currency_id = %s WHERE id = %s", [self.env.ref('base.USD').id, self.env.ref('base.main_company').id])

        transfer_provider = self.env.ref('payment.payment_provider_transfer')
        transfer_provider.write({
            'state': 'enabled',
            'is_published': True,
        })
        transfer_provider._transfer_ensure_pending_msg_is_set()

        self.start_tour("/", 'event_buy_tickets', login="admin")

    def test_demo(self):
        if self.env['ir.module.module']._get('payment_custom').state != 'installed':
            self.skipTest("Transfer provider is not installed")

        transfer_provider = self.env.ref('payment.payment_provider_transfer')
        transfer_provider.write({
            'state': 'enabled',
            'is_published': True,
        })
        transfer_provider._transfer_ensure_pending_msg_is_set()

        self.start_tour("/", 'event_buy_tickets', login="demo")

    def test_buy_last_ticket(self):
        if self.env['ir.module.module']._get('payment_custom').state != 'installed':
            self.skipTest("Transfer provider is not installed")

        transfer_provider = self.env.ref('payment.payment_provider_transfer')
        transfer_provider.write({
            'state': 'enabled',
            'is_published': True,
        })
        transfer_provider._transfer_ensure_pending_msg_is_set()

        self.start_tour("/", 'event_buy_last_ticket')

    # TO DO - add public test with new address when convert to web.tour format.


class TestUnitPriceUi(TestUiCommon):
    """Test of the controller used to display the unit price.

    This price depends on the selected quantity and the user groups. The last determines whether the price should be
    tax included or excluded. """
    def setUp(self):
        super().setUp()
        self.headers_json = {"Content-Type": "application/json", }
        self.company_currency = self.env.company.currency_id
        self.precision_delta = self.company_currency.rounding

    def setup_display_tax_incl(self):
        self.env['res.config.settings'].create({
            'show_line_subtotals_tax_selection': 'tax_included',
            'group_show_line_subtotals_tax_included': True,
            'group_show_line_subtotals_tax_excluded': False,
        }).execute()

    def setup_display_price_not_reduced(self):
        self.env['product.pricelist'].search([]).write({'discount_policy': 'without_discount'})

    def assert_price(self, expected_unit_price, expected_unit_price_not_reduced=None, quantity=1, msg=None):
        msg_suffix = f': {msg}' if msg else ''
        result = self.url_open(f'/website_event_sale/ticket-price-info/{self.event_ticket_std.id}',
                               data=json.dumps({
                                   'params': {'quantity': quantity}
                               }),
                               headers=self.headers_json).json()['result']
        self.assertAlmostEqual(result['price'], expected_unit_price,
                               msg=f'Price: {msg_suffix}',
                               delta=self.precision_delta)
        if expected_unit_price_not_reduced:
            self.assertAlmostEqual(result['price_not_reduced'], expected_unit_price_not_reduced,
                                   msg=f'Price not reduce: {msg_suffix}',
                                   delta=self.precision_delta)
        else:
            self.assertNotIn('price_not_reduced', result,
                             msg=f"Don't disclose not reduced price if not configured to{msg_suffix}")
        result_currency = result['currency']
        for field in ['symbol', 'position', 'decimal_places']:
            self.assertEqual(result_currency[field], self.pricelist_currency[field],
                             msg=f"Currency.{field}{msg_suffix}")

    def test_price_unit_depending_on_quantity_tax_excl(self):
        self.assert_price(1000, msg='Full price')
        self.assert_price(750, quantity=2,
                          msg='1000 - 25% = 750 because the quantity >= 2, configured to not show the full price')
        self.setup_display_price_not_reduced()
        self.assert_price(750, quantity=2, expected_unit_price_not_reduced=1000,
                          msg='1000 - 25% = 750 because the quantity >= 2, configured to show the full price')

    def test_price_unit_depending_on_quantity_tax_incl(self):
        self.setup_display_tax_incl()
        self.assert_price(1100, msg='1000 + 10% tax')
        self.assert_price(825, quantity=2,
                          msg='1000 - 25% = 750 because the quantity >= 2, +10% tax = 825'
                              ', configured to not show the full price')
        self.setup_display_price_not_reduced()
        self.assert_price(825, quantity=2, expected_unit_price_not_reduced=1100,
                          msg='1000 - 25% = 750 because the quantity >= 2, +10% tax = 825'
                              ', configured to show the full price (1000 + 10% tax = 1100)')
