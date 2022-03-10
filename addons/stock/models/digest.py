# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Digest(models.Model):
    _inherit = 'digest.digest'

    kpi_stock_delivery_count = fields.Boolean('Deliveries')
    kpi_stock_delivery_count_value = fields.Integer(compute='_compute_kpi_stock_delivery_count_value')
    kpi_stock_receipt_count = fields.Boolean('Receipts')
    kpi_stock_receipt_count_value = fields.Integer(compute='_compute_kpi_stock_receipt_count_value')

    def _compute_picking_count_gen(self, picking_condition):
        """ Compute the number of picking done according to the given picking condition for each record kpi parameters
        and yield the record and the computed value.
        """
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            yield record, self.env['stock.picking'].search_count(
                [*picking_condition,
                 ('state', '=', 'done'),
                 ('date_done', '>=', start),
                 ('date_done', '<', end),
                 ('company_id', '=', company.id)])

    def _compute_kpi_stock_delivery_count_value(self):
        self._ensure_user_has_one_of_the_group('stock.group_stock_manager')
        for record, value in self._compute_picking_count_gen([  # view_move_search outgoing filter condition
            ('location_id.usage', 'in', ('internal', 'transit')),
            ('location_dest_id.usage', 'not in', ('internal', 'transit'))
        ]):
            record.kpi_stock_delivery_count_value = value

    def _compute_kpi_stock_receipt_count_value(self):
        self._ensure_user_has_one_of_the_group('stock.group_stock_manager')
        for record, value in self._compute_picking_count_gen([  # view_move_search incoming filter condition
            ('location_id.usage', 'not in', ('internal', 'transit')),
            ('location_dest_id.usage', 'in', ('internal', 'transit'))
        ]):
            record.kpi_stock_receipt_count_value = value

    def _compute_kpis_actions(self, company, user):
        res = super(Digest, self)._compute_kpis_actions(company, user)
        menu_root_id = self.env.ref('stock.menu_stock_root').id
        res['kpi_stock_delivery_count'] = 'stock.stock_move_action_outgoing&menu_id=%s' % menu_root_id
        res['kpi_stock_receipt_count'] = 'stock.stock_move_action_incoming&menu_id=%s' % menu_root_id
        return res
