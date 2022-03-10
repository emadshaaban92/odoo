# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Digest(models.Model):
    _inherit = 'digest.digest'

    kpi_stock_valuation_total = fields.Boolean('Total Inventory Valuation')
    kpi_stock_valuation_total_value = fields.Monetary(compute='_compute_kpi_stock_valuation_total_value')

    def _compute_kpi_stock_valuation_total_value(self):
        self._ensure_user_has_one_of_the_group('stock.group_stock_manager')
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            results = self.env['stock.valuation.layer'] \
                .read_group([('company_id', '=', company.id),
                             ('create_date', '>=', start),
                             ('create_date', '<', end)],
                            ['value:sum'],
                            [])
            self.kpi_stock_valuation_total_value = results[0]['value'] if results else 0

    def _compute_kpis_app_name(self):
        res = super(Digest, self)._compute_kpis_app_name()
        res['kpi_stock_valuation_total'] = 'stock'
        return res

    def _compute_kpis_actions(self, company, user):
        res = super(Digest, self)._compute_kpis_actions(company, user)
        menu_root_id = self.env.ref('stock.menu_stock_root').id
        res['kpi_stock_valuation_total'] = 'stock_account.stock_valuation_layer_action&menu_id=%s' % menu_root_id
        return res
