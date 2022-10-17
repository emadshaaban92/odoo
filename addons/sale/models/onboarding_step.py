# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import _, api, Command, models
from odoo.modules.module import get_module_resource


class OnboardingStep(models.Model):
    _inherit = 'onboarding.onboarding.step'

    @api.model
    def action_save_sale_quotation_onboarding_layout_step(self):
        return self.action_safe_set_just_done('sale.sale_quotation_onboarding_layout_step')

    @api.model
    def action_open_sale_onboarding_payment_provider(self):
        self.env.company.get_chart_of_accounts_or_fail()
        return self.env['ir.actions.actions']._for_xml_id('sale.action_open_sale_payment_provider_onboarding_wizard')

    @api.model
    def action_save_sale_quotation_order_confirmation_step(self):
        return self.action_safe_set_just_done('sale.sale_quotation_onboarding_order_confirmation_step')

    @api.model
    def _get_sample_sales_order(self):
        """ Get a sample quotation or create one if it does not exist. """
        # use current user as partner
        partner = self.env.user.partner_id
        company_id = self.env.company.id
        # is there already one?
        sample_sales_order = self.env['sale.order'].search([
            ('company_id', '=', company_id),
            ('partner_id', '=', partner.id),
            ('state', '=', 'draft'),
        ], limit=1)
        if not sample_sales_order:
            # take any existing product or create one
            product = self.env['product.product'].search([], limit=1)
            if not product:
                default_image_path = get_module_resource('product', 'static/img', 'product_product_13-image.jpg')
                product = self.env['product.product'].create({
                    'name': _('Sample Product'),
                    'active': False,
                    'image_1920': base64.b64encode(open(default_image_path, 'rb').read())
                })
                product.product_tmpl_id.write({'active': False})
            sample_sales_order = self.env['sale.order'].create({
                'partner_id': partner.id,
                'order_line': [
                    Command.create({
                        'name': _('Sample Order Line'),
                        'product_id': product.id,
                        'product_uom_qty': 10,
                        'price_unit': 123,
                    })
                ]
            })
        return sample_sales_order

    @api.model
    def action_open_sale_onboarding_sample_quotation(self):
        """ Onboarding step for sending a sample quotation. Open a window to compose an email,
            with the edi_invoice_template message loaded by default. """
        sample_sales_order = self._get_sample_sales_order()
        template = self.env.ref('sale.email_template_edi_sale', False)

        message_composer = self.env['mail.compose.message'].with_context(
            default_use_template=bool(template),
            mark_so_as_sent=True,
            default_email_layout_xmlid='mail.mail_notification_layout_with_responsible_signature',
            proforma=self.env.context.get('proforma', False),
            force_email=True,
        ).create({
            'res_id': sample_sales_order.id,
            'template_id': template and template.id or False,
            'model': 'sale.order',
            'composition_mode': 'comment'})

        # Simulate the onchange (like trigger in form the view)
        update_values = message_composer._onchange_template_id(template.id, 'comment', 'sale.order', sample_sales_order.id)['value']
        message_composer.write(update_values)

        message_composer._action_send_mail()

        self.action_safe_set_just_done('sale.sale_quotation_onboarding_sample_quotation_step')

        action = self.env['ir.actions.actions']._for_xml_id('sale.action_orders')
        action.update({
            'views': [[self.env.ref('sale.view_order_form').id, 'form']],
            'view_mode': 'form',
            'target': 'main',
        })
        return action

    @api.model
    def action_save_sale_quotation_payment_onboarding_step(self):
        """ Override of payment to mark the sale onboarding step as done.

        The payment onboarding step of Sales is only marked as done if it was started from Sales.
        This prevents incorrectly marking the step as done if another module's payment onboarding
        step was marked as done.

        :return: None
        """
        self.action_save_payment_onboarding_payment_provider_step()
        if self.env.company.sale_onboarding_payment_method:  # The onboarding step was started from Sales
            return self.action_safe_set_just_done('sale.sale_quotation_onboarding_order_confirmation_step')
