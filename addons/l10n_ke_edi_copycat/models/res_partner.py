# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_ke_exemption_number = fields.Char("Exemption Number")
