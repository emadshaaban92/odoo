from odoo import fields, models
from odoo.tools import float_compare

class StockWarnUnwantedReplenish(models.TransientModel):
    _name = 'stock.warn.unwanted.replenish'
    _description = 'Warn unwanted replenish'

    stock_orderpoint_ids = fields.Many2many('stock.warehouse.orderpoint', string='Stock Orderpoints')

    def action_validate_all(self):
        self = self.with_context(force_unwanted_replenish=True)
        self.stock_orderpoint_ids.action_replenish()

    def action_validate_correct(self):
        valid_orderpoints = self.stock_orderpoint_ids.filtered(lambda orderpoint: not(orderpoint.unwanted_replenish))
        valid_orderpoints.action_replenish()

    def action_validate_recompute(self):
        orderpoints_to_recompute = self.stock_orderpoint_ids.filtered(lambda orderpoint: orderpoint.unwanted_replenish)
        for orderpoint in orderpoints_to_recompute:
            new_qty_to_order = orderpoint.product_max_qty - orderpoint.product_id.virtual_available
            orderpoint.qty_to_order = new_qty_to_order if float_compare(new_qty_to_order, 0.0, precision_rounding=orderpoint.product_uom.rounding) > 0 else 0
        self.action_validate_all()
