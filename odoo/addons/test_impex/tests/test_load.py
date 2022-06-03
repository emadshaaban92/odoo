# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import contextlib
import json
import pkgutil
import re

from odoo import fields
from odoo.addons.base.tests.common import SavepointCaseWithUserDemo
from odoo.tests import common
from odoo.tools.misc import mute_logger
from odoo.exceptions import ValidationError

def message(msg, type='error', from_=0, to_=0, record=0, field='value', **kwargs):
    return dict(kwargs,
                type=type, rows={'from': from_, 'to': to_}, record=record,
                field=field, message=msg)

def moreaction(**kwargs):
    return dict(kwargs,
        type='ir.actions.act_window',
        target='new',
        context={'create': False},
        name='Possible Values',
        view_mode='tree,form',
        views=[(False, 'list'), (False, 'form')],
        help=u"See all possible values")

def values(seq, field='value'):
    return [item[field] for item in seq]


class ImporterCase(common.TransactionCase):
    model_name = False

    def __init__(self, *args, **kwargs):
        super(ImporterCase, self).__init__(*args, **kwargs)
        self.model = None

    def setUp(self):
        super(ImporterCase, self).setUp()
        self.model = self.env[self.model_name]
        self.env['ir.model.data'].clear_caches()
        self.cr.cache.clear()

    def import_(self, fields, rows, keys=None, context=None):
        context = context or {}
        context.update({
            'import_file': True
        })
        return self.model.with_context(context or {}).load(fields, rows, key_fields=keys)

    def read(self, fields=('value',), domain=(), context=None):
        records = self.model.with_context(context or {}).search(domain)
        return records.read(fields)

    def browse(self, domain=(), context=None):
        return self.model.with_context(context or {}).search(domain)

    def xid(self, record):
        ModelData = self.env['ir.model.data']

        data = ModelData.search([('model', '=', record._name), ('res_id', '=', record.id)])
        if data:
            d = data.read(['name', 'module'])[0]
            if d['module']:
                return '%s.%s' % (d['module'], d['name'])
            return d['name']

        name = record.display_name
        # fix dotted name_get results, otherwise xid lookups blow up
        name = name.replace('.', '-')
        ModelData.create({
            'name': name,
            'model': record._name,
            'res_id': record.id,
            'module': '__test__'
        })
        return '__test__.' + name

    def add_translations(self, name, type, code, *tnx):
        self.env['res.lang']._activate_lang(code)
        Translations = self.env['ir.translation']
        for source, value in tnx:
            Translations.create({
                'name': name,
                'lang': code,
                'type': type,
                'src': source,
                'value': value,
                'state': 'translated',
            })


class test_ids_stuff(ImporterCase):
    model_name = 'export.integer'

    def test_create_with_id(self):
        result = self.import_(['.id', 'value'], [['42', '36']])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [{
            'type': 'error',
            'rows': {'from': 0, 'to': 0},
            'record': 0,
            'field': '.id',
            'message': u"Unknown database identifier '42'",
        }])

    def test_create_with_xid(self):
        result = self.import_(['id', 'value'], [['somexmlid', '42']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual(
            '__import__.somexmlid',
            self.xid(self.browse()[0]))

    def test_update_with_id(self):
        record = self.model.create({'value': 36})
        self.assertEqual(
            36,
            record.value)

        result = self.import_(['.id', 'value'], [[str(record.id), '42']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual(
            [42], # updated value to imported
            values(self.read()))

    def test_update_with_xid(self):
        self.import_(['id', 'value'], [['somexmlid', '36']])
        self.assertEqual([36], values(self.read()))

        self.import_(['id', 'value'], [['somexmlid', '1234567']])
        self.assertEqual([1234567], values(self.read()))


class test_boolean_field(ImporterCase):
    model_name = 'export.boolean'

    def test_empty(self):
        self.assertEqual(
            self.import_(['value'], []),
            {'ids': [], 'messages': [], 'nextrow': False})

    def test_exported(self):
        result = self.import_(['value'], [['False'], ['True'], ])
        self.assertEqual(len(result['ids']), 2)
        self.assertFalse(result['messages'])
        records = self.read()
        self.assertEqual([
            False,
            True,
        ], values(records))

    def test_falses(self):
        for lang, source, value in [('fr_FR', 'no', u'non'),
                                    ('de_DE', 'no', u'nein'),
                                    ('ru_RU', 'no', u'нет'),
                                    ('nl_BE', 'false', u'vals'),
                                    ('lt_LT', 'false', u'klaidingas')]:
            self.add_translations('test_import.py', 'code', lang, (source, value))
        falses = [[u'0'], [u'no'], [u'false'], [u'FALSE'], [u''],
                  [u'non'], # no, fr
                  [u'nein'], # no, de
                  [u'нет'], # no, ru
                  [u'vals'], # false, nl
                  [u'klaidingas'], # false, lt,
        ]

        result = self.import_(['value'], falses)
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), len(falses))
        self.assertEqual([False] * len(falses), values(self.read()))

    def test_trues(self):
        # Since importing wrong boolean values is now returning error, import should not return any ids if an error is raised.
        trues = [['None'], ['nil'], ['()'], ['f'], ['#f'],
                  # Problem: OpenOffice (and probably excel) output localized booleans
                  ['VRAI'], ['ok'], ['true'], ['yes'], ['1'], ]
        result = self.import_(['value'], trues)
        self.assertEqual(result['ids'], False)
        self.assertEqual(result['messages'], [{
            'rows': {'from': i, 'to': i}, 'type': 'error', 'record': i, 'field': 'value',
            'message': "Unknown value '%s' for boolean field 'Value'" % v[0],
            'moreinfo': "Use '1' for yes and '0' for no", 'field_name': 'Value'
        } for i, v in enumerate(trues) if v[0] not in ('true', 'yes', '1')])

        # Only correct boolean values are accepted.
        result = self.import_(['value'], [['1'], ['yes'], ['true']])
        self.assertEqual(len(result['ids']), 3)
        self.assertEqual(
            [True] * 3,
            values(self.read()))


class test_integer_field(ImporterCase):
    model_name = 'export.integer'

    def test_none(self):
        self.assertEqual(
            self.import_(['value'], []),
            {'ids': [], 'messages': [], 'nextrow': False})

    def test_empty(self):
        result = self.import_(['value'], [['']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual(
            [False],
            values(self.read()))

    def test_zero(self):
        result = self.import_(['value'], [['0']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])

        result = self.import_(['value'], [['-0']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])

        self.assertEqual([False, False], values(self.read()))

    def test_positives(self):
        result = self.import_(['value'], [
            ['1'],
            ['42'],
            [str(2**31-1)],
            ['12345678']
        ])
        self.assertEqual(len(result['ids']), 4)
        self.assertFalse(result['messages'])

        self.assertEqual([
            1, 42, 2**31-1, 12345678
        ], values(self.read()))

    def test_negatives(self):
        result = self.import_(['value'], [
            ['-1'],
            ['-42'],
            [str(-(2**31 - 1))],
            [str(-(2**31))],
            ['-12345678']
        ])
        self.assertEqual(len(result['ids']), 5)
        self.assertFalse(result['messages'])
        self.assertEqual([
            -1, -42, -(2**31 - 1), -(2**31), -12345678
        ], values(self.read()))

    @mute_logger('odoo.sql_db', 'odoo.models')
    def test_out_of_range(self):
        result = self.import_(['value'], [[str(2**31)]])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [{
            'type': 'error',
            'rows': {'from': 0, 'to': 0},
            'record': 0,
            'message': "integer out of range\n"
        }])

        result = self.import_(['value'], [[str(-2**32)]])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [{
            'type': 'error',
            'rows': {'from': 0, 'to': 0},
            'record': 0,
            'message': "integer out of range\n"
        }])

    def test_nonsense(self):
        result = self.import_(['value'], [['zorglub']])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [{
            'field_name': 'Value',
            'type': 'error',
            'rows': {'from': 0, 'to': 0},
            'record': 0,
            'field': 'value',
            'message': u"'zorglub' does not seem to be an integer for field 'Value'",
        }])


class test_float_field(ImporterCase):
    model_name = 'export.float'

    def test_none(self):
        self.assertEqual(
            self.import_(['value'], []),
            {'ids': [], 'messages': [], 'nextrow': False})

    def test_empty(self):
        result = self.import_(['value'], [['']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual(
            [False],
            values(self.read()))

    def test_zero(self):
        result = self.import_(['value'], [['0']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])

        result = self.import_(['value'], [['-0']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])

        self.assertEqual([False, False], values(self.read()))

    def test_positives(self):
        result = self.import_(['value'], [
            ['1'],
            ['42'],
            [str(2**31-1)],
            ['12345678'],
            [str(2**33)],
            ['0.000001'],
        ])
        self.assertEqual(len(result['ids']), 6)
        self.assertFalse(result['messages'])

        self.assertEqual([
            1, 42, 2**31-1, 12345678, 2.0**33, .000001
        ], values(self.read()))

    def test_negatives(self):
        result = self.import_(['value'], [
            ['-1'],
            ['-42'],
            [str(-2**31 + 1)],
            [str(-2**31)],
            ['-12345678'],
            [str(-2**33)],
            ['-0.000001'],
        ])
        self.assertEqual(len(result['ids']), 7)
        self.assertFalse(result['messages'])
        self.assertEqual([
            -1, -42, -(2**31 - 1), -(2**31), -12345678, -2.0**33, -.000001
        ], values(self.read()))

    def test_nonsense(self):
        result = self.import_(['value'], [['foobar']])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [
            message(u"'foobar' does not seem to be a number for field 'Value'", field_name='Value')])

class test_string_field(ImporterCase):
    model_name = 'export.string.bounded'

    def test_empty(self):
        result = self.import_(['value'], [['']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual([False], values(self.read()))

    def test_imported(self):
        result = self.import_(['value'], [
            [u'foobar'],
            [u'foobarbaz'],
            [u'Með suð í eyrum við spilum endalaust'],
            [u"People 'get' types. They use them all the time. Telling "
             u"someone he can't pound a nail with a banana doesn't much "
             u"surprise him."]
        ])
        self.assertEqual(len(result['ids']), 4)
        self.assertFalse(result['messages'])
        self.assertEqual([
            u"foobar",
            u"foobarbaz",
            u"Með suð í eyrum ",
            u"People 'get' typ",
        ], values(self.read()))


class test_unbound_string_field(ImporterCase):
    model_name = 'export.string'

    def test_imported(self):
        result = self.import_(['value'], [
            [u'í dag viðrar vel til loftárása'],
            # ackbar.jpg
            [u"If they ask you about fun, you tell them – fun is a filthy"
             u" parasite"]
        ])
        self.assertEqual(len(result['ids']), 2)
        self.assertFalse(result['messages'])
        self.assertEqual([
            u"í dag viðrar vel til loftárása",
            u"If they ask you about fun, you tell them – fun is a filthy parasite"
        ], values(self.read()))


class test_required_string_field(ImporterCase):
    model_name = 'export.string.required'

    @mute_logger('odoo.sql_db', 'odoo.models')
    def test_empty(self):
        result = self.import_(['value'], [[]])
        self.assertEqual(result['messages'], [message(
            u"Missing required value for the field 'Value' (value)")])
        self.assertIs(result['ids'], False)

    @mute_logger('odoo.sql_db', 'odoo.models')
    def test_not_provided(self):
        result = self.import_(['const'], [['12']])
        self.assertEqual(result['messages'], [message(
            u"Missing required value for the field 'Value' (value)")])
        self.assertIs(result['ids'], False)

    @mute_logger('odoo.sql_db', 'odoo.models')
    def test_ignore_excess_messages(self):
        result = self.import_(['const'], [[str(n)] for n in range(100)])
        self.assertIs(result['ids'], False)
        self.assertEqual(len(result['messages']), 11)
        for m in result['messages'][:-1]:
            self.assertEqual(m['type'], 'error')
            self.assertEqual(m['message'], u"Missing required value for the field 'Value' (value)")
        last = result['messages'][-1]
        self.assertEqual(last['type'], 'warning')
        self.assertEqual(
            last['message'],
            u"Found more than 10 errors and more than one error per 10 records, interrupted to avoid showing too many errors."
        )

class test_text(ImporterCase):
    model_name = 'export.text'

    def test_empty(self):
        result = self.import_(['value'], [['']])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual([False], values(self.read()))

    def test_imported(self):
        s = (u"Breiðskífa er notað um útgefna hljómplötu sem inniheldur "
             u"stúdíóupptökur frá einum flytjanda. Breiðskífur eru oftast "
             u"milli 25-80 mínútur og er lengd þeirra oft miðuð við 33⅓ "
             u"snúninga 12 tommu vínylplötur (sem geta verið allt að 30 mín "
             u"hvor hlið).\n\nBreiðskífur eru stundum tvöfaldar og eru þær þá"
             u" gefnar út á tveimur geisladiskum eða tveimur vínylplötum.")
        result = self.import_(['value'], [[s]])
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])
        self.assertEqual([s], values(self.read()))


class test_selection(ImporterCase):
    model_name = 'export.selection'
    translations_fr = [
        ("Foo", "tete"),
        ("Bar", "titi"),
        ("Qux", "toto"),
    ]

    def test_imported(self):
        result = self.import_(['value'], [
            ['Qux'],
            ['Bar'],
            ['Foo'],
            ['2'],
        ])
        self.assertEqual(len(result['ids']), 4)
        self.assertFalse(result['messages'])
        self.assertEqual(['3', '2', '1', '2'], values(self.read()))

    def test_imported_translated(self):
        self.add_translations(
            'ir.model.fields.selection,name', 'model', 'fr_FR', *self.translations_fr)

        result = self.import_(['value'], [
            ['toto'],
            ['tete'],
            ['titi'],
        ], context={'lang': 'fr_FR'})
        self.assertEqual(len(result['ids']), 3)
        self.assertFalse(result['messages'])

        self.assertEqual(['3', '1', '2'], values(self.read()))

        result = self.import_(['value'], [['Foo']], context={'lang': 'fr_FR'})
        self.assertEqual(len(result['ids']), 1)
        self.assertFalse(result['messages'])

    def test_invalid(self):
        result = self.import_(['value'], [['Baz']])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [message(
            u"Value 'Baz' not found in selection field 'Value'",
            moreinfo="Foo Bar Qux 4".split(), field_name='Value', field_path=['value'])])

        result = self.import_(['value'], [['42']])
        self.assertIs(result['ids'], False)
        self.assertEqual(result['messages'], [message(
            u"Value '42' not found in selection field 'Value'",
            moreinfo="Foo Bar Qux 4".split(),
            field_name='Value', field_path=['value'])])


class test_selection_with_default(ImporterCase):
    model_name = 'export.selection.withdefault'

    def test_empty(self):
        """ Empty cells should set corresponding field to False
        """
        result = self.import_(['value'], [['']])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        self.assertEqual(
            values(self.read()),
            [False])

    def test_default(self):
        """ Non-provided cells should set corresponding field to default
        """
        result = self.import_(['const'], [['42']])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        self.assertEqual(
            values(self.read()),
            ['2'])


class test_selection_function(ImporterCase):
    model_name = 'export.selection.function'
    translations_fr = [
        ("Corge", "toto"),
        ("Grault", "titi"),
        ("Wheee", "tete"),
        ("Moog", "tutu"),
    ]

    def test_imported(self):
        """ import uses fields_get, so translates import label (may or may not
        be good news) *and* serializes the selection function to reverse it:
        import does not actually know that the selection field uses a function
        """
        # NOTE: conflict between a value and a label => pick first
        result = self.import_(['value'], [
            ['3'],
            ["Grault"],
        ])
        self.assertEqual(len(result['ids']), 2)
        self.assertFalse(result['messages'])
        self.assertEqual(values(self.read()), ['3', '1'])

    def test_translated(self):
        """ Expects output of selection function returns translated labels
        """
        self.add_translations(
            'ir.model.fields.selection,name', 'model', 'fr_FR', *self.translations_fr)

        result = self.import_(['value'], [
            ['titi'],
            ['tete'],
        ], context={'lang': 'fr_FR'})
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 2)
        self.assertEqual(values(self.read()), ['1', '2'])

        result = self.import_(['value'], [['Wheee']], context={'lang': 'fr_FR'})
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)


class test_m2o(ImporterCase):
    model_name = 'export.many2one'

    def test_by_name(self):
        # create integer objects
        record1 = self.env['export.integer'].create({'value': 42})
        record2 = self.env['export.integer'].create({'value': 36})
        # get its name
        name1 = dict(record1.name_get())[record1.id]
        name2 = dict(record2.name_get())[record2.id]

        # preheat the oven
        for _ in range(5):
            with contextlib.closing(self.env.cr.savepoint(flush=False)):
                self.import_(['value'], [[name1], [name1], [name2]])

        # 1 x SAVEPOINT load
        # 3 x name_search
        # 1 x SAVEPOINT _load_records
        # 3 x insert
        # 1 x RELEASE SAVEPOINT _load_records
        # 1 x RELEASE SAVEPOINT load
        # => 10
        with self.assertQueryCount(8):
            result = self.import_(['value'], [
                # import by name_get
                [name1],
                [name1],
                [name2],
            ])

        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 3)
        # correct ids assigned to corresponding records
        self.assertEqual([
            (record1.id, name1),
            (record1.id, name1),
            (record2.id, name2),],
            values(self.read()))

    def test_by_xid(self):
        record = self.env['export.integer'].create({'value': 42})
        xid = self.xid(record)

        result = self.import_(['value/id'], [[xid]])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)
        b = self.browse()
        self.assertEqual(42, b[0].value.value)

    def test_by_id(self):
        record = self.env['export.integer'].create({'value': 42})
        result = self.import_(['value/.id'], [[record.id]])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)
        b = self.browse()
        self.assertEqual(42, b[0].value.value)

    def test_by_names(self):
        record1 = self.env['export.integer'].create({'value': 42})
        record2 = self.env['export.integer'].create({'value': 42})
        name1 = dict(record1.name_get())[record1.id]
        name2 = dict(record2.name_get())[record2.id]
        # names should be the same
        self.assertEqual(name1, name2)

        result = self.import_(['value'], [[name2]])
        self.assertEqual(
            result['messages'],
            [message(u"Found multiple matches for value 'export.integer:42' in field 'Value' (2 matches)",
                     type='warning')])
        self.assertEqual(len(result['ids']), 1)
        self.assertEqual([
            (record1.id, name1)
        ], values(self.read()))

    def test_fail_by_implicit_id(self):
        """ Can't implicitly import records by id
        """
        # create integer objects
        record1 = self.env['export.integer'].create({'value': 42})
        record2 = self.env['export.integer'].create({'value': 36})

        # Because name_search all the things. Fallback schmallback
        result = self.import_(['value'], [
                # import by id, without specifying it
                [record1.id],
                [record2.id],
                [record1.id],
        ])
        self.assertEqual(result['messages'], [
            message(u"No matching record found for name '%s' in field 'Value'" % id,
                    from_=index, to_=index, record=index,
                    moreinfo=moreaction(res_model='export.integer'), field_name='Value', field_path=['value'],
                    field_type='name', value=id)
            for index, id in enumerate([record1.id, record2.id, record1.id])])
        self.assertIs(result['ids'], False)

    @mute_logger('odoo.sql_db')
    def test_fail_id_mistype(self):
        result = self.import_(['value/.id'], [["foo"]])

        self.assertEqual(result['messages'], [
            message(u"Invalid database id 'foo' for the field 'Value'",
                    moreinfo=moreaction(res_model='ir.model.data',
                                        domain=[('model', '=', 'export.integer')]),
                    field_name='Value', field_path=['value', '.id'])
        ])
        self.assertIs(result['ids'], False)

    def test_sub_field(self):
        """ Does not implicitly create the record, does not warn that you can't
        import m2o subfields (at all)...
        """
        result = self.import_(['value/value'], [['42']])
        self.assertEqual(result['messages'], [
            message(u"Can not create Many-To-One records indirectly, import "
                    u"the field separately")])
        self.assertIs(result['ids'], False)

    def test_fail_noids(self):
        result = self.import_(['value'], [['nameisnoexist:3']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name 'nameisnoexist:3' "
            u"in field 'Value'", moreinfo=moreaction(
                res_model='export.integer'),
            field_name='Value', field_path=['value'], field_type='name', value='nameisnoexist:3'
        )])
        self.assertIs(result['ids'], False)

        result = self.import_(['value/id'], [['noxidhere']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for external id 'noxidhere' "
            u"in field 'Value'", moreinfo=moreaction(
                res_model='ir.model.data', domain=[('model', '=', 'export.integer')]),
            field_name='Value', field_path=['value', 'id'], field_type="external id", value="noxidhere")])
        self.assertIs(result['ids'], False)

        result = self.import_(['value/.id'], [['66']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for database id '66' "
            u"in field 'Value'", moreinfo=moreaction(
                res_model='ir.model.data', domain=[('model', '=', 'export.integer')]),
            field_name='Value', field_path=['value', '.id'], field_type="database id", value="66")])
        self.assertIs(result['ids'], False)

    def test_fail_multiple(self):
        result = self.import_(
            ['value', 'value/id'],
            [['somename', 'somexid']])
        self.assertEqual(result['messages'], [message(
            u"Ambiguous specification for field 'Value', only provide one of "
            u"name, external id or database id")])
        self.assertIs(result['ids'], False)

    def test_name_create_enabled_m2o(self):
        result = self.import_(['value'], [[101]])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name '101' "
            u"in field 'Value'", moreinfo=moreaction(
                res_model='export.integer'),
            field_name='Value', field_path=['value'], field_type='name', value=101)])
        self.assertIs(result['ids'], False)
        context = {
            'name_create_enabled_fields': {'value': True},
        }
        result = self.import_(['value'], [[101]], context=context)
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

class TestInvalidStrings(ImporterCase):
    model_name = 'export.m2o.str'

    @mute_logger('odoo.sql_db')
    def test_fail_unpaired_surrogate(self):
        result = self.import_(['child_id'], [['\uddff']])
        self.assertTrue(result['messages'])
        self.assertIn('surrogates', result['messages'][0]['message'])

    @mute_logger('odoo.sql_db')
    def test_fail_nul(self):
        result = self.import_(['child_id'], [['\x00']])
        self.assertTrue(result['messages'])
        self.assertIn('NUL', result['messages'][0]['message'])

class test_m2m(ImporterCase):
    model_name = 'export.many2many'

    # apparently, one and only thing which works is a
    # csv_internal_sep-separated list of ids, xids, or names (depending if
    # m2m/.id, m2m/id or m2m[/anythingelse]
    def test_ids(self):
        id1 = self.env['export.many2many.other'].create({'value': 3, 'str': 'record0'}).id
        id2 = self.env['export.many2many.other'].create({'value': 44, 'str': 'record1'}).id
        id3 = self.env['export.many2many.other'].create({'value': 84, 'str': 'record2'}).id
        id4 = self.env['export.many2many.other'].create({'value': 9, 'str': 'record3'}).id
        id5 = self.env['export.many2many.other'].create({'value': 99, 'str': 'record4'}).id

        result = self.import_(['value/.id'], [
            ['%d,%d' % (id1, id2)],
            ['%d,%d,%d' % (id1, id3, id4)],
            ['%d,%d,%d' % (id1, id2, id3)],
            ['%d' % id5]
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 4)

        ids = lambda records: [record.id for record in records]

        b = self.browse()
        self.assertEqual(ids(b[0].value), [id1, id2])
        self.assertEqual(values(b[0].value), [3, 44])

        self.assertEqual(ids(b[2].value), [id1, id2, id3])
        self.assertEqual(values(b[2].value), [3, 44, 84])

    def test_noids(self):
        result = self.import_(['value/.id'], [['42']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for database id '42' in field "
            u"'Value'", moreinfo=moreaction(
                res_model='ir.model.data', domain=[('model', '=', 'export.many2many.other')]),
            field_name='Value', field_path=['value', '.id'], field_type="database id", value='42')])
        self.assertIs(result['ids'], False)

    def test_xids(self):
        record0 = self.env['export.many2many.other'].create({'value': 3, 'str': 'record0'})
        record1 = self.env['export.many2many.other'].create({'value': 44, 'str': 'record1'})
        record2 = self.env['export.many2many.other'].create({'value': 84, 'str': 'record2'})
        record3 = self.env['export.many2many.other'].create({'value': 9, 'str': 'record3'})

        result = self.import_(['value/id'], [
            ['%s,%s' % (self.xid(record0), self.xid(record1))],
            ['%s' % self.xid(record3)],
            ['%s,%s' % (self.xid(record2), self.xid(record1))],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 3)

        b = self.browse()
        self.assertCountEqual(values(b[0].value), [3, 44])
        self.assertCountEqual(values(b[2].value), [44, 84])

    def test_noxids(self):
        result = self.import_(['value/id'], [['noxidforthat']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for external id 'noxidforthat' in field"
            u" 'Value'", moreinfo=moreaction(
                res_model='ir.model.data', domain=[('model', '=', 'export.many2many.other')]),
            field_name='Value', field_path=['value', 'id'], field_type='external id', value='noxidforthat')])
        self.assertIs(result['ids'], False)

    def test_names(self):
        record0 = self.env['export.many2many.other'].create({'value': 3, 'str': 'record0'})
        record1 = self.env['export.many2many.other'].create({'value': 44, 'str': 'record1'})
        record2 = self.env['export.many2many.other'].create({'value': 84, 'str': 'record2'})
        record3 = self.env['export.many2many.other'].create({'value': 9, 'str': 'record3'})

        name = lambda record: record.display_name

        result = self.import_(['value'], [
            ['%s,%s' % (name(record1), name(record2))],
            ['%s,%s,%s' % (name(record0), name(record1), name(record2))],
            ['%s,%s' % (name(record0), name(record3))],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 3)

        b = self.browse()
        self.assertEqual(values(b[1].value), [3, 44, 84])
        self.assertEqual(values(b[2].value), [3, 9])

    def test_nonames(self):
        result = self.import_(['value'], [['wherethem2mhavenonames']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name 'wherethem2mhavenonames' in "
            u"field 'Value'", moreinfo=moreaction(
                res_model='export.many2many.other'),
            field_name='Value', field_path=['value'], field_type="name", value='wherethem2mhavenonames')])
        self.assertIs(result['ids'], False)

    def test_import_to_existing(self):
        id1 = self.env['export.many2many.other'].create({'value': 3, 'str': 'record0'}).id
        id2 = self.env['export.many2many.other'].create({'value': 44, 'str': 'record1'}).id
        id3 = self.env['export.many2many.other'].create({'value': 84, 'str': 'record2'}).id
        id4 = self.env['export.many2many.other'].create({'value': 9, 'str': 'record3'}).id

        xid = 'myxid'
        result = self.import_(['id', 'value/.id'], [[xid, '%d,%d' % (id1, id2)]])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)
        result = self.import_(['id', 'value/.id'], [[xid, '%d,%d' % (id3, id4)]])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        b = self.browse()
        self.assertEqual(len(b), 1)
        # TODO: replacement of existing m2m values is correct?
        self.assertEqual(values(b[0].value), [84, 9])


class test_o2m(ImporterCase):
    model_name = 'export.one2many'

    def test_name_get(self):
        s = u'Java is a DSL for taking large XML files and converting them ' \
            u'to stack traces'
        result = self.import_(
            ['const', 'value'],
            [['5', s]])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name '%s' in field 'Value'" % s[:50],
            moreinfo=moreaction(res_model='export.one2many.child'),
            field_name='Value', field_path=['value'], field_type='name', value=s[:50])])
        self.assertIs(result['ids'], False)

    def test_single(self):
        result = self.import_(['const', 'value/value'], [
            ['5', '63']
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        (b,) = self.browse()
        self.assertEqual(b.const, 5)
        self.assertEqual(values(b.value), [63])

    def test_multicore(self):
        result = self.import_(['const', 'value/value'], [
            ['5', '63'],
            ['6', '64'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 2)

        b1, b2 = self.browse()
        self.assertEqual(b1.const, 5)
        self.assertEqual(values(b1.value), [63])
        self.assertEqual(b2.const, 6)
        self.assertEqual(values(b2.value), [64])

    def test_multisub(self):
        result = self.import_(['const', 'value/value'], [
            ['5', '63'],
            ['', '64'],
            ['', '65'],
            ['', '66'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        (b,) = self.browse()
        self.assertEqual(set(values(b.value)), set([63, 64, 65, 66]))

    def test_multisub_nogap(self):
        result = self.import_(['const', 'value/value'], [
            ['5', '63'],
            ['5', '64'],
            ['5', '65'],
            ['5', '66'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        (b,) = self.browse()
        self.assertEqual(set(values(b.value)), set([63, 64, 65, 66]))

    def test_multi_subfields(self):
        result = self.import_(['value/str', 'const', 'value/value'], [
            ['this', '5', '63'],
            ['is', '', '64'],
            ['the', '', '65'],
            ['rhythm', '', '66'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        (b,) = self.browse()
        self.assertEqual(set(values(b.value.sorted())), set([63, 64, 65, 66]))
        self.assertEqual(
            values(b.value.sorted(), 'str'),
            'this is the rhythm'.split())

    def test_multi_subfields_nogap(self):
        result = self.import_(['value/str', 'const', 'value/value'], [
            ['of', '5', '63'],
            ['the', '5', '64'],
            ['night', '5', '65'],
            ['oh-yeah', '5', '66'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        (b,) = self.browse()
        self.assertEqual(set(values(b.value.sorted())), set([63, 64, 65, 66]))
        self.assertEqual(
            values(b.value.sorted(), 'str'),
            'of the night oh-yeah'.split())

    def test_subfields_fail_by_implicit_id(self):
        result = self.import_(['value/parent_id'], [['noxidforthat']])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name 'noxidforthat' in field 'Value/Parent'",
            moreinfo=moreaction(res_model='export.one2many'),
            field_name='Value', field_path=['value', 'parent_id'], field_type='name', value='noxidforthat')])
        self.assertIs(result['ids'], False)

    def test_link_inline(self):
        """ m2m-style specification for o2ms
        """
        id1 = self.env['export.one2many.child'].create({'str': 'Bf', 'value': 109}).id
        id2 = self.env['export.one2many.child'].create({'str': 'Me', 'value': 262}).id

        result = self.import_(['const', 'value/.id'], [
            ['42', '%d,%d' % (id1, id2)]
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        [b] = self.browse()
        self.assertEqual(b.const, 42)
        # automatically forces link between core record and o2ms
        self.assertEqual(set(values(b.value)), set([109, 262]))
        self.assertEqual(values(b.value, field='parent_id'), [b, b])

    def test_link(self):
        """ O2M relating to an existing record (update) force a LINK_TO as well
        """
        id1 = self.env['export.one2many.child'].create({'str': 'Bf', 'value': 109}).id
        id2 = self.env['export.one2many.child'].create({'str': 'Me', 'value': 262}).id

        result = self.import_(['const', 'value/.id'], [
            ['42', str(id1)],
            ['', str(id2)],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        [b] = self.browse()
        self.assertEqual(b.const, 42)
        # automatically forces link between core record and o2ms
        self.assertCountEqual(values(b.value), [109, 262])
        self.assertEqual(values(b.value, field='parent_id'), [b, b])

    def test_link_2(self):
        id1 = self.env['export.one2many.child'].create({'str': 'Bf', 'value': 109}).id
        id2 = self.env['export.one2many.child'].create({'str': 'Me', 'value': 262}).id

        result = self.import_(['const', 'value/.id', 'value/value'], [
            ['42', str(id1), '1'],
            ['', str(id2), '2'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        [b] = self.browse()
        self.assertEqual(b.const, 42)
        self.assertEqual(set(values(b.value)), set([1, 2]))
        self.assertEqual(values(b.value, field='parent_id'), [b, b])

    def test_o2m_repeated_with_xids(self):
        # concern: formerly this would link existing records, and fault if
        # the records did not exist. This is more in line with other XID uses,
        # however it does make thing work where they'd previously fail for
        # well-defined reasons.
        result = self.import_(['id', 'const', 'value/id', 'value/value'], [
            ['a', '5', 'aa', '11'],
            ['', '', 'ab', '12'],
            ['', '', 'ac', '13'],
            ['', '', 'ad', '14'],
            ['b', '10', 'ba', '15'],
            ['', '', 'bb', '16'],
        ])
        self.assertFalse(result['messages'])
        result = self.import_(['id', 'const', 'value/id', 'value/value'], [
            ['a', '5', 'aa', '11'],
            ['', '', 'ab', '12'],
            ['', '', 'ac', '13'],
            ['', '', 'ad', '14'],
            ['b', '8', 'ba', '25'],
            ['', '', 'bb', '16'],
        ])
        self.assertFalse(result['messages'])

        [a, b] = self.browse().sorted(lambda r: r.const)
        self.assertEqual(len(a.value), 4)
        self.assertEqual(len(b.value), 2)
        self.assertEqual(b.const, 8)
        self.assertEqual(b.value.mapped('value'), [25, 16])

    def test_name_create_enabled_m2o_in_o2m(self):
        result = self.import_(['value/m2o'], [[101]])
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name '101' "
            u"in field 'Value/M2O'", moreinfo=moreaction(
                res_model='export.integer'),
            field_name='Value', field_path=['value', 'm2o'], field_type='name', value=101)])
        self.assertEqual(result['ids'], False)
        context = {
            'name_create_enabled_fields': {'value/m2o': True},
        }
        result = self.import_(['value/m2o'], [[101]], context=context)
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)
        [b] = self.browse()
        self.assertEqual(b.value.m2o.value, 101)


class test_o2m_multiple(ImporterCase):
    model_name = 'export.one2many.multiple'

    def test_multi_mixed(self):
        result = self.import_(['const', 'child1/value', 'child2/value'], [
            ['5', '11', '21'],
            ['', '12', '22'],
            ['', '13', '23'],
            ['', '14', ''],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        [b] = self.browse()
        self.assertEqual(set(values(b.child1)), set([11, 12, 13, 14]))
        self.assertEqual(set(values(b.child2)), set([21, 22, 23]))

    def test_multi(self):
        result = self.import_(['const', 'child1/value', 'child2/value'], [
            ['5', '11', '21'],
            ['', '12', ''],
            ['', '13', ''],
            ['', '14', ''],
            ['', '', '22'],
            ['', '', '23'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        [b] = self.browse()
        self.assertEqual(set(values(b.child1)), set([11, 12, 13, 14]))
        self.assertEqual(set(values(b.child2)), set([21, 22, 23]))

    def test_multi_fullsplit(self):
        result = self.import_(['const', 'child1/value', 'child2/value'], [
            ['5', '11', ''],
            ['', '12', ''],
            ['', '13', ''],
            ['', '14', ''],
            ['', '', '21'],
            ['', '', '22'],
            ['', '', '23'],
        ])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

        [b] = self.browse()
        self.assertEqual(b.const, 5)
        self.assertEqual(set(values(b.child1)), set([11, 12, 13, 14]))
        self.assertEqual(set(values(b.child2)), set([21, 22, 23]))


class test_realworld(SavepointCaseWithUserDemo):

    @classmethod
    def setUpClass(cls):
        super(test_realworld, cls).setUpClass()
        cls._load_partners_set()

    def test_bigfile(self):
        data = json.loads(pkgutil.get_data(self.__module__, 'contacts_big.json').decode('utf-8'))
        result = self.env['res.partner'].load(['name', 'mobile', 'email', 'image_1920'], data)
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), len(data))

    def test_backlink(self):
        fnames = ["name", "type", "street", "city", "country_id", "category_id",
                  "is_company", "parent_id"]
        data = json.loads(pkgutil.get_data(self.__module__, 'contacts.json').decode('utf-8'))
        result = self.env['res.partner'].load(fnames, data)
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), len(data))

    def test_recursive_o2m(self):
        """ The content of the o2m field's dict needs to go through conversion
        as it may be composed of convertables or other relational fields
        """
        self.env['ir.model.data'].clear_caches()
        Model = self.env['export.one2many.recursive']
        result = Model.load(
            ['value', 'child/const', 'child/child1/str', 'child/child2/value'],
            [
                ['4', '42', 'foo', '55'],
                ['', '43', 'bar', '56'],
                ['', '', 'baz', ''],
                ['', '55', 'qux', '57'],
                ['5', '99', 'wheee', ''],
                ['', '98', '', '12'],
            ],
        )

        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 2)

        b = Model.browse(result['ids'])
        self.assertEqual((b[0].value, b[1].value), (4, 5))

        self.assertEqual([child.str for child in b[0].child.sorted()[1].child1],
                         ['bar', 'baz'])
        self.assertFalse(len(b[1].child.sorted()[1].child1))
        self.assertEqual([child.value for child in b[1].child.sorted()[1].child2],
                         [12])

    def test_o2m_subfields_fail_by_implicit_id(self):
        self.env['ir.model.data'].clear_caches()
        Model = self.env['export.one2many.recursive']
        result = Model.with_context(import_file=True).load(
            ['child/child1/parent_id'],
            [['5'],],
        )
        self.assertEqual(result['messages'], [message(
            u"No matching record found for name '5' in field 'Child/Child1/Parent'", field='child',
            moreinfo=moreaction(res_model='export.one2many.multiple'),
            field_name='Child', field_path=['child', 'child1', 'parent_id'], field_type='name', value='5')])
        self.assertIs(result['ids'], False)


class test_date(ImporterCase):
    model_name = 'export.date'

    def test_empty(self):
        self.assertEqual(
            self.import_(['value'], []),
            {'ids': [], 'messages': [], 'nextrow': False})

    def test_basic(self):
        result = self.import_(['value'], [['2012-02-03']])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

    def test_invalid(self):
        result = self.import_(['value'], [['not really a date']])
        self.assertEqual(result['messages'], [
            message(u"'not really a date' does not seem to be a valid date "
                    u"for field 'Value'",
                    moreinfo=u"Use the format '2012-12-31'", field_name='Value', field_path=['value'])])
        self.assertIs(result['ids'], False)


class test_datetime(ImporterCase):
    model_name = 'export.datetime'

    def test_empty(self):
        self.assertEqual(
            self.import_(['value'], []),
            {'ids': [], 'messages': [], 'nextrow': False})

    def test_basic(self):
        result = self.import_(['value'], [['2012-02-03 11:11:11']])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)

    def test_invalid(self):
        result = self.import_(['value'], [['not really a datetime']])
        self.assertEqual(result['messages'], [
            message(u"'not really a datetime' does not seem to be a valid "
                    u"datetime for field 'Value'",
                    moreinfo=u"Use the format '2012-12-31 23:59:59'", field_name='Value', field_path=['value'])])
        self.assertIs(result['ids'], False)

    def test_checktz1(self):
        """ Imported date should be interpreted as being in the tz provided by
        the context
        """
        # write dummy tz in user (Asia/Hovd UTC+0700), should be superseded by
        # context
        self.env.user.write({'tz': 'Asia/Hovd'})

        # UTC+1400
        result = self.import_(
            ['value'], [['2012-02-03 11:11:11']], context={'tz': 'Pacific/Kiritimati'})
        self.assertFalse(result['messages'])
        self.assertEqual(
            [fields.Datetime.to_string(value['value']) for value in self.read(domain=[('id', 'in', result['ids'])])],
            ['2012-02-02 21:11:11'])

        # UTC-0930
        result = self.import_(
            ['value'], [['2012-02-03 11:11:11']], context={'tz': 'Pacific/Marquesas'})
        self.assertFalse(result['messages'])
        self.assertEqual(
            [fields.Datetime.to_string(value['value']) for value in self.read(domain=[('id', 'in', result['ids'])])],
            ['2012-02-03 20:41:11'])

    def test_usertz(self):
        """ If the context does not hold a timezone, the importing user's tz
        should be used
        """
        # UTC +1000
        self.env.user.write({'tz': 'Asia/Yakutsk'})

        result = self.import_(
            ['value'], [['2012-02-03 11:11:11']])
        self.assertFalse(result['messages'])
        self.assertEqual(
            [fields.Datetime.to_string(value['value']) for value in self.read(domain=[('id', 'in', result['ids'])])],
            ['2012-02-03 01:11:11'])

    def test_notz(self):
        """ If there is no tz either in the context or on the user, falls back
        to UTC
        """
        self.env.user.write({'tz': False})

        result = self.import_(['value'], [['2012-02-03 11:11:11']])
        self.assertFalse(result['messages'])
        self.assertEqual(
            [fields.Datetime.to_string(value['value']) for value in self.read(domain=[('id', 'in', result['ids'])])],
            ['2012-02-03 11:11:11'])


class test_unique(ImporterCase):
    model_name = 'export.unique'

    @mute_logger('odoo.sql_db')
    def test_unique(self):
        result = self.import_(['value'], [
            ['1'],
            ['1'],
            ['2'],
            ['3'],
            ['3'],
        ])
        self.assertFalse(result['ids'])
        self.assertEqual(result['messages'], [
            dict(message=u"The value for the field 'value' already exists "
                         u"(this is probably 'Value' in the current model).",
                 type='error', rows={'from': 1, 'to': 1},
                 record=1, field='value'),
            dict(message=u"The value for the field 'value' already exists "
                         u"(this is probably 'Value' in the current model).",
                 type='error', rows={'from': 4, 'to': 4},
                 record=4, field='value'),
        ])

    @mute_logger('odoo.sql_db')
    def test_unique_pair(self):
        result = self.import_(['value2', 'value3'], [
            ['0', '1'],
            ['1', '0'],
            ['1', '1'],
            ['1', '1'],
        ])
        self.assertFalse(result['ids'])
        self.assertEqual(len(result['messages']), 1)
        message = result['messages'][0]
        self.assertEqual(message['type'], 'error')
        self.assertEqual(message['record'], 3)
        self.assertEqual(message['rows'], {'from': 3, 'to': 3})
        m = re.match(
            r"The values for the fields '([^']+)' already exist "
            r"\(they are probably '([^']+)' in the current model\)\.",
            message['message']
        )
        self.assertIsNotNone(m)
        self.assertItemsEqual(
            m.group(1).split(', '),
            ['value2', 'value3']
        )
        self.assertItemsEqual(
            m.group(2).split(', '),
            ['Value2', 'Value3']
        )

class test_inherits(ImporterCase):
    """ The import process should only assign a new xid (derived from the
    childs') if the child is being created and triggers the creation of the
    parent
    """
    model_name = 'export.inherits.child'
    def test_create_no_parent(self):
        r = self.import_(['id', 'value_parent', 'value'], [
            ['xxx.child', '0', '1'],
        ])
        rec = self.env[self.model_name].browse(r['ids'])

        self.assertEqual(rec.value_parent, 0)
        self.assertEqual(rec.value, 1)
        self.assertEqual(rec.parent_id.value_parent, 0)
        self.assertEqual(
            rec._get_external_ids()[rec.id],
            ['xxx.child'],
        )
        self.assertEqual(
            rec.parent_id._get_external_ids()[rec.parent_id.id],
            ['xxx.child_export_inherits_parent'],
        )

    def test_create_parent_no_xid(self):
        parent = self.env['export.inherits.parent'].create({'value_parent': 0})
        r = self.import_(['id', 'parent_id/.id', 'value'], [
            ['xxx.child', str(parent.id), '1'],
        ])
        rec = self.env[self.model_name].browse(r['ids'])
        self.assertEqual(rec.value_parent, 0)
        self.assertEqual(rec.parent_id, parent)

        self.assertEqual(
            rec._get_external_ids()[rec.id],
            ['xxx.child'],
        )
        self.assertEqual(
            rec.parent_id._get_external_ids()[rec.parent_id.id],
            [],
            "no xid should be created for the parent"
        )

    def test_create_parent_with_xid(self):
        parent = self.env['export.inherits.parent'].create({'value_parent': 0})
        pid = self.env['ir.model.data'].create({
            'model': 'export.inherits.parent',
            'res_id': parent.id,
            'module': 'xxx',
            'name': 'parent',
        })
        r = self.import_(['id', 'parent_id/.id', 'value'], [
            ['xxx.child', str(parent.id), '1'],
        ])
        rec = self.env[self.model_name].browse(r['ids'])
        self.assertEqual(rec.value_parent, 0)
        self.assertEqual(rec.parent_id, parent)
        self.assertTrue(pid.exists().res_id, parent.id)

        self.assertEqual(
            rec._get_external_ids()[rec.id],
            ['xxx.child'],
        )
        self.assertEqual(
            rec.parent_id._get_external_ids()[rec.parent_id.id],
            ['xxx.parent'],
        )

    def test_create_parent_by_xid(self):
        parent = self.env['export.inherits.parent'].create({'value_parent': 0})
        pid = self.env['ir.model.data'].create({
            'model': 'export.inherits.parent',
            'res_id': parent.id,
            'module': 'xxx',
            'name': 'parent',
        })
        r = self.import_(['id', 'parent_id/id', 'value'], [
            ['xxx.child', 'xxx.parent', '1'],
        ])
        rec = self.env[self.model_name].browse(r['ids'])
        self.assertEqual(rec.value_parent, 0)
        self.assertEqual(rec.parent_id, parent)
        self.assertTrue(pid.exists().res_id, parent.id)

        self.assertEqual(
            rec._get_external_ids()[rec.id],
            ['xxx.child'],
        )
        self.assertEqual(
            rec.parent_id._get_external_ids()[rec.parent_id.id],
            ['xxx.parent'],
        )

    def test_update_parent_no_xid(self):
        parent = self.env['export.inherits.parent'].create({'value_parent': 0})
        child = self.env[self.model_name].create({
            'parent_id': parent.id,
            'value': 1,
        })
        self.env['ir.model.data'].create({
            'model': self.model_name,
            'res_id': child.id,
            'module': 'xxx',
            'name': 'child'
        })

        self.import_(['id', 'value'], [
            ['xxx.child', '42']
        ])
        self.assertEqual(child.value, 42)
        self.assertEqual(child.parent_id, parent)

        self.assertEqual(
            child._get_external_ids()[child.id],
            ['xxx.child'],
        )
        self.assertEqual(
            parent._get_external_ids()[parent.id],
            [],
        )

    def test_update_parent_with_xid(self):
        parent = self.env['export.inherits.parent'].create({'value_parent': 0})
        child = self.env[self.model_name].create({
            'parent_id': parent.id,
            'value': 1,
        })
        pid, cid = self.env['ir.model.data'].create([{
            'model': 'export.inherits.parent',
            'res_id': parent.id,
            'module': 'xxx',
            'name': 'parent',
        }, {
            'model': self.model_name,
            'res_id': child.id,
            'module': 'xxx',
            'name': 'child'
        }])

        self.import_(['id', 'value'], [
            ['xxx.child', '42']
        ])
        self.assertEqual(child.value, 42)
        self.assertEqual(child.parent_id, parent)
        self.assertEqual(pid.exists().res_id, parent.id)
        self.assertEqual(cid.exists().res_id, child.id)

        self.assertEqual(
            child._get_external_ids()[child.id],
            ['xxx.child'],
        )
        self.assertEqual(
            parent._get_external_ids()[parent.id],
            ['xxx.parent'],
        )

class test_no_xid_int(ImporterCase):
    model_name = 'export.id.int'

    def setUp(self):
        super().setUp()
        self.existing = self.model.create({'const': 7, 'value': 3})

    def test_update(self):
        result = self.import_(['const', 'value'], [['8', '3']], keys=['value'])
        self.assertFalse(result['messages'])
        self.assertEqual(len(result['ids']), 1)
        self.assertEqual(self.existing.const, 8)

    def test_invalid_key(self):
        result = self.import_(['const', 'value'], [['8', '3']], keys=['const'])
        self.assertEqual(values(self.read()), [3, 3])

    def test_create_update(self):
        data = [
                ['8', '3'],
                ['9', '4']
            ]
        result = self.import_(['const', 'value'], data, keys=['value'])
        for index, record in enumerate(self.browse()):
            self.assertEqual(record.const, int(data[index][0]))
            self.assertEqual(record.value, int(data[index][1]))

    def test_empty_keys(self):
        result = self.import_(['const', 'value'], [
                ['8', ''],
                ['9', '']
            ], keys=['value'])
        self.assertEqual(len(self.browse()), 3)

    def test_multi_match(self):
        self.model.create({'const': 100, 'value': 3})
        with self.assertRaises(ValidationError):
            result = self.import_(['const', 'value'], [['8', '3']], keys=['value'])

# class test_multi_key(ImporterCase):
#     model_name = 'export.multi.key'

# class test_no_xid_char(ImporterCase):
#     model_name = 'export.o2m.key'

# class test_no_xid_o2m(ImporterCase):
#     model_name = 'export.o2m.key'
