# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    repair_id = fields.Many2one('repair.order', check_company=True)
    repair_line_type = fields.Selection([
            ('add', 'Add'),
            ('remove', 'Remove'),
        ],
        'Type', default=False, store=True, readonly=False, index=True)

    @api.onchange('repair_line_type')
    def _onchange_repair_line_type(self):
        for move in self:
            if move.repair_id:
                if not move.picking_type_id:
                    move.picking_type_id = move.repair_id.picking_type_id.id
                if move.repair_line_type:
                    move.location_id, move.location_dest_id = move._get_repair_locations(move.repair_line_type)

    def _search_picking_for_assignation_domain(self):
        """As we want to assign "Add" and "Remove" repair_line_type of a same repair to the same picking,
        The default method is overrided to allow different source and destination locations in the assignation domain."""
        domain = super()._search_picking_for_assignation_domain()
        if self.repair_id:
            domain_keys = [(i, field_name) for i, field_name in zip(range(len(domain)), (field_name for field_name, _, _ in domain))]
            for i, field_name in reversed(domain_keys):
                if field_name in ('location_id', 'location_dest_id'):
                    del domain[i]
        return domain

    def write(self, vals):
        res = super().write(vals)
        for move in self:
            if move.repair_id:
                #if 'picking_type_id' in vals:
                #    move._set_repair_line_type()
                if move.repair_id.sale_order_id:
                    type_is_add = move.repair_line_type == 'add'
                    if not move.sale_line_id and type_is_add:
                        move._create_sale_order_line()
                    else: #sale_line_id or type != 'add'
                        so_locked = move.sale_line_id.order_id.state in ['sale', 'done']
                        if 'product_id' in vals:
                            if so_locked:
                                move.sale_line_id.write({'product_uom_qty' : 0.0})
                                if type_is_add:
                                    move._create_sale_order_line()
                            else:
                                move.sale_line_id.write({'product_id' : vals['product_id']})
                        if type_is_add and 'product_uom_qty' in vals:
                            move.sale_line_id.write({'product_uom_qty' : vals['product_uom_qty']})
                            if move.repair_id.under_warranty:
                                move.sale_line_id.write({'price_unit' : 0.0})
                        if 'repair_line_type' in vals and not type_is_add:
                            move.sale_line_id.write({'product_uom_qty' : 0.0})
        return res

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            if move.repair_id:
                move.name = move.repair_id.name
                move.group_id = move.repair_id.procurement_group_id.id
                move.origin = move.name
                if move.repair_line_type:
                    move.picking_type_id = move.repair_id.picking_type_id.id
                    move.repair_id.write({'operation_move_ids' : [(4, move.id, 0)]})
                    if move.repair_line_type == 'add' and move.repair_id.sale_order_id:
                        move._create_sale_order_line()
        return moves

    def unlink(self):
        for move in self:
            if move.repair_id and move.repair_id.sale_order_id:
                move.sale_line_id.write({'product_uom_qty' : 0.0})
        super().unlink()

    def _create_sale_order_line(self):
        self.ensure_one()
        so_line_vals = {
                    'order_id': self.repair_id.sale_order_id.id,
                    'product_id': self.product_id.id,
                    'product_uom_qty' : self.product_uom_qty,
                    'move_ids' : [(4, self.id, 0)],
                }
        if self.repair_id.under_warranty:
            so_line_vals['price_unit'] = 0.0
        self.sale_line_id.create(so_line_vals)

    def _get_repair_locations(self, repair_line_type):
        self.ensure_one()
        if self.repair_id:
            if repair_line_type == 'add':
                location_id = self.picking_type_id.default_location_src_id
                location_dest_id = self.picking_type_id.default_location_dest_id
                return location_id, location_dest_id
            elif repair_line_type == 'remove':
                location_id = self.picking_type_id.default_location_dest_id
                location_dest_id = self.env['stock.location'].search([('scrap_location', '=', True), ('company_id', 'in', [self.company_id.id, False])], limit=1)
                return location_id, location_dest_id
        return False, False
