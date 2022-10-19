# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PortalRatingMixin(models.AbstractModel):
    """Technical mixin that unite portal and rating mixin to solve inheritance problem."""
    _name = 'portal.rating.mixin'
    _description = "Portal and Rating Mixin"
    _inherit = ['portal.mixin', 'rating.mixin']
