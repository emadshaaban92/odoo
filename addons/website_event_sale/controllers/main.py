# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import datetime
from odoo import _
from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventSaleController(WebsiteEventController):

    @route()
    def event_register(self, event, **post):
        event = event.with_context(pricelist=request.website.id)
        if not request.context.get('pricelist'):
            pricelist = request.website.pricelist_id
            if pricelist:
                event = event.with_context(pricelist=pricelist.id)
        return super().event_register(event, **post)

    def _process_tickets_form(self, event, form_details):
        """ Add price information on ticket order """
        res = super()._process_tickets_form(event, form_details)
        for item in res:
            item['price'] = item['ticket']['price'] if item['ticket'] else 0
        return res

    def _create_attendees_from_registration_post(self, event, registration_data):
        # we have at least one registration linked to a ticket -> sale mode activate
        if not any(info.get('event_ticket_id') for info in registration_data):
            return super()._create_attendees_from_registration_post(event, registration_data)

        order_sudo = request.website.sale_get_order(force_create=True)

        tickets_data = defaultdict(int)
        for data in registration_data:
            event_ticket_id = data.get('event_ticket_id')
            if event_ticket_id:
                tickets_data[event_ticket_id] += 1

        cart_data = {}
        for ticket_id, count in tickets_data.items():
            ticket_sudo = request.env['event.event.ticket'].sudo().browse(ticket_id)
            cart_values = order_sudo._cart_update(
                product_id=ticket_sudo.product_id.id,
                add_qty=count,
                event_ticket_id=ticket_id,
            )
            cart_data[ticket_id] = cart_values['line_id']

        for data in registration_data:
            event_ticket_id = data.get('event_ticket_id')
            if event_ticket_id:
                data['sale_order_id'] = order_sudo.id
                data['sale_order_line_id'] = cart_data[event_ticket_id]

        request.session['website_sale_cart_quantity'] = order_sudo.cart_quantity

        return super()._create_attendees_from_registration_post(event, registration_data)

    @route()
    def registration_confirm(self, event, **post):
        res = super().registration_confirm(event, **post)

        registrations = self._process_attendees_form(event, post)

        # we have at least one registration linked to a ticket -> sale mode activate
        if any(info['event_ticket_id'] for info in registrations):
            order_sudo = request.website.sale_get_order()
            if order_sudo.amount_total:
                return request.redirect("/shop/checkout")
            # free tickets -> order with amount = 0: auto-confirm, no checkout
            elif order_sudo:
                order_sudo.action_confirm()  # tde notsure: email sending ?
                request.website.sale_reset()

        return res

    def _prepare_event_values(self, name, event_start, event_end, address_values=None):
        values = super()._prepare_event_values(name, event_start, event_end, address_values)
        product = request.env.ref('event_sale.product_product_event', raise_if_not_found=False)
        if product:
            values.update({
                'event_ticket_ids': [[0, 0, {
                    'name': _('Registration'),
                    'product_id': product.id,
                    'end_sale_datetime': False,
                    'seats_max': 1000,
                    'price': 0,
                }]]
            })
        return values

    @route(['/website_event_sale/ticket-price-info/<int:event_ticket_id>'],
           type='json', auth="public", website=True, sitemap=False)
    def get_ticket_price_info(self, event_ticket_id, quantity=1):
        """
        :param: int event_ticket_id: id of an event ticket
        :param: int quantity: optional quantity (default 1)
        :return: a dict containing detailed unit price of the ticket for the given quantity
        """
        pricelist = request.website.pricelist_id
        event_ticket = request.env['event.event.ticket'].browse(event_ticket_id)
        company_id = event_ticket.event_id.sudo().company_id
        ticket_currency = company_id.currency_id
        ctx = dict(quantity=quantity)
        if pricelist:
            ctx.update(pricelist=pricelist.id)
            currency_id = pricelist.currency_id
            discount_policy = pricelist.discount_policy
        else:
            currency_id = ticket_currency
            discount_policy = None

        event_ticket = event_ticket.with_context(ctx)

        if not request.env.user.has_group('account.group_show_line_subtotals_tax_excluded'):
            # All in tax included
            price = event_ticket.price_reduce_taxinc
            price_not_reduced = event_ticket.with_context(pricelist=None, quantity=1).price_reduce_taxinc
        else:
            # All in tax excluded
            price = event_ticket.price_reduce
            price_not_reduced = ticket_currency._convert(
                event_ticket.price,
                currency_id,
                company_id,
                datetime.date.today())

        values = {
            'price': price,
            'currency': {
                'symbol': currency_id.symbol,
                'position': currency_id.position,
                'decimal_places': currency_id.decimal_places,
            },
        }
        if price_not_reduced > price and discount_policy == 'without_discount':
            values['price_not_reduced'] = price_not_reduced
        return values
