# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    salesperson_id = fields.Many2one('res.users', related='website_id.salesperson_id', string='Salesperson', inverse=True, domain="[('share', '=', False)]")
    salesteam_id = fields.Many2one('crm.team', related='website_id.salesteam_id', string='Sales Team', inverse=True)
    module_website_sale_delivery = fields.Boolean("eCommerce Shipping Costs")
    # field used to have a nice radio in form view, resuming the 2 fields above
    sale_delivery_settings = fields.Selection([
        ('none', 'No shipping management on website'),
        ('internal', "Delivery methods are only used internally: the customer doesn't pay for shipping costs"),
        ('website', "Delivery methods are selectable on the website: the customer pays for shipping costs"),
    ], string="Shipping Management")

    group_delivery_invoice_address = fields.Boolean(string="Shipping Address", implied_group='account.group_delivery_invoice_address', group='base.group_portal,base.group_user,base.group_public')
    group_show_uom_price = fields.Boolean(default=False, string="Base Unit Price", implied_group="website_sale.group_show_uom_price", group='base.group_portal,base.group_user,base.group_public')
    group_product_price_comparison = fields.Boolean(
        string="Comparison Price",
        implied_group="website_sale.group_product_price_comparison",
        group='base.group_portal,base.group_user,base.group_public')

    module_website_sale_digital = fields.Boolean("Digital Content")
    module_website_sale_wishlist = fields.Boolean("Wishlists")
    module_website_sale_comparison = fields.Boolean("Product Comparison Tool")
    module_website_sale_autocomplete = fields.Boolean('Address Autocomplete')

    module_account = fields.Boolean("Invoicing")
    module_website_sale_picking = fields.Boolean('On Site Payments & Picking')

    cart_recovery_mail_template = fields.Many2one('mail.template', string='Cart Recovery Email', domain="[('model', '=', 'sale.order')]",
                                                  related='website_id.cart_recovery_mail_template_id', inverse=True)
    cart_abandoned_delay = fields.Float("Abandoned Delay", help="Number of hours after which the cart is considered abandoned.",
                                        related='website_id.cart_abandoned_delay', inverse=True)
    add_to_cart_action = fields.Selection(related='website_id.add_to_cart_action', inverse=True)
    terms_url = fields.Char(compute='_compute_terms_url', string="URL", help="A preview will be available at this URL.")

    module_delivery = fields.Boolean(
        compute='_compute_module_delivery', store=True, readonly=False)
    module_website_sale_delivery = fields.Boolean(
        compute='_compute_module_delivery', store=True, readonly=False)
    group_product_pricelist = fields.Boolean(
        compute='_compute_group_product_pricelist', store=True, readonly=False)

    enabled_extra_checkout_step = fields.Boolean(string="Extra Step During Checkout")
    enabled_buy_now_button = fields.Boolean(string="Buy Now")

    account_on_checkout = fields.Selection(
        string="Customer Accounts",
        selection=[
            ("optional", "Optional"),
            ("disabled", "Disabled (buy as guest)"),
            ("mandatory", "Mandatory (no guest checkout)"),
        ],
        compute="_compute_account_on_checkout",
        inverse="_inverse_account_on_checkout",
        readonly=False, required=True)

    @api.depends('website_id')
    def _compute_terms_url(self):
        for record in self:
            record.terms_url = '%s/terms' % record.website_id.get_base_url()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        sale_delivery_settings = 'none'
        if self.env['ir.module.module'].search([('name', '=', 'delivery')], limit=1).state in ('installed', 'to install', 'to upgrade'):
            sale_delivery_settings = 'internal'
            if self.env['ir.module.module'].search([('name', '=', 'website_sale_delivery')], limit=1).state in ('installed', 'to install', 'to upgrade'):
                sale_delivery_settings = 'website'

        res.update(
            sale_delivery_settings=sale_delivery_settings,
            enabled_extra_checkout_step=self.env.ref('website_sale.extra_info_option').active,
            enabled_buy_now_button=self.env.ref('website_sale.product_buy_now').active,
        )
        return res

    def set_values(self):
        super().set_values()
        extra_step_view = self.env.ref('website_sale.extra_info_option')
        if extra_step_view.active != self.enabled_extra_checkout_step:
            extra_step_view.active = self.enabled_extra_checkout_step
        buy_now_view = self.env.ref('website_sale.product_buy_now')
        if buy_now_view.active != self.enabled_buy_now_button:
            buy_now_view.active = self.enabled_buy_now_button

    @api.depends('sale_delivery_settings')
    def _compute_module_delivery(self):
        for wizard in self:
            wizard.module_delivery = wizard.sale_delivery_settings in ['internal', 'website']
            wizard.module_website_sale_delivery = wizard.sale_delivery_settings == 'website'

    @api.depends('group_discount_per_so_line')
    def _compute_group_product_pricelist(self):
        self.filtered(lambda w: w.group_discount_per_so_line).update({
            'group_product_pricelist': True,
        })

    @api.depends('website_id.account_on_checkout')
    def _compute_account_on_checkout(self):
        for record in self:
            record.account_on_checkout = record.website_id.account_on_checkout or 'disabled'

    def _inverse_account_on_checkout(self):
        for record in self:
            if not record.website_id:
                continue
            record.website_id.account_on_checkout = record.account_on_checkout
            # account_on_checkout implies different values for `auth_signup_uninvited`
            if record.account_on_checkout in ['optional', 'mandatory']:
                record.website_id.auth_signup_uninvited = 'b2c'
            else:
                record.website_id.auth_signup_uninvited = 'b2b'

    def action_update_terms(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.env["website"].get_client_action_url('/terms', True),
            'target': 'self',
        }

    def action_open_extra_info(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.env["website"].get_client_action_url('/shop/extra_info', True),
            'target': 'self',
        }

    def action_open_sale_mail_templates(self):
        return {
            'name': _('Customize Email Templates'),
            'type': 'ir.actions.act_window',
            'domain': [('model', '=', 'sale.order')],
            'res_model': 'mail.template',
            'view_id': False,
            'view_mode': 'tree,form',
        }
