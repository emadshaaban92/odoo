# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo.tests import Form
from odoo.tests.common import SavepointCase
from odoo.addons.mrp.tests.common import TestMrpCommon
from odoo.exceptions import ValidationError, UserError


class TestWorkOrderProcessCommon(TestMrpCommon):

    @classmethod
    def setUpClass(cls):
        super(TestWorkOrderProcessCommon, cls).setUpClass()
        cls.source_location_id = cls.stock_location_14.id
        cls.warehouse = cls.env.ref('stock.warehouse0')
        # setting up alternative workcenters
        cls.wc_alt_1 = cls.env['mrp.workcenter'].create({
            'name': 'Nuclear Workcenter bis',
            'capacity': 3,
            'time_start': 9,
            'time_stop': 5,
            'time_efficiency': 80,
        })
        cls.wc_alt_2 = cls.env['mrp.workcenter'].create({
            'name': 'Nuclear Workcenter ter',
            'capacity': 1,
            'time_start': 10,
            'time_stop': 5,
            'time_efficiency': 85,
        })
        cls.product_4.uom_id = cls.uom_unit
        cls.planning_bom = cls.env['mrp.bom'].create({
            'product_id': cls.product_4.id,
            'product_tmpl_id': cls.product_4.product_tmpl_id.id,
            'product_uom_id': cls.uom_unit.id,
            'product_qty': 4.0,
            'operation_ids': [
                (0, 0, {'name': 'Gift Wrap Maching', 'workcenter_id': cls.workcenter_1.id, 'time_cycle': 15, 'sequence': 1}),
            ],
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': cls.product_2.id, 'product_qty': 2}),
                (0, 0, {'product_id': cls.product_1.id, 'product_qty': 4})
            ]})
        cls.dining_table = cls.env['product.product'].create({
            'name': 'Table (MTO)',
            'type': 'product',
            'tracking': 'serial',
        })
        cls.product_table_sheet = cls.env['product.product'].create({
            'name': 'Table Top',
            'type': 'product',
            'tracking': 'serial',
        })
        cls.product_table_leg = cls.env['product.product'].create({
            'name': 'Table Leg',
            'type': 'product',
            'tracking': 'lot',
        })
        cls.product_bolt = cls.env['product.product'].create({
            'name': 'Bolt',
            'type': 'product',
        })
        cls.product_screw = cls.env['product.product'].create({
            'name': 'Screw',
            'type': 'product',
        })

        cls.mrp_workcenter = cls.env['mrp.workcenter'].create({
            'name': 'Assembly Line 1',
            'resource_calendar_id': cls.env.ref('resource.resource_calendar_std').id,
        })
        cls.mrp_bom_desk = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.dining_table.product_tmpl_id.id,
            'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
            'sequence': 3,
            'consumption': 'flexible',
            'operation_ids': [
                (0, 0, {'workcenter_id': cls.mrp_workcenter.id, 'name': 'Manual Assembly'}),
            ],
        })
        cls.mrp_bom_desk.write({
            'bom_line_ids': [
                (0, 0, {
                    'product_id': cls.product_table_sheet.id,
                    'product_qty': 1,
                    'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
                    'sequence': 1,
                    'operation_id': cls.mrp_bom_desk.operation_ids.id}),
                (0, 0, {
                    'product_id': cls.product_table_leg.id,
                    'product_qty': 4,
                    'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
                    'sequence': 2,
                    'operation_id': cls.mrp_bom_desk.operation_ids.id}),
                (0, 0, {
                    'product_id': cls.product_bolt.id,
                    'product_qty': 4,
                    'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
                    'sequence': 3,
                    'operation_id': cls.mrp_bom_desk.operation_ids.id}),
                (0, 0, {
                    'product_id': cls.product_screw.id,
                    'product_qty': 10,
                    'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
                    'sequence': 4,
                    'operation_id': cls.mrp_bom_desk.operation_ids.id}),
            ]
        })
        cls.mrp_workcenter_1 = cls.env['mrp.workcenter'].create({
            'name': 'Drill Station 1',
            'resource_calendar_id': cls.env.ref('resource.resource_calendar_std').id,
        })
        cls.mrp_workcenter_3 = cls.env['mrp.workcenter'].create({
            'name': 'Assembly Line 1',
            'resource_calendar_id': cls.env.ref('resource.resource_calendar_std').id,
        })


class TestWorkOrderProcess(TestWorkOrderProcessCommon):
    def full_availability(self):
        """set full availability for all calendars"""
        calendar = self.env['resource.calendar'].search([])
        calendar.write({'attendance_ids': [(5, 0, 0)]})
        calendar.write({'attendance_ids': [
            (0, 0, {'name': 'Monday', 'dayofweek': '0', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
            (0, 0, {'name': 'Tuesday', 'dayofweek': '1', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
            (0, 0, {'name': 'Wednesday', 'dayofweek': '2', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
            (0, 0, {'name': 'Thursday', 'dayofweek': '3', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
            (0, 0, {'name': 'Friday', 'dayofweek': '4', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
            (0, 0, {'name': 'Saturday', 'dayofweek': '5', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
            (0, 0, {'name': 'Sunday', 'dayofweek': '6', 'hour_from': 0, 'hour_to': 24, 'day_period': 'morning'}),
        ]})

    def test_00_workorder_process(self):
        """ Testing consume quants and produced quants with workorder """
        dining_table = self.dining_table
        product_table_sheet = self.product_table_sheet
        product_table_leg = self.product_table_leg
        product_bolt = self.product_bolt
        product_screw = self.product_screw
        mrp_bom_desk = self.mrp_bom_desk

        self.env['stock.move'].search([('product_id', 'in', [product_bolt.id, product_screw.id])])._do_unreserve()

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = mrp_bom_desk
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table = production_table_form.save()
        production_table.action_confirm()

        # Set tracking lot on finish and consume products.
        dining_table.tracking = 'lot'
        product_table_sheet.tracking = 'lot'
        product_table_leg.tracking = 'lot'
        product_bolt.tracking = "lot"

        # Initial inventory of product sheet, lags and bolt
        lot_sheet = self.env['stock.production.lot'].create({'product_id': product_table_sheet.id, 'company_id': self.env.company.id})
        lot_leg = self.env['stock.production.lot'].create({'product_id': product_table_leg.id, 'company_id': self.env.company.id})
        lot_bolt = self.env['stock.production.lot'].create({'product_id': product_bolt.id, 'company_id': self.env.company.id})

        # Initialize inventory
        # --------------------
        inventory = self.env['stock.inventory'].create({
            'name': 'Inventory Product Table',
            'line_ids': [(0, 0, {
                'product_id': product_table_sheet.id,
                'product_uom_id': product_table_sheet.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_sheet.id,
                'location_id': self.source_location_id
            }), (0, 0, {
                'product_id': product_table_leg.id,
                'product_uom_id': product_table_leg.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_leg.id,
                'location_id': self.source_location_id
            }), (0, 0, {
                'product_id': product_bolt.id,
                'product_uom_id': product_bolt.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_bolt.id,
                'location_id': self.source_location_id
            }), (0, 0, {
                'product_id': product_screw.id,
                'product_uom_id': product_screw.uom_id.id,
                'product_qty': 20,
                'location_id': self.source_location_id
            })]
        })
        inventory.action_start()
        inventory.action_validate()

        # Create work order
        production_table.button_plan()
        # Check Work order created or not
        self.assertEqual(len(production_table.workorder_ids), 1)

        # ---------------------------------------------------------
        # Process all workorder and check it state.
        # ----------------------------------------------------------

        workorder = production_table.workorder_ids[0]
        self.assertEqual(workorder.state, 'ready', "workorder state should be ready.")

        # --------------------------------------------------------------
        # Process assembly line
        # ---------------------------------------------------------
        finished_lot =self.env['stock.production.lot'].create({'product_id': production_table.product_id.id, 'company_id': self.env.company.id})
        workorder.write({'finished_lot_id': finished_lot.id})
        workorder.button_start()
        for workorder_line_id in workorder._workorder_line_ids():
            if workorder_line_id.product_id.id == product_bolt.id:
                workorder_line_id.write({'lot_id': lot_bolt.id, 'qty_done': 1})
            if workorder_line_id.product_id.id == product_table_sheet.id:
                workorder_line_id.write({'lot_id': lot_sheet.id, 'qty_done': 1})
            if workorder_line_id.product_id.id == product_table_leg.id:
                workorder_line_id.write({'lot_id': lot_leg.id, 'qty_done': 1})
        self.assertEqual(workorder.state, 'progress')

        workorder.record_production()
        self.assertEqual(workorder.state, 'done')
        move_table_sheet = production_table.move_raw_ids.filtered(lambda x : x.product_id == product_table_sheet)
        self.assertEqual(move_table_sheet.quantity_done, 1)

        # ---------------------------------------------------------------
        # Check consume quants and produce quants after posting inventory
        # ---------------------------------------------------------------
        production_table.button_mark_done()

        self.assertEqual(product_screw.qty_available, 10)
        self.assertEqual(product_bolt.qty_available, 19)
        self.assertEqual(product_table_leg.qty_available, 19)
        self.assertEqual(product_table_sheet.qty_available, 19)

    def test_00b_workorder_process(self):
        """ Testing consume quants and produced quants with workorder """
        dining_table = self.dining_table
        product_table_sheet = self.product_table_sheet
        product_table_leg = self.product_table_leg
        product_bolt = self.product_bolt
        product_screw = self.product_screw
        bom = self.mrp_bom_desk

        self.env['stock.move'].search([('product_id', '=', product_bolt.id)])._do_unreserve()

        bom.operation_ids = False
        bom.write({
            'operation_ids': [
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_1.id,
                    'name': 'Packing',
                    'time_cycle': 30,
                    'sequence': 5}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Testing',
                    'time_cycle': 60,
                    'sequence': 10}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Long time assembly',
                    'time_cycle': 180,
                    'sequence': 15}),
            ]
        })

        bom.bom_line_ids.filtered(lambda p: p.product_id == product_table_sheet).operation_id = bom.operation_ids[0]
        bom.bom_line_ids.filtered(lambda p: p.product_id == product_table_leg).operation_id = bom.operation_ids[1]
        bom.bom_line_ids.filtered(lambda p: p.product_id == product_bolt).operation_id = bom.operation_ids[2]

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = bom
        production_table_form.product_qty = 2.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table = production_table_form.save()
        # Set tracking lot on finish and consume products.
        dining_table.tracking = 'lot'
        product_table_sheet.tracking = 'lot'
        product_table_leg.tracking = 'lot'
        product_bolt.tracking = "lot"
        production_table.action_confirm()
        # Initial inventory of product sheet, lags and bolt
        lot_sheet = self.env['stock.production.lot'].create({'product_id': product_table_sheet.id, 'company_id': self.env.company.id})
        lot_leg = self.env['stock.production.lot'].create({'product_id': product_table_leg.id, 'company_id': self.env.company.id})
        lot_bolt = self.env['stock.production.lot'].create({'product_id': product_bolt.id, 'company_id': self.env.company.id})

        # Initialize inventory
        # --------------------
        inventory = self.env['stock.inventory'].create({
            'name': 'Inventory Product Table',
            'line_ids': [(0, 0, {
                'product_id': product_table_sheet.id,
                'product_uom_id': product_table_sheet.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_sheet.id,
                'location_id': self.source_location_id
            }), (0, 0, {
                'product_id': product_table_leg.id,
                'product_uom_id': product_table_leg.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_leg.id,
                'location_id': self.source_location_id
            }), (0, 0, {
                'product_id': product_bolt.id,
                'product_uom_id': product_bolt.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_bolt.id,
                'location_id': self.source_location_id
            })]
        })
        inventory.action_start()
        inventory.action_validate()

        # Create work order
        production_table.button_plan()
        # Check Work order created or not
        self.assertEqual(len(production_table.workorder_ids), 3)

        # ---------------------------------------------------------
        # Process all workorder and check it state.
        # ----------------------------------------------------------

        workorders = production_table.workorder_ids
        self.assertEqual(workorders[0].state, 'ready', "First workorder state should be ready.")
        self.assertEqual(workorders[1].state, 'pending')
        self.assertEqual(workorders[2].state, 'pending')

        # --------------------------------------------------------------
        # Process cutting operation...
        # ---------------------------------------------------------
        finished_lot = self.env['stock.production.lot'].create({'product_id': production_table.product_id.id, 'company_id': self.env.company.id})
        workorders[0].write({'finished_lot_id': finished_lot.id, 'qty_producing': 1.0})
        workorders[0].button_start()
        workorders[0]._workorder_line_ids()[0].write({'lot_id': lot_sheet.id, 'qty_done': 1})
        self.assertEqual(workorders[0].state, 'progress')

        workorders[0].record_production()

        move_table_sheet = production_table.move_raw_ids.filtered(lambda p: p.product_id == product_table_sheet)
        self.assertEqual(move_table_sheet.quantity_done, 1)

        # --------------------------------------------------------------
        # Process drilling operation ...
        # ---------------------------------------------------------
        workorders[1].button_start()
        workorders[1].qty_producing = 1.0
        workorders[1]._workorder_line_ids()[0].write({'lot_id': lot_leg.id, 'qty_done': 4})
        workorders[1].record_production()
        move_leg = production_table.move_raw_ids.filtered(lambda p: p.product_id == product_table_leg)
        #self.assertEqual(workorders[1].state, 'done')
        self.assertEqual(move_leg.quantity_done, 4)

        # --------------------------------------------------------------
        # Process fitting operation ...
        # ---------------------------------------------------------
        workorders[2].button_start()
        workorders[2].qty_producing = 1.0
        move_lot = workorders[2]._workorder_line_ids()[0]
        move_lot.write({'lot_id': lot_bolt.id, 'qty_done': 4})
        move_table_bolt = production_table.move_raw_ids.filtered(lambda p: p.product_id.id == product_bolt.id)
        workorders[2].record_production()
        self.assertEqual(move_table_bolt.quantity_done, 4)

        # Change the quantity of the production order to 1
        wiz = self.env['change.production.qty'].create({'mo_id': production_table.id ,
                                                        'product_qty': 1.0})
        wiz.change_prod_qty()
        # ---------------------------------------------------------------
        # Check consume quants and produce quants after posting inventory
        # ---------------------------------------------------------------
        production_table.post_inventory()
        self.assertEqual(sum(move_table_sheet.mapped('quantity_done')), 1, "Wrong quantity of consumed product %s" % move_table_sheet.product_id.name)
        self.assertEqual(sum(move_leg.mapped('quantity_done')), 4, "Wrong quantity of consumed product %s" % move_leg.product_id.name)
        self.assertEqual(sum(move_table_bolt.mapped('quantity_done')), 4, "Wrong quantity of consumed product %s" % move_table_bolt.product_id.name)

    def test_explode_from_order(self):
        # bom3 produces 2 Dozen of Doors (p6), aka 24
        # To produce 24 Units of Doors (p6)
        # - 2 Units of Tools (p5) -> need 4
        # - 8 Dozen of Sticks (p4) -> need 16
        # - 12 Units of Wood (p2) -> need 24
        # bom2 produces 1 Unit of Sticks (p4)
        # To produce 1 Unit of Sticks (p4)
        # - 2 Dozen of Sticks (p4) -> need 8
        # - 3 Dozen of Stones (p3) -> need 12

        # Update capacity, start time, stop time, and time efficiency.
        # ------------------------------------------------------------
        self.workcenter_1.write({'capacity': 1, 'time_start': 0, 'time_stop': 0, 'time_efficiency': 100})

        # Set manual time cycle 20 and 10.
        # --------------------------------
        self.bom_3.operation_ids[0].time_cycle_manual = 10
        self.bom_3.operation_ids[1].time_cycle_manual = 10
        self.bom_2.operation_ids.time_cycle_manual = 20

        man_order_form = Form(self.env['mrp.production'])
        man_order_form.product_id = self.product_6
        man_order_form.bom_id = self.bom_3
        man_order_form.product_qty = 48
        man_order_form.product_uom_id = self.product_6.uom_id
        man_order = man_order_form.save()
        # reset quantities
        self.product_1.type = "product"
        self.env['stock.quant'].with_context(inventory_mode=True).create({
            'product_id': self.product_1.id,
            'inventory_quantity': 0.0,
            'location_id': self.warehouse_1.lot_stock_id.id,
        })

        (self.product_2 | self.product_4).write({
            'tracking': 'none',
        })
        # assign consume material
        man_order.action_confirm()
        man_order.action_assign()
        self.assertEqual(man_order.reservation_state, 'confirmed', "Production order should be in waiting state.")

        # check consume materials of manufacturing order
        self.assertEqual(len(man_order.move_raw_ids), 4, "Consume material lines are not generated proper.")
        product_2_consume_moves = man_order.move_raw_ids.filtered(lambda x: x.product_id == self.product_2)
        product_3_consume_moves = man_order.move_raw_ids.filtered(lambda x: x.product_id == self.product_3)
        product_4_consume_moves = man_order.move_raw_ids.filtered(lambda x: x.product_id == self.product_4)
        product_5_consume_moves = man_order.move_raw_ids.filtered(lambda x: x.product_id == self.product_5)
        consume_qty_2 = product_2_consume_moves.product_uom_qty
        self.assertEqual(consume_qty_2, 24.0, "Consume material quantity of Wood should be 24 instead of %s" % str(consume_qty_2))
        consume_qty_3 = product_3_consume_moves.product_uom_qty
        self.assertEqual(consume_qty_3, 12.0, "Consume material quantity of Stone should be 12 instead of %s" % str(consume_qty_3))
        self.assertEqual(len(product_4_consume_moves), 2, "Consume move are not generated proper.")
        for consume_moves in product_4_consume_moves:
            consume_qty_4 = consume_moves.product_uom_qty
            self.assertIn(consume_qty_4, [8.0, 16.0], "Consume material quantity of Stick should be 8 or 16 instead of %s" % str(consume_qty_4))
        self.assertFalse(product_5_consume_moves, "Move should not create for phantom bom")

        # create required lots
        lot_product_2 = self.env['stock.production.lot'].create({'product_id': self.product_2.id, 'company_id': self.env.company.id})
        lot_product_4 = self.env['stock.production.lot'].create({'product_id': self.product_4.id, 'company_id': self.env.company.id})

        # refuel stock
        inventory = self.env['stock.inventory'].create({
            'name': 'Inventory For Product C',
            'line_ids': [(0, 0, {
                'product_id': self.product_2.id,
                'product_uom_id': self.product_2.uom_id.id,
                'product_qty': 30,
                'prod_lot_id': lot_product_2.id,
                'location_id': self.stock_location_14.id
            }), (0, 0, {
                'product_id': self.product_3.id,
                'product_uom_id': self.product_3.uom_id.id,
                'product_qty': 60,
                'location_id': self.stock_location_14.id
            }), (0, 0, {
                'product_id': self.product_4.id,
                'product_uom_id': self.product_4.uom_id.id,
                'product_qty': 60,
                'prod_lot_id': lot_product_4.id,
                'location_id': self.stock_location_14.id
            })]
        })
        inventory.action_start()
        inventory.action_validate()

        # re-assign consume material
        man_order.action_assign()

        # Check production order status after assign.
        self.assertEqual(man_order.reservation_state, 'assigned', "Production order should be in assigned state.")
        # Plan production order.
        man_order.button_plan()

        # check workorders
        # - main bom: Door: 2 operations
        #   operation 1: Cutting
        #   operation 2: Welding, waiting for the previous one
        # - kit bom: Stone Tool: 1 operation
        #   operation 1: Gift Wrapping
        workorders = man_order.workorder_ids
        kit_wo = man_order.workorder_ids.filtered(lambda wo: wo.operation_id.name == "Gift Wrap Maching")
        door_wo_1 = man_order.workorder_ids.filtered(lambda wo: wo.operation_id.name == "Cutting Machine")
        door_wo_2 = man_order.workorder_ids.filtered(lambda wo: wo.operation_id.name == "Weld Machine")

        for workorder in workorders:
            self.assertEqual(workorder.workcenter_id, self.workcenter_1, "Workcenter does not match.")
        self.assertEqual(kit_wo.state, 'ready', "Workorder should be in ready state.")
        self.assertEqual(door_wo_1.state, 'ready', "Workorder should be in ready state.")
        self.assertEqual(door_wo_2.state, 'pending', "Workorder should be in pending state.")
        self.assertEqual(kit_wo.duration_expected, 960, "Workorder duration should be 960 instead of %s." % str(kit_wo.duration_expected))
        self.assertEqual(door_wo_1.duration_expected, 480, "Workorder duration should be 480 instead of %s." % str(door_wo_1.duration_expected))
        self.assertEqual(door_wo_2.duration_expected, 480, "Workorder duration should be 480 instead of %s." % str(door_wo_2.duration_expected))

        # subbom: kit for stone tools
        kit_wo.button_start()
        finished_lot = self.env['stock.production.lot'].create({'product_id': man_order.product_id.id, 'company_id': self.env.company.id})
        kit_wo.write({
            'finished_lot_id': finished_lot.id,
            'qty_producing': 48
        })

        kit_wo.record_production()

        self.assertEqual(kit_wo.state, 'done', "Workorder should be in done state.")

        # first operation of main bom
        finished_lot = self.env['stock.production.lot'].create({'product_id': man_order.product_id.id, 'company_id': self.env.company.id})
        door_wo_1.button_start()
        door_wo_1.write({
            'finished_lot_id': finished_lot.id,
            'qty_producing': 48
        })
        door_wo_1.record_production()
        self.assertEqual(door_wo_1.state, 'done', "Workorder should be in done state.")

        # second operation of main bom
        self.assertEqual(door_wo_2.state, 'ready', "Workorder should be in ready state.")
        door_wo_2.button_start()
        door_wo_2.record_production()
        self.assertEqual(door_wo_2.state, 'done', "Workorder should be in done state.")

    def test_01_without_workorder(self):
        """ Testing consume quants and produced quants without workorder """
        unit = self.ref("uom.product_uom_unit")
        custom_laptop = self.env['product.product'].create({
            'name': 'Drawer',
            'type': 'product',
            'tracking': 'lot',
        })

        # Create new product charger and keybord
        # --------------------------------------
        product_charger = self.env['product.product'].create({
            'name': 'Charger',
            'type': 'product',
            'tracking': 'lot',
            'uom_id': unit,
            'uom_po_id': unit})
        product_keybord = self.env['product.product'].create({
            'name': 'Usb Keybord',
            'type': 'product',
            'tracking': 'lot',
            'uom_id': unit,
            'uom_po_id': unit})

        # Create bill of material for customized laptop.

        bom_custom_laptop = self.env['mrp.bom'].create({
            'product_tmpl_id': custom_laptop.product_tmpl_id.id,
            'product_qty': 10,
            'product_uom_id': unit,
            'bom_line_ids': [(0, 0, {
                'product_id': product_charger.id,
                'product_qty': 20,
                'product_uom_id': unit
            }), (0, 0, {
                'product_id': product_keybord.id,
                'product_qty': 20,
                'product_uom_id': unit
            })]
        })

        # Create production order for customize laptop.

        mo_custom_laptop_form = Form(self.env['mrp.production'])
        mo_custom_laptop_form.product_id = custom_laptop
        mo_custom_laptop_form.bom_id = bom_custom_laptop
        mo_custom_laptop_form.product_qty = 10.0
        mo_custom_laptop_form.product_uom_id = self.env.ref("uom.product_uom_unit")
        mo_custom_laptop = mo_custom_laptop_form.save()

        mo_custom_laptop.action_confirm()
        # Assign component to production order.
        mo_custom_laptop.action_assign()

        # Check production order status of availablity

        self.assertEqual(mo_custom_laptop.reservation_state, 'confirmed')

        # --------------------------------------------------
        # Set inventory for rawmaterial charger and keybord
        # --------------------------------------------------

        lot_charger = self.env['stock.production.lot'].create({'product_id': product_charger.id, 'company_id': self.env.company.id})
        lot_keybord = self.env['stock.production.lot'].create({'product_id': product_keybord.id, 'company_id': self.env.company.id})

        # Initialize Inventory
        # --------------------
        inventory = self.env['stock.inventory'].create({
            'name': 'Inventory Product Table',
            'line_ids': [(0, 0, {
                'product_id': product_charger.id,
                'product_uom_id': product_charger.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_charger.id,
                'location_id': self.source_location_id
            }), (0, 0, {
                'product_id': product_keybord.id,
                'product_uom_id': product_keybord.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_keybord.id,
                'location_id': self.source_location_id
            })]
        })
        inventory.action_start()
        inventory.action_validate()

        # Check consumed move status
        mo_custom_laptop.action_assign()
        self.assertEqual(mo_custom_laptop.reservation_state, 'assigned')

        # Check current status of raw materials.
        for move in mo_custom_laptop.move_raw_ids:
            self.assertEqual(move.product_uom_qty, 20, "Wrong consume quantity of raw material %s: %s instead of %s" % (move.product_id.name, move.product_uom_qty, 20))
            self.assertEqual(move.quantity_done, 0, "Wrong produced quantity on raw material %s: %s instead of %s" % (move.product_id.name, move.quantity_done, 0))

        # -----------------
        # Start production
        # -----------------

        # Produce 6 Unit of custom laptop will consume ( 12 Unit of keybord and 12 Unit of charger)
        laptop_lot_001 = self.env['stock.production.lot'].create({'product_id': custom_laptop.id , 'company_id': self.env.company.id})
        mo_form = Form(mo_custom_laptop)
        mo_form.qty_producing = 6
        mo_form.lot_producing_id = laptop_lot_001
        mo_custom_laptop = mo_form.save()
        details_operation_form = Form(mo_custom_laptop.move_raw_ids[0], view=self.env.ref('stock.view_stock_move_operations'))
        with details_operation_form.move_line_ids.edit(0) as ml:
            ml.qty_done = 12
        details_operation_form.save()
        details_operation_form = Form(mo_custom_laptop.move_raw_ids[1], view=self.env.ref('stock.view_stock_move_operations'))
        with details_operation_form.move_line_ids.edit(0) as ml:
            ml.qty_done = 12
        details_operation_form.save()

        action = mo_custom_laptop.button_mark_done()
        backorder = Form(self.env[action['res_model']].with_context(**action['context']))
        backorder.save().action_backorder()

        # Check consumed move after produce 6 quantity of customized laptop.
        for move in mo_custom_laptop.move_raw_ids:
            self.assertEqual(move.quantity_done, 12, "Wrong produced quantity on raw material %s" % (move.product_id.name))
        self.assertEqual(len(mo_custom_laptop.move_raw_ids), 2)

        # Check done move and confirmed move quantity.
        charger_done_move = mo_custom_laptop.move_raw_ids.filtered(lambda x: x.product_id.id == product_charger.id and x.state == 'done')
        keybord_done_move = mo_custom_laptop.move_raw_ids.filtered(lambda x: x.product_id.id == product_keybord.id and x.state == 'done')
        self.assertEqual(charger_done_move.product_uom_qty, 12)
        self.assertEqual(keybord_done_move.product_uom_qty, 12)

        # Produce remaining 4 quantity
        # ----------------------------

        # Produce 4 Unit of custom laptop will consume ( 8 Unit of keybord and 8 Unit of charger).
        laptop_lot_002 = self.env['stock.production.lot'].create({'product_id': custom_laptop.id, 'company_id': self.env.company.id})
        mo_custom_laptop = mo_custom_laptop.procurement_group_id.mrp_production_ids[1]
        mo_form = Form(mo_custom_laptop)
        mo_form.qty_producing = 4
        mo_form.lot_producing_id = laptop_lot_002
        mo_custom_laptop = mo_form.save()
        details_operation_form = Form(mo_custom_laptop.move_raw_ids[0], view=self.env.ref('stock.view_stock_move_operations'))
        with details_operation_form.move_line_ids.edit(0) as ml:
            ml.qty_done = 8
        details_operation_form.save()
        details_operation_form = Form(mo_custom_laptop.move_raw_ids[1], view=self.env.ref('stock.view_stock_move_operations'))
        with details_operation_form.move_line_ids.edit(0) as ml:
            ml.qty_done = 8
        details_operation_form.save()

        charger_move = mo_custom_laptop.move_raw_ids.filtered(lambda x: x.product_id.id == product_charger.id and x.state != 'done')
        keybord_move = mo_custom_laptop.move_raw_ids.filtered(lambda x: x.product_id.id == product_keybord.id and x.state !='done')
        self.assertEqual(charger_move.quantity_done, 8, "Wrong consumed quantity of %s" % charger_move.product_id.name)
        self.assertEqual(keybord_move.quantity_done, 8, "Wrong consumed quantity of %s" % keybord_move.product_id.name)

    def test_03_test_serial_number_defaults(self):
        """ Test that the correct serial number is suggested on consecutive work orders. """
        laptop = self.laptop
        graphics_card = self.graphics_card
        unit = self.env.ref("uom.product_uom_unit")

        laptop.tracking = 'serial'

        bom_laptop = self.env['mrp.bom'].create({
            'product_tmpl_id': laptop.product_tmpl_id.id,
            'product_qty': 1,
            'product_uom_id': unit.id,
            'bom_line_ids': [(0, 0, {
                'product_id': graphics_card.id,
                'product_qty': 1,
                'product_uom_id': unit.id
            })],
            'operation_ids': [
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_1.id,
                    'name': 'Packing',
                    'time_cycle': 30,
                    'sequence': 5}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Testing',
                    'time_cycle': 60,
                    'sequence': 10}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Long time assembly',
                    'time_cycle': 180,
                    'sequence': 15}),
            ],
        })

        mo_laptop_form = Form(self.env['mrp.production'])
        mo_laptop_form.product_id = laptop
        mo_laptop_form.bom_id = bom_laptop
        mo_laptop_form.product_qty = 3
        mo_laptop = mo_laptop_form.save()

        mo_laptop.action_confirm()
        mo_laptop.button_plan()
        workorders = mo_laptop.workorder_ids.sorted()
        self.assertEqual(len(workorders), 3)

        workorders[0].button_start()
        serial_a = self.env['stock.production.lot'].create({'product_id': laptop.id, 'company_id': self.env.company.id})
        workorders[0].finished_lot_id = serial_a
        workorders[0].record_production()
        serial_b = self.env['stock.production.lot'].create({'product_id': laptop.id, 'company_id': self.env.company.id})
        workorders[0].finished_lot_id = serial_b
        workorders[0].record_production()
        serial_c = self.env['stock.production.lot'].create({'product_id': laptop.id, 'company_id': self.env.company.id})
        workorders[0].finished_lot_id = serial_c
        workorders[0].record_production()
        self.assertEqual(workorders[0].state, 'done')

        for workorder in workorders - workorders[0]:
            workorder.button_start()
            self.assertEqual(workorder.finished_lot_id, serial_a)
            workorder.record_production()
            self.assertEqual(workorder.finished_lot_id, serial_b)
            workorder.record_production()
            self.assertEqual(workorder.finished_lot_id, serial_c)
            workorder.record_production()
            self.assertEqual(workorder.state, 'done')

    def test_03b_test_serial_number_defaults(self):
        """ Check the constraint on the workorder final_lot. The first workorder
        produces 2/2 units without serial number (serial is only required when
        you register a component) then the second workorder try to register a
        serial number. It should be allowed since the first workorder did not
        specify a seiral number.
        """
        drawer = self.env['product.product'].create({
            'name': 'Drawer',
            'type': 'product',
            'tracking': 'lot',
        })
        drawer_drawer = self.env['product.product'].create({
            'name': 'Drawer Black',
            'type': 'product',
            'tracking': 'lot',
        })
        drawer_case = self.env['product.product'].create({
            'name': 'Drawer Case Black',
            'type': 'product',
            'tracking': 'lot',
        })
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': drawer.product_tmpl_id.id,
            'product_uom_id': self.env.ref('uom.product_uom_unit').id,
            'sequence': 2,
            'operation_ids': [
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_1.id,
                    'name': 'Packing',
                    'time_cycle': 30,
                    'sequence': 5}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Testing',
                    'time_cycle': 60,
                    'sequence': 10}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Long time assembly',
                    'time_cycle': 180,
                    'sequence': 15}),
            ],
            'bom_line_ids': [(0, 0, {
                'product_id': drawer_drawer.id,
                'product_qty': 1,
                'product_uom_id': self.env.ref('uom.product_uom_unit').id,
                'sequence': 1,
            }), (0, 0, {
                'product_id': drawer_case.id,
                'product_qty': 1,
                'product_uom_id': self.env.ref('uom.product_uom_unit').id,
                'sequence': 2,
            })]
        })
        inventory = self.env['stock.inventory'].create({
            'name': 'Initial inventory',
            'line_ids': [(0, 0, {
                'product_id': drawer_drawer.id,
                'product_uom_id': drawer_drawer.uom_id.id,
                'product_qty': 50.0,
                'location_id': self.stock_location_14.id,
            }), (0, 0, {
                'product_id': drawer_case.id,
                'product_uom_id': drawer_case.uom_id.id,
                'product_qty': 50.0,
                'location_id': self.stock_location_14.id,
            })]
        })
        inventory.action_start()
        inventory.action_validate()

        product = bom.product_tmpl_id.product_variant_id
        product.tracking = 'serial'

        lot_1 = self.env['stock.production.lot'].create({
            'product_id': product.id,
            'name': 'LOT000001',
            'company_id': self.env.company.id,
        })

        lot_2 = self.env['stock.production.lot'].create({
            'product_id': product.id,
            'name': 'LOT000002',
            'company_id': self.env.company.id,
        })
        self.env['stock.production.lot'].create({
            'product_id': product.id,
            'name': 'LOT000003',
            'company_id': self.env.company.id,
        })

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = product
        mo_form.bom_id = bom
        mo_form.product_qty = 2.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()

        workorder_0 = mo.workorder_ids[0]
        workorder_0.button_start()
        workorder_0.record_production()
        workorder_0.record_production()

        workorder_1 = mo.workorder_ids[1]
        workorder_1.button_start()
        with Form(workorder_1) as wo:
            wo.finished_lot_id = lot_1
        workorder_1.record_production()

        self.assertTrue(len(workorder_1.allowed_lots_domain) > 1)
        with Form(workorder_1) as wo:
            wo.finished_lot_id = lot_2
        workorder_1.record_production()

        workorder_2 = mo.workorder_ids[2]
        self.assertEqual(workorder_2.allowed_lots_domain, lot_1 | lot_2)

        self.assertEqual(workorder_0.finished_workorder_line_ids.qty_done, 2)
        self.assertFalse(workorder_0.finished_workorder_line_ids.lot_id)
        self.assertEqual(sum(workorder_1.finished_workorder_line_ids.mapped('qty_done')), 2)
        self.assertEqual(workorder_1.finished_workorder_line_ids.mapped('lot_id'), lot_1 | lot_2)

    def test_04_test_planning_date(self):
        """ Test that workorder are planned at the correct time. """
        # The workcenter is working 24/7
        self.full_availability()

        dining_table = self.dining_table

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = self.mrp_bom_desk
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table = production_table_form.save()
        production_table.action_confirm()

        # Create work order
        production_table.button_plan()
        workorder = production_table.workorder_ids[0]

        # Check that the workorder is planned now and that it lasts one hour
        self.assertAlmostEqual(workorder.date_planned_start, datetime.now(), delta=timedelta(seconds=10), msg="Workorder should be planned now.")
        self.assertAlmostEqual(workorder.date_planned_finished, datetime.now() + timedelta(hours=1), delta=timedelta(seconds=10), msg="Workorder should be done in an hour.")

    def test_04b_test_planning_date(self):
        """ Test that workorder are planned at the correct time when setting a start date """
        # The workcenter is working 24/7
        self.full_availability()

        dining_table = self.dining_table

        date_start = datetime.now() + timedelta(days=1)

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = self.mrp_bom_desk
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table_form.date_planned_start = date_start
        production_table = production_table_form.save()
        production_table.action_confirm()

        # Create work order
        production_table.button_plan()
        workorder = production_table.workorder_ids[0]

        # Check that the workorder is planned now and that it lasts one hour
        self.assertAlmostEqual(workorder.date_planned_start, date_start, delta=timedelta(seconds=1), msg="Workorder should be planned tomorrow.")
        self.assertAlmostEqual(workorder.date_planned_finished, date_start + timedelta(hours=1), delta=timedelta(seconds=1), msg="Workorder should be done one hour later.")

    def test_planning_overlaps_wo(self):
        """ Test that workorder doesn't overlaps between then when plan the MO """
        self.full_availability()

        dining_table = self.dining_table

        # Take between +30min -> +90min
        date_start = datetime.now() + timedelta(minutes=30)

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = self.mrp_bom_desk
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table_form.date_planned_start = date_start
        production_table = production_table_form.save()
        production_table.action_confirm()

        # Create work order
        production_table.button_plan()
        workorder_prev = production_table.workorder_ids[0]

        # Check that the workorder is planned now and that it lasts one hour
        self.assertAlmostEqual(workorder_prev.date_planned_start, date_start, delta=timedelta(seconds=10), msg="Workorder should be planned in +30min")
        self.assertAlmostEqual(workorder_prev.date_planned_finished, date_start + timedelta(hours=1), delta=timedelta(seconds=10), msg="Workorder should be done in +90min")

        # As soon as possible, but because of the first one, it will planned only after +90 min
        date_start = datetime.now()

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = self.mrp_bom_desk
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table_form.date_planned_start = date_start
        production_table = production_table_form.save()
        production_table.action_confirm()

        # Create work order
        production_table.button_plan()
        workorder = production_table.workorder_ids[0]

        # Check that the workorder is planned now and that it lasts one hour
        self.assertAlmostEqual(workorder.date_planned_start, workorder_prev.date_planned_finished, delta=timedelta(seconds=10), msg="Workorder should be planned after the first one")
        self.assertAlmostEqual(workorder.date_planned_finished, workorder_prev.date_planned_finished + timedelta(hours=1), delta=timedelta(seconds=10), msg="Workorder should be done one hour later.")

    def test_change_production_1(self):
        """Change the quantity to produce on the MO while workorders are already planned."""
        dining_table = self.dining_table
        dining_table.tracking = 'lot'
        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = self.mrp_bom_desk
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table = production_table_form.save()
        production_table.action_confirm()

        # Create work order
        production_table.button_plan()

        context = {'active_id': production_table.id, 'active_model': 'mrp.production'}
        change_qty_form = Form(self.env['change.production.qty'].with_context(context))
        change_qty_form.product_qty = 2.00
        change_qty = change_qty_form.save()
        change_qty.change_prod_qty()

        self.assertEqual(production_table.workorder_ids[0].qty_producing, 2, "Quantity to produce not updated")

    def test_planning_0(self):
        """ Test alternative conditions
        1. alternative relation is directionnal
        2. a workcenter cannot be it's own alternative """
        self.workcenter_1.alternative_workcenter_ids = self.wc_alt_1 | self.wc_alt_2
        self.assertEqual(self.wc_alt_1.alternative_workcenter_ids, self.env['mrp.workcenter'], "Alternative workcenter is not reciprocal")
        self.assertEqual(self.wc_alt_2.alternative_workcenter_ids, self.env['mrp.workcenter'], "Alternative workcenter is not reciprocal")
        with self.assertRaises(ValidationError):
            self.workcenter_1.alternative_workcenter_ids |= self.workcenter_1

    def test_planning_1(self):
        """ Testing planning workorder with alternative workcenters
        Plan 6 times the same MO, the workorders should be split accross workcenters
        The 3 workcenters are free, this test plans 3 workorder in a row then three next.
        The workcenters have not exactly the same parameters (efficiency, start time) so the
        the last 3 workorder are not dispatched like the 3 first.
        At the end of the test, the calendars will look like:
            - calendar wc1 :[mo1][mo4]
            - calendar wc2 :[mo2 ][mo5 ]
            - calendar wc3 :[mo3  ][mo6  ]"""
        planned_date = datetime(2019, 5, 13, 9, 0)
        self.workcenter_1.alternative_workcenter_ids = self.wc_alt_1 | self.wc_alt_2
        workcenters = [self.wc_alt_2, self.wc_alt_1, self.workcenter_1]
        for i in range(3):
            # Create an MO for product4
            mo_form = Form(self.env['mrp.production'])
            mo_form.product_id = self.product_4
            mo_form.bom_id = self.planning_bom
            mo_form.product_qty = 1
            mo_form.date_planned_start = planned_date
            mo = mo_form.save()
            mo.action_confirm()
            mo.button_plan()
            # Check that workcenters change
            self.assertEqual(mo.workorder_ids.workcenter_id, workcenters[i], "wrong workcenter %d" % i)
            self.assertAlmostEqual(mo.date_planned_start, planned_date, delta=timedelta(seconds=10))
            self.assertAlmostEqual(mo.date_planned_start, mo.workorder_ids.date_planned_start, delta=timedelta(seconds=10))

        for i in range(3):
            # Planning 3 more should choose workcenters in opposite order as
            # - wc_alt_2 as the best efficiency
            # - wc_alt_1 take a little less start time
            # - workcenter_1 is the worst
            mo_form = Form(self.env['mrp.production'])
            mo_form.product_id = self.product_4
            mo_form.bom_id = self.planning_bom
            mo_form.product_qty = 1
            mo_form.date_planned_start = planned_date
            mo = mo_form.save()
            mo.action_confirm()
            mo.button_plan()
            # Check that workcenters change
            self.assertEqual(mo.workorder_ids.workcenter_id, workcenters[i], "wrong workcenter %d" % i)
            self.assertNotEqual(mo.date_planned_start, planned_date)
            self.assertAlmostEqual(mo.date_planned_start, mo.workorder_ids.date_planned_start, delta=timedelta(seconds=10))

    def test_planning_2(self):
        """ Plan some manufacturing orders with 2 workorders each
        Batch size of the operation will influence start dates of workorders
        The first unit to be produced can go the second workorder before finishing
        to produce the second unit.
        calendar wc1 : [q1][q2]
        calendar wc2 :     [q1][q2]"""
        self.workcenter_1.alternative_workcenter_ids = self.wc_alt_1 | self.wc_alt_2
        self.planning_bom.operation_ids = False
        self.planning_bom.write({
           'operation_ids': [
                (0, 0, {'name': 'Cutting Machine', 'workcenter_id': self.workcenter_1.id, 'time_cycle': 12, 'sequence': 1, 'batch': 'yes', 'batch_size': 1}),
               (0, 0, {'name': 'Weld Machine', 'workcenter_id': self.workcenter_1.id, 'time_cycle': 18, 'sequence': 2}),
            ],
        })
        # Allow second workorder to start once the first one is not ended yet
        self.env['mrp.workcenter'].search([]).write({'capacity': 1})
        # workcenters work 24/7
        self.full_availability()

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 2
        mo = mo_form.save()
        mo.action_confirm()
        plan = datetime.now()
        mo.button_plan()
        self.assertEqual(mo.workorder_ids[0].workcenter_id, self.wc_alt_2, "wrong workcenter")
        self.assertEqual(mo.workorder_ids[1].workcenter_id, self.wc_alt_1, "wrong workcenter")

        duration1 = self.planning_bom.operation_ids[0].time_cycle * 100.0 / self.wc_alt_2.time_efficiency + self.wc_alt_2.time_start
        duration2 = 2.0 * self.planning_bom.operation_ids[0].time_cycle * 100.0 / self.wc_alt_1.time_efficiency + self.wc_alt_1.time_start + self.wc_alt_1.time_stop
        wo2_start = mo.workorder_ids[1].date_planned_start
        wo2_stop = mo.workorder_ids[1].date_planned_finished

        wo2_start_theo = self.wc_alt_2.resource_calendar_id.plan_hours(duration1 / 60.0, plan, compute_leaves=False, resource=self.wc_alt_2.resource_id)
        wo2_stop_theo = self.wc_alt_1.resource_calendar_id.plan_hours(duration2 / 60.0, wo2_start, compute_leaves=False, resource=self.wc_alt_2.resource_id)

        self.assertAlmostEqual(wo2_start, wo2_start_theo, delta=timedelta(seconds=10), msg="Wrong plannification")
        self.assertAlmostEqual(wo2_stop, wo2_stop_theo, delta=timedelta(seconds=10), msg="Wrong plannification")

    def test_planning_3(self):
        """ Plan some manufacturing orders with 1 workorder on 1 workcenter
        the first workorder will be hard set in the future to see if the second
        one take the free slot before on the calendar
        calendar after first mo : [   ][mo1]
        calendar after second mo: [mo2][mo1] """

        self.workcenter_1.alternative_workcenter_ids = self.wc_alt_1 | self.wc_alt_2
        self.env['mrp.workcenter'].search([]).write({'tz': 'UTC'}) # compute all date in UTC

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo_form.date_planned_start = datetime(2019, 5, 13, 14, 0, 0, 0)
        mo = mo_form.save()
        start = mo.date_planned_start
        mo.action_confirm()
        mo.button_plan()
        self.assertEqual(mo.workorder_ids[0].workcenter_id, self.wc_alt_2, "wrong workcenter")
        wo1_start = mo.workorder_ids[0].date_planned_start
        wo1_stop = mo.workorder_ids[0].date_planned_finished
        self.assertAlmostEqual(wo1_start, start, delta=timedelta(seconds=10), msg="Wrong plannification")
        self.assertAlmostEqual(wo1_stop, start + timedelta(minutes=85.58), delta=timedelta(seconds=10), msg="Wrong plannification")

        # second MO should be plan before as there is a free slot before
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo_form.date_planned_start = datetime(2019, 5, 13, 9, 0, 0, 0)
        mo = mo_form.save()
        mo.action_confirm()
        mo.button_plan()
        self.assertEqual(mo.workorder_ids[0].workcenter_id, self.wc_alt_2, "wrong workcenter")
        wo1_start = mo.workorder_ids[0].date_planned_start
        wo1_stop = mo.workorder_ids[0].date_planned_finished
        self.assertAlmostEqual(wo1_start, datetime(2019, 5, 13, 9, 0, 0, 0), delta=timedelta(seconds=10), msg="Wrong plannification")
        self.assertAlmostEqual(wo1_stop, datetime(2019, 5, 13, 9, 0, 0, 0) + timedelta(minutes=85.59), delta=timedelta(seconds=10), msg="Wrong plannification")

    def test_planning_4(self):
        """ Plan a manufacturing orders with 1 workorder on 1 workcenter
        the workcenter calendar is empty. which means the workcenter is never
        available. Planning a workorder on it should raise an error"""

        self.workcenter_1.alternative_workcenter_ids = self.wc_alt_1 | self.wc_alt_2
        self.env['resource.calendar'].search([]).write({'attendance_ids': [(5, False, False)]})

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo = mo_form.save()
        mo.action_confirm()
        with self.assertRaises(UserError):
            mo.button_plan()

    def test_planning_5(self):
        """ Cancelling a production with workorders should free all reserved slot
        in the related workcenters calendars """
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo = mo_form.save()
        mo.action_confirm()
        mo.button_plan()

        mo.action_cancel()
        self.assertEqual(mo.workorder_ids.mapped('date_start'), [False])
        self.assertEqual(mo.workorder_ids.mapped('date_finished'), [False])

    def test_planning_6(self):
        """ Marking a workorder as done before the theoretical date should update
        the reservation slot in the calendar the be able to reserve the next
        production sooner """
        self.env['mrp.workcenter'].search([]).write({'tz': 'UTC'}) # compute all date in UTC
        mrp_workcenter_3 = self.env['mrp.workcenter'].create({
            'name': 'assembly line 1',
            'resource_calendar_id': self.env.ref('resource.resource_calendar_std').id,
        })
        self.planning_bom.operation_ids = False
        self.planning_bom.write({
            'operation_ids': [(0, 0, {
                'workcenter_id': mrp_workcenter_3.id,
                'name': 'Manual Assembly',
                'time_cycle': 60,
            })]
        })
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo_form.date_planned_start = datetime(2019, 5, 13, 9, 0, 0, 0)
        mo = mo_form.save()
        mo.action_confirm()
        mo.button_plan()
        wo = mo.workorder_ids
        self.assertAlmostEqual(wo.date_planned_start, datetime(2019, 5, 13, 9, 0, 0, 0), delta=timedelta(seconds=10))
        self.assertAlmostEqual(wo.date_planned_finished, datetime(2019, 5, 13, 9, 0, 0, 0) + timedelta(minutes=60), delta=timedelta(seconds=10))
        wo.button_start()
        wo.record_production()
        # Marking workorder as done should change the finished date
        self.assertAlmostEqual(wo.date_finished, datetime.now(), delta=timedelta(seconds=10))
        self.assertAlmostEqual(wo.date_planned_finished, datetime.now(), delta=timedelta(seconds=10))

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo_form.date_planned_start = datetime(2019, 5, 13, 9, 0, 0, 0)
        mo = mo_form.save()
        mo.action_confirm()
        mo.button_plan()
        wo = mo.workorder_ids
        wo.button_start()
        self.assertAlmostEqual(wo.date_start, datetime.now(), delta=timedelta(seconds=10))
        self.assertAlmostEqual(wo.date_planned_start, datetime.now(), delta=timedelta(seconds=10))
        self.assertAlmostEqual(wo.date_planned_finished, datetime.now(), delta=timedelta(seconds=10))

    def test_planning_7(self):
        """ set the workcenter capacity to 10. Produce a dozen of product tracked by
        SN. The production should be done in two batches"""
        self.workcenter_1.capacity = 10
        self.workcenter_1.time_efficiency = 100
        self.workcenter_1.time_start = 0
        self.workcenter_1.time_stop = 0
        self.planning_bom.operation_ids.time_cycle = 60
        self.product_4.tracking = 'serial'
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_uom_id = self.uom_dozen
        mo_form.product_qty = 1
        mo = mo_form.save()
        mo.action_confirm()
        mo.button_plan()
        wo = mo.workorder_ids
        self.assertEqual(wo.duration_expected, 120)

    def test_plan_unplan_date(self):
        """ Testing planning a workorder then cancel it and then plan it again.
        The planned date must be the same the first time and the second time the
        workorder is planned."""
        planned_date = datetime(2019, 5, 13, 9, 0)
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_4
        mo_form.bom_id = self.planning_bom
        mo_form.product_qty = 1
        mo_form.date_planned_start = planned_date
        mo = mo_form.save()
        mo.action_confirm()
        # Plans the MO and checks the date.
        mo.button_plan()
        self.assertAlmostEqual(mo.date_planned_start, planned_date, delta=timedelta(seconds=10))
        self.assertEqual(bool(mo.workorder_ids.exists()), True)
        leave = mo.workorder_ids.leave_id
        self.assertEqual(bool(leave.exists()), True)
        # Unplans the MO and checks the workorder and its leave no more exist.
        mo.button_unplan()
        self.assertEqual(bool(mo.workorder_ids.exists()), False)
        self.assertEqual(bool(leave.exists()), False)
        # Plans (again) the MO and checks the date is still the same.
        mo.button_plan()
        self.assertAlmostEqual(mo.date_planned_start, planned_date, delta=timedelta(seconds=10))
        self.assertAlmostEqual(mo.date_planned_start, mo.workorder_ids.date_planned_start, delta=timedelta(seconds=10))

    def test_kit_planning(self):
        """ Bom made of component 1 and component 2 which is a kit made of
        component 1 too. Check the workorder lines are well created after reservation
        Main bom :
            - comp1 (qty=1)
            - kit (qty=1)
                - comp1 (qty=4)
                - comp2 (qty=1)
        should give :
            - wo line 1 (comp1, qty=1)
            - wo line 2 (comp1, qty=4)
            - wo line 3 (comp2, qty=1) """
        # Kit bom
        self.env['mrp.bom'].create({
            'product_id': self.product_4.id,
            'product_tmpl_id': self.product_4.product_tmpl_id.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1.0,
            'type': 'phantom',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_2.id, 'product_qty': 1}),
                (0, 0, {'product_id': self.product_1.id, 'product_qty': 4})
            ]})

        # Main bom
        main_bom = self.env['mrp.bom'].create({
            'product_id': self.product_5.id,
            'product_tmpl_id': self.product_5.product_tmpl_id.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1.0,
            'operation_ids': [
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_1.id,
                    'name': 'Packing',
                    'time_cycle': 30,
                    'sequence': 5}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Testing',
                    'time_cycle': 60,
                    'sequence': 10}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Long time assembly',
                    'time_cycle': 180,
                    'sequence': 15}),
            ],
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_1.id, 'product_qty': 1}),
                (0, 0, {'product_id': self.product_4.id, 'product_qty': 1})
            ]})

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.product_5
        mo_form.bom_id = main_bom
        mo_form.product_qty = 1
        mo = mo_form.save()
        mo.action_confirm()
        mo.action_assign()
        mo.button_plan()

        self.assertEqual(len(mo.workorder_ids), 3)
        long_time_assembly = mo.workorder_ids[2]
        self.assertEqual(len(long_time_assembly.raw_workorder_line_ids), 3)
        line1 = long_time_assembly.raw_workorder_line_ids[0]
        line2 = long_time_assembly.raw_workorder_line_ids[1]
        line3 = long_time_assembly.raw_workorder_line_ids[2]
        self.assertEqual(line1.product_id, self.product_1)
        self.assertEqual(line1.qty_done, 1)
        self.assertEqual(line2.product_id, self.product_2)
        self.assertEqual(line2.qty_done, 1)
        self.assertEqual(line3.product_id, self.product_1)
        self.assertEqual(line3.qty_done, 4)

    def test_conflict_and_replan(self):
        """ TEST Json data conflicted and the replan button of a workorder """
        dining_table = self.dining_table
        bom = self.mrp_bom_desk
        bom.operation_ids = False
        bom.write({
            'operation_ids': [
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Packing',
                    'time_cycle': 30,
                    'sequence': 5}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Testing',
                    'time_cycle': 60,
                    'sequence': 10}),
                (0, 0, {
                    'workcenter_id': self.mrp_workcenter_3.id,
                    'name': 'Long time assembly',
                    'time_cycle': 180,
                    'sequence': 15}),
            ]})


        bom.bom_line_ids.filtered(lambda p: p.product_id == self.product_table_sheet).operation_id = bom.operation_ids[0].id
        bom.bom_line_ids.filtered(lambda p: p.product_id == self.product_table_leg).operation_id = bom.operation_ids[1].id
        bom.bom_line_ids.filtered(lambda p: p.product_id == self.product_bolt).operation_id = bom.operation_ids[2].id

        production_table_form = Form(self.env['mrp.production'])
        production_table_form.product_id = dining_table
        production_table_form.bom_id = bom
        production_table_form.product_qty = 1.0
        production_table_form.product_uom_id = dining_table.uom_id
        production_table = production_table_form.save()

        production_table.action_confirm()
        # Create work order
        production_table.button_plan()
        # Check Work order created or not
        self.assertEqual(len(production_table.workorder_ids), 3)

        workorders = production_table.workorder_ids
        wo1, wo2, wo3 = workorders[0], workorders[1], workorders[2]

        self.assertEqual(wo1.state, 'ready', "First workorder state should be ready.")
        self.assertEqual(wo1.workcenter_id.id, self.mrp_workcenter_3.id)
        self.assertEqual(wo2.state, 'pending')
        self.assertEqual(wo3.state, 'pending')

        self.assertFalse(wo1.id in wo1._get_conflicted_workorder_ids(), "Shouldn't conflict")
        self.assertFalse(wo2.id in wo2._get_conflicted_workorder_ids(), "Shouldn't conflict")
        self.assertFalse(wo3.id in wo3._get_conflicted_workorder_ids(), "Shouldn't conflict")

        # Conflicted with wo1
        wo2.write({'date_planned_start': wo1.date_planned_start, 'date_planned_finished': wo1.date_planned_finished})
        # Bad order of workorders (wo3-wo1-wo2) + Late
        wo3.write({'date_planned_start': wo1.date_planned_start - timedelta(weeks=1), 'date_planned_finished': wo1.date_planned_finished - timedelta(weeks=1)})

        self.assertTrue(wo2.id in wo2._get_conflicted_workorder_ids(), "Should conflict with wo1")
        self.assertTrue(wo1.id in wo1._get_conflicted_workorder_ids(), "Should conflict with wo2")

        self.assertTrue('text-danger' in wo2.json_popover, "Popover should in be in red (due to conflict)")
        self.assertTrue('text-danger' in wo3.json_popover, "Popover should in be in red (due to bad order of wo)")
        self.assertTrue('text-warning' in wo3.json_popover, "Popover contains of warning (late)")

        wo1.button_start()
        self.assertEqual(wo1.state, 'progress')
        self.assertEqual(wo2.id in wo2._get_conflicted_workorder_ids(), False, "Shouldn't have a conflict because wo1 is in progress")

        wo1_date_planned_start = wo1.date_planned_start
        wo2_date_planned_start = wo2.date_planned_start
        wo3_date_planned_start = wo3.date_planned_start

        wo2.action_replan()  # Replan all MO of WO

        self.assertEqual(wo1.date_planned_start, wo1_date_planned_start, "Planned date of Workorder 1 shouldn't change (because it is in progress)")
        self.assertNotEqual(wo2.date_planned_start, wo2_date_planned_start, "Planned date of Workorder 2 should be updated")
        self.assertNotEqual(wo3.date_planned_start, wo3_date_planned_start, "Planned date of Workorder 3 should be updated")
        self.assertTrue(wo3.date_planned_start > wo2.date_planned_start, "Workorder 2 should be before the 3")


class TestRoutingAndKits(SavepointCase):
    @classmethod
    def setUpClass(cls):
        """
        kit1 (consu)
        compkit1
        finished1
        compfinished1

        Finished1 (Bom1)
            - compfinished1
            - kit1
        Kit1 (BomKit1)
            - compkit1

        Rounting1 (finished1)
            - operation 1
            - operation 2
        Rounting2 (kit1)
            - operation 1
        """
        super(TestRoutingAndKits, cls).setUpClass()
        cls.uom_unit = cls.env['uom.uom'].search([
            ('category_id', '=', cls.env.ref('uom.product_uom_categ_unit').id),
            ('uom_type', '=', 'reference')
        ], limit=1)
        cls.kit1 = cls.env['product.product'].create({
            'name': 'kit1',
            'type': 'consu',
        })
        cls.compkit1 = cls.env['product.product'].create({
            'name': 'compkit1',
            'type': 'product',
        })
        cls.finished1 = cls.env['product.product'].create({
            'name': 'finished1',
            'type': 'product',
        })
        cls.compfinished1 = cls.env['product.product'].create({
            'name': 'compfinished',
            'type': 'product',
        })
        cls.workcenter_finished1 = cls.env['mrp.workcenter'].create({
            'name': 'workcenter1',
        })
        cls.workcenter_kit1 = cls.env['mrp.workcenter'].create({
            'name': 'workcenter2',
        })
        cls.bom_finished1 = cls.env['mrp.bom'].create({
            'product_id': cls.finished1.id,
            'product_tmpl_id': cls.finished1.product_tmpl_id.id,
            'product_uom_id': cls.uom_unit.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': cls.compfinished1.id, 'product_qty': 1}),
                (0, 0, {'product_id': cls.kit1.id, 'product_qty': 1}),
            ],
            'operation_ids': [
                (0, 0, {'sequence': 1, 'name': 'finished operation 1', 'workcenter_id': cls.workcenter_finished1.id}),
                (0, 0, {'sequence': 2, 'name': 'finished operation 2', 'workcenter_id': cls.workcenter_finished1.id}),
            ],
        })
        cls.bom_kit1 = cls.env['mrp.bom'].create({
            'product_id': cls.kit1.id,
            'product_tmpl_id': cls.kit1.product_tmpl_id.id,
            'product_uom_id': cls.uom_unit.id,
            'product_qty': 1,
            'type': 'phantom',
            'bom_line_ids': [
                (0, 0, {'product_id': cls.compkit1.id, 'product_qty': 1}),
            ],
            'operation_ids': [
                (0, 0, {'name': 'Kit operation', 'workcenter_id': cls.workcenter_kit1.id})
            ]
        })

    def test_1(self):
        """Operations are set on `self.bom_kit1` but none on `self.bom_finished1`."""
        self.bom_kit1.bom_line_ids.operation_id = self.bom_kit1.operation_ids[0]

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 1.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()

        self.assertEqual(len(mo.workorder_ids), 3)
        self.assertEqual(len(mo.workorder_ids[0].raw_workorder_line_ids), 0)
        self.assertEqual(mo.workorder_ids[1].raw_workorder_line_ids.product_id, self.compfinished1)
        self.assertEqual(mo.workorder_ids[2].raw_workorder_line_ids.product_id, self.compkit1)

    def test_2(self):
        """Operations are not set on `self.bom_kit1` and `self.bom_finished1`."""
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 1.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()

        self.assertEqual(len(mo.workorder_ids), 3)
        self.assertEqual(len(mo.workorder_ids[0].raw_workorder_line_ids), 0)
        self.assertEqual(mo.workorder_ids[1].raw_workorder_line_ids.product_id, self.compfinished1)
        self.assertEqual(mo.workorder_ids[2].raw_workorder_line_ids.product_id, self.compkit1)

    def test_3(self):
        """Operations are set both `self.bom_kit1` and `self.bom_finished1`."""
        self.bom_kit1.bom_line_ids.operation_id = self.bom_kit1.operation_ids
        self.bom_finished1.bom_line_ids[0].operation_id = self.bom_finished1.operation_ids[0]
        self.bom_finished1.bom_line_ids[1].operation_id = self.bom_finished1.operation_ids[1]

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 1.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()

        self.assertEqual(len(mo.workorder_ids), 3)
        self.assertEqual(mo.workorder_ids[0].raw_workorder_line_ids.product_id, self.compfinished1)
        self.assertFalse(mo.workorder_ids[1].raw_workorder_line_ids.product_id.id)
        self.assertEqual(mo.workorder_ids[2].raw_workorder_line_ids.product_id, self.compkit1)

    def test_4(self):
        """Operations are set on `self.kit1`, none are set on `self.bom_finished1` and a kit
        without routing was added to `self.bom_finished1`. We expect the component of the kit
        without routing to be consumed at the last workorder of the main BoM.
        """
        kit2 = self.env['product.product'].create({
            'name': 'kit2',
            'type': 'consu',
        })
        compkit2 = self.env['product.product'].create({
            'name': 'compkit2',
            'type': 'product',
        })
        bom_kit2 = self.env['mrp.bom'].create({
            'product_id': kit2.id,
            'product_tmpl_id': kit2.product_tmpl_id.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1,
            'type': 'phantom',
            'bom_line_ids': [(0, 0, {'product_id': compkit2.id, 'product_qty': 1})]
        })
        self.bom_finished1.write({'bom_line_ids': [(0, 0, {'product_id': kit2.id, 'product_qty': 1})]})

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 1.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()

        self.assertEqual(len(mo.workorder_ids), 3)

        self.assertEqual(len(mo.workorder_ids[0].raw_workorder_line_ids), 0)
        self.assertEqual(set(mo.workorder_ids[1].raw_workorder_line_ids.product_id.ids), set([self.compfinished1.id, compkit2.id]))
        self.assertEqual(mo.workorder_ids[2].raw_workorder_line_ids.product_id, self.compkit1)

    def test_5(self):
        # Main bom: set the normal component to the first of the two operations of the routing.
        bomline_compfinished = self.bom_finished1.bom_line_ids.filtered(lambda bl: bl.product_id == self.compfinished1)
        bomline_compfinished.operation_id = self.bom_finished1.operation_ids[0]

        # Main bom: the kit do not have an operation set but there's one on its bom
        bomline_kit1 = self.bom_finished1.bom_line_ids - bomline_compfinished
        self.assertFalse(bomline_kit1.operation_id.id)
        self.bom_kit1.bom_line_ids.operation_id = self.bom_kit1.operation_ids

        # Main bom: add a kit without routing
        kit2 = self.env['product.product'].create({
            'name': 'kit2',
            'type': 'consu',
        })
        compkit2 = self.env['product.product'].create({
            'name': 'compkit2',
            'type': 'product',
        })
        bom_kit2 = self.env['mrp.bom'].create({
            'product_id': kit2.id,
            'product_tmpl_id': kit2.product_tmpl_id.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1,
            'type': 'phantom',
            'bom_line_ids': [(0, 0, {'product_id': compkit2.id, 'product_qty': 1})]
        })
        self.bom_finished1.write({'bom_line_ids': [(0, 0, {'product_id': kit2.id, 'product_qty': 1})]})

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 1.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()

        self.assertEqual(len(mo.workorder_ids), 3)
        self.assertEqual(mo.workorder_ids[0].raw_workorder_line_ids.product_id, self.compfinished1)
        self.assertEqual(mo.workorder_ids[1].raw_workorder_line_ids.product_id, compkit2)
        self.assertEqual(mo.workorder_ids[2].raw_workorder_line_ids.product_id, self.compkit1)

    # -------------------------------------------------------------------------
    # Those 2 next tests aren't related to routing and kit but to flexible
    # consumption.
    # -------------------------------------------------------------------------
    def test_merge_lot(self):
        """ Produce 10 units of product tracked by lot on two workorder. On the
        first one, produce 4 onto lot1 then 6 onto lot1 as well. The second
        workorder should be prefilled with 10 units and lot1"""
        self.finished1.tracking = 'lot'
        lot1 = self.env['stock.production.lot'].create({
            'product_id': self.finished1.id,
            'company_id': self.env.company.id,
        })
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 10.0
        mo = mo_form.save()

        mo.action_confirm()
        mo.button_plan()
        wo1 = mo.workorder_ids.filtered(lambda wo: wo.state == 'ready')[0]
        wo1.button_start()
        wo1.qty_producing = 4
        wo1.finished_lot_id = lot1
        wo1.record_production()
        wo1.qty_producing = 6
        wo1.finished_lot_id = lot1
        wo1.record_production()
        wo2 = mo.workorder_ids.filtered(lambda wo: wo.state == 'ready')[0]
        wo2.button_start()
        self.assertEqual(wo2.qty_producing, 10)
        self.assertEqual(wo2.finished_lot_id, lot1)

    def test_add_move(self):
        """ Make a production using multi step routing. Add an additional move
        on a specific operation and check that the produce is consumed into the
        right workorder. """
        self.bom_finished1.consumption = 'flexible'
        add_product = self.env['product.product'].create({
            'name': 'Additional',
            'type': 'product',
        })
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 10.0
        mo = mo_form.save()

        mo_form = Form(mo)
        with mo_form.move_raw_ids.new() as move:
            move.name = mo.name
            move.product_id = add_product
            move.product_uom = add_product.uom_id
            move.location_id = mo.location_src_id
            move.location_dest_id = mo.production_location_id
            move.product_uom_qty = 2
            move.operation_id = mo.bom_id.operation_ids[0]
        mo = mo_form.save()
        self.assertEqual(len(mo.move_raw_ids), 3)
        mo.action_confirm()
        self.assertEqual(mo.move_raw_ids.mapped('state'), ['confirmed'] * 3)
        mo.button_plan()
        self.assertEqual(len(mo.workorder_ids), 3)
        wo1 = mo.workorder_ids[0]
        lines = wo1.raw_workorder_line_ids
        self.assertEqual(lines.product_id, add_product)

    def test_add_move_2(self):
        """ Make a production using multi step routing. Add an additional move
        on a specific operation and check that the produce is consumed into the
        right workorder. """
        self.bom_finished1.consumption = 'flexible'
        add_product = self.env['product.product'].create({
            'name': 'Additional',
            'type': 'product',
        })
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished1
        mo_form.bom_id = self.bom_finished1
        mo_form.product_qty = 10.0
        mo = mo_form.save()
        mo.action_confirm()
        mo_form = Form(mo)
        with mo_form.move_raw_ids.new() as move:
            move.name = mo.name
            move.product_id = add_product
            move.product_uom = add_product.uom_id
            move.location_id = mo.location_src_id
            move.location_dest_id = mo.production_location_id
            move.product_uom_qty = 2
            move.operation_id = mo.bom_id.operation_ids[0]
        mo = mo_form.save()
        new_move = mo.move_raw_ids.filtered(lambda move: move.additional)
        self.assertEqual(len(mo.move_raw_ids), 3)
        self.assertEqual(len(new_move), 1)
        self.assertEqual(mo.move_raw_ids.mapped('state'), ['confirmed'] * 3)
        mo.button_plan()
        self.assertEqual(len(mo.workorder_ids), 3)
        wo1 = mo.workorder_ids[0]
        lines = wo1.raw_workorder_line_ids
        self.assertEqual(lines.product_id, add_product)
