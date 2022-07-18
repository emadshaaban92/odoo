# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math
import re

from odoo import api, models

MODEL_TO_MENU_ACTION_VIEW_MODE_PREFERRED = re.compile(r"kanban|tree|form")


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _get_best_menu_root_for_model(self, res_model):
        """Get the best menu root id for the given res_model and the access rights of the user.

        When a link to a model was sent to a user it was targeting a page without menu, so it was hard for the user to
        act on it. The goal of this method is to find the best suited menu to display on a page of a given model.

        Technically, the method tries to find a menu root which has a sub menu visible to the user that has an action
        linked to the given model. If there are more than one possibility, it uses a simple heuristic to returns the
        best one.

        :param str res_model: the model name for which we want to find the best menu root
        :return (int): the best menu root id or None if not found
        """
        self_sudo = self.sudo()

        # Prefetch menu fields and all menu's actions of type act_window
        menus = self_sudo.env['ir.ui.menu'].browse(self_sudo._visible_menu_ids())
        self_sudo.env['ir.actions.act_window'].browse([
            int(menu['action'].split(',')[1])
            for menu in menus.read(['action', 'parent_path'])
            if menu['action'] and menu['action'].startswith('ir.actions.act_window,')
        ]).filtered('res_model')

        # Heuristic to find the best menu
        max_preference = -math.inf
        menu_root_id = None
        for menu in menus:
            action = menu.action
            if not action or action.type != 'ir.actions.act_window' or action.res_model != res_model:
                continue
            preference = 0 if re.match(MODEL_TO_MENU_ACTION_VIEW_MODE_PREFERRED, action.view_mode) else -5
            # number of : in context =~ number of variable in the context (dictionary)
            preference -= action.context.count(':') if action.context else 0
            # number of , (+1) /3 in domain =~ number of condition
            preference -= (action.domain.count(',') + 1) // 3 if action.domain else 0
            if preference > max_preference:
                menu_root_id = int(menu.parent_path[:menu.parent_path.index('/')])
                max_preference = preference

        return menu_root_id
