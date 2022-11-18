# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.tests import Form
from odoo import Command


class TestPurchaseRequisitionSaleStock(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.client = cls.env['res.partner'].create({'name': 'Client'})
        cls.vendor_1 = cls.env['res.partner'].create({'name': 'Vendor 1'})
        cls.vendor_2 = cls.env['res.partner'].create({'name': 'Vendor 2'})
        cls.mto_route = cls.env.ref('stock.route_warehouse0_mto')
        cls.buy_route = cls.env.ref('purchase_stock.route_warehouse0_buy')
        cls.mto_route.active = True

        cls.mto_product = cls.env['product.product'].create({
            'name': 'MTO product',
            'categ_id': cls.env.ref('product.product_category_all').id,
            'type': 'product',
            'seller_ids': [Command.create({
                'partner_id': cls.vendor_1.id,
                'price': 10.0,
                'delay': 0,
            })],
            'route_ids': [Command.set((cls.mto_route + cls.buy_route).ids)],
        })

    def test_01_alternatives_po_for_mto_po(self):
        # Create a SO with the MTO product
        so_form = Form(self.env['sale.order'])
        so_form.partner_id = self.env.user.partner_id
        with so_form.order_line.new() as line:
            line.product_id = self.mto_product
        sale_order = so_form.save()
        sale_order.action_confirm()
        self.assertEqual(sale_order.purchase_order_count, 1, "Only one Purchase Order should be linked at this point")

        # Check if the PO is correctly linked to the sale order
        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor_1.id)])
        self.assertEqual(purchase_order.sale_order_count, 1, "Only one Sale Order should be linked to it")
        self.assertListEqual(purchase_order._get_sale_orders().ids, [sale_order.id], "Purchase Order should be linked to the original Sale Order")

        # Create an alternative RFQ for another vendor
        action = purchase_order.action_create_alternative()
        alt_po_wizard = Form(self.env['purchase.requisition.create.alternative'].with_context(**action['context']))
        alt_po_wizard.partner_id = self.vendor_2
        alt_po_wizard.copy_products = True
        alt_po_wizard = alt_po_wizard.save()
        alt_po_wizard.action_create_alternative()

        alt_po = purchase_order.alternative_po_ids.filtered(lambda po: po.id != purchase_order.id)
        self.assertEqual(len(purchase_order.alternative_po_ids), 2, "Base PO should be linked with the alternative PO")
        self.assertEqual(sale_order.purchase_order_count, 2, "Both Purchase Orders should be linked to the Sale Order now")

        linked_purchase_orders = sale_order._get_purchase_orders()
        self.assertEqual(len(linked_purchase_orders.filtered(lambda po: po.id == alt_po.id)), 1, "Both Purchase Order should be linked to the Sale Order")
        self.assertEqual(len(linked_purchase_orders.filtered(lambda po: po.id == purchase_order.id)), 1, "Both Purchase Order should be linked to the Sale Order")
        self.assertListEqual(alt_po._get_sale_orders().ids, [sale_order.id], "The alternative Purchase Order should be linked to the original Sale Order")
