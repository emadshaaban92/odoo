# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_website_order_line(self):
        """ This method will merge multiple discount lines generated by a same program
            into a single one (temporary line with `new()`).
            This case will only occur when the program is a discount applied on multiple
            products with different taxes.
            In this case, each taxes will have their own discount line. This is required
            to have correct amount of taxes according to the discount.
            But we wan't these lines to be `visually` merged into a single one in the
            e-commerce since the end user should only see one discount line.
            This is only possible since we don't show taxes in cart.
            eg:
                line 1: 10% discount on product with tax `A` - $15
                line 2: 10% discount on product with tax `B` - $11.5
                line 3: 10% discount on product with tax `C` - $10
            would be `hidden` and `replaced` by
                line 1: 10% discount - $36.5

            Note: The line will be created without tax(es) and the amount will be computed
                  depending if B2B or B2C is enabled.
        """
        super()._compute_website_order_line()
        for order in self:
            # TODO: potential performance bottleneck downstream
            programs = order._get_applied_programs_with_rewards_on_current_order()
            for program in programs:
                program_lines = order.order_line.filtered(lambda line:
                    line.product_id == program.discount_line_product_id)
                if len(program_lines) > 1:
                    if self.env.user.has_group('sale.group_show_price_subtotal'):
                        price_unit = sum(program_lines.mapped('price_subtotal'))
                    else:
                        price_unit = sum(program_lines.mapped('price_total'))
                    # TODO: batch then flush
                    order.website_order_line += self.env['sale.order.line'].new({
                        'product_id': program_lines[0].product_id.id,
                        'price_unit': price_unit,
                        'name': program_lines[0].name,
                        'product_uom_qty': 1,
                        'product_uom': program_lines[0].product_uom.id,
                        'order_id': order.id,
                        'is_reward_line': True,
                    })
                    order.website_order_line -= program_lines

    def _compute_cart_info(self):
        super(SaleOrder, self)._compute_cart_info()
        for order in self:
            reward_lines = order.website_order_line.filtered(lambda line: line.is_reward_line)
            order.cart_quantity -= int(sum(reward_lines.mapped('product_uom_qty')))

    def get_promo_code_error(self, delete=True):
        error = request.session.get('error_promo_code')
        if error and delete:
            request.session.pop('error_promo_code')
        return error

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        self.recompute_coupon_lines()
        return res

    def _get_free_shipping_lines(self):
        self.ensure_one()
        free_shipping_prgs_ids = self._get_applied_programs_with_rewards_on_current_order().filtered(lambda p: p.reward_type == 'free_shipping')
        if not free_shipping_prgs_ids:
            return self.env['sale.order.line']
        free_shipping_product_ids = free_shipping_prgs_ids.mapped('discount_line_product_id')
        return self.order_line.filtered(lambda l: l.product_id in free_shipping_product_ids)

    @api.model
    def _garbage_collector(self, *args, **kwargs):
        """Remove/free coupon from abandonned ecommerce order."""
        ICP = self.env['ir.config_parameter']
        validity = ICP.get_param('website_sale_coupon.abandonned_coupon_validity', 4)
        validity = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=int(validity)))
        coupon_to_reset = self.env['coupon.coupon'].search([
            ('state', '=', 'used'),
            ('sales_order_id.state', '=', 'draft'),
            ('sales_order_id.write_date', '<', validity),
            ('sales_order_id.website_id', '!=', False),
        ])
        for coupon in coupon_to_reset:
            coupon.sales_order_id.applied_coupon_ids -= coupon
        coupon_to_reset.write({'state': 'new'})
        coupon_to_reset.mapped('sales_order_id').recompute_coupon_lines()
