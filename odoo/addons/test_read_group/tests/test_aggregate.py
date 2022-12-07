# -*- coding: utf-8 -*-
from odoo import fields
from odoo.fields import Datetime
from odoo.tests import common
from odoo import Command


class TestReadAggregate(common.TransactionCase):

    def test_simple_aggregate(self):
        Model = self.env['test_read_group.aggregate']
        partner_1_id = self.env['res.partner'].create({'name': 'z_one'}).id
        partner_2_id = self.env['res.partner'].create({'name': 'a_two'}).id
        Model.create({'key': 1, 'partner_id': partner_1_id, 'value': 1})
        Model.create({'key': 1, 'partner_id': partner_1_id, 'value': 2})
        Model.create({'key': 1, 'partner_id': partner_2_id, 'value': 3})
        Model.create({'key': 2, 'partner_id': partner_2_id, 'value': 4})
        Model.create({'key': 2, 'partner_id': partner_2_id})
        Model.create({'key': 2, 'value': 5})
        Model.create({'partner_id': partner_2_id, 'value': 5})
        Model.create({'value': 6})
        Model.create({})

        with self.assertQueries([
            """
SELECT SUM("test_read_group_aggregate"."value") AS "value:sum", "test_read_group_aggregate"."key" AS "key"
FROM "test_read_group_aggregate"
GROUP BY "test_read_group_aggregate"."key"
ORDER BY "test_read_group_aggregate"."key" ASC
            """
        ]):
            self.assertEqual(
                Model.read_aggregate([], groupby=['key'], aggregates=['value:sum']),
                [
                    {
                        'key': 1,
                        'value:sum': 1 + 2 + 3,
                    },
                    {
                        'key': 2,
                        'value:sum': 4 + 5,
                    },
                    {
                        'key': None,
                        'value:sum': 5 + 6,
                    },
                ]
            )

        with self.assertQueries([
            """
SELECT SUM("test_read_group_aggregate"."value") AS "value:sum", "test_read_group_aggregate"."key" AS "key", "test_read_group_aggregate"."partner_id" AS "partner_id"
FROM "test_read_group_aggregate"
    LEFT JOIN "res_partner" AS "test_read_group_aggregate__partner_id" ON ("test_read_group_aggregate"."partner_id" = "test_read_group_aggregate__partner_id"."id")
GROUP BY "test_read_group_aggregate"."key", "test_read_group_aggregate"."partner_id", "test_read_group_aggregate__partner_id"."display_name", "test_read_group_aggregate__partner_id"."id"
ORDER BY "test_read_group_aggregate"."key" ASC, "test_read_group_aggregate__partner_id"."display_name", "test_read_group_aggregate__partner_id"."id"
            """
        ]):
            self.assertEqual(
                Model.read_aggregate([], groupby=['key', 'partner_id'], aggregates=['value:sum']),
                [
                    {
                        'key': 1,
                        'partner_id': partner_2_id,
                        'value:sum': 3,
                    },
                    {
                        'key': 1,
                        'partner_id': partner_1_id,
                        'value:sum': 1 + 2,
                    },
                    {
                        'key': 2,
                        'partner_id': partner_2_id,
                        'value:sum': 4,
                    },
                    {
                        'key': 2,
                        'partner_id': None,
                        'value:sum': 5,
                    },
                    {
                        'key': None,
                        'partner_id': partner_2_id,
                        'value:sum': 5,
                    },
                    {
                        'key': None,
                        'partner_id': None,
                        'value:sum': 6,
                    },
                ]
            )

        # Same than before but with private method, the order doesn't traverse many2one order, then the order is based on id of partner
        with self.assertQueries([
            """
SELECT SUM("test_read_group_aggregate"."value") AS "value:sum", "test_read_group_aggregate"."key" AS "key", "test_read_group_aggregate"."partner_id" AS "partner_id"
FROM "test_read_group_aggregate"
GROUP BY "test_read_group_aggregate"."key", "test_read_group_aggregate"."partner_id"
ORDER BY "test_read_group_aggregate"."key" ASC, "test_read_group_aggregate"."partner_id" ASC
            """
        ]):
            self.assertEqual(
                Model._read_aggregate([], groupby=['key', 'partner_id'], aggregates=['value:sum']),
                [
                    {
                        'key': 1,
                        'partner_id': partner_1_id,
                        'value:sum': 1 + 2,
                    },
                    {
                        'key': 1,
                        'partner_id': partner_2_id,
                        'value:sum': 3,
                    },
                    {
                        'key': 2,
                        'partner_id': partner_2_id,
                        'value:sum': 4,
                    },
                    {
                        'key': 2,
                        'partner_id': None,
                        'value:sum': 5,
                    },
                    {
                        'key': None,
                        'partner_id': partner_2_id,
                        'value:sum': 5,
                    },
                    {
                        'key': None,
                        'partner_id': None,
                        'value:sum': 6,
                    },
                ]
            )

    def test_ambiguous_field_name(self):
        """ Check that aggregate doesn't generate ambiguous (display_name) alias for PostgreSQL
        """
        Model = self.env['test_read_group.aggregate']
        partner_1_id = self.env['res.partner'].create({'name': 'z_one'}).id
        Model.create({'key': 1, 'partner_id': partner_1_id, 'value': 1, 'display_name': 'blabla'})
        with self.assertQueries([
            """
SELECT COUNT(*) AS "*:count", "test_read_group_aggregate"."display_name" AS "display_name", "test_read_group_aggregate"."partner_id" AS "partner_id"
FROM "test_read_group_aggregate"
    LEFT JOIN "res_partner" AS "test_read_group_aggregate__partner_id" ON ("test_read_group_aggregate"."partner_id" = "test_read_group_aggregate__partner_id"."id")
GROUP BY "test_read_group_aggregate"."display_name", "test_read_group_aggregate"."partner_id", "test_read_group_aggregate__partner_id"."display_name", "test_read_group_aggregate__partner_id"."id"
ORDER BY "test_read_group_aggregate__partner_id"."display_name" DESC, "test_read_group_aggregate__partner_id"."id" DESC
            """
        ]):
            self.assertEqual(
                Model.read_aggregate([], groupby=['display_name', 'partner_id'], order="partner_id DESC"),
                [{'display_name': 'blabla', 'partner_id': partner_1_id, '*:count': 1}]
            )

    def test_bool_aggregates(self):
        Model = self.env['test_read_group.aggregate.boolean']
        Model.create({'key': 1, 'bool_and': True})
        Model.create({'key': 1, 'bool_and': True})

        Model.create({'key': 2, 'bool_and': True})
        Model.create({'key': 2, 'bool_and': False})

        Model.create({'key': 3, 'bool_and': False})
        Model.create({'key': 3, 'bool_and': False})

        Model.create({'key': 4, 'bool_and': True, 'bool_or': True, 'bool_array': True})
        Model.create({'key': 4})

        self.assertEqual(
            Model.read_aggregate([], groupby=['key'], aggregates=['bool_and:bool_and', 'bool_and:bool_or', 'bool_and:array_agg_distinct']),
            [
                {'key': 1, 'bool_and:bool_and': True, 'bool_and:bool_or': True, 'bool_and:array_agg_distinct': [True]},
                {'key': 2, 'bool_and:bool_and': False, 'bool_and:bool_or': True, 'bool_and:array_agg_distinct': [False, True]},
                {'key': 3, 'bool_and:bool_and': False, 'bool_and:bool_or': False, 'bool_and:array_agg_distinct': [False]},
                {'key': 4, 'bool_and:bool_and': False, 'bool_and:bool_or': True, 'bool_and:array_agg_distinct': [False, True]},
            ]
        )

    def test_count_aggregates(self):
        Model = self.env['test_read_group.aggregate']
        Model.create({'key': 1})
        Model.create({'key': 1})
        Model.create({})

        self.assertEqual(
            Model.read_aggregate([], aggregates=['key:count']),
            [
                {'key:count': 2},
            ]
        )

        self.assertEqual(
            Model.read_aggregate([], aggregates=['key:count_distinct']),
            [
                {'key:count_distinct': 1},
            ]
        )

    def test_array_aggregates(self):
        Model = self.env['test_read_group.aggregate']
        Model.create({'key': 1})
        Model.create({'key': 1})
        Model.create({'key': 2})

        self.assertEqual(
            Model.read_aggregate([], aggregates=['key:array_agg']),
            [
                {'key:array_agg': [1, 1, 2]},
            ]
        )

        self.assertEqual(
            Model.read_aggregate([], aggregates=['key:array_agg_distinct']),
            [
                {'key:array_agg_distinct': [1, 2]},
            ]
        )

    def test_flush_read_aggregate(self):
        Model = self.env['test_read_group.aggregate']
        a = Model.create({'key': 1, 'value': 5})
        b = Model.create({'key': 1, 'value': 5})

        self.assertEqual(
            Model.read_aggregate([], groupby=['key'], aggregates=['value:sum']),
            [
                {'key': 1, 'value:sum': 5 + 5},
            ]
        )

        # Test flush of domain
        a.key = 2
        self.assertEqual(
            Model.read_aggregate([('key', '>', 1)], groupby=['key'], aggregates=['value:sum']),
            [
                {'key': 2, 'value:sum': 5},
            ]
        )

        # test flush of groupby clause
        a.key = 3
        self.assertEqual(
            Model.read_aggregate([], groupby=['key'], aggregates=['value:sum']),
            [
                {'key': 1, 'value:sum': 5},
                {'key': 3, 'value:sum': 5},
            ]
        )

        # Test flush of aggregates
        b.value = 8
        self.assertEqual(
            Model.read_aggregate([], groupby=['key'], aggregates=['value:sum']),
            [
                {'key': 1, 'value:sum': 8},
                {'key': 3, 'value:sum': 5},
            ]
        )

    def test_having_clause(self):
        Model = self.env['test_read_group.aggregate']
        Model.create({'key': 1, 'value': 8})
        Model.create({'key': 1, 'value': 2})

        Model.create({'key': 2, 'value': 5})

        Model.create({'key': 3, 'value': 2})
        Model.create({'key': 3, 'value': 4})
        Model.create({'key': 3, 'value': 1})
        with self.assertQueries([
            """
SELECT SUM("test_read_group_aggregate"."value") AS "value:sum", "test_read_group_aggregate"."key" AS "key"
FROM "test_read_group_aggregate"
GROUP BY "test_read_group_aggregate"."key"
HAVING SUM("test_read_group_aggregate"."value") > %s
ORDER BY "test_read_group_aggregate"."key" ASC
            """
        ]):
            self.assertEqual(
                Model._read_aggregate([], groupby=['key'], aggregates=['value:sum'], having=[("value:sum", '>', 8)]),
                [{'key': 1, 'value:sum': 2 + 8}]
            )

        with self.assertQueries([
            """
SELECT SUM("test_read_group_aggregate"."value") AS "value:sum", COUNT(*) AS "*:count", "test_read_group_aggregate"."key" AS "key"
FROM "test_read_group_aggregate"
GROUP BY "test_read_group_aggregate"."key"
HAVING (COUNT(*) < %s AND SUM("test_read_group_aggregate"."value") > %s)
ORDER BY "test_read_group_aggregate"."key" ASC
            """
        ]):
            self.assertEqual(
                Model._aggregate(
                    [],
                    groupby=['key'],
                    aggregates=['value:sum', '*:count'],
                    having=[
                        ('*:count', '<', 3),
                        ("value:sum", '>', 4),
                    ]
                ),
                [
                    {'key': 1, 'value:sum': 2 + 8, "*:count": 2},
                    {'key': 2, 'value:sum': 5, "*:count": 1},
                ]
            )

    def test_groupby_date(self):
        """ Test what happens when grouping on date fields """
        Model = self.env['test_read_group.fill_temporal']
        Model.create({})  # Falsy date
        Model.create({'date': '2022-01-29'})  # Saturday (week of '2022-01-24')
        Model.create({'date': '2022-01-29'})  # Same day
        Model.create({'date': '2022-01-30'})  # Sunday
        Model.create({'date': '2022-01-31'})  # Monday (other week)
        Model.create({'date': '2022-02-01'})  # (other month)
        Model.create({'date': '2022-05-29'})  # other quarter
        Model.create({'date': '2023-01-29'})  # other year

        gb = Model.read_aggregate([], groupby=['date:day'])

        self.assertEqual(gb, [
            {
                'date:day': fields.Date.to_date('2022-01-29'),
                '*:count': 2,
            },
            {
                'date:day': fields.Date.to_date('2022-01-30'),
                '*:count': 1,
            },
            {
                'date:day': fields.Date.to_date('2022-01-31'),
                '*:count': 1,
            },
            {
                'date:day': fields.Date.to_date('2022-02-01'),
                '*:count': 1,
            },
            {
                'date:day': fields.Date.to_date('2022-05-29'),
                '*:count': 1,
            },
            {
                'date:day': fields.Date.to_date('2023-01-29'),
                '*:count': 1,
            },
            {
                'date:day': None,
                '*:count': 1,
            }
        ])

        gb = Model.read_aggregate([], groupby=['date:week'])

        self.assertEqual(gb, [
            {
                'date:week': fields.Date.to_date('2022-01-24'),
                '*:count': 3,
            },
            {
                'date:week': fields.Date.to_date('2022-01-31'),
                '*:count': 2,
            },
            {
                'date:week': fields.Date.to_date('2022-05-23'),
                '*:count': 1,
            },
            {
                'date:week': fields.Date.to_date('2023-01-23'),
                '*:count': 1,
            },
            {
                'date:week': None,
                '*:count': 1,
            }
        ])

        gb = Model.read_aggregate([], groupby=['date:week'])

        self.assertEqual(gb, [
            {
                'date:week': fields.Date.to_date('2022-01-24'),
                '*:count': 3,
            },
            {
                'date:week': fields.Date.to_date('2022-01-31'),
                '*:count': 2,
            },
            {
                'date:week': fields.Date.to_date('2022-05-23'),
                '*:count': 1,
            },
            {
                'date:week': fields.Date.to_date('2023-01-23'),
                '*:count': 1,
            },
            {
                'date:week': None,
                '*:count': 1,
            }
        ])

        gb = Model.read_aggregate([], groupby=['date:month'])
        self.assertEqual(gb, [
            {
                'date:month': fields.Date.to_date('2022-01-01'),
                '*:count': 4,
            },
            {
                'date:month': fields.Date.to_date('2022-02-01'),
                '*:count': 1,
            },
            {
                'date:month': fields.Date.to_date('2022-05-01'),
                '*:count': 1,
            },
            {
                'date:month': fields.Date.to_date('2023-01-01'),
                '*:count': 1,
            },
            {
                'date:month': None,
                '*:count': 1,
            }
        ])

        gb = Model.read_aggregate([], groupby=['date:quarter'])
        self.assertEqual(gb, [
            {
                'date:quarter': fields.Date.to_date('2022-01-01'),
                '*:count': 5,
            },
            {
                'date:quarter': fields.Date.to_date('2022-04-01'),
                '*:count': 1,
            },
            {
                'date:quarter': fields.Date.to_date('2023-01-01'),
                '*:count': 1,
            },
            {
                'date:quarter': None,
                '*:count': 1,
            }
        ])

        gb = Model.read_aggregate([], groupby=['date:year'])
        self.assertEqual(gb, [
            {
                'date:year': fields.Date.to_date('2022-01-01'),
                '*:count': 6,
            },
            {
                'date:year': fields.Date.to_date('2023-01-01'),
                '*:count': 1,
            },
            {
                'date:year': None,
                '*:count': 1,
            }
        ])
        # Reverse order
        gb = Model.read_aggregate([], groupby=['date:year'], order="date:year DESC")
        self.assertEqual(gb, [
            {
                'date:year': None,
                '*:count': 1,
            },
            {
                'date:year': fields.Date.to_date('2023-01-01'),
                '*:count': 1,
            },
            {
                'date:year': fields.Date.to_date('2022-01-01'),
                '*:count': 6,
            }
        ])

    def test_groupby_datetime(self):
        Model = self.env['test_read_group.fill_temporal']
        create_values = [
            {'datetime': False, 'value': 13},
            {'datetime': '1916-08-18 01:50:00', 'value': 3},
            {'datetime': '1916-08-19 01:30:00', 'value': 7},
            {'datetime': '1916-10-18 02:30:00', 'value': 5},
        ]
        # Time Zone                      UTC     UTC DST
        tzs = ["America/Anchorage",  # −09:00    −08:00
               "Europe/Brussels",    # +01:00    +02:00
               "Pacific/Kwajalein"]  # +12:00    +12:00
        for tz in tzs:
            Model = Model.with_context(tz=tz)
            records = Model.create(create_values)
            Model._read_aggregate([('id', 'in', records.ids)], ['value:sum'], ['datetime:hour'])
            self.assertEqual(
                Model._read_aggregate([('id', 'in', records.ids)], ['value:sum'], ['datetime:hour']),
                [
                    {
                        'value:sum': 3,
                        'datetime:hour': fields.Datetime.context_timestamp(
                            Model, fields.Datetime.to_datetime('1916-08-18 01:00:00')
                        ).replace(tzinfo=None),
                    },
                    {
                        'value:sum': 7,
                        'datetime:hour': fields.Datetime.context_timestamp(
                            Model, fields.Datetime.to_datetime('1916-08-19 01:00:00')
                        ).replace(tzinfo=None),
                    },
                    {
                        'value:sum': 5,
                        'datetime:hour': fields.Datetime.context_timestamp(
                            Model, fields.Datetime.to_datetime('1916-10-18 02:00:00')
                        ).replace(tzinfo=None),
                    },
                    {
                        'value:sum': 13,
                        'datetime:hour': None,
                    },
                ]
            )

    def test_auto_join(self):
        """ Test what happens when grouping with a domain using a one2many field with auto_join. """
        model = self.env['test_read_group.order']
        records = model.create([{
            'line_ids': [Command.create({'value': 1}), Command.create({'value': 2})],
        }, {
            'line_ids': [Command.create({'value': 1})],
        }])

        domain1 = [('id', 'in', records.ids), ('line_ids.value', '=', 1)]
        domain2 = [('id', 'in', records.ids), ('line_ids.value', '>', 0)]

        # reference results
        self.assertEqual(len(model.search(domain1)), 2)
        self.assertEqual(len(model.search(domain2)), 2)

        result1 = model.read_aggregate(domain1)
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0]['*:count'], 2)

        result2 = model.read_aggregate(domain2)
        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0]['*:count'], 2)

        # same requests, with auto_join
        self.patch(type(model).line_ids, 'auto_join', True)

        self.assertEqual(len(model.search(domain1)), 2)
        self.assertEqual(len(model.search(domain2)), 2)

        result1 = model.read_aggregate(domain1)
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0]['*:count'], 2)

        result2 = model.read_aggregate(domain2)
        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0]['*:count'], 2)

    def test_many2many_groupby(self):
        users = self.env['test_read_group.user'].create([
            {'name': 'Mario'},
            {'name': 'Luigi'},
        ])
        tasks = self.env['test_read_group.task'].create([
            {   # both users
                'name': "Super Mario Bros.",
                'user_ids': [Command.set(users.ids)],
            },
            {   # mario only
                'name': "Paper Mario",
                'user_ids': [Command.set(users[0].ids)],
            },
            {   # luigi only
                'name': "Luigi's Mansion",
                'user_ids': [Command.set(users[1].ids)],
            },
            {   # no user
                'name': 'Donkey Kong',
            },
        ])

        task_by_users = tasks.aggregate(
            [('id', 'in', tasks.ids)],
            ['name:array_agg'],
            ['user_ids'],
        )
        # TODO: should we order by the relation and not by the id also for many2many (same than many2one) ?
        self.assertEqual(task_by_users, [
            {   # tasks of Mario
                'user_ids': users[0].id,
                'name:array_agg': ["Paper Mario", "Super Mario Bros."],
            },
            {   # tasks of Luigi
                'user_ids': users[1].id,
                'name:array_agg': ["Luigi's Mansion", "Super Mario Bros."],
            },
            {   # tasks of nobody
                'user_ids': None,
                'name:array_agg': ["Donkey Kong"],
            },
        ])
