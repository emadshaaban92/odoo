# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin = fields.Float(
        "Margin", compute='_compute_margin',
        digits='Product Price', store=True, groups="base.group_user", precompute=True)
    margin_percent = fields.Float(
        "Margin (%)", compute='_compute_margin', store=True, groups="base.group_user", precompute=True)
    purchase_price = fields.Float(
        string="Cost", compute="_compute_purchase_price",
        digits='Product Price', store=True, precompute=True,
        groups="base.group_user")

    @api.depends('product_id', 'company_id', 'currency_id', 'uom_id')
    def _compute_purchase_price(self):
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product_cost = line.product_id.standard_price
            line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)

    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            line.margin = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
            line.margin_percent = line.price_subtotal and line.margin/line.price_subtotal

    def _convert_price(self, product_cost, from_uom):
        self.ensure_one()
        if not product_cost:
            # If the standard_price is 0
            # Avoid unnecessary computations
            # and currency conversions
            if not self.purchase_price:
                return product_cost
        from_currency = self.product_id.cost_currency_id
        to_cur = self.currency_id or self.order_id.currency_id
        to_uom = self.uom_id
        if to_uom and to_uom != from_uom:
            product_cost = from_uom._compute_price(
                product_cost,
                to_uom,
            )
        return from_currency._convert(
            from_amount=product_cost,
            to_currency=to_cur,
            company=self.company_id or self.env.company,
            date=self.order_id.date_order or fields.Date.today(),
            round=False,
        ) if to_cur and product_cost else product_cost
        # The pricelist may not have been set, therefore no conversion
        # is needed because we don't know the target currency..
