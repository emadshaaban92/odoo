# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_is_zero


class Location(models.Model):
    _name = "stock.location"
    _description = "Inventory Locations"
    _parent_name = "location_id"
    _parent_store = True
    _order = 'complete_name'
    _rec_name = 'complete_name'
    _check_company_auto = True

    @api.model
    def default_get(self, fields):
        res = super(Location, self).default_get(fields)
        if 'barcode' in fields and 'barcode' not in res and res.get('complete_name'):
            res['barcode'] = res['complete_name']
        return res

    name = fields.Char('Location Name', required=True)
    complete_name = fields.Char("Full Location Name", compute='_compute_complete_name', store=True)
    active = fields.Boolean('Active', default=True, help="By unchecking the active field, you may hide a location without deleting it.")
    usage = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory Loss'),
        ('production', 'Production'),
        ('transit', 'Transit Location')], string='Location Type',
        default='internal', index=True, required=True,
        help="* Vendor Location: Virtual location representing the source location for products coming from your vendors"
             "\n* View: Virtual location used to create a hierarchical structures for your warehouse, aggregating its child locations ; can't directly contain products"
             "\n* Internal Location: Physical locations inside your own warehouses,"
             "\n* Customer Location: Virtual location representing the destination location for products sent to your customers"
             "\n* Inventory Loss: Virtual location serving as counterpart for inventory operations used to correct stock levels (Physical inventories)"
             "\n* Production: Virtual counterpart location for production operations: this location consumes the components and produces finished products"
             "\n* Transit Location: Counterpart location that should be used in inter-company or inter-warehouses operations")
    location_id = fields.Many2one(
        'stock.location', 'Parent Location', index=True, ondelete='cascade', check_company=True,
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.")
    child_ids = fields.One2many('stock.location', 'location_id', 'Contains')
    comment = fields.Text('Additional Information')
    posx = fields.Integer('Corridor (X)', default=0, help="Optional localization details, for information purpose only")
    posy = fields.Integer('Shelves (Y)', default=0, help="Optional localization details, for information purpose only")
    posz = fields.Integer('Height (Z)', default=0, help="Optional localization details, for information purpose only")
    parent_path = fields.Char(index=True)
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        help='Let this field empty if this location is shared between companies')
    scrap_location = fields.Boolean('Is a Scrap Location?', default=False, help='Check this box to allow using this location to put scrapped/damaged goods.')
    return_location = fields.Boolean('Is a Return Location?', help='Check this box to allow using this location as a return location.')
    removal_strategy_id = fields.Many2one('product.removal', 'Removal Strategy', help="Defines the default method used for suggesting the exact location (shelf) where to take the products from, which lot etc. for this location. This method can be enforced at the product category level, and a fallback is made on the parent locations if none is set here.")
    putaway_rule_ids = fields.One2many('stock.putaway.rule', 'location_in_id', 'Putaway Rules')
    barcode = fields.Char('Barcode', copy=False)
    quant_ids = fields.One2many('stock.quant', 'location_id')
    cyclic_inventory_frequency = fields.Integer("Inventory Frequency (Days)", default=0, help=" When different than 0, inventory adjustments for products stored at this location will be created automatically at the defined frequency.")
    last_inventory_date = fields.Datetime("Last Effective Inventory", readonly=True, help="Date of the last inventory at this location.")
    next_inventory_date = fields.Date("Next Expected Inventory", compute="_compute_next_inventory_date", store=True, help="Date for next planned inventory based on cyclic schedule.")
    storage_category_id = fields.Many2one('stock.storage.category', string='Storage Category')

    _sql_constraints = [('barcode_company_uniq', 'unique (barcode,company_id)', 'The barcode for a location must be unique per company !'),
                        ('inventory_freq_nonneg', 'check(cyclic_inventory_frequency >= 0)', 'The inventory frequency (days) for a location must be non-negative')]

    @api.depends('name', 'location_id.complete_name')
    def _compute_complete_name(self):
        for location in self:
            if location.location_id and location.usage != 'view':
                location.complete_name = '%s/%s' % (location.location_id.complete_name, location.name)
            else:
                location.complete_name = location.name

    @api.depends('cyclic_inventory_frequency', 'last_inventory_date', 'usage', 'company_id')
    def _compute_next_inventory_date(self):
        for location in self:
            if location.company_id and location.usage in ['internal', 'transit'] and location.cyclic_inventory_frequency > 0:
                try:
                    if location.last_inventory_date:
                        days_until_next_inventory = location.cyclic_inventory_frequency - (fields.Date.today() - location.last_inventory_date.date()).days
                        if days_until_next_inventory <= 0:
                            location.next_inventory_date = fields.Date.today() + timedelta(days=1)
                        else:
                            location.next_inventory_date = location.last_inventory_date + timedelta(days=days_until_next_inventory)
                    else:
                        location.next_inventory_date = fields.Date.today() + timedelta(days=location.cyclic_inventory_frequency)
                except OverflowError:
                    raise UserError(_("The selected Inventory Frequency (Days) creates a date too far into the future."))
            else:
                location.next_inventory_date = False

    @api.onchange('usage')
    def _onchange_usage(self):
        if self.usage not in ('internal', 'inventory'):
            self.scrap_location = False

    def write(self, values):
        if 'company_id' in values:
            for location in self:
                if location.company_id.id != values['company_id']:
                    raise UserError(_("Changing the company of this record is forbidden at this point, you should rather archive it and create a new one."))
        if 'usage' in values and values['usage'] == 'view':
            if self.mapped('quant_ids'):
                raise UserError(_("This location's usage cannot be changed to view as it contains products."))
        if 'usage' in values or 'scrap_location' in values:
            modified_locations = self.filtered(
                lambda l: any(l[f] != values[f] if f in values else False
                              for f in {'usage', 'scrap_location'}))
            reserved_quantities = self.env['stock.move.line'].search_count([
                ('location_id', 'in', modified_locations.ids),
                ('product_qty', '>', 0),
            ])
            if reserved_quantities:
                raise UserError(_(
                    "You cannot change the location type or its use as a scrap"
                    " location as there are products reserved in this location."
                    " Please unreserve the products first."
                ))
        if 'active' in values:
            if values['active'] == False:
                for location in self:
                    warehouses = self.env['stock.warehouse'].search([('active', '=', True), '|', ('lot_stock_id', '=', location.id), ('view_location_id', '=', location.id)])
                    if warehouses:
                        raise UserError(_("You cannot archive the location %s as it is"
                        " used by your warehouse %s") % (location.display_name, warehouses[0].display_name))

            if not self.env.context.get('do_not_check_quant'):
                children_location = self.env['stock.location'].with_context(active_test=False).search([('id', 'child_of', self.ids)])
                internal_children_locations = children_location.filtered(lambda l: l.usage == 'internal')
                children_quants = self.env['stock.quant'].search(['&', '|', ('quantity', '!=', 0), ('reserved_quantity', '!=', 0), ('location_id', 'in', internal_children_locations.ids)])
                if children_quants and values['active'] == False:
                    raise UserError(_('You still have some product in locations %s') %
                        (', '.join(children_quants.mapped('location_id.name'))))
                else:
                    super(Location, children_location - self).with_context(do_not_check_quant=True).write({
                        'active': values['active'],
                    })

        return super(Location, self).write(values)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """ search full name and barcode """
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        elif operator in expression.NEGATIVE_TERM_OPERATORS:
            domain = [('barcode', operator, name), ('complete_name', operator, name)]
        else:
            domain = ['|', ('barcode', operator, name), ('complete_name', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    def _get_putaway_strategy(self, product, quantity=0, package=None):
        """Returns the location where the product has to be put, if any compliant
        putaway strategy is found. Otherwise returns self.
        The quantity should be in the default UOM of the product, it is used when
        no package is specified.
        """
        package_type = package and package.package_type_id or self.env['stock.package.type']

        # Looking for a putaway about the product.
        putaway_rules = self.putaway_rule_ids.filtered(lambda x: x.product_id == product and (package_type in x.package_type_ids or package_type == x.package_type_ids))
        for putaway_rule in putaway_rules:
            putaway_location = putaway_rule._get_putaway_location(product, quantity, package)
            if putaway_location:
                return putaway_location
        # If not product putaway found, we're looking with category so.
        categ = product.categ_id
        while categ:
            putaway_rules = self.putaway_rule_ids.filtered(lambda x: x.category_id == categ and (package_type in x.package_type_ids or package_type == x.package_type_ids))
            for putaway_rule in putaway_rules:
                putaway_location = putaway_rule._get_putaway_location(product, quantity, package)
                if putaway_location:
                    return putaway_location
            categ = categ.parent_id
        # If not product category found and if package_type, looking putaway rules with only package_type
        if package_type:
            putaway_rules = self.putaway_rule_ids.filtered(lambda x: not x.product_id and (package_type in x.package_type_ids or package_type == x.package_type_ids))
            for putaway_rule in putaway_rules:
                putaway_location = putaway_rule._get_putaway_location(product, quantity, package)
                if putaway_location:
                    return putaway_location

        return self

    @api.returns('stock.warehouse', lambda value: value.id)
    def get_warehouse(self):
        """ Returns warehouse id of warehouse that contains location """
        domain = [('view_location_id', 'parent_of', self.ids)]
        return self.env['stock.warehouse'].search(domain, limit=1)

    def should_bypass_reservation(self):
        self.ensure_one()
        return self.usage in ('supplier', 'customer', 'inventory', 'production') or self.scrap_location or (self.usage == 'transit' and not self.company_id)

    def _check_can_be_used(self, product, quantity=0, package=None):
        """Check if product/package can be stored in the location. Quantity
        should in the default uom of product, it's only used when no package is
        specified."""
        self.ensure_one()
        if package and package.package_type_id:
            return self._check_package_storage(product, package=package)
        return self._check_product_storage(product, quantity=quantity)

    def _check_product_storage(self, product, quantity):
        """Check if a number of product can be stored in the location. Quantity
        should in the default uom of product."""
        self.ensure_one()
        if self.storage_category_id:
            # check weight
            if self.storage_category_id.max_weight < product.weight:
                return False
            # check if only allow new product when empty
            if self.storage_category_id.allow_new_product == "empty" and any(not float_is_zero(q.quantity, precision_rounding=q.product_id.uom_id.rounding) for q in self.quant_ids):
                return False
            # check if only allow same product
            if self.storage_category_id.allow_new_product == "same" and self.quant_ids and self.quant_ids.product_id != product:
                return False
            # check if enough space
            product_capacity = self.storage_category_id.product_capacity_ids.filtered(lambda pc: pc.product_id == product)
            if product_capacity:
                product_qty = sum(self.quant_ids.filtered(lambda q: q.product_id == product).mapped('quantity'))
                reserved_qty = sum(self.env['stock.move.line'].search([
                    ('product_id', '=', product.id),
                    ('location_dest_id', '=', self.id),
                    ('state', 'not in', ['draft', 'done', 'cancel'])
                ]).mapped('product_qty'))
                if product_qty + reserved_qty + quantity > product_capacity.quantity:
                    return False
        return True

    def _check_package_storage(self, product, package):
        """Check if the given package can be stored in the location."""
        self.ensure_one()
        if self.storage_category_id:
            # check weight
            if self.storage_category_id.max_weight < package.package_type_id.max_weight:
                return False
            # check if only allow new product when empty
            if self.storage_category_id.allow_new_product == "empty" and any(not float_is_zero(q.quantity, precision_rounding=q.product_id.uom_id.rounding) for q in self.quant_ids):
                return False
            # check if only allow same product
            if self.storage_category_id.allow_new_product == "same" and self.quant_ids and self.quant_ids.product_id != product:
                return False
            # check if enough space
            package_capacity = self.storage_category_id.package_capacity_ids.filtered(lambda pc: pc.package_type_id == package.package_type_id)
            if package_capacity:
                package_number = len(self.quant_ids.package_id.filtered(lambda q: q.package_type_id == package.package_type_id))
                if package_number >= package_capacity.quantity:
                    return False
        return True


class Route(models.Model):
    _name = 'stock.location.route'
    _description = "Inventory Routes"
    _order = 'sequence'
    _check_company_auto = True

    name = fields.Char('Route', required=True, translate=True)
    active = fields.Boolean('Active', default=True, help="If the active field is set to False, it will allow you to hide the route without removing it.")
    sequence = fields.Integer('Sequence', default=0)
    rule_ids = fields.One2many('stock.rule', 'route_id', 'Rules', copy=True)
    product_selectable = fields.Boolean('Applicable on Product', default=True, help="When checked, the route will be selectable in the Inventory tab of the Product form.")
    product_categ_selectable = fields.Boolean('Applicable on Product Category', help="When checked, the route will be selectable on the Product Category.")
    warehouse_selectable = fields.Boolean('Applicable on Warehouse', help="When a warehouse is selected for this route, this route should be seen as the default route when products pass through this warehouse.")
    supplied_wh_id = fields.Many2one('stock.warehouse', 'Supplied Warehouse')
    supplier_wh_id = fields.Many2one('stock.warehouse', 'Supplying Warehouse')
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        help='Leave this field empty if this route is shared between all companies')
    product_ids = fields.Many2many(
        'product.template', 'stock_route_product', 'route_id', 'product_id',
        'Products', copy=False, check_company=True)
    categ_ids = fields.Many2many('product.category', 'stock_location_route_categ', 'route_id', 'categ_id', 'Product Categories', copy=False)
    warehouse_domain_ids = fields.One2many('stock.warehouse', compute='_compute_warehouses')
    warehouse_ids = fields.Many2many(
        'stock.warehouse', 'stock_route_warehouse', 'route_id', 'warehouse_id',
        'Warehouses', copy=False, domain="[('id', 'in', warehouse_domain_ids)]")

    @api.depends('company_id')
    def _compute_warehouses(self):
        for loc in self:
            domain = [('company_id', '=', loc.company_id.id)] if loc.company_id else []
            loc.warehouse_domain_ids = self.env['stock.warehouse'].search(domain)

    @api.onchange('company_id')
    def _onchange_company(self):
        if self.company_id:
            self.warehouse_ids = self.warehouse_ids.filtered(lambda w: w.company_id == self.company_id)

    @api.onchange('warehouse_selectable')
    def _onchange_warehouse_selectable(self):
        if not self.warehouse_selectable:
            self.warehouse_ids = [(5, 0, 0)]

    def toggle_active(self):
        for route in self:
            route.with_context(active_test=False).rule_ids.filtered(lambda ru: ru.active == route.active).toggle_active()
        super(Route, self).toggle_active()
