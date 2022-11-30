# Part of Odoo. See LICENSE file for full copyright and licensing details.

from random import randint

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
from odoo.tools.misc import format_date

class Repair(models.Model):
    _name = 'repair.order'
    _description = 'Repair Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, create_date desc'

    components_availability = fields.Char(
        string="Component Status", compute='_compute_components_availability',
        help="Latest component availability status for this RO. If green, then the RO's readiness status is ready.")
    components_availability_state = fields.Selection([
        ('available', 'Available'),
        ('expected', 'Expected'),
        ('late', 'Late')], compute='_compute_components_availability')
    name = fields.Char(
        'Repair Reference',
        default='New', index='trigram',
        copy=False, required=True,
        readonly=True)
    procurement_group_id = fields.Many2one(
        'procurement.group', 'Procurement Group',
        copy=False)
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, check_company=True)
    product_qty = fields.Float(
        'Product Quantity',
        default=1.0, digits='Product Unit of Measure',
        readonly=True, states={'draft': [('readonly', False)]})
    product_uom = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        compute='_compute_product_uom', store=True, precompute=True,
        readonly=True, states={'draft': [('readonly', False)]}, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True, check_company=True, change_default=True,
        help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.')
    state = fields.Selection([
        ('draft', 'New'),
        ('confirmed', 'Confirmed'),
        ('under_repair', 'Under Repair'),
        ('done', 'Repaired'),
        ('cancel', 'Cancelled')], string='Status',
        copy=False, default='draft', readonly=True, tracking=True, index=True,
        help="* The \'New\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Under Repair\' status is used when the repair is ongoing.\n"
             "* The \'Repaired\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order.")
    schedule_date = fields.Date("Scheduled Date", default=fields.Datetime.now, index=True, required=True, copy=False)
    under_warranty = fields.Boolean('Under Warranty', help='If ticked, the sales price will be set to 0 for all products transferred from the repair order.')
    location_id = fields.Many2one(
        'stock.location', 'Location',
        compute="_compute_location_id", store=True, precompute=True,
        index=True, readonly=True, check_company=True,
        help="This is the location where the product to repair is located.",
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', True)]})
    lot_id = fields.Many2one(
        'stock.lot', 'Lot/Serial',
        domain="[('product_id','=', product_id), ('company_id', '=', company_id)]", check_company=True,
        help="Products repaired are all belonging to this lot")
    operation_move_ids = fields.One2many('stock.move', 'repair_id', "Parts",
        domain=[('repair_line_type', '!=', False)], check_company=True)
    move_id = fields.Many2one(
        'stock.move', 'Inventory Move',
        copy=False, readonly=True, tracking=True, check_company=True)
    internal_notes = fields.Html('Internal Notes')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user, check_company=True)
    company_id = fields.Many2one(
        'res.company', 'Company',
        readonly=True, required=True, index=True,
        default=lambda self: self.env.company)
    sale_order_id = fields.Many2one(
        'sale.order', 'Sale Order', check_company=True,
        copy=False, help="Sale Order from which the product to be repaired comes from.")
    picking_id = fields.Many2one(
        'stock.picking', 'Return', check_company=True,
        copy=False, help="Return Order from which the product to be repaired comes from.")
    allowed_picking_type_ids = fields.Many2many('stock.picking.type', compute='_compute_allowed_picking_type_ids')
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type', copy=True, readonly=False,
        compute='_compute_picking_type_id', store=True, precompute=True,
        domain="[('code', '=', 'repair_operation'), ('company_id', '=', company_id)]",
        required=True, check_company=True, index=True)
    is_returned = fields.Boolean(
        "Returned", compute='_compute_is_returned',
        help="True if this repair is linked to a Return Order and the order is 'Done'. False otherwise.")
    tag_ids = fields.Many2many('repair.tags', string="Tags")
    tracking = fields.Selection(string='Product Tracking', related="product_id.tracking", readonly=False)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')], default='0', string="Priority")

    unreserve_visible = fields.Boolean(
        'Allowed to Unreserve Production', compute='_compute_unreserve_visible',
        help='Technical field to check when we can unreserve')
    reserve_visible = fields.Boolean(
        'Allowed to Reserve Production', compute='_compute_unreserve_visible',
        help='Technical field to check when we can reserve quantities')

    @api.depends('product_id')
    def _compute_allowed_picking_type_ids(self):
        '''
            computes the ids of return picking types
        '''
        out_picking_types = self.env['stock.picking.type'].search_read(domain=[('code', '=', 'outgoing')],
                                                                          fields=['return_picking_type_id'], load='')
        self.allowed_picking_type_ids = [
            pt['return_picking_type_id'] for pt in out_picking_types if pt['return_picking_type_id']]

    @api.depends('state', 'schedule_date', 'operation_move_ids', 'operation_move_ids.forecast_availability', 'operation_move_ids.forecast_expected_date')
    def _compute_components_availability(self):
        repairs = self.filtered(lambda ro: ro.state not in ('cancel', 'done', 'draft'))
        repairs.components_availability_state = 'available'
        repairs.components_availability = _('Available')

        other_repairs = self - repairs
        other_repairs.components_availability = False
        other_repairs.components_availability_state = False

        all_operation_moves = repairs.operation_move_ids
        # Force to prefetch more than 1000 by 1000
        all_operation_moves._fields['forecast_availability'].compute_value(all_operation_moves)
        for repair in repairs:
            if any(float_compare(move.forecast_availability, 0 if move.state == 'draft' else move.product_qty, precision_rounding=move.product_id.uom_id.rounding) == -1 for move in repair.operation_move_ids):
                repair.components_availability = _('Not Available')
                repair.components_availability_state = 'late'
            else:
                forecast_date = max(repair.operation_move_ids.filtered('forecast_expected_date').mapped('forecast_expected_date'), default=False)
                if forecast_date:
                    repair.components_availability = _('Exp %s', format_date(self.env, forecast_date))
                    if repair.schedule_date:
                        repair.components_availability_state = 'late' if forecast_date > repair.schedule_date else 'expected'

    @api.depends('picking_id', 'picking_id.state')
    def _compute_is_returned(self):
        self.is_returned = False
        returned = self.filtered(lambda r: r.picking_id and r.picking_id.state == 'done')
        returned.is_returned = True

    @api.onchange('location_id', 'picking_id')
    def _onchange_location_picking(self):
        location_warehouse = self.location_id.warehouse_id
        picking_warehouse = self.picking_id.location_dest_id.warehouse_id
        if location_warehouse and picking_warehouse and location_warehouse != picking_warehouse:
            return {
                'warning': {'title': _("Warning"), 'message': _("Note that the warehouses of the return and repair locations don't match!")},
            }

    @api.depends('product_id')
    def _compute_product_uom(self):
        for repair in self:
            if repair.product_id:
                repair.product_uom = repair.product_id.uom_id

    @api.onchange('product_id')
    def onchange_product_id(self):
        if (self.product_id and self.lot_id and self.lot_id.product_id != self.product_id) or not self.product_id:
            self.lot_id = False

    @api.onchange('product_uom')
    def onchange_product_uom(self):
        res = {}
        if not self.product_id or not self.product_uom:
            return res
        if self.product_uom.category_id != self.product_id.uom_id.category_id:
            res['warning'] = {'title': _('Warning'), 'message': _('The product unit of measure you chose has a different category than the product unit of measure.')}
            self.product_uom = self.product_id.uom_id.id
        return res

    @api.depends('company_id')
    def _compute_location_id(self):
        for order in self:
            if order.company_id:
                if order.location_id.company_id != order.company_id:
                    warehouse = self.env['stock.warehouse'].search([('company_id', '=', order.company_id.id)], limit=1)
                    order.location_id = warehouse.lot_stock_id
            else:
                order.location_id = False

    @api.depends('company_id')
    def _compute_picking_type_id(self):
        domain = [
            ('code', '=', 'repair_operation'),
            ('warehouse_id.company_id', 'in', self.company_id.ids),
        ]
        picking_types = self.env['stock.picking.type'].search_read(domain, ['company_id'], load=False, limit=1)
        picking_type_by_company = {pt['company_id']: pt['id'] for pt in picking_types}
        for ro in self:
            if ro.picking_type_id and ro.picking_type_id.company_id == ro.company_id:
                continue
            ro.picking_type_id = picking_type_by_company.get(ro.company_id.id, False)

    @api.depends('operation_move_ids', 'state', 'operation_move_ids.product_uom_qty')
    def _compute_unreserve_visible(self):
        for repair in self:
            already_reserved = repair.state not in ('done', 'cancel') and repair.mapped('operation_move_ids.move_line_ids')
            any_quantity_done = any(m.quantity_done > 0 for m in repair.operation_move_ids)

            repair.unreserve_visible = not any_quantity_done and already_reserved
            repair.reserve_visible = repair.state in ('confirmed', 'under_repair') and any(move.product_uom_qty and move.state in ['confirmed', 'partially_available'] for move in repair.operation_move_ids)


    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        self.operation_move_ids.picking_type_id = self.picking_type_id

    @api.onchange('schedule_date')
    def _onchange_schedule_date(self):
        self.operation_move_ids.date = self.schedule_date
        if self.move_id:
            self.move_id.date = self.schedule_date


    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        if any(order.state not in ('draft', 'cancel') for order in self):
            raise UserError(_('You can not delete a repair order once it has been confirmed. You must first cancel it.'))

    @api.model_create_multi
    def create(self, vals_list):
        # We generate a standard reference
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order') or '/'
            if not vals.get('procurement_group_id'):
                vals['procurement_group_id'] = self.env["procurement.group"].create({'name': vals['name']}).id
        return super().create(vals_list)

    def write(self, vals):
        super().write(vals)
        for order in self:
            if 'picking_type_id' in vals:
                order.operation_move_ids.write({'picking_type_id': order.picking_type_id.id})

            moves = order.operation_move_ids.filtered('sale_line_id')
            if 'under_warranty' in vals:
                if order.under_warranty:
                    moves.mapped('sale_line_id').write({'price_unit' : 0.0})
                else:
                    moves.mapped('sale_line_id')._compute_price_unit()

            if 'state' in vals and order.state == 'done':
                for move in moves:
                    move.sale_line_id.write({'qty_delivered' : move.sale_line_id.product_uom_qty})

    def button_dummy(self):
        # TDE FIXME: this button is very interesting
        return True

    def action_create_invoice(self):
        self.ensure_one()
        if self.sale_order_id:
            raise UserError(_("You cannot create a quotation for this repair as it's already linked to an existing sale order."))
        if not self.partner_id:
            raise UserError(_("You need to define a customer for the repair order in order to create an associated quotation."))
        self.sale_order_id.create({
            "company_id" : self.company_id.id,
            "partner_id" : self.partner_id.id,
            "repair_order_ids" : [(4, self.id, 0)],
        })

        #Add Sale Order Lines for 'add' operation_move_ids
        for move in filter(lambda move: move.repair_line_type == 'add', self.operation_move_ids):
            move._create_sale_order_line()

    def action_repair_cancel_draft(self):
        if self.filtered(lambda repair: repair.state != 'cancel'):
            raise UserError(_("Repair must be canceled in order to reset it to new."))
        # self.mapped('operations').write({'state': 'draft'})#FIXME
        return self.write({'state': 'draft'})

    def action_validate(self):
        self.ensure_one()
        if self.filtered(lambda repair: any(op.product_uom_qty < 0 for op in repair.operation_move_ids)):#FIXME : still necessary for stock.move ?
            raise UserError(_("You can not enter negative quantities."))
        if not self.product_id or self.product_id.type == 'consu':
            return self.action_repair_confirm()
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        available_qty_owner = self.env['stock.quant']._get_available_quantity(self.product_id, self.location_id, self.lot_id, owner_id=self.partner_id, strict=True)
        available_qty_noown = self.env['stock.quant']._get_available_quantity(self.product_id, self.location_id, self.lot_id, strict=True)
        repair_qty = self.product_uom._compute_quantity(self.product_qty, self.product_id.uom_id)
        for available_qty in [available_qty_owner, available_qty_noown]:
            if float_compare(available_qty, repair_qty, precision_digits=precision) >= 0:
                return self.action_repair_confirm()

        return {
            'name': self.product_id.display_name + _(': Insufficient Quantity To Repair'),
            'view_mode': 'form',
            'res_model': 'stock.warn.insufficient.qty.repair',
            'view_id': self.env.ref('repair.stock_warn_insufficient_qty_repair_form_view').id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_product_id': self.product_id.id,
                'default_location_id': self.location_id.id,
                'default_repair_id': self.id,
                'default_quantity': repair_qty,
                'default_product_uom_name': self.product_id.uom_name
            },
            'target': 'new'
        }

    def action_repair_confirm(self):
        """ Repair order state is set to 'Confirmed'.
        @param *arg: Arguments
        @return: True
        """
        if self.filtered(lambda repair: repair.state != 'draft'):
            raise UserError(_("Only draft repairs can be confirmed."))
        self._check_company()
        self.operation_move_ids._check_company()
        self.operation_move_ids._adjust_procure_method()
        self.operation_move_ids._action_confirm()
        self.operation_move_ids._trigger_scheduler()
        self.write({'state': 'confirmed'})
        return True


    def action_repair_cancel(self):
        #self.operation_move_ids._clear_quantities_to_zero()
        self.operation_move_ids._action_cancel()
        return self.write({'state': 'cancel'})

    def action_send_mail(self):
        self.ensure_one()
        template_id = self.env.ref('repair.mail_template_repair_quotation').id
        ctx = {
            'default_model': 'repair.order',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_light',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def print_repair_order(self):
        return self.env.ref('repair.action_report_repair_order').report_action(self)

    def action_repair_start(self):
        """ Writes repair order state to 'Under Repair'
        @return: True
        """
        if self.filtered(lambda repair: repair.state != 'confirmed'):
            raise UserError(_("Repair must be confirmed before starting reparation."))
        # self.mapped('operation_move_ids').write({'state': 'confirmed'})#FIXME
        return self.write({'state': 'under_repair'})

    def action_repair_end(self):
        """ Writes repair order state to 'Ready'.
        @return: True
        """
        if self.filtered(lambda repair: repair.state != 'under_repair'):
            raise UserError(_("Repair must be under repair in order to end reparation."))
        self._check_product_tracking()
        for repair in self:
            vals = {'state': 'done'}
            vals['move_id'] = repair.action_repair_done().get(repair.id)
            repair.write(vals)
        return True

    def action_repair_done(self):
        """ Creates stock move for operation and stock move for final product of repair order.
        @return: Move ids of final products

        """
        self._check_company()
        self.operation_move_ids._check_company()
        res = {}
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        Move = self.env['stock.move']
        for repair in self:
            # Try to create move with the appropriate owner
            if repair.product_id:
                owner_id = False
                available_qty_owner = self.env['stock.quant']._get_available_quantity(repair.product_id, repair.location_id, repair.lot_id, owner_id=repair.partner_id, strict=True)
                if float_compare(available_qty_owner, repair.product_qty, precision_digits=precision) >= 0:
                    owner_id = repair.partner_id.id

            moves = self.operation_move_ids

            if repair.product_id:
                move = Move.create({
                    'name': repair.name,
                    'product_id': repair.product_id.id,
                    'product_uom': repair.product_uom.id or repair.product_id.uom_id.id,
                    'product_uom_qty': repair.product_qty,
                    'partner_id': repair.partner_id.id,
                    'location_id': repair.location_id.id,
                    'location_dest_id': repair.location_id.id,
                    'move_line_ids': [(0, 0, {'product_id': repair.product_id.id,
                                               'lot_id': repair.lot_id.id,
                                               'reserved_uom_qty': 0,  # bypass reservation here
                                               'product_uom_id': repair.product_uom.id or repair.product_id.uom_id.id,
                                               'qty_done': repair.product_qty,
                                               'package_id': False,
                                               'result_package_id': False,
                                               'owner_id': owner_id,
                                               'location_id': repair.location_id.id,
                                               'company_id': repair.company_id.id,
                                               'location_dest_id': repair.location_id.id,})],
                    'repair_id': repair.id,
                    'origin': repair.name,
                    'company_id': repair.company_id.id,
                })
                consumed_lines = moves.mapped('move_line_ids')
                produced_lines = move.move_line_ids
                moves |= move
                produced_lines.write({'consume_line_ids': [(6, 0, consumed_lines.ids)]})
                res[repair.id] = move.id
            moves._action_done()
        return res

    def action_view_sale_order(self):
        return {
                    "type": "ir.actions.act_window",
                    "res_model": "sale.order",
                    "views": [[False, "form"]],
                    "res_id": self.sale_order_id.id,
                }

    def copy(self, default=None):
        res = super().copy(default)
        vals_list =[{
            'name': operation.name,
            'repair_id': res.id,
            'repair_line_type': operation.repair_line_type,
            'location_id': operation.location_id.id,
            'location_dest_id': operation.location_dest_id.id,
            'product_id': operation.product_id.id,
            'description_picking': operation.description_picking,
            'product_uom_qty': operation.product_uom_qty,
        } for operation in self.operation_move_ids]
        res.operation_move_ids = self.env['stock.move'].create(vals_list)
        return res

    def _check_product_tracking(self):
        invalid_lines = self.operation_move_ids.filtered(lambda x: x.has_tracking != 'none' and not x.lot_ids)
        if invalid_lines:
            products = invalid_lines.product_id
            raise ValidationError(_(
                "Serial number is required for operation lines with products: %s",
                ", ".join(products.mapped('display_name')),
            ))

class RepairTags(models.Model):
    """ Tags of Repair's tasks """
    _name = "repair.tags"
    _description = "Repair Tags"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
