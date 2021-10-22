# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    def _get_account_journal(self, template_code):
        return {
            **(super()._get_account_journal(template_code)),
            'inventory_valuation': {
                'name': _('Inventory Valuation'),
                'code': 'STJ',
                'type': 'general',
                'sequence': 8,
                'show_on_dashboard': False,
            },
        }

    def _get_template_data(self, template_code):
        return {
            **super()._get_template_data(template_code),
            'property_stock_journal': 'inventory_valuation',
        }
