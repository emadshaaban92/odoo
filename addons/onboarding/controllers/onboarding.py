# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class OnboardingController(http.Controller):
    @http.route('/onboarding/<string:route_name>', auth='user', type='json')
    def get_onboarding_data(self, route_name=None):
        if not request.env.user.has_group('base.group_system'):
            return {}

        onboarding = request.env['onboarding.onboarding'].search([('route_name', '=', route_name)])
        if onboarding and not self._safe_search_or_create_progress(onboarding).is_onboarding_closed:
            # JS implementation of the onboarding panel expects this data structure
            return {
                'html': request.env['ir.qweb']._render(
                    'onboarding.onboarding_panel', onboarding._prepare_rendering_values())
            }

        return {}

    @staticmethod
    def _safe_search_or_create_progress(onboarding):
        try:
            current_progress = onboarding._search_or_create_progress()
        except ValidationError as e:
            # If initially not found but was created by another process before we tried to create
            current_progress = onboarding.current_progress_id
            if not current_progress:  # If other cause of ValidationError
                raise e
        return current_progress
