from datetime import datetime, timedelta
from odoo.tests import common, Form, tagged

@tagged('post_install', '-at_install')
class TestWarnUnwantedReplenish(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.buy_route = cls.env.ref('purchase_stock.route_warehouse0_buy')

        # Create a vendor (& suppliers) and a customer
        cls.vendor = cls.env['res.partner'].create(dict(name='Vendor'))
        cls.customer = cls.env['res.partner'].create(dict(name='Customer'))

        cls.supplier_A = cls.env['product.supplierinfo'].create({
            'partner_id' : cls.vendor.id,
            'min_qty' : 0.0,
            'price' : 10.0,
            'delay' : 0
        })

        cls.supplier_B = cls.env['product.supplierinfo'].create({
            'partner_id' : cls.vendor.id,
            'min_qty' : 0.0,
            'price' : 12.0,
            'delay' : 0
        })

        # Create a "A" and a "B" Product :
        # No Stock
        # Partner/Customer Lead Time = 0
        # Manual reordering 0 0

        cls.product_A = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'categ_id': cls.env.ref('product.product_category_all').id,
            'purchase_method': 'purchase',
            'invoice_policy': 'delivery',
            'standard_price': 5.0,
            'list_price': 10.0,
            'seller_ids': [(4, cls.supplier_A.id, 0)],
            'route_ids': [(4, cls.buy_route.id, 0)],
            'sale_delay' : 0,
        })

        cls.product_B = cls.env['product.product'].create({
            'name': 'Product B',
            'type': 'product',
            'categ_id': cls.env.ref('product.product_category_all').id,
            'purchase_method': 'purchase',
            'invoice_policy': 'delivery',
            'standard_price': 6.0,
            'list_price': 12.0,
            'seller_ids': [(4, cls.supplier_B.id, 0)],
            'route_ids': [(4, cls.buy_route.id, 0)],
            'sale_delay' : 0,
        })


        orderpoint_form = Form(cls.env['stock.warehouse.orderpoint'])
        orderpoint_form.product_id = cls.product_A
        orderpoint_form.product_min_qty = 0.000
        orderpoint_form.product_max_qty = 0.000
        cls.orderpoint_A = orderpoint_form.save()
        cls.orderpoint_A.trigger = 'manual'

        orderpoint_form = Form(cls.env['stock.warehouse.orderpoint'])
        orderpoint_form.product_id = cls.product_B
        orderpoint_form.product_min_qty = 0.000
        orderpoint_form.product_max_qty = 0.000
        cls.orderpoint_B = orderpoint_form.save()
        cls.orderpoint_B.trigger = 'manual'

        # Create Sales
        # For A and for B
        # Delivered today
        # Confirm SO

        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'partner_invoice_id': cls.customer.id,
            'partner_shipping_id': cls.customer.id,
        })
        cls.sol_product_order = cls.env['sale.order.line'].create({
            'product_id': cls.product_A.id,
            'product_uom_qty': 10,
            'order_id': cls.sale_order.id,
        })
        cls.sol_product_order = cls.env['sale.order.line'].create({
            'product_id': cls.product_B.id,
            'product_uom_qty': 10,
            'order_id': cls.sale_order.id,
        })

        cls.sale_order.action_confirm()

        # Create PO for Product A
        # Confirm PO with date planned : TODAY
        # Incoming Picking : reschedule in one week

        cls.po_A = cls.env['purchase.order'].create({
            'partner_id': cls.vendor.id,
            'order_line': [
                (0, 0, {
                    'name': cls.product_A.name,
                    'product_id': cls.product_A.id,
                    'product_qty': 10.0,
                    'price_unit': 10.0,
                    'date_planned': datetime.today(),
                })],
        })

        cls.po_A.button_confirm()

        cls.picking_A = cls.po_A.picking_ids[0]
        cls.picking_A.scheduled_date = (datetime.today() + timedelta(days=10))

    def test_01_ProductA_flow(self):
        """
        TEST 1
          Replenishment ->
              Product A
                  unwanted_replenish SHALL be TRUE
                  Order Once click SHALL show Wizard
                      [Validate All Orders] -> New PO
                      [Validate Correct Orders] -> Nothing change
        """
        self.assertTrue(self.orderpoint_A.unwanted_replenish, 'Orderpoint A not set to unwanted_replenish')

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'A draft purchase order already exist.')

        #Validate Correct Orders
        orderpoint_replenish_action = self.orderpoint_A.action_replenish()
        unwanted_replenish_wizard_form = Form(self.env['stock.warn.unwanted.replenish'].with_context(
            **orderpoint_replenish_action['context']
        ))
        unwanted_replenish_wizard = unwanted_replenish_wizard_form.save()
        unwanted_replenish_wizard.action_validate_correct()

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'Purchase order created.')

        #Force Orders
        orderpoint_replenish_action = self.orderpoint_A.action_replenish()
        unwanted_replenish_wizard_form = Form(self.env['stock.warn.unwanted.replenish'].with_context(
            **orderpoint_replenish_action['context']
        ))
        unwanted_replenish_wizard = unwanted_replenish_wizard_form.save()
        unwanted_replenish_wizard.action_validate_all()

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertTrue(purchase_order, 'No purchase order created.')
        self.assertIn(self.product_A, purchase_order.order_line.product_id, 'Product A shall be present in the Purchase Order')

    def test_02_ProductB_flow(self):
        """
        TEST 2
          Replenishment ->
              Product B
                  unwanted_replenish SHALL be FALSE
                  [Order Once] -> New PO
        """
        self.assertFalse(self.orderpoint_B.unwanted_replenish, 'Orderpoint B is set to unwanted_replenish')

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'A draft purchase order already exist.')

        self.orderpoint_B.action_replenish()

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertTrue(purchase_order, 'No purchase order created.')
        self.assertIn(self.product_B, purchase_order.order_line.product_id, 'Product B shall be present in the Purchase Order')

    def test_03_ProductA_B_no_change_valids(self):
        """
        TEST 3
          Replenishment ->
              Product A & B
                  Order click SHALL show Wizard
                      [Validate Correct Orders] -> New PO for B
        """
        self.assertTrue(self.orderpoint_A.unwanted_replenish, 'Orderpoint A not set to unwanted_replenish')
        self.assertFalse(self.orderpoint_B.unwanted_replenish, 'Orderpoint B is set to unwanted_replenish')

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'A draft purchase order already exist.')

        #Select Orderpoints A & B
        orderpoint_A_B = self.orderpoint_A + self.orderpoint_B

        #Validate Correct Orders
        orderpoint_replenish_action = orderpoint_A_B.action_replenish()
        unwanted_replenish_wizard_form = Form(self.env['stock.warn.unwanted.replenish'].with_context(
            **orderpoint_replenish_action['context']
        ))
        unwanted_replenish_wizard = unwanted_replenish_wizard_form.save()
        unwanted_replenish_wizard.action_validate_correct()

        #PO exists and has only a line for product B
        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertTrue(purchase_order, 'No purchase order created.')
        self.assertNotIn(self.product_A, purchase_order.order_line.product_id, 'Product A shall not be present in the Purchase Order')
        self.assertIn(self.product_B, purchase_order.order_line.product_id, 'Product B shall be present in the Purchase Order')

    def test_04_ProductA_B_no_change_force(self):
        """
        TEST 4
          Replenishment ->
              Product A & B
                  Order click SHALL show Wizard
                      [Validate All Orders] -> New PO for A and B
        """
        self.assertTrue(self.orderpoint_A.unwanted_replenish, 'Orderpoint A not set to unwanted_replenish')
        self.assertFalse(self.orderpoint_B.unwanted_replenish, 'Orderpoint B is set to unwanted_replenish')

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'A draft purchase order already exist.')

        #Select Orderpoints A & B
        orderpoint_A_B = self.orderpoint_A + self.orderpoint_B

        #Force Orders
        orderpoint_replenish_action = orderpoint_A_B.action_replenish()
        unwanted_replenish_wizard_form = Form(self.env['stock.warn.unwanted.replenish'].with_context(
            **orderpoint_replenish_action['context']
        ))
        unwanted_replenish_wizard = unwanted_replenish_wizard_form.save()
        unwanted_replenish_wizard.action_validate_all()

        #PO exists and has lines for products A & B
        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertTrue(purchase_order, 'No purchase order created.')
        self.assertIn(self.product_A, purchase_order.order_line.product_id, 'Product A shall be present in the Purchase Order')
        self.assertIn(self.product_B, purchase_order.order_line.product_id, 'Product B shall be present in the Purchase Order')

    def test_05_ProductA_B_update_A_valids(self):
        """
        TEST 5
          Replenishment ->
              Product A & B
                  Order click SHALL show Wizard
                      Product A
                          Modify Visible Days of A past 1 Week -> unwanted_replenish= false, qty_to_order = 0
                          Modify Max QTY (such as > than qty_to_rder) -> qty_to_order >0
                      [Validate Correct Orders] -> New PO for A and B
        """
        self.assertTrue(self.orderpoint_A.unwanted_replenish, 'Orderpoint A not set to unwanted_replenish')
        self.assertFalse(self.orderpoint_B.unwanted_replenish, 'Orderpoint B is set to unwanted_replenish')

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'A draft purchase order already exist.')

        #Select Orderpoints A & B
        orderpoint_A_B = self.orderpoint_A + self.orderpoint_B

        #Create Wizard
        orderpoint_replenish_action = orderpoint_A_B.action_replenish()
        unwanted_replenish_wizard_form = Form(self.env['stock.warn.unwanted.replenish'].with_context(
            **orderpoint_replenish_action['context']
        ))
        unwanted_replenish_wizard = unwanted_replenish_wizard_form.save()
        #Update Orderpoint A
        self.orderpoint_A.visibility_days = 10
        self.assertFalse(self.orderpoint_A.unwanted_replenish, 'Orderpoint A shall not be set to unwanted_replenish')
        self.assertEqual(self.orderpoint_A.qty_to_order, 0, "Orderpoint A quantity to order shall be equal to 0")
        #Max Qty > Change to Order :> unwanted_replenish = false
        self.orderpoint_A.product_max_qty += 10
        self.assertEqual(self.orderpoint_A.qty_to_order, 10, "Orderpoint A quantity to order shall be equal to 10")
        #Valids only
        unwanted_replenish_wizard.action_validate_correct()

        #PO exists and has lines for products A & B
        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertTrue(purchase_order, 'No purchase order created.')
        self.assertIn(self.product_A, purchase_order.order_line.product_id, 'Product A shall be present in the Purchase Order')
        self.assertIn(self.product_B, purchase_order.order_line.product_id, 'Product B shall be present in the Purchase Order')

    def test_06(self):
        """
        TEST 6
          Replenishment ->
              Product A & B
                  Order click SHALL show Wizard
                      [Recompute and Validate Orders] -> A.qty_to_order recomputed, New PO for A & B
        """
        self.assertTrue(self.orderpoint_A.unwanted_replenish, 'Orderpoint A not set to unwanted_replenish')
        self.assertFalse(self.orderpoint_B.unwanted_replenish, 'Orderpoint B is set to unwanted_replenish')

        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertFalse(purchase_order, 'A draft purchase order already exist.')

        self.orderpoint_A.product_max_qty = 15.0
        self.orderpoint_A.qty_to_order = 20.0

        #Select Orderpoints A & B
        orderpoint_A_B = self.orderpoint_A + self.orderpoint_B

        #Recompute Bad Order(s) and Validate all
        orderpoint_replenish_action = orderpoint_A_B.action_replenish()
        unwanted_replenish_wizard_form = Form(self.env['stock.warn.unwanted.replenish'].with_context(
            **orderpoint_replenish_action['context']
        ))
        unwanted_replenish_wizard = unwanted_replenish_wizard_form.save()
        unwanted_replenish_wizard.action_validate_recompute()

        #PO exists and has only a line for product B
        purchase_order = self.env['purchase.order'].search([('partner_id', '=', self.vendor.id), ('state', '=', 'draft')])
        self.assertTrue(purchase_order, 'No purchase order created.')
        self.assertEqual(self.product_A, purchase_order.order_line[0].product_id, 'Product A shall be present in the Purchase Order')
        self.assertAlmostEqual(purchase_order.order_line[0].product_qty, 15.0, delta=self.product_A.uom_id.rounding)
        self.assertIn(self.product_B, purchase_order.order_line.product_id, 'Product B shall be present in the Purchase Order')
        return
