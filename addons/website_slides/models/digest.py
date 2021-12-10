# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Digest(models.Model):
    _inherit = 'digest.digest'

    kpi_nbr_of_graduated_attendees = fields.Boolean('Graduated Attendees')
    kpi_nbr_of_graduated_attendees_value = fields.Integer(
        compute='_compute_kpi_nbr_of_graduated_attendees_value'
    )
    kpi_nbr_of_new_attendees = fields.Boolean('New Attendees')
    kpi_nbr_of_new_attendees_value = fields.Integer(compute='_compute_kpi_nbr_of_new_attendees_value')

    def _compute_kpi_nbr_of_graduated_attendees_value(self):
        self._ensure_user_has_one_of_the_group('website_slides.group_website_slides_manager')
        for record in self:
            start, end, _ = record._get_kpi_compute_parameters()
            record.kpi_nbr_of_graduated_attendees_value = self.env['slide.channel.partner'].search_count([
                ('completion_date', '>=', start),
                ('completion_date', '<', end)
            ])

    def _compute_kpi_nbr_of_new_attendees_value(self):
        self._ensure_user_has_one_of_the_group('website_slides.group_website_slides_manager')
        for record in self:
            start, end, _ = record._get_kpi_compute_parameters()
            record.kpi_nbr_of_new_attendees_value = self.env['slide.channel.partner'].search_count([
                ('create_date', '>=', start),
                ('create_date', '<', end)
            ])

    def _compute_kpis_actions(self, company, user):
        res = super(Digest, self)._compute_kpis_actions(company, user)
        menu_root_id = self.env.ref('website_slides.website_slides_menu_root').id
        res['kpi_nbr_of_new_attendees'] = 'website_slides.slide_channel_partner_action_report&menu_id=%s' % menu_root_id
        res['kpi_nbr_of_graduated_attendees'] = \
            'website_slides.slide_channel_partner_action_report_graduated&menu_id=%s' % menu_root_id
        return res
