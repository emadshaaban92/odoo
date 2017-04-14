# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.tests import common


class TestDropship(common.TransactionCase):

    def setUp(self):
        super(TestDropship, self).setUp()
        # Usefull models
        self.ResPartner = self.env['res.partner']
        self.Product = self.env['product.product']
        self.SaleOrder = self.env['sale.order']
        self.PurchaseOrder = self.env['purchase.order']
        self.StockQuant = self.env['stock.quant']
        #Usefull IDs
        self.category_1_id = self.ref('product.product_category_1')
        self.uom_unit_id = self.ref('product.product_uom_unit')
        self.partner_id = self.ref('base.res_partner_2')
        self.payment_term_id = self.ref('account.account_payment_term')
        self.route_drop_shipping = self.ref('stock_dropshipping.route_drop_shipping')
        self.location_id = self.ref('stock.stock_location_customers')
        
        self.supplier_dropship = self.ResPartner.create({'name': 'Vendor of Dropshipping test'})
        self.drop_shop_product = self.Product.create({
                'name': 'Pen drive',
                'type': 'product',
                'categ_id': self.category_1_id,
                'list_price': 100.0,
                'standard_price': 0.0,
                'seller_ids': [(0, 0, {'delay': 1, 'name': self.supplier_dropship.id, 'min_qty': 2.0})],
                'uom_id': self.uom_unit_id,
                'uom_po_id': self.uom_unit_id
                })

        self.sale_order_drp_shpng = self.SaleOrder.create({
                'partner_id': self.partner_id,
                'note': 'Create sale order for drop shipping',
                'payment_term_id': self.payment_term_id,
                'order_line': [(0, 0, {'product_id': self.drop_shop_product.id, 'product_uom_qty': 200, 'price_unit': 1.00, 'route_id': self.route_drop_shipping, 'product_uom': self.drop_shop_product.uom_id.id})],
                })

    def test_00_dropship(self):
        """Check for Dropshipping Flow"""
        self.sale_order_drp_shpng.action_confirm()

        # Check the sales order created a procurement group which has a procurement of 200 pieces
        procurement_order = self.sale_order_drp_shpng.procurement_group_id.procurement_ids[0]
        self.assertEquals(procurement_order.product_qty, 200.0, 'procurement group should have 200 pieces.')

        # Check a quotation was created to a certain vendor and confirm so it becomes a confirmed purchase order
        purchase = procurement_order.purchase_line_id.order_id
        
        purchase.button_confirm()
        po_id = self.PurchaseOrder.search([('partner_id', '=', self.supplier_dropship.id)])
        self.assertEquals(purchase.state, 'purchase', 'Purchase order should be in the approved state')

        # Use 'Receive Products' button to immediately view this picking, it should have created a picking with 200 pieces
        self.assertEquals(len(po_id), 1, 'There should be one picking')

        # Send the 200 pieces.
        self.assertEquals(po_id.ids and len(po_id.ids), 1, 'Problem with the Purchase Order detected')
        pickings = po_id[0].picking_ids
        pickings.do_transfer()

        # Check one quant was created in Customers location with 200 pieces and one move in the history_ids
        quants = self.StockQuant.search([('location_id', '=', self.location_id), ('product_id', '=', self.drop_shop_product.id)])
        self.assertTrue(quants, 'No Quant found')
        self.assertEquals(len(quants.ids), 1, 'There should be exactly one quant')
        self.assertEquals(len(quants[0].history_ids), 1, 'The quant should have exactly 1 move in its history')
