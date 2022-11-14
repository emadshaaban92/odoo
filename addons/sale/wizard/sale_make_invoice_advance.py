# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import float_is_zero


class SaleAdvancePaymentInv(models.TransientModel):
    _name = 'sale.advance.payment.inv'
    _description = "Sales Advance Payment Invoice"

    advance_payment_method = fields.Selection(
        selection=[
            ('delivered', "Regular invoice"),
            ('percentage', "Down payment (percentage)"),
            ('fixed', "Down payment (fixed amount)"),
        ],
        string="Create Invoice",
        default='delivered',
        required=True,
        help="A standard invoice is issued with all the order lines ready for invoicing,"
            "according to their invoicing policy (based on ordered or delivered quantity).")
    count = fields.Integer(string="Order Count", compute='_compute_count')
    sale_order_ids = fields.Many2many(
        'sale.order', default=lambda self: self.env.context.get('active_ids'))

    # Down Payment logic
    has_down_payments = fields.Boolean(
        string="Has down payments", compute="_compute_has_down_payments")
    deduct_down_payments = fields.Boolean(string="Deduct down payments", default=True)

    # New Down Payment
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Down Payment Product",
        domain=[('type', '=', 'service')],
        compute='_compute_product_id',
        readonly=False,
        store=True)
    amount = fields.Float(
        string="Down Payment Amount",
        help="The percentage of amount to be invoiced in advance.")
    fixed_amount = fields.Monetary(
        string="Down Payment Amount (Fixed)",
        help="The fixed amount to be invoiced in advance.")
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        compute='_compute_company_id',
        store=True)

    # Only used when there is no down payment product available
    #  to setup the down payment product
    deposit_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Income Account",
        domain=[('deprecated', '=', False)],
        help="Account used for deposits")
    deposit_taxes_id = fields.Many2many(
        comodel_name='account.tax',
        string="Customer Taxes",
        domain=[('type_tax_use', '=', 'sale')],
        help="Taxes used for deposits")

    #=== COMPUTE METHODS ===#

    @api.depends('sale_order_ids')
    def _compute_count(self):
        for wizard in self:
            wizard.count = len(wizard.sale_order_ids)

    @api.depends('sale_order_ids')
    def _compute_has_down_payments(self):
        for wizard in self:
            wizard.has_down_payments = bool(
                wizard.sale_order_ids.order_line.filtered('is_downpayment')
            )

    # next computed fields are only used for down payments invoices and therefore should only
    # have a value when 1 unique SO is invoiced through the wizard
    @api.depends('sale_order_ids')
    def _compute_currency_id(self):
        self.currency_id = False
        for wizard in self:
            if wizard.count == 1:
                wizard.currency_id = wizard.sale_order_ids.currency_id

    @api.depends('sale_order_ids')
    def _compute_company_id(self):
        self.company_id = False
        for wizard in self:
            if wizard.count == 1:
                wizard.company_id = wizard.sale_order_ids.company_id

    @api.depends('company_id')  # 'dumb' depends to trigger the computation
    def _compute_product_id(self):
        self.product_id = False
        dp_product_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'sale.default_deposit_product_id'))
        if not dp_product_id:
            return
        for wizard in self:
            if wizard.count == 1:
                wizard.product_id = dp_product_id

    #=== ONCHANGE METHODS ===#

    @api.onchange('advance_payment_method')
    def _onchange_advance_payment_method(self):
        if self.advance_payment_method == 'percentage':
            amount = self.default_get(['amount']).get('amount')
            return {'value': {'amount': amount}}

    #=== CONSTRAINT METHODS ===#

    @api.constrains('advance_payment_method', 'amount', 'fixed_amount')
    def _check_amount_is_positive(self):
        for wizard in self:
            if wizard.advance_payment_method == 'percentage' and wizard.amount <= 0.00:
                raise UserError(_('The value of the down payment amount must be positive.'))
            elif wizard.advance_payment_method == 'fixed' and wizard.fixed_amount <= 0.00:
                raise UserError(_('The value of the down payment amount must be positive.'))

    @api.constrains('product_id')
    def _check_down_payment_product_is_valid(self):
        for wizard in self:
            if wizard.count > 1 or not wizard.product_id:
                continue
            if wizard.product_id.invoice_policy != 'order':
                raise UserError(_(
                    "The product used to invoice a down payment should have an invoice policy"
                    "set to \"Ordered quantities\"."
                    " Please update your deposit product to be able to create a deposit invoice."))
            if wizard.product_id.type != 'service':
                raise UserError(_(
                    "The product used to invoice a down payment should be of type 'Service'."
                    " Please use another product or update this product."))

    #=== ACTION METHODS ===#

    def create_invoices(self):
        invoices = self._create_invoices(self.sale_order_ids)
        if self.env.context.get('open_invoices'):
            return self.sale_order_ids.action_view_invoice(invoices=invoices)

        return {'type': 'ir.actions.act_window_close'}

    #=== BUSINESS METHODS ===#

    def _create_invoices(self, sale_orders):
        self.ensure_one()
        if self.advance_payment_method == 'delivered':
            return sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            self.sale_order_ids.ensure_one()
            self = self.with_company(self.company_id)
            order = self.sale_order_ids

            # Create deposit product if necessary
            if not self.product_id:
                self.product_id = self.env['product.product'].create(
                    self._prepare_down_payment_product_values()
                )
                self.env['ir.config_parameter'].sudo().set_param(
                    'sale.default_deposit_product_id', self.product_id.id)

            # Create down payment section if necessary
            if not any(line.display_type and line.is_downpayment for line in order.order_line):
                self.env['sale.order.line'].create(
                    self._prepare_down_payment_section_values(order)
                )

            down_payment_lines = self.env['sale.order.line'].create(
                self._prepare_down_payment_lines_values(order)
            )

            invoice = self.env['account.move'].sudo().create(
                self._prepare_invoice_values(order, down_payment_lines)
            ).with_user(self.env.uid)  # Unsudo the invoice after creation

            invoice.message_post_with_view(
                'mail.message_origin_link',
                values={'self': invoice, 'origin': order},
                subtype_id=self.env.ref('mail.mt_note').id)

            return invoice

    def _prepare_down_payment_product_values(self):
        self.ensure_one()
        return {
            'name': _('Down payment'),
            'type': 'service',
            'invoice_policy': 'order',
            'company_id': False,
            'property_account_income_id': self.deposit_account_id.id,
            'taxes_id': [Command.set(self.deposit_taxes_id.ids)],
        }

    def _prepare_down_payment_section_values(self, order):
        context = {'lang': order.partner_id.lang}

        so_values = {
            'name': _('Down Payments'),
            'product_uom_qty': 0.0,
            'order_id': order.id,
            'display_type': 'line_section',
            'is_downpayment': True,
            'sequence': order.order_line and order.order_line[-1].sequence + 1 or 10,
        }

        del context
        return so_values

    def _prepare_down_payment_lines_values(self, order):
        """ Create one down payment line per tax or unique taxes combination.
            Apply the tax(es) to their respective lines.

            :param order: Order for which the down payment lines are created.
            :return:      An array of dicts with the down payment lines values.
        """
        self.ensure_one()
        down_payment_amount = self._get_down_payment_amount(order)
        if self.advance_payment_method == 'percentage':
            down_payment_ratio = self.amount / 100
        else:
            down_payment_ratio = down_payment_amount / order.amount_total

        group_by_taxes = defaultdict(lambda: {
            'lines': self.env['sale.order.line'],
            'sum_price_subtotal': 0.0,
        })

        order_lines = order.order_line.filtered(lambda l: not l.display_type)

        if any(tax.amount_type == 'fixed' for tax in order_lines.tax_id.flatten_taxes_hierarchy()):
            # no breakdown per taxes if any tax with amount type "fixed"
            group_by_taxes[None]['lines'] = order_lines
            group_by_taxes[None]['sum_price_subtotal'] = down_payment_amount
        else:
            # get total base amount by tax(es) group
            tax_base_line_dicts = [line._convert_to_tax_base_line_dict() for line in order_lines]
            computed_taxes = self.env['account.tax']._compute_taxes(
                tax_base_line_dicts,
                handle_price_include=False
            )
            for base_line in computed_taxes['base_lines_to_update']:
                tax_ids = tuple(sorted(base_line[0]['taxes'].ids))
                group_by_taxes[tax_ids]['lines'] += base_line[0]['record']
                group_by_taxes[tax_ids]['sum_price_subtotal'] += base_line[1]['price_subtotal'] * down_payment_ratio

        line_values = []

        base_line_values = self._prepare_base_downpayment_line_values(order)
        for tax_ids, values in group_by_taxes.items():
            analytic_distribution = {}
            amount_total = sum(values['lines'].mapped("price_total"))
            if not float_is_zero(amount_total, precision_rounding=self.currency_id.rounding):
                for line in values['lines']:
                    distrib_dict = line.analytic_distribution or {}
                    for account, distribution in distrib_dict.items():
                        analytic_distribution[account] = distribution * line.price_total + analytic_distribution.get(account, 0)
                for account, distribution_amount in analytic_distribution.items():
                    analytic_distribution[account] = distribution_amount / amount_total

            line_values.append({
                **base_line_values,
                'tax_id': [Command.set(tax_ids)] if tax_ids else [],
                'price_unit': values['sum_price_subtotal'],
                'analytic_distribution': analytic_distribution,
            })
        return line_values

    def _prepare_base_downpayment_line_values(self, order):
        self.ensure_one()
        context = {'lang': order.partner_id.lang}
        values = {
            'name': _('Down Payment: %s (Draft)', time.strftime('%m %Y')),
            'product_uom_qty': 0.0,
            'order_id': order.id,
            'discount': 0.0,
            'product_id': self.product_id.id,
            'is_downpayment': True,
            'sequence': order.order_line and order.order_line[-1].sequence + 1 or 10,
        }
        del context
        return values

    def _get_down_payment_amount(self, order):
        self.ensure_one()
        if self.advance_payment_method == 'percentage':
            amount = order.amount_total * self.amount / 100
        else:  # Fixed amount
            amount = self.fixed_amount
        return amount

    def _prepare_invoice_values(self, order, so_lines):
        self.ensure_one()
        return {
            **order._prepare_invoice(),
            'invoice_line_ids': [
                Command.create(
                    line._prepare_invoice_line(
                        name=self._get_down_payment_description(order),
                        quantity=1.0,
                    )
                ) for line in so_lines
            ],
        }

    def _get_down_payment_description(self, order):
        self.ensure_one()
        context = {'lang': order.partner_id.lang}
        if self.advance_payment_method == 'percentage':
            name = _("Down payment of %s%%", self.amount)
        else:
            name = _('Down Payment')
        del context

        return name
