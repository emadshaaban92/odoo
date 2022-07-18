# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from unittest.mock import Mock

from odoo.tests.common import TransactionCase


class TestMenuRootLookupByModel(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Menu = cls.env['ir.ui.menu']
        Action = cls.env['ir.actions.act_window']

        def _new_menu(name, parent_id=None, action=None):
            inst = Menu.create({'name': name, 'parent_id': parent_id})
            if action:
                inst.action = action
            return inst

        new_menu = Mock(side_effect=_new_menu)

        def new_action(name, res_model, view_mode=None, domain=None, context=None):
            return Action.create({
                'name': name,
                'res_model': res_model,
                'view_mode': view_mode,
                'domain': domain,
                'context': context or {},
                'type': 'ir.actions.act_window',
            })

        # Remove all menus and setup test menu with known results
        Menu.search([]).unlink()

        menu_root_invoicing = new_menu('Invoicing')
        menu_invoicing_customer = new_menu('Customers', parent_id=menu_root_invoicing.id)
        new_menu('Customers', parent_id=menu_invoicing_customer.id,
                 action=new_action('Customers', res_model='res.partner', view_mode='kanban,tree,form',
                                   context="""{
                                               'search_default_customer': 1,
                                               'res_partner_search_mode': 'customer', 
                                               'default_is_company': True, 
                                               'default_customer_rank': 1
                                           }"""))
        menu_root_contact = new_menu('Contacts')
        new_menu('Contacts', parent_id=menu_root_contact.id,
                 action=new_action('Contacts', res_model='res.partner', view_mode='kanban,tree,form,activity',
                                   context="{'default_is_company': " + (' ' * 1000) + "True" + ('\n' * 1000) + "}",
                                   domain='[]'))
        menu_root_sales = new_menu('Sales')
        menu_sales_orders = new_menu('Orders', parent_id=menu_root_sales.id)
        new_menu('Customers', parent_id=menu_sales_orders.id,
                 action=new_action('Customers', res_model='res.partner', view_mode='kanban,tree,form',
                                   context="""{
                                                    'search_default_customer': 1,
                                                    'res_partner_search_mode': 'customer', 
                                                    'default_is_company': True, 
                                                    'default_customer_rank': 1
                                                }"""))
        menu_root_settings = new_menu('Settings')
        menu_settings_user_and_companies = new_menu('Users & Companies', parent_id=menu_root_settings.id)
        new_menu('Companies', parent_id=menu_settings_user_and_companies.id,
                 action=new_action('Companies', res_model='res.company', view_mode='tree,kanban,form'))

        cls.menu_count = new_menu.call_count
        cls.menu_root_contact = menu_root_contact
        cls.menu_root_settings = menu_root_settings
        cls.Menu = Menu

    def test_menu_setup(self):
        self.assertEqual(len(self.Menu._visible_menu_ids()), self.menu_count)

    def test_look_for_existing_menu_root(self):
        self.env['ir.ui.menu']._visible_menu_ids()
        self.env.invalidate_all()
        with self.assertQueryCount(__system__=3):
            self.assertEqual(self.Menu._get_best_menu_root_for_model('res.partner'), self.menu_root_contact.id)
        self.env['ir.ui.menu']._visible_menu_ids()
        self.env.invalidate_all()
        with self.assertQueryCount(__system__=3):
            self.assertEqual(self.Menu._get_best_menu_root_for_model('res.company'), self.menu_root_settings.id)

    def test_look_for_non_existing_menu_root(self):
        self.env['ir.ui.menu']._visible_menu_ids()
        self.env.invalidate_all()
        with self.assertQueryCount(__system__=3):
            self.assertEqual(self.Menu._get_best_menu_root_for_model('res.bank'), None)

    @classmethod
    def tearDownClass(cls):
        cls.registry.reset_changes()
        super().tearDownClass()
