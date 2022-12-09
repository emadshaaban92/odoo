# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = 'product.pricelist'

    valid_loyalty_program_ids = fields.Many2one('loyalty.program')
    loyalty_program_ids = fields.Many2many('loyalty.program')
