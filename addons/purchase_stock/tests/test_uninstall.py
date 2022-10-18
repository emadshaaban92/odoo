# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG
from odoo.tests.common import tagged

from .common import PurchaseTestCommon


@tagged('post_install', '-at_install')
class TestUninstallPurchaseStock(PurchaseTestCommon):
    def test_qty_received_method(self):
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        purchase_order = self.env['purchase.order'].create({
            'partner_id': partner.id,
            'state': 'purchase',
            'order_line': [(0, 0, {
                'product_id': self.t_shirt.id,
            })],
        }).with_user(self.res_users_purchase_user)
        order_line = purchase_order.order_line
        stock_move = order_line.move_ids

        stock_move.quantity_done = 1
        stock_move.picking_id.button_validate()

        self.assertEqual(purchase_order.order_line.qty_received, 1)

        stock_moves_option = self.env['ir.model.fields.selection'].search([
            ('field_id.model', '=', 'purchase.order.line'),
            ('field_id.name', '=', 'qty_received_method'),
            ('value', '=', 'stock_moves'),
        ])

        def _compute_qty_received(records):
            records.read()
            with self.assertQueryCount(0):
                _compute_qty_received.origin(records)
                records.flush()

        OrderLine = self.env['purchase.order.line']
        OrderLine._patch_method('_compute_qty_received', _compute_qty_received)
        stock_moves_option.sudo().with_context(**{
            MODULE_UNINSTALL_FLAG: True
        }).unlink()
        OrderLine._revert_method('_compute_qty_received')

        self.assertEqual(order_line.qty_received_method, 'manual')
        self.assertEqual(order_line.qty_received, 1)
