# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    loyalty_program_ids = fields.Many2many('loyalty.program')
