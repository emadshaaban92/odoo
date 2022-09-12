# -*- coding: utf-8 -*-

from odoo.fields import Command
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.project.tests.test_project_base import TestProjectCommon

from datetime import date


@tagged('-at_install', 'post_install')
class TestTaskDependencies(TestProjectCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project_pigs.write({
            'allow_task_dependencies': True,
        })
        cls.task_3 = cls.env['project.task'].with_context({'mail_create_nolog': True}).create({
            'name': 'Pigs UserTask 2',
            'user_ids': cls.user_projectuser,
            'project_id': cls.project_pigs.id,
        })

    def flush_tracking(self):
        """ Force the creation of tracking values. """
        self.env.flush_all()
        self.cr.precommit.run()

    def test_task_dependencies(self):
        """ Test the task dependencies feature

            Test Case:
            =========
            1) Add task2 as dependency in task1
            2) Checks if the task1 has the task in depend_on_ids field.
        """
        self.assertEqual(len(self.task_1.depend_on_ids), 0, "The task 1 should not have any dependency.")
        self.task_1.write({
            'depend_on_ids': [Command.link(self.task_2.id)],
        })
        self.assertEqual(len(self.task_1.depend_on_ids), 1, "The task 1 should have a dependency.")
        self.task_1.write({
            'depend_on_ids': [Command.link(self.task_3.id)],
        })
        self.assertEqual(len(self.task_1.depend_on_ids), 2, "The task 1 should have two dependencies.")

    def test_cyclic_dependencies(self):
        """ Test the cyclic dependencies

            Test Case:
            =========
            1) Check initial setting on three tasks
            2) Add task2 as dependency in task1
            3) Add task3 as dependency in task2
            4) Add task1 as dependency in task3 and check a validation error is raised
            5) Add task1 as dependency in task2 and check a validation error is raised
        """
        # 1) Check initial setting on three tasks
        self.assertTrue(
            len(self.task_1.depend_on_ids) == len(self.task_2.depend_on_ids) == len(self.task_3.depend_on_ids) == 0,
            "The three tasks should depend on no tasks.")
        self.assertTrue(self.task_1.allow_task_dependencies, 'The task dependencies feature should be enable.')
        self.assertTrue(self.task_2.allow_task_dependencies, 'The task dependencies feature should be enable.')
        self.assertTrue(self.task_3.allow_task_dependencies, 'The task dependencies feature should be enable.')

        # 2) Add task2 as dependency in task1
        self.task_1.write({
            'depend_on_ids': [Command.link(self.task_2.id)],
        })
        self.assertEqual(len(self.task_1.depend_on_ids), 1, 'The task 1 should have one dependency.')

        # 3) Add task3 as dependency in task2
        self.task_2.write({
            'depend_on_ids': [Command.link(self.task_3.id)],
        })
        self.assertEqual(len(self.task_2.depend_on_ids), 1, "The task 2 should have one dependency.")

        # 4) Add task1 as dependency in task3 and check a validation error is raised
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.task_3.write({
                'depend_on_ids': [Command.link(self.task_1.id)],
            })
        self.assertEqual(len(self.task_3.depend_on_ids), 0, "The dependency should not be added in the task 3 because of a cyclic dependency.")

        # 5) Add task1 as dependency in task2 and check a validation error is raised
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.task_2.write({
                'depend_on_ids': [Command.link(self.task_1.id)],
            })
        self.assertEqual(len(self.task_2.depend_on_ids), 1, "The number of dependencies should no change in the task 2 because of a cyclic dependency.")

    def test_tracking_dependencies(self):
        # Enable the company setting
        self.env['res.config.settings'].create({
            'group_project_task_dependencies': True
        }).execute()
        # `depend_on_ids` is tracked
        self.task_1.with_context(mail_notrack=True).write({
            'depend_on_ids': [Command.link(self.task_2.id)]
        })
        self.cr.precommit.clear()
        # Check that changing a dependency tracked field in task_2 does not log a message in task_1.
        self.task_2.write({'date_deadline': date(1983, 3, 1)}) # + 0 message in task_1 and 1 in task_2
        self.flush_tracking()
        self.assertEqual(len(self.task_1.message_ids), 0,
            'Changing the deadline on task 2 should not have logged a message in task 1.')

        # Check that changing a dependency tracked field in task_1 does not log a message in task_2.
        self.task_1.date_deadline = date(2020, 1, 2) # + 1 message in task_1 and 0 in task_2
        self.flush_tracking()
        self.assertEqual(len(self.task_1.message_ids), 1,
            'Changing the deadline on task 1 should have logged a message in task 1.')
        self.assertEqual(len(self.task_2.message_ids), 1,
            'Changing the deadline on task 1 should not have logged a message in task 2.')

        # Check that changing a field that is not tracked at all on task 2 does not impact task 1.
        self.task_2.color = 100 # no new message
        self.flush_tracking()
        self.assertEqual(len(self.task_1.message_ids), 1,
            'Changing the color on task 2 should not have logged a message in task 1 since it is not tracked.')

    def test_tracking_stage_dependencies(self):
        """
            this test ensure that the stage modification from blocking tasks are correctly sending notifications to their parent when necessary.
            When all blocking task of a task are in a folded stage, log a notification.
            When a blocking tasking is reopened, and all the other blocking tasks of the parents are closed, log a notification.
        """
        # Enable the company setting
        self.env['res.config.settings'].create({
            'group_project_task_dependencies': True
        }).execute()
        # adds stages to the project
        stages = dev, validation, done, cancel = self.env['project.task.type'].create([{
            'sequence': 1,
            'name': 'Dev',
            'fold': False,
        }, {
            'sequence': 2,
            'name': 'Validation',
            'fold': False,
        }, {
            'sequence': 29,
            'name': 'Done',
            'fold': True,
        }, {
            'sequence': 30,
            'name': 'Cancel',
            'fold': True,
        }])
        self.project_pigs.write(
            {'type_ids': [Command.link(stage_id) for stage_id in stages.ids]})
        child_tasks = child_task_1, child_task_2, child_task_3 = self.env['project.task'].create([{
            'name': 'child_task_%s' % i,
            'user_ids': self.user_projectuser,
            'project_id': self.project_pigs.id,
            'stage_id': dev.id,
        } for i in range(1, 4)])
        parent_task_1, parent_task_2, parent_task_3 = self.env['project.task'].create([{
            'name': 'parent_task_%s' % (i + 1),
            'user_ids': self.user_projectuser,
            'project_id': self.project_pigs.id,
            'stage_id': dev.id,
            'depend_on_ids': depend_on_ids,
        } for i, depend_on_ids in enumerate([child_task_1, child_tasks, child_tasks])])
        self.cr.precommit.clear()

        # Close the task 1. This ensures that when one task is blocking many tasks, only the parent tasks with all their blocking tasks done get a log message.
        child_task_1.write({'stage_id': done.id})
        self.flush_tracking()
        self.assertEqual(len(parent_task_1.message_ids), 2, 'Changing the stage of child_task_1 to a folded stage should have logged a message in parent_task_1.')
        self.assertEqual(parent_task_1.message_ids[0].body, "<p>This task is ready to be worked on, as all of its blocking tasks have now been closed.</p>", 'Wrong message')
        self.assertEqual(len(parent_task_2.message_ids), 1, 'Changing the stage of child_task_1 to a folded stage should not have logged a message in parent_task_2.')
        self.assertEqual(len(parent_task_3.message_ids), 1, 'Changing the stage of child_task_1 to a folded stage should not have logged a message in parent_task_3.')

        # Close the task 2. This ensures that when a task depends on many tasks, only the last blocking task logs a chat message.
        child_task_2.write({'stage_id': done.id})
        self.flush_tracking()
        self.assertEqual(len(parent_task_1.message_ids), 2, 'Changing the stage of child_task_2 should not have logged a message in parent_task_1.')
        self.assertEqual(len(parent_task_2.message_ids), 1, 'Changing the stage of child_task_2 to a folded stage should not have logged a message in parent_task_2.')
        self.assertEqual(len(parent_task_3.message_ids), 1, 'Changing the stage of child_task_2 to a folded stage should not have logged a message in parent_task_3.')

        # Change the stage of task 3. This ensure that when a task is moved from one stage to another, no message is logged on the parent if the new stage is not a
        # folded stage and the parent task was not yet ready to be worked on.
        child_task_3.write({'stage_id': validation.id})
        self.flush_tracking()
        self.assertEqual(len(parent_task_1.message_ids), 2, 'Changing the stage of child_task_3 should not have logged a message in parent_task_1.')
        self.assertEqual(len(parent_task_2.message_ids), 1,
                         'Changing the stage of child_task_3 from a non folded stage to a non folded stage should not have logged a message in parent_task_2.')
        self.assertEqual(len(parent_task_3.message_ids), 1,
                         'Changing the stage of child_task_3 from a non folded stage to a non folded stage should not have logged a message in parent_task_3.')

        # Change the stage of task 3. This ensures that when a task is blocking many tasks, the message is logged to all the parent tasks, not just one.
        child_task_3.write({'stage_id': done.id})
        self.flush_tracking()
        self.assertEqual(len(parent_task_1.message_ids), 2, 'Changing the stage of child_task_3 should not have logged a message in parent_task_1.')
        self.assertEqual(len(parent_task_2.message_ids), 2,
                         'Changing the stage of child_task_3 from a non folded stage to a folded stage should have logged a message in parent_task_2.')
        self.assertEqual(parent_task_2.message_ids[0].body, "<p>This task is ready to be worked on, as all of its blocking tasks have now been closed.</p>", 'Wrong message')
        self.assertEqual(len(parent_task_3.message_ids), 2,
                         'Changing the stage of child_task_3 from a non folded stage to a folded stage should have logged a message in parent_task_3.')
        self.assertEqual(parent_task_3.message_ids[0].body, "<p>This task is ready to be worked on, as all of its blocking tasks have now been closed.</p>", 'Wrong message')

        # Change the stage of task 3. This ensure that when a task is moved from one stage to another, no message is logged on the parent if the new stage is a
        # folded stage and the parent task was already ready to be worked on.
        child_task_3.write({'stage_id': cancel.id})
        self.flush_tracking()
        self.assertEqual(len(parent_task_1.message_ids), 2, 'Changing the stage of child_task_3 should not have logged a message in parent_task_1.')
        self.assertEqual(len(parent_task_2.message_ids), 2,
                         'Changing the stage of child_task_3 from a folded stage to a folded stage should not have logged a message in parent_task_2.')
        self.assertEqual(len(parent_task_3.message_ids), 2,
                         'Changing the stage of child_task_3 from a folded stage to a folded stage should not have logged a message in parent_task_3.')

        # Change the stage of task 3. This ensure that when a task is moved from one stage to another, a message is logged on the parent if the new stage is not a
        # folded stage and the parent task was ready to be worked on.
        child_task_3.write({'stage_id': dev.id})
        self.flush_tracking()
        self.assertEqual(len(parent_task_1.message_ids), 2, 'Changing the stage of child_task_1 should not have logged a message in parent_task_1.')
        self.assertEqual(len(parent_task_2.message_ids), 3,
                         'Changing the stage of child_task_3 from a folded stage to a non folded stage should have logged a message in parent_task_2.')
        self.assertEqual(parent_task_2.message_ids[0].body, "<p>This task is no longer ready to be worked on, as task 'child_task_3' has been reopened.</p>", 'Wrong message')
        self.assertEqual(len(parent_task_3.message_ids), 3,
                         'Changing the stage of child_task_3 from a folded stage to a non folded stage should have logged a message in parent_task_3.')
        self.assertEqual(parent_task_3.message_ids[0].body, "<p>This task is no longer ready to be worked on, as task 'child_task_3' has been reopened.</p>", 'Wrong message')

    def test_task_dependencies_settings_change(self):

        def set_task_dependencies_setting(enabled):
            features_config = self.env["res.config.settings"].create({'group_project_task_dependencies': enabled})
            features_config.execute()

        self.project_pigs.write({
            'allow_task_dependencies': False,
        })

        # As the Project General Setting group_project_task_dependencies needs to be toggled in order
        # to be applied on the existing projects we need to force it so that it does not depends on anything
        # (like demo data for instance)
        set_task_dependencies_setting(False)
        set_task_dependencies_setting(True)
        self.assertTrue(self.project_pigs.allow_task_dependencies, "Projects allow_task_dependencies should follow group_project_task_dependencies setting changes")

        self.project_chickens = self.env['project.project'].create({
            'name': 'My Chicken Project'
        })
        self.assertTrue(self.project_chickens.allow_task_dependencies, "New Projects allow_task_dependencies should default to group_project_task_dependencies")

        set_task_dependencies_setting(False)
        self.assertFalse(self.project_pigs.allow_task_dependencies, "Projects allow_task_dependencies should follow group_project_task_dependencies setting changes")

        self.project_ducks = self.env['project.project'].create({
            'name': 'My Ducks Project'
        })
        self.assertFalse(self.project_ducks.allow_task_dependencies, "New Projects allow_task_dependencies should default to group_project_task_dependencies")

    def test_duplicate_project_with_task_dependencies(self):
        self.project_pigs.allow_task_dependencies = True
        self.task_1.depend_on_ids = self.task_2
        pigs_copy = self.project_pigs.copy()

        task1_copy = pigs_copy.task_ids.filtered(lambda t: t.name == 'Pigs UserTask')
        task2_copy = pigs_copy.task_ids.filtered(lambda t: t.name == 'Pigs ManagerTask')

        self.assertEqual(len(task1_copy), 1, "Should only contain 1 copy of UserTask")
        self.assertEqual(len(task2_copy), 1, "Should only contain 1 copy of ManagerTask")

        self.assertEqual(task1_copy.depend_on_ids.ids, [task2_copy.id],
                         "Copy should only create a relation between both copy if they are both part of the project")

        task1_copy.depend_on_ids = self.task_1

        pigs_copy_copy = pigs_copy.copy()
        task1_copy_copy = pigs_copy_copy.task_ids.filtered(lambda t: t.name == 'Pigs UserTask')

        self.assertEqual(task1_copy_copy.depend_on_ids.ids, [self.task_1.id],
                         "Copy should not alter the relation if the other task is in a different project")

    def test_duplicate_project_with_subtask_dependencies(self):
        self.project_goats.allow_task_dependencies = True
        self.project_goats.allow_subtasks = True
        parent_task = self.env['project.task'].with_context({'mail_create_nolog': True}).create({
            'name': 'Parent Task',
            'project_id': self.project_goats.id,
            'child_ids': [
                Command.create({'name': 'Node 1'}),
                Command.create({'name': 'SuperNode 2', 'child_ids': [Command.create({'name': 'Node 2'})]}),
                Command.create({'name': 'Node 3'}),
            ],
        })

        node1 = parent_task.child_ids[0]
        node2 = parent_task.child_ids[1].child_ids
        node3 = parent_task.child_ids[2]

        node1.dependent_ids = node2
        node2.dependent_ids = node3

        # Test copying the whole Node tree
        parent_task_copy = parent_task.copy()
        parent_copy_node1 = parent_task_copy.child_ids[0]
        parent_copy_node2 = parent_task_copy.child_ids[1].child_ids
        parent_copy_node3 = parent_task_copy.child_ids[2]

        # Relation should only be copied between the newly created node
        self.assertEqual(len(parent_copy_node1.dependent_ids), 1)
        self.assertEqual(parent_copy_node1.dependent_ids.ids, parent_copy_node2.ids, 'Node1copy - Node2copy relation should be present')
        self.assertEqual(len(parent_copy_node2.dependent_ids), 1)
        self.assertEqual(parent_copy_node2.dependent_ids.ids, parent_copy_node3.ids, 'Node2copy - Node3copy relation should be present')

        # Original Node should not have new relation
        self.assertEqual(len(node1.dependent_ids), 1)
        self.assertEqual(node1.dependent_ids.ids, node2.ids, 'Only Node1 - Node2 relation should be present')
        self.assertEqual(len(node2.dependent_ids), 1)
        self.assertEqual(node2.dependent_ids.ids, node3.ids, 'Only Node2 - Node3 relation should be present')

        # Test copying Node inside the chain
        single_copy_node2 = node2.copy()

        # Relation should be present between the other original node and the newly copied node
        self.assertEqual(len(single_copy_node2.depend_on_ids), 1)
        self.assertEqual(single_copy_node2.depend_on_ids.ids, node1.ids, 'Node1 - Node2copy relation should be present')
        self.assertEqual(len(single_copy_node2.dependent_ids), 1)
        self.assertEqual(single_copy_node2.dependent_ids.ids, node3.ids, 'Node2copy - Node3 relation should be present')

        # Original Node should have new relations
        self.assertEqual(len(node1.dependent_ids), 2)
        self.assertEqual(len(node3.depend_on_ids), 2)
