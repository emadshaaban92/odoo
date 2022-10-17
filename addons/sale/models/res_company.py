# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    _sql_constraints = [
        ('check_quotation_validity_days',
            'CHECK(quotation_validity_days > 0)',
            "Quotation Validity is required and must be greater than 0."),
    ]

    portal_confirmation_sign = fields.Boolean(string="Online Signature", default=True)
    portal_confirmation_pay = fields.Boolean(string="Online Payment")
    quotation_validity_days = fields.Integer(string="Default Quotation Validity (Days)", default=30)

    # sale onboarding
    sale_onboarding_payment_method = fields.Selection(
        selection=[
            ('digital_signature', "Sign online"),
            ('paypal', "PayPal"),
            ('stripe', "Stripe"),
            ('other', "Pay with another payment provider"),
            ('manual', "Manual Payment"),
        ],
        string="Sale onboarding selected payment method")
