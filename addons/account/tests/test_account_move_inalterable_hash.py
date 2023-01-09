from unittest.mock import patch

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.models import Model
from odoo.tests import tagged
from odoo import fields, _, Command
from odoo.exceptions import UserError
from odoo.tools import format_date


@tagged('post_install', '-at_install')
class TestAccountMoveInalterableHash(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.move1 = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.from_string('2021-01-01'),
            'company_id': cls.company_data['company'].id,
            'date': fields.Date.from_string('2021-01-01'),
            'partner_id': cls.partner_a.id,
            'invoice_line_ids': [
                Command.create({
                    'product_id': cls.product_a.id,
                    'quantity': 2.0,
                    'price_unit': 1000.0,
                    'tax_ids': [],
                }),
            ],
        })

    def test_account_move_get_dict_fields_values_to_hash(self):
        """
        Knowing that:
        account.move()._get_inalterable_fields() = ['name', 'date', 'journal_id']
        account.move.line()._get_inalterable_fields() = ['debit', 'credit', 'account_id', 'partner_id']
        //!\\ This test should probably not be modified as it makes sure that the
        computation of the hash is not altered between versions which would break
        the inalterability hash report.
        """
        dict_to_hash = self.move1._get_dict_fields_values_to_hash(self.move1.line_ids)
        line1 = self.move1.line_ids[0]
        line2 = self.move1.line_ids[1]
        self.assertEqual(dict_to_hash, {
            'date': str(self.move1.date),
            'journal_id': str(self.move1.journal_id.id),
            'company_id': str(self.move1.company_id.id),
            f'line_{line1.id}_debit': '0.0',
            f'line_{line2.id}_debit': '2000.0',
            f'line_{line1.id}_credit': '2000.0',
            f'line_{line2.id}_credit': '0.0',
            f'line_{line1.id}_account_id': str(line1.account_id.id),
            f'line_{line2.id}_account_id': str(line2.account_id.id),
            f'line_{line1.id}_partner_id': str(self.move1.partner_id.id),
            f'line_{line2.id}_partner_id': str(self.move1.partner_id.id),
        })

    def test_account_move_inalterable_hash(self):
        """Test that we cannot alter a field used for the computation of the inalterable hash"""
        self.company_data['default_journal_sale'].restrict_mode_hash_table = True
        self.move1.action_post()

        expected_error_msg = "You cannot edit the following fields due to restrict mode being activated.*"

        with self.assertRaisesRegex(UserError, f"{expected_error_msg} Inalterable hash"):
            self.move1['inalterable_hash'] = 'fake_hash'
        with self.assertRaisesRegex(UserError, f"{expected_error_msg}Inalteralbile no-gap sequence number"):
            self.move1['secure_sequence_number'] = 666
        with self.assertRaisesRegex(UserError, f"{expected_error_msg} Date"):
            self.move1['date'] = fields.Date.from_string('2022-01-02')
        with self.assertRaisesRegex(UserError, f"{expected_error_msg} Company"):
            self.move1['company_id'] = 666
        with self.assertRaisesRegex(UserError, f"{expected_error_msg} Company.*Date|Date.*Company"):
            self.move1.write({
                'company_id': 666,
                'date': fields.Date.from_string('2022-01-03')
            })

        with self.assertRaisesRegex(UserError, f"{expected_error_msg} Account"):
            self.move1.line_ids[0]['account_id'] = self.move1.line_ids[1]['account_id']
        with self.assertRaisesRegex(UserError, f"{expected_error_msg} Partner"):
            self.move1.line_ids[0]['partner_id'] = 666

        # The following fields are not part of the hash so they can be modified
        self.move1['name'] = 'new_name'
        self.move1.line_ids[0]['discount_percentage'] = 10

    def test_account_move_hash_integrity_report(self):
        """Test the hash integrity report"""
        self.company_data['default_journal_sale'].restrict_mode_hash_table = True
        moves = self.env['account.move']

        # No record yet
        move_type_check = self.env['report.account.report_journals_hash_integrity']._check_hash_integrity(True, moves, 'date')
        self.assertEqual(move_type_check['status'], 'no_record')
        self.assertEqual(move_type_check['msg'], _("There isn't any record flagged for data inalterability."))

        # Everything should be correctly hashed and verified
        moves |= (
            self.init_invoice("out_invoice", self.partner_a, "2022-01-01")
            | self.init_invoice("out_invoice", self.partner_b, "2022-01-02")
            | self.init_invoice("out_invoice", self.partner_a, "2022-01-03")
            | self.init_invoice("out_invoice", self.partner_b, "2022-01-04")
            | self.init_invoice("out_invoice", self.partner_a, "2022-01-05")
        )
        moves.action_post()
        move_type_check = self.env['report.account.report_journals_hash_integrity']._check_hash_integrity(True, moves, 'date')
        self.assertEqual(move_type_check['status'], 'verified')
        self.assertEqual(move_type_check['first_date'], format_date(self.env, fields.Date.to_string(moves[0].date)))
        self.assertEqual(move_type_check['last_date'], format_date(self.env, fields.Date.to_string(moves[-1].date)))

        # Let's change one of the fields used by the hash. It should be detected by the integrity report.
        # We need to bypass the write method of account.move to do so.
        Model.write(moves[2], {'date': fields.Date.from_string('2022-01-07')})
        move_type_check = self.env['report.account.report_journals_hash_integrity']._check_hash_integrity(True, moves, 'date')
        self.assertEqual(move_type_check['status'], 'corrupted')
        self.assertEqual(move_type_check['msg'], _('Corrupted data on record %s with id %s', moves[2].name, moves[2].id))

        # Let's try with the inalterable_hash field itself
        Model.write(moves[2], {'date': fields.Date.from_string("2022-01-03")})  # Revert the previous change
        Model.write(moves[-1], {'inalterable_hash': 'fake_hash'})
        move_type_check = self.env['report.account.report_journals_hash_integrity']._check_hash_integrity(True, moves, 'date')
        self.assertEqual(move_type_check['status'], 'corrupted')
        self.assertEqual(move_type_check['msg'], _('Corrupted data on record %s with id %s', moves[-1].name, moves[-1].id))
