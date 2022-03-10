# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Digest(models.Model):
    _inherit = 'digest.digest'

    kpi_website_visitor_count = fields.Boolean('Visitors')
    kpi_website_visitor_count_value = fields.Integer(compute='_compute_kpi_website_visitors_count_value')
    kpi_website_track_count = fields.Boolean('Tracked Page Views')  # Non uniq
    kpi_website_track_count_value = fields.Integer(compute='_compute_kpi_website_track_count_value')

    def _compute_website_visitor_count(self, website_ids, start, end):
        if len(website_ids) == 0:
            return 0
        self._cr.execute("""
            SELECT count(DISTINCT t.visitor_id)
                FROM website_track t
                JOIN website_visitor v ON v.id=t.visitor_id 
                WHERE v.website_id IN %(website_ids)s AND t.visit_datetime >= %(start)s AND t.visit_datetime < %(end)s
                """, params={'website_ids': website_ids, 'start': start, 'end': end})
        return self._cr.fetchone()[0]

    def _compute_website_track_count(self, website_ids, start, end):
        return self.env['website.track'].search_count(
            [('visitor_id.website_id', 'in', website_ids),
             ('visit_datetime', '>=', start),
             ('visit_datetime', '<', end)]) if len(website_ids) > 0 else 0

    def _compute_by_websites_gen(self, compute_kpi):
        """ This method allows to compute kpi through the given function based on transformed parameters:
        instead of (start, end, company): (start, end, website ids of the company).

        :param function compute_kpi: function to compute the kpi that receives as parameters start, end, website ids of
        the company
        :return: generator that yields for each record of self, a tuple containing the record and the computed kpi
        (computed with the provided function). The record is returned to allow the calling method to set the kpi value
        on the record (avoiding a set attr call in this method).
        """
        # Following dicts are for memoization of partial results during the loop (lru_cache not usable)
        website_ids_by_company = dict()
        kpi_by_new_params = dict()
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            if company.id not in website_ids_by_company:
                website_ids_by_company[company.id] = tuple(
                    self.env['website'].search([('company_id', '=', company.id)]).ids)
            website_ids = website_ids_by_company[company.id]
            new_params = (website_ids, start, end)
            if new_params not in kpi_by_new_params:
                kpi_by_new_params[new_params] = compute_kpi(website_ids, start, end)
            yield record, kpi_by_new_params[new_params]

    def _compute_kpi_website_visitors_count_value(self):
        """ Compute the aggregated unique visitor of the websites company.
        Note that this computation relies on website_visitor which may create multiple visitor for the same user
        (indeed the user is not always identified).
        """
        self._ensure_user_has_one_of_the_group('website.group_website_designer')
        for record, value in self._compute_by_websites_gen(self._compute_website_visitor_count):
            record.kpi_website_visitor_count_value = value

    def _compute_kpi_website_track_count_value(self):
        self._ensure_user_has_one_of_the_group('website.group_website_designer')
        for record, value in self._compute_by_websites_gen(self._compute_website_track_count):
            record.kpi_website_track_count_value = value

    def _compute_kpis_actions(self, company, user):
        res = super(Digest, self)._compute_kpis_actions(company, user)
        menu_root_id = self.env.ref('website.menu_website_configuration').id
        res['kpi_website_visitor_count'] = 'website.website_visitors_action&menu_id=%s' % menu_root_id
        res['kpi_website_track_count'] = 'website.website_visitor_view_action&menu_id=%s' % menu_root_id
        return res
