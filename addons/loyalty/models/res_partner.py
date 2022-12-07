# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_cards_id = fields.One2many('loyalty.card', 'partner_id')
    active_cards = fields.Integer('Active cards', compute='_compute_count_active_cards')

    @api.depends('loyalty_cards_id')
    def _compute_count_active_cards(self):
        count = 0
        for card in self.loyalty_cards_id:
            if(card.points > 0 and (card.expiration_date == False or card.expiration_date >= fields.Date().context_today(self))):
                count += 1
        self.active_cards = count

    def action_view_loyalty_cards(self):
        action = self.env['ir.actions.act_window']._for_xml_id('loyalty.loyalty_card_action')
        all_child = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        action["domain"] = [("partner_id", "in", all_child.ids)]
        action["context"] = {"search_default_active" : True}
        return action
