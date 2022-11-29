# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RegistrationEditor(models.TransientModel):
    _name = "registration.editor"
    _description = 'Edit Attendee Details on Sales Confirmation'

    sale_order_id = fields.Many2one('sale.order', 'Sales Order', required=True, ondelete='cascade')
    event_registration_ids = fields.One2many('registration.editor.line', 'editor_id', string='Registrations to Edit')
    seats_available_insufficient = fields.Boolean(
        'Not enough seats for all registrations', compute='_compute_seats_available_insufficient', readonly=True)
    is_multi_event = fields.Boolean('Is Multi Event', compute="_compute_is_multi_event",
        help="Technical field used to determine if the SO is composed of multiple events")
    so_registration_qty_removed = fields.Boolean('# Registrations', compute="_compute_so_registration_qty_removed")

    @api.depends('sale_order_id', 'event_registration_ids')
    def _compute_so_registration_qty_removed(self):
        for editor in self:
            sol_registrations = editor.sale_order_id.order_line.filtered('event_id')
            nb_registrations = len(editor.event_registration_ids)
            editor.so_registration_qty_removed = sum(sol_registrations.mapped('product_uom_qty')) < nb_registrations

    @api.depends('sale_order_id')
    def _compute_is_multi_event(self):
        for editor in self:
            editor.is_multi_event = len(editor.sale_order_id.order_line.event_id) > 1

    @api.depends('event_registration_ids')
    def _compute_seats_available_insufficient(self):
        for editor in self:
            editor.seats_available_insufficient = False

            events_counts = Counter()
            event_tickets_counts = defaultdict(Counter)

            for registration in editor.event_registration_ids:
                events_counts[registration.event_id] += 1
                event_tickets_counts[registration.event_id][registration.event_ticket_id] += 1

            for event, nb_seats_event in events_counts.items():
                # Check nb of seats in each event for all registrations on sale order
                try:
                    event._check_seats_availability(nb_seats_event)
                except ValidationError:
                    editor.seats_available_insufficient = True
                    break
                # Check nb of seats for each ticket of the event for all registrations on sale order
                for ticket, nb_seats_ticket in event_tickets_counts[event].items():
                    try:
                        ticket._check_seats_availability(nb_seats_ticket)
                    except ValidationError:
                        editor.seats_available_insufficient = True
                        break
                if editor.seats_available_insufficient:
                    break

    @api.model
    def default_get(self, fields):
        res = super(RegistrationEditor, self).default_get(fields)
        if not res.get('sale_order_id'):
            sale_order_id = res.get('sale_order_id', self._context.get('active_id'))
            res['sale_order_id'] = sale_order_id
        sale_order = self.env['sale.order'].browse(res.get('sale_order_id'))
        registrations = self.env['event.registration'].search([
            ('sale_order_id', '=', sale_order.id),
            ('event_ticket_id', 'in', sale_order.mapped('order_line.event_ticket_id').ids),
            ('state', '!=', 'cancel')])
        so_line_ticket = sale_order.order_line.grouped('event_ticket_id')

        attendee_list = []
        for event_ticket, so_lines in so_line_ticket.items():
            for so_line in so_lines:
                existing_registrations = [r for r in registrations if r.event_ticket_id == event_ticket and r.sale_order_line_id == so_line]
                for reg in existing_registrations:
                    attendee_list.append([0, 0, {
                        'event_id': reg.event_id.id,
                        'event_ticket_id': reg.event_ticket_id.id,
                        'registration_id': reg.id,
                        'name': reg.name,
                        'email': reg.email,
                        'phone': reg.phone,
                        'mobile': reg.mobile,
                        'sale_order_line_id': so_line.id,
                    }])
                    registrations -= reg
                for count in range(int(so_line.product_uom_qty) - len(existing_registrations)):
                    attendee_list.append([0, 0, {
                        'event_id': so_line.event_id.id,
                        'event_ticket_id': event_ticket.id,
                        'sale_order_line_id': so_line.id,
                        'name': so_line.order_partner_id.name,
                        'email': so_line.order_partner_id.email,
                        'phone': so_line.order_partner_id.phone,
                        'mobile': so_line.order_partner_id.mobile,
                    }])
        res['event_registration_ids'] = attendee_list
        res = self._convert_to_write(res)
        return res

    def action_make_registration(self):
        self.ensure_one()

        registrations_so = self.env['event.registration'].search([('sale_order_id', '=', self.sale_order_id.id), ('state', '!=', 'cancel')])
        registrations_to_cancel = registrations_so - self.event_registration_ids.registration_id
        registrations_to_cancel.action_cancel()

        registrations_to_create = []
        for registration_line in self.event_registration_ids:
            values = registration_line.get_registration_data()
            if registration_line.registration_id:
                registration_line.registration_id.write(values)
            else:
                registrations_to_create.append(values)

        self.env['event.registration'].create(registrations_to_create)
        self.sale_order_id.order_line._update_registrations(
            confirm=self.sale_order_id.amount_total == 0 and not self.seats_available_insufficient)

        return {'type': 'ir.actions.act_window_close'}


class RegistrationEditorLine(models.TransientModel):
    """Event Registration"""
    _name = "registration.editor.line"
    _description = 'Edit Attendee Line on Sales Confirmation'
    _order = "id desc"

    editor_id = fields.Many2one('registration.editor')
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sales Order Line')
    event_id = fields.Many2one('event.event', string='Event', required=True)
    registration_id = fields.Many2one('event.registration', 'Original Registration')
    event_ticket_id = fields.Many2one('event.event.ticket', string='Event Ticket')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    name = fields.Char(string='Name')

    def get_registration_data(self):
        self.ensure_one()
        return {
            'event_id': self.event_id.id,
            'event_ticket_id': self.event_ticket_id.id,
            'partner_id': self.editor_id.sale_order_id.partner_id.id,
            'name': self.name or self.editor_id.sale_order_id.partner_id.name,
            'phone': self.phone or self.editor_id.sale_order_id.partner_id.phone,
            'mobile': self.mobile or self.editor_id.sale_order_id.partner_id.mobile,
            'email': self.email or self.editor_id.sale_order_id.partner_id.email,
            'sale_order_id': self.editor_id.sale_order_id.id,
            'sale_order_line_id': self.sale_order_line_id.id,
        }
