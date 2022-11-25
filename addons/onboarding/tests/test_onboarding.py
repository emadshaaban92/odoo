# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.addons.onboarding.tests.common import TestOnboardingCommon
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger


class TestOnboarding(TestOnboardingCommon):
    def test_onboarding_completion_global(self):
        # Completing onboarding as company_1
        self.assertEqual(self.env.company, self.company_1)
        self.assertDictEqual(
            self.onboarding_1.current_progress_id._get_and_update_onboarding_state(),
            {self.onboarding_1_step_1.id: 'not_done', self.onboarding_1_step_2.id: 'not_done'})

        self.onboarding_1_step_1.action_set_just_done()
        # Test completed step state consolidation from `just_done` to `done`
        self.assertDictEqual(
            self.onboarding_1.current_progress_id._get_and_update_onboarding_state(),
            {self.onboarding_1_step_1.id: 'just_done', self.onboarding_1_step_2.id: 'not_done'})
        self.assertDictEqual(
            self.onboarding_1.current_progress_id._get_and_update_onboarding_state(),
            {self.onboarding_1_step_1.id: 'done', self.onboarding_1_step_2.id: 'not_done'})
        self.assert_step_is_done(self.onboarding_1_step_1, self.company_2)
        self.assert_onboarding_is_not_done(self.onboarding_1, self.company_2)

        self.onboarding_1_step_2.action_set_just_done()
        self.assert_step_is_done(self.onboarding_1_step_2, self.company_2)
        self.assert_onboarding_is_done(self.onboarding_1, self.company_2)

        # Once onboarding is done, a key 'onboarding_state' is added to the rendering values
        self.assertDictEqual(
            self.onboarding_1.current_progress_id._get_and_update_onboarding_state(),
            {self.onboarding_1_step_1.id: 'done', self.onboarding_1_step_2.id: 'just_done', 'onboarding_state': 'just_done'})
        # Consolidate values
        self.assertDictEqual(
            self.onboarding_1.current_progress_id._get_and_update_onboarding_state(),
            {self.onboarding_1_step_1.id: 'done', self.onboarding_1_step_2.id: 'done', 'onboarding_state': 'done'})

        self.onboarding_1.current_progress_id.action_close()
        self.assertTrue(self.onboarding_1.current_progress_id.is_onboarding_closed)

        # Adding new step resets onboarding state to 'not_done' even if closed
        onboarding_1_step_3 = self.env['onboarding.onboarding.step'].create({
            'title': 'Test Onboarding 1 - Step 3',
            'onboarding_ids': [(4, self.onboarding_1.id)],
            'is_per_company': False,
            'panel_step_open_action_name': 'action_fake_open_onboarding_step',
        })
        self.assert_step_is_not_done(onboarding_1_step_3)
        self.assert_onboarding_is_not_done(self.onboarding_1)

        # Completing it sets onboarding state to done again
        onboarding_1_step_3.action_set_just_done()
        self.assert_onboarding_is_done(self.onboarding_1)

        # If a company is added, onboarding is 'done'
        company_3 = self.env.company.create({
            'currency_id': self.env.ref('base.EUR').id,
            'name': 'Another Test Company',
        })
        self.assert_onboarding_is_done(self.onboarding_1.with_company(company_3))

        # Adding new step resets onboarding state to 'not_done'
        self.env['onboarding.onboarding.step'].create({
            'title': 'Test Onboarding 1 - Step 4',
            'onboarding_ids': [(4, self.onboarding_1.id)],
            'is_per_company': False,
            'panel_step_open_action_name': 'action_fake_open_onboarding_step',
        })

        # Closing the panel still allows to track if all steps are completed
        self.onboarding_1.action_close()
        self.assertTrue(self.onboarding_1.current_progress_id.is_onboarding_closed)
        self.assert_onboarding_is_not_done(self.onboarding_1)

    def test_onboarding_completion_per_company(self):
        """Checks the behavior of onboarding and step states in multi-company setting:
        the onboarding state has to track the completion of each of its steps, global and
        per-company, to determine if whether it is completed.
        """
        # Completing onboarding as company_1
        self.assertEqual(self.env.company, self.company_1)

        # Updating onboarding (and steps) to per-company
        (self.onboarding_1 + self.onboarding_2).action_toggle_is_per_company()
        # Required after progress reset (simulate role of controller)
        self.onboarding_1._search_or_create_progress()

        self.onboarding_1_step_1.action_set_just_done()
        self.assert_step_is_done(self.onboarding_1_step_1)

        self.onboarding_1_step_2.action_set_just_done()
        self.assert_onboarding_is_done(self.onboarding_1)

        # Completing onboarding as existing company_2
        self.activate_company(self.company_2)
        # First access from company_2
        self.onboarding_1._search_or_create_progress()

        # Blank state for company 2
        self.assert_step_is_not_done(self.onboarding_1_step_1)
        self.assert_onboarding_is_not_done(self.onboarding_1)

        # But no change for company 1
        self.assert_step_is_done(self.onboarding_1_step_1.with_company(self.company_1))
        self.assert_onboarding_is_done(self.onboarding_1.with_company(self.company_1))

        self.onboarding_1_step_1.action_set_just_done()
        self.assert_step_is_done(self.onboarding_1_step_1)
        self.assert_onboarding_is_not_done(self.onboarding_1)
        self.onboarding_1_step_2.with_company(self.company_2).action_set_just_done()
        self.assert_step_is_done(self.onboarding_1_step_2)
        self.assert_onboarding_is_done(self.onboarding_1)

        # is_onboarding_closed status is also company-independent
        self.onboarding_1.action_close()
        self.assertTrue(self.onboarding_1.current_progress_id.is_onboarding_closed)
        self.assertFalse(self.onboarding_1.with_company(self.company_1).current_progress_id.is_onboarding_closed)

    def test_onboarding_to_company_change(self):
        """Checks that changing onboarding to per-company resets completions states.
        """
        # Completing onboarding as company_1
        self.assertEqual(self.env.company, self.company_1)
        self.onboarding_1_step_1.action_set_just_done()
        self.onboarding_1_step_2.action_set_just_done()
        self.assert_onboarding_is_done(self.onboarding_1)

        # Updating onboarding to per-company
        (self.onboarding_1 + self.onboarding_2).action_toggle_is_per_company()
        self.assert_onboarding_is_not_done(self.onboarding_1)

        # Simulate role of controller
        self.onboarding_1._search_or_create_progress()

        self.assert_onboarding_is_not_done(self.onboarding_1)

        # Same for standalone step
        self.step_initially_w_o_onboarding.action_set_just_done()
        self.assert_step_is_done(self.step_initially_w_o_onboarding)
        self.step_initially_w_o_onboarding.is_per_company = not self.step_initially_w_o_onboarding.is_per_company
        self.assert_step_is_not_done(self.step_initially_w_o_onboarding)

    def test_onboarding_shared_steps(self):
        self.onboarding_2_step_2.action_set_just_done()
        self.assert_step_is_done(self.onboarding_2_step_2)
        # Completing common step is also required to be "done"
        self.assert_onboarding_is_not_done(self.onboarding_2)

        self.onboarding_1_step_1.action_set_just_done()
        self.assert_onboarding_is_not_done(self.onboarding_1)
        self.assert_onboarding_is_done(self.onboarding_2)

    @mute_logger('odoo.sql_db')
    def test_only_one_progress_per_company_or_without(self):
        # Remove shared step
        self.onboarding_1.write({
            'step_ids': [Command.unlink(self.onboarding_1_step_1.id)]
        })
        self.assertFalse(self.onboarding_1.current_progress_id.company_id)

        with self.assertRaises(ValidationError):
            self.env['onboarding.progress'].create({
                'onboarding_id': self.onboarding_1.id,
                'company_id': False
            })

        # Updating onboarding to per-company
        self.onboarding_1.action_toggle_is_per_company()
        # Required after progress reset (simulate role of controller)
        self.onboarding_1._search_or_create_progress()

        with self.assertRaises(ValidationError):
            self.env['onboarding.progress'].create({
                'onboarding_id': self.onboarding_1.id,
                'company_id': self.env.company.id
            })

    @mute_logger('odoo.sql_db')
    def test_only_one_progress_step_per_company_or_without(self):
        # Remove shared step
        self.onboarding_1.write({'step_ids': [Command.unlink(self.onboarding_1_step_1.id)]})
        self.assertFalse(self.onboarding_1.current_progress_id.company_id)

        onboarding_progress = self.onboarding_1._search_or_create_progress()
        self.onboarding_1_step_1.action_set_just_done()  # creates an onboarding_progress_step record

        with self.assertRaises(ValidationError):
            self.env['onboarding.progress.step'].create({
                'progress_ids': [onboarding_progress.id],
                'step_id': self.onboarding_1_step_1.id,
                'company_id': False
            })

        # Updating onboarding to per-company
        self.onboarding_1.action_toggle_is_per_company()
        # Required after progress reset (simulate role of controller)
        onboarding_progress = self.onboarding_1._search_or_create_progress()
        self.onboarding_1_step_1.action_set_just_done()

        with self.assertRaises(ValidationError):
            self.env['onboarding.progress.step'].create({
                'progress_ids': [onboarding_progress.id],
                'step_id': self.onboarding_1_step_1.id,
                'company_id': self.env.company.id,
            })

    def test_onboarding_step_without_onboarding(self):
        self.assertEqual(self.step_initially_w_o_onboarding.current_step_state, 'not_done')
        self.step_initially_w_o_onboarding.action_set_just_done()

        # Impossible to create a second progress step record
        with self.assertRaises(ValidationError):
            self.env['onboarding.progress.step'].create({
                'step_id': self.step_initially_w_o_onboarding.id,
                'company_id': False,
            })
        self.assert_step_is_done(self.step_initially_w_o_onboarding)

        self.onboarding_3 = self.env['onboarding.onboarding'].create({
            'name': 'Test Onboarding 3',
            'route_name': 'onboarding3',
        })
        self.onboarding_3._search_or_create_progress()

        with self.assertRaises(ValidationError):
            self.step_initially_w_o_onboarding.onboarding_ids = [(4, self.onboarding_3.id)]

        self.step_initially_w_o_onboarding.write({
            'panel_step_open_action_name': 'action_fake_open_onboarding_step'
        })
        self.step_initially_w_o_onboarding.onboarding_ids = [(4, self.onboarding_3.id)]

        # Behaves as others
        self.assert_onboarding_is_done(self.onboarding_3)
        self.assert_onboarding_is_not_done(self.onboarding_3.with_company(self.company_2))
        self.onboarding_3.with_company(self.company_2)._search_or_create_progress()
        self.assert_onboarding_is_not_done(self.onboarding_3.with_company(self.company_2))

        self.step_initially_w_o_onboarding.with_company(self.company_2).action_set_just_done()
        self.assert_onboarding_is_done(self.onboarding_3.with_company(self.company_2))

    def test_onboarding_per_company_consistency(self):
        self.assertFalse(self.onboarding_1.is_per_company)
        self.assertFalse(self.onboarding_2.is_per_company)
        self.assertFalse(self.onboarding_1_step_1.is_per_company)

        with self.assertRaises(ValidationError):
            # Impossible to add a 'is_per_company' step to a non-per-company onboarding
            self.env['onboarding.onboarding.step'].create([{
                'title': 'Test Onboarding 1 - Step N',
                'onboarding_ids': [self.onboarding_1.id],
                'panel_step_open_action_name': 'action_fake_open_onboarding_step',
                'is_per_company': True
            }])

        with self.assertRaises(ValidationError):
            # Impossible to create an 'is_per_company' onboarding with non per-company steps
            self.env['onboarding.onboarding'].create([{
                'name': 'Test Onboarding N',
                'is_per_company': True,
                'route_name': 'onboardingN',
                'step_ids': [self.onboarding_1_step_1.id]
            }])

        with self.assertRaises(ValidationError):
            # Impossible to change 'is_per_company' for step included in an onboarding
            self.onboarding_1_step_1.write({
                'is_per_company': True
            })

        with self.assertRaises(ValidationError):
            # Impossible to change 'is_per_company' for onboarding including steps
            self.onboarding_1.write({
                'is_per_company': True
            })

        with self.assertRaises(ValidationError):
            # Impossible to toggle is_per_company for onboarding with steps used in other onboardings
            self.onboarding_1.action_toggle_is_per_company()

        with self.assertRaises(ValidationError):
            # Impossible to toggle is_per_company for onboarding with steps used in other onboardings
            self.onboarding_1.action_toggle_is_per_company()

        # Possible to change is_per_company for a complete set of onboarding + related steps
        self.assertFalse(self.onboarding_1.is_per_company)
        (self.onboarding_1 + self.onboarding_2).action_toggle_is_per_company()
        self.assertTrue(self.onboarding_1.is_per_company)

        # possible to toggle is_per_company for a single onboarding if steps are not shared
        self.onboarding_2.step_ids = False
        self.onboarding_1.action_toggle_is_per_company()
        self.assertFalse(self.onboarding_1.is_per_company)

        # Possible to directly change is_per_company for standalone onboardings and steps
        self.onboarding_1.step_ids = False
        self.onboarding_1.is_per_company = not self.onboarding_1.is_per_company
        self.assertTrue(self.onboarding_1.is_per_company)

        self.assertFalse(self.onboarding_1_step_1.is_per_company)
        self.onboarding_1_step_1.onboarding_ids = False
        self.onboarding_1_step_1.is_per_company = not self.onboarding_1_step_1.is_per_company
        self.assertTrue(self.onboarding_1_step_1.is_per_company)
