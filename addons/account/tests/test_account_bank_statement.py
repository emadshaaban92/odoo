# -*- coding: utf-8 -*-
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.exceptions import ValidationError, UserError
from odoo import fields, Command


@tagged('post_install', '-at_install')
class TestAccountBankStatementLine(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        # We need a third currency as you could have a company's currency != journal's currency !=
        cls.currency_data_2 = cls.setup_multi_currency_data(default_values={
            'name': 'Dark Chocolate Coin',
            'symbol': '🍫',
            'currency_unit_label': 'Dark Choco',
            'currency_subunit_label': 'Dark Cacao Powder',
        }, rate2016=6.0, rate2017=4.0)
        cls.currency_data_3 = cls.setup_multi_currency_data(default_values={
            'name': 'Black Chocolate Coin',
            'symbol': '🍫',
            'currency_unit_label': 'Black Choco',
            'currency_subunit_label': 'Black Cacao Powder',
        }, rate2016=12.0, rate2017=8.0)

        cls.bank_journal_1 = cls.company_data['default_journal_bank']
        cls.bank_journal_2 = cls.bank_journal_1.copy()
        cls.bank_journal_3 = cls.bank_journal_2.copy()
        cls.currency_1 = cls.company_data['currency']
        cls.currency_2 = cls.currency_data['currency']
        cls.currency_3 = cls.currency_data_2['currency']
        cls.currency_4 = cls.currency_data_3['currency']

        cls.statement_line = cls.env['account.bank.statement.line'].create({
            'journal_id': cls.bank_journal_1.id,
            'date': '2019-01-01',
            'payment_ref': 'line_1',
            'partner_id': cls.partner_a.id,
            'foreign_currency_id': cls.currency_2.id,
            'amount': 1250.0,
            'amount_currency': 2500.0,
        })

        cls.expected_st_line = {
            'date': fields.Date.from_string('2019-01-01'),
            'journal_id': cls.statement_line.journal_id.id,
            'payment_ref': 'line_1',
            'partner_id': cls.partner_a.id,
            'currency_id': cls.currency_1.id,
            'foreign_currency_id': cls.currency_2.id,
            'amount': 1250.0,
            'amount_currency': 2500.0,
            'is_reconciled': False,
        }

        cls.expected_bank_line = {
            'name': cls.statement_line.payment_ref,
            'partner_id': cls.statement_line.partner_id.id,
            'currency_id': cls.currency_1.id,
            'account_id': cls.statement_line.journal_id.default_account_id.id,
            'debit': 1250.0,
            'credit': 0.0,
            'amount_currency': 1250.0,
        }

        cls.expected_counterpart_line = {
            'name': cls.statement_line.payment_ref,
            'partner_id': cls.statement_line.partner_id.id,
            'currency_id': cls.currency_2.id,
            'account_id': cls.statement_line.journal_id.suspense_account_id.id,
            'debit': 0.0,
            'credit': 1250.0,
            'amount_currency': -2500.0,
        }

    def assertBankStatementLine(self, statement_line, expected_statement_line_vals, expected_move_line_vals):
        self.assertRecordValues(statement_line, [expected_statement_line_vals])
        self.assertRecordValues(statement_line.line_ids.sorted('balance'), expected_move_line_vals)

    def create_bank_transaction(self,
                                amount,
                                date,
                                amount_currency=None,
                                currency_id=None,
                                statement_id=None,
                                partner_id=None,
                                journal_id=None,
                                sequence=0):
        values = {
            'payment_ref': str(amount),
            'amount': amount,
            'date': date,
            'partner_id': partner_id,
            'sequence': sequence,
        }
        if amount_currency:
            values['amount_currency'] = amount_currency
            values['foreign_currency_id'] = currency_id
        if statement_id and journal_id and statement_id.journal_id != journal_id:
            raise(ValidationError("The statement and the journal are contradictory"))
        if statement_id:
            values['journal_id'] = statement_id.journal_id.id
            values['statement_id'] = statement_id.id
        if journal_id:
            values['journal_id'] = journal_id.id
        return self.env['account.bank.statement.line'].create(values)
    # -------------------------------------------------------------------------
    # TESTS about the statement line model.
    # -------------------------------------------------------------------------

    def _test_statement_line_edition(
            self,
            journal,
            amount, amount_currency,
            journal_currency, foreign_currency,
            expected_liquidity_values, expected_counterpart_values):
        ''' Test the edition of a statement line from itself or from its linked journal entry.
        :param journal:                     The account.journal record that will be set on the statement line.
        :param amount:                      The amount in journal's currency.
        :param amount_currency:             The amount in the foreign currency.
        :param journal_currency:            The journal's currency as a res.currency record.
        :param foreign_currency:            The foreign currency as a res.currency record.
        :param expected_liquidity_values:   The expected account.move.line values for the liquidity line.
        :param expected_counterpart_values: The expected account.move.line values for the counterpart line.
        '''
        if journal_currency:
            journal.currency_id = journal_currency.id

        statement_line = self.env['account.bank.statement.line'].create({
            'date': '2019-01-01',
            'journal_id': journal.id,
            'payment_ref': 'line_1',
            'partner_id': self.partner_a.id,
            'foreign_currency_id': foreign_currency and foreign_currency.id,
            'amount': amount,
            'amount_currency': amount_currency,
        })

        # ==== Test the statement line amounts are correct ====
        # If there is a bug in the compute/inverse methods, the amount/amount_currency could be
        # incorrect directly after the creation of the statement line.

        self.assertRecordValues(statement_line, [{
            'amount': amount,
            'amount_currency': amount_currency,
        }])
        self.assertRecordValues(statement_line.move_id, [{
            'partner_id': self.partner_a.id,
            'currency_id': (statement_line.foreign_currency_id or statement_line.currency_id).id,
        }])

        # ==== Test the edition of statement line amounts ====
        # The statement line must remain consistent with its account.move.
        # To test the compute/inverse methods are correctly managing all currency setup,
        # we check the edition of amounts in both directions statement line <-> journal entry.

        # Check initial state of the statement line.
        liquidity_lines, suspense_lines, other_lines = statement_line._seek_for_lines()
        self.assertRecordValues(liquidity_lines, [expected_liquidity_values])
        self.assertRecordValues(suspense_lines, [expected_counterpart_values])

        # Check the account.move is still correct after editing the account.bank.statement.line.
        statement_line.write({
            'amount': statement_line.amount * 2,
            'amount_currency': statement_line.amount_currency * 2,
        })
        self.assertRecordValues(statement_line, [{
            'amount': amount * 2,
            'amount_currency': amount_currency * 2,
        }])
        self.assertRecordValues(liquidity_lines, [{
            **expected_liquidity_values,
            'debit': expected_liquidity_values.get('debit', 0.0) * 2,
            'credit': expected_liquidity_values.get('credit', 0.0) * 2,
            'amount_currency': expected_liquidity_values.get('amount_currency', 0.0) * 2,
        }])
        self.assertRecordValues(suspense_lines, [{
            'debit': expected_counterpart_values.get('debit', 0.0) * 2,
            'credit': expected_counterpart_values.get('credit', 0.0) * 2,
            'amount_currency': expected_counterpart_values.get('amount_currency', 0.0) * 2,
        }])

        # Check the account.bank.statement.line is still correct after editing the account.move.
        statement_line.move_id.write({'line_ids': [
            (1, liquidity_lines.id, {
                'debit': expected_liquidity_values.get('debit', 0.0),
                'credit': expected_liquidity_values.get('credit', 0.0),
                'amount_currency': expected_liquidity_values.get('amount_currency', 0.0),
            }),
            (1, suspense_lines.id, {
                'debit': expected_counterpart_values.get('debit', 0.0),
                'credit': expected_counterpart_values.get('credit', 0.0),
                'amount_currency': expected_counterpart_values.get('amount_currency', 0.0),
            }),
        ]})
        self.assertRecordValues(statement_line, [{
            'amount': amount,
            'amount_currency': amount_currency,
        }])

    def _test_edition_customer_and_supplier_flows(
            self,
            amount, amount_currency,
            journal_currency, foreign_currency,
            expected_liquidity_values, expected_counterpart_values):
        ''' Test '_test_statement_line_edition' using the customer (positive amounts)
        & the supplier flow (negative amounts).
        :param amount:                      The amount in journal's currency.
        :param amount_currency:             The amount in the foreign currency.
        :param journal_currency:            The journal's currency as a res.currency record.
        :param foreign_currency:            The foreign currency as a res.currency record.
        :param expected_liquidity_values:   The expected account.move.line values for the liquidity line.
        :param expected_counterpart_values: The expected account.move.line values for the counterpart line.
        '''

        # Check the full process with positive amount (customer process).
        self._test_statement_line_edition(
            self.bank_journal_2,
            amount, amount_currency,
            journal_currency, foreign_currency,
            expected_liquidity_values,
            expected_counterpart_values,
        )

        # Check the full process with negative amount (supplier process).
        self._test_statement_line_edition(
            self.bank_journal_3,
            -amount, -amount_currency,
            journal_currency, foreign_currency,
            {
                **expected_liquidity_values,
                'debit': expected_liquidity_values.get('credit', 0.0),
                'credit': expected_liquidity_values.get('debit', 0.0),
                'amount_currency': -expected_liquidity_values.get('amount_currency', 0.0),
            },
            {
                **expected_counterpart_values,
                'debit': expected_counterpart_values.get('credit', 0.0),
                'credit': expected_counterpart_values.get('debit', 0.0),
                'amount_currency': -expected_counterpart_values.get('amount_currency', 0.0),
            },
        )

    def test_edition_journal_curr_2_statement_curr_3(self):
        self._test_edition_customer_and_supplier_flows(
            80.0,               120.0,
            self.currency_2,    self.currency_3,
            {'debit': 40.0,     'credit': 0.0,      'amount_currency': 80.0,        'currency_id': self.currency_2.id},
            {'debit': 0.0,      'credit': 40.0,     'amount_currency': -120.0,      'currency_id': self.currency_3.id},
        )

    def test_edition_journal_curr_2_statement_curr_1(self):
        self._test_edition_customer_and_supplier_flows(
            120.0,              80.0,
            self.currency_2,    self.currency_1,
            {'debit': 80.0,     'credit': 0.0,      'amount_currency': 120.0,       'currency_id': self.currency_2.id},
            {'debit': 0.0,      'credit': 80.0,     'amount_currency': -80.0,       'currency_id': self.currency_1.id},
        )

    def test_edition_journal_curr_1_statement_curr_2(self):
        self._test_edition_customer_and_supplier_flows(
            # pylint: disable=C0326
            80.0,               120.0,
            self.currency_1,    self.currency_2,
            {'debit': 80.0,     'credit': 0.0,      'amount_currency': 80.0,        'currency_id': self.currency_1.id},
            {'debit': 0.0,      'credit': 80.0,     'amount_currency': -120.0,      'currency_id': self.currency_2.id},
        )

    def test_edition_journal_curr_2_statement_false(self):
        self._test_edition_customer_and_supplier_flows(
            80.0,               0.0,
            self.currency_2,    False,
            {'debit': 40.0,     'credit': 0.0,      'amount_currency': 80.0,        'currency_id': self.currency_2.id},
            {'debit': 0.0,      'credit': 40.0,     'amount_currency': -80.0,       'currency_id': self.currency_2.id},
        )

    def test_edition_journal_curr_1_statement_false(self):
        self._test_edition_customer_and_supplier_flows(
            80.0,               0.0,
            self.currency_1,    False,
            {'debit': 80.0,     'credit': 0.0,      'amount_currency': 80.0,        'currency_id': self.currency_1.id},
            {'debit': 0.0,      'credit': 80.0,     'amount_currency': -80.0,       'currency_id': self.currency_1.id},
        )

    def test_zero_amount_journal_curr_1_statement_curr_2(self):
        self.bank_journal_2.currency_id = self.currency_1

        statement_line = self.env['account.bank.statement.line'].create({
            'journal_id': self.bank_journal_2.id,
            'date': '2019-01-01',
            'payment_ref': 'line_1',
            'partner_id': self.partner_a.id,
            'foreign_currency_id': self.currency_2.id,
            'amount': 0.0,
            'amount_currency': 10.0,
        })

        self.assertRecordValues(statement_line.line_ids, [
            # pylint: disable=C0326
            {'debit': 0.0,      'credit': 0.0,      'amount_currency': 0.0,         'currency_id': self.currency_1.id},
            {'debit': 0.0,      'credit': 0.0,      'amount_currency': -10.0,       'currency_id': self.currency_2.id},
        ])

    def test_zero_amount_currency_journal_curr_1_statement_curr_2(self):
        self.bank_journal_2.currency_id = self.currency_1

        statement_line = self.env['account.bank.statement.line'].create({
            'journal_id': self.bank_journal_2.id,
            'date': '2019-01-01',
            'payment_ref': 'line_1',
            'partner_id': self.partner_a.id,
            'foreign_currency_id': self.currency_2.id,
            'amount': 10.0,
            'amount_currency': 0.0,
        })

        self.assertRecordValues(statement_line.move_id.line_ids, [
            # pylint: disable=C0326
            {'debit': 10.0,     'credit': 0.0,      'amount_currency': 10.0,        'currency_id': self.currency_1.id},
            {'debit': 0.0,      'credit': 10.0,     'amount_currency': 0.0,         'currency_id': self.currency_2.id},
        ])

    def test_zero_amount_journal_curr_2_statement_curr_1(self):
        self.bank_journal_2.currency_id = self.currency_2

        statement_line = self.env['account.bank.statement.line'].create({
            'journal_id': self.bank_journal_2.id,
            'date': '2019-01-01',
            'payment_ref': 'line_1',
            'partner_id': self.partner_a.id,
            'foreign_currency_id': self.currency_1.id,
            'amount': 0.0,
            'amount_currency': 10.0,
        })

        self.assertRecordValues(statement_line.move_id.line_ids, [
            {'debit': 10.0,     'credit': 0.0,      'amount_currency': 0.0,         'currency_id': self.currency_2.id},
            {'debit': 0.0,      'credit': 10.0,     'amount_currency': -10.0,       'currency_id': self.currency_1.id},
        ])

    def test_zero_amount_currency_journal_curr_2_statement_curr_1(self):
        self.bank_journal_2.currency_id = self.currency_2

        statement_line = self.env['account.bank.statement.line'].create({
            'journal_id': self.bank_journal_2.id,
            'date': '2019-01-01',
            'payment_ref': 'line_1',
            'partner_id': self.partner_a.id,
            'foreign_currency_id': self.currency_1.id,
            'amount': 10.0,
            'amount_currency': 0.0,
        })

        self.assertRecordValues(statement_line.move_id.line_ids, [
            {'debit': 0.0,      'credit': 0.0,      'amount_currency': 10.0,        'currency_id': self.currency_2.id},
            {'debit': 0.0,      'credit': 0.0,      'amount_currency': 0.0,         'currency_id': self.currency_1.id},
        ])

    # def test_zero_amount_journal_curr_2_statement_curr_3(self):
    #     self.bank_journal_2.currency_id = self.currency_2
    #
    #     statement_line = self.env['account.bank.statement'].create({
    #         'journal_id': self.bank_journal_2.id,
    #         'date': '2019-01-01',
    #         'payment_ref': 'line_1',
    #         'partner_id': self.partner_a.id,
    #         'foreign_currency_id': self.currency_3.id,
    #         'amount': 0.0,
    #         'amount_currency': 10.0,
    #     })
    #
    #     self.assertRecordValues(statement_line.move_id.line_ids, [
    #         {'debit': 0.0,      'credit': 0.0,      'amount_currency': 0.0,         'currency_id': self.currency_2.id},
    #         {'debit': 0.0,      'credit': 0.0,      'amount_currency': -10.0,       'currency_id': self.currency_3.id},
    #     ])

    # def test_zero_amount_currency_journal_curr_2_statement_curr_3(self):
    #     self.bank_journal_2.currency_id = self.currency_2
    #
    #     statement_line = self.env['account.bank.statement'].create({
    #         'journal_id': self.bank_journal_2.id,
    #         'date': '2019-01-01',
    #         'payment_ref': 'line_1',
    #         'partner_id': self.partner_a.id,
    #         'foreign_currency_id': self.currency_3.id,
    #         'amount': 10.0,
    #         'amount_currency': 0.0,
    #     })
    #
    #     self.assertRecordValues(statement_line.move_id.line_ids, [
    #         {'debit': 5.0,      'credit': 0.0,      'amount_currency': 10.0,        'currency_id': self.currency_2.id},
    #         {'debit': 0.0,      'credit': 5.0,      'amount_currency': 0.0,         'currency_id': self.currency_3.id},
    #     ])

    def test_constraints(self):
        def assertStatementLineConstraint(statement_line_vals):
            with self.assertRaises(Exception), self.cr.savepoint():
                self.env['account.bank.statement.line'].create(statement_line_vals)

        statement_line_vals = {
            'journal_id': self.bank_journal_2.id,
            'date': '2019-01-01',
            'payment_ref': 'line_1',
            'partner_id': self.partner_a.id,
            'foreign_currency_id': False,
            'amount': 10.0,
            'amount_currency': 0.0,
        }

        # ==== Test constraints at creation ====

        # Foreign currency must not be the same as the journal one.
        assertStatementLineConstraint({
            **statement_line_vals,
            'foreign_currency_id': self.currency_1.id,
        })

        # Can't have a stand alone amount in foreign currency without foreign currency set.
        assertStatementLineConstraint({
            **statement_line_vals,
            'amount_currency': 10.0,
        })

        # ==== Test constraints at edition ====

        st_line = self.env['account.bank.statement.line'].create(statement_line_vals)

        # You can't messed up the journal entry by adding another liquidity line.
        addition_lines_to_create = [
            {
                'debit': 1.0,
                'credit': 0,
                'account_id': self.bank_journal_2.default_account_id.id,
                'move_id': st_line.move_id.id,
            },
            {
                'debit': 0,
                'credit': 1.0,
                'account_id': self.company_data['default_account_revenue'].id,
                'move_id': st_line.move_id.id,
            },
        ]
        with self.assertRaises(UserError), self.cr.savepoint():
            st_line.move_id.write({
                'line_ids': [(0, 0, vals) for vals in addition_lines_to_create]
            })

        with self.assertRaises(UserError), self.cr.savepoint():
            st_line.line_ids.create(addition_lines_to_create)

        # You can't set the journal entry in an unconsistent state.
        # with self.assertRaises(UserError), self.cr.savepoint():
        #     st_line.move_id.action_post()

    def test_statement_line_move_onchange_1(self):
        ''' Test the consistency between the account.bank.statement.line and the generated account.move.lines
        using the form view emulator.
        '''

        # Check the initial state of the statement line.
        self.assertBankStatementLine(self.statement_line, self.expected_st_line, [self.expected_counterpart_line, self.expected_bank_line])

        # Inverse the amount + change them.
        self.statement_line.write({
            'amount': -2000.0,
            'amount_currency': -4000.0,
            'foreign_currency_id': self.currency_3.id,
        })

        self.assertBankStatementLine(self.statement_line, {
            **self.expected_st_line,
            'amount': -2000.0,
            'amount_currency': -4000.0,
            'foreign_currency_id': self.currency_3.id,
        }, [
            {
                **self.expected_bank_line,
                'debit': 0.0,
                'credit': 2000.0,
                'amount_currency': -2000.0,
                'currency_id': self.currency_1.id,
            },
            {
                **self.expected_counterpart_line,
                'debit': 2000.0,
                'credit': 0.0,
                'amount_currency': 4000.0,
                'currency_id': self.currency_3.id,
            },
        ])

        # Check changing the label and the partner.
        self.statement_line.write({
            'payment_ref': 'line_1 (bis)',
            'partner_id': self.partner_b.id,
        })

        self.assertBankStatementLine(self.statement_line, {
            **self.expected_st_line,
            'payment_ref': self.statement_line.payment_ref,
            'partner_id': self.statement_line.partner_id.id,
            'amount': -2000.0,
            'amount_currency': -4000.0,
            'foreign_currency_id': self.currency_3.id,
        }, [
            {
                **self.expected_bank_line,
                'name': self.statement_line.payment_ref,
                'partner_id': self.statement_line.partner_id.id,
                'debit': 0.0,
                'credit': 2000.0,
                'amount_currency': -2000.0,
                'currency_id': self.currency_1.id,
            },
            {
                **self.expected_counterpart_line,
                'name': self.statement_line.payment_ref,
                'partner_id': self.statement_line.partner_id.id,
                'debit': 2000.0,
                'credit': 0.0,
                'amount_currency': 4000.0,
                'currency_id': self.currency_3.id,
            },
        ])

    def test_prepare_counterpart_amounts_using_st_line_rate(self):

        def assertAppliedRate(
            journal_currency, foreign_currency, aml_currency,
            amount, amount_currency, aml_amount_currency, aml_balance,
            expected_amount_currency, expected_balance,
        ):
            journal = self.bank_journal_1.copy()
            journal.currency_id = journal_currency

            statement_line = self.env['account.bank.statement.line'].create({
                'journal_id': journal.id,
                'date': '2019-01-01',
                'payment_ref': 'test_prepare_counterpart_amounts_using_st_line_rate',
                'foreign_currency_id': foreign_currency.id if foreign_currency != journal_currency else None,
                'amount': amount,
                'amount_currency': amount_currency if foreign_currency != journal_currency else 0.0,
            })

            res = statement_line._prepare_counterpart_amounts_using_st_line_rate(aml_currency, -aml_balance, -aml_amount_currency)
            self.assertAlmostEqual(res['amount_currency'], expected_amount_currency)
            self.assertAlmostEqual(res['balance'], expected_balance)

        for params in (
            (self.currency_2, self.currency_3, self.currency_3, 80.0, 120.0, 120.0, 20.0, -120.0, -40.0),
            (self.currency_2, self.currency_1, self.currency_2, 120.0, 80.0, 120.0, 40.0, -80.0, -80.0),
            (self.currency_2, self.currency_3, self.currency_2, 80.0, 120.0, 80.0, 26.67, -120.0, -40.0),
            (self.currency_2, self.currency_3, self.currency_4, 80.0, 120.0, 480.0, 40.0, -120.0, -40.0),
            (self.currency_1, self.currency_2, self.currency_2, 80.0, 120.0, 120.0, 40.0, -120.0, -80.0),
            (self.currency_1, self.currency_2, self.currency_3, 80.0, 120.0, 480.0, 80.0, -120.0, -80.0),
            (self.currency_2, self.currency_2, self.currency_2, 80.0, 80.0, 80.0, 26.67, -80.0, -40.0),
            (self.currency_2, self.currency_2, self.currency_3, 80.0, 80.0, 240.0, 40.0, -80.0, -40.0),
            (self.currency_1, self.currency_1, self.currency_3, 80.0, 80.0, 480.0, 80.0, -80.0, -80.0),
            (self.currency_2, self.currency_1, self.currency_1, 120.0, 80.0, 80.0, 80.0, -80.0, -80.0),
            (self.currency_2, self.currency_3, self.currency_1, 80.0, 120.0, 40.0, 40.0, -120.0, -40.0),
            (self.currency_1, self.currency_2, self.currency_1, 80.0, 120.0, 80.0, 80.0, -120.0, -80.0),
            (self.currency_2, self.currency_2, self.currency_1, 80.0, 80.0, 40.0, 40.0, -80.0, -40.0),
            (self.currency_1, self.currency_1, self.currency_1, 80.0, 80.0, 80.0, 80.0, -80.0, -80.0),
        ):
            with self.subTest(params=params):
                assertAppliedRate(*params)

    def test_zero_amount_statement_line(self):
        ''' Ensure the statement line is directly marked as reconciled when having an amount of zero. '''
        self.company_data['company'].account_journal_suspense_account_id.reconcile = False

        statement_line = self.env['account.bank.statement.line'].create({
            'date': '2019-01-01',
            'payment_ref': "Happy new year",
            'amount': 0.0,
        })

        self.assertRecordValues(statement_line, [{'is_reconciled': True, 'amount_residual': 0.0}])

    def test_statement_line_ordering(self):

        self.env.user.company_id = self.company_data_2['company']

        line7 = self.create_bank_transaction(7, '2020-01-10', sequence=1)
        line8 = self.create_bank_transaction(8, '2020-01-10', sequence=2)
        line2 = self.create_bank_transaction(2, '2020-01-13')
        line6 = self.create_bank_transaction(6, '2020-01-11')
        line5 = self.create_bank_transaction(5, '2020-01-12')
        line4 = self.create_bank_transaction(4, '2020-01-12')
        line1 = self.create_bank_transaction(1, '2020-01-13')
        line3 = self.create_bank_transaction(3, '2020-01-12')

        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 1,   'running_balance_start': 35,    'running_balance_end': 36,  'statement_id': False},
                {'amount': 2,   'running_balance_start': 33,    'running_balance_end': 35,  'statement_id': False},
                {'amount': 3,   'running_balance_start': 30,    'running_balance_end': 33,  'statement_id': False},
                {'amount': 4,   'running_balance_start': 26,    'running_balance_end': 30,  'statement_id': False},
                {'amount': 5,   'running_balance_start': 21,    'running_balance_end': 26,  'statement_id': False},
                {'amount': 6,   'running_balance_start': 15,     'running_balance_end': 21,  'statement_id': False},
                {'amount': 7,   'running_balance_start': 8,     'running_balance_end': 15,   'statement_id': False},
                {'amount': 8,   'running_balance_start': 0,     'running_balance_end': 8,   'statement_id': False},
            ],
        )

        # Same but with a subset of lines to ensure the balance is not only computed based on selected records.
        self.env['account.bank.statement.line'].flush_model()
        self.env['account.bank.statement.line'].invalidate_model()
        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([
                ('company_id', '=', self.env.company.id),
                ('amount', '>=', 3),
                ('amount', '<=', 6),
            ]),
            [
                {'amount': 3, 'running_balance_start': 30, 'running_balance_end': 33},
                {'amount': 4, 'running_balance_start': 26, 'running_balance_end': 30},
                {'amount': 5, 'running_balance_start': 21, 'running_balance_end': 26},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21},
            ],
        )

        # Put line2 -> line4 inside a statement.
        statement1 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line4.id,
            'end_statement_line_id': line2.id,
        })

        self.env['account.bank.statement'].flush_model()
        self.env['account.bank.statement.line'].flush_model()
        self.env['account.bank.statement.line'].invalidate_model()
        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 1,   'running_balance_start': 35,    'running_balance_end': 36,  'statement_id': False},
                {'amount': 2,   'running_balance_start': 33,    'running_balance_end': 35,  'statement_id': statement1.id},
                {'amount': 3,   'running_balance_start': 30,    'running_balance_end': 33,  'statement_id': statement1.id},
                {'amount': 4,   'running_balance_start': 26,    'running_balance_end': 30,  'statement_id': statement1.id},
                {'amount': 5,   'running_balance_start': 21,    'running_balance_end': 26,  'statement_id': False},
                {'amount': 6,   'running_balance_start': 15,     'running_balance_end': 21,  'statement_id': False},
                {'amount': 7,   'running_balance_start': 8,     'running_balance_end': 15,   'statement_id': False},
                {'amount': 8,   'running_balance_start': 0,     'running_balance_end': 8,   'statement_id': False},
            ],
        )

        # line3, line4 and line5 have the same date. Move line5 at the first place using the sequence.
        line5.sequence -= 1

        self.env['account.bank.statement.line'].flush_model()
        self.env['account.bank.statement.line'].invalidate_model()
        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 1,   'running_balance_start': 35,    'running_balance_end': 36,  'statement_id': False},
                {'amount': 2,   'running_balance_start': 33,    'running_balance_end': 35,  'statement_id': statement1.id},
                {'amount': 5,   'running_balance_start': 28,    'running_balance_end': 33,  'statement_id': statement1.id},
                {'amount': 3,   'running_balance_start': 25,    'running_balance_end': 28,  'statement_id': statement1.id},
                {'amount': 4,   'running_balance_start': 21,    'running_balance_end': 25,  'statement_id': statement1.id},
                {'amount': 6,   'running_balance_start': 15,     'running_balance_end': 21,  'statement_id': False},
                {'amount': 7,   'running_balance_start': 8,     'running_balance_end': 15,   'statement_id': False},
                {'amount': 8,   'running_balance_start': 0,     'running_balance_end': 8,   'statement_id': False},
            ],
        )

    def test_statement_line_set_statement_1(self):
        """
Scenario 1:                             |  Case 1:
Before change:                          |  The user sets L3.statement_id = S4
                                        |  Result:
L1.statement_id = False                 |  L1.statement_id = False
L2.statement_id = S1                    |  L2.statement_id = S1
L3.statement_id = S1                    |  L3.statement_id = S4
L4.statement_id = S1                    |  L4.statement_id = S4
L5.statement_id = S1                    |  L5.statement_id = S4
L6.statement_id = S2                    |  L6.statement_id = S2
L7.statement_id = S3                    |  L7.statement_id = S3

Case 2:                                 |  Case 3:
The user sets L3.statement_id = S2      |  The user sets L3.statement_id = S3
Result:                                 |  Result:
L1.statement_id = False                 |  L1.statement_id = False
L2.statement_id = S1                    |  L2.statement_id = S1
L3.statement_id = S2                    |  L3.statement_id = S3
L4.statement_id = S2                    |  L4.statement_id = S3
L5.statement_id = S2                    |  L5.statement_id = S3
L6.statement_id = S2                    |  L6.statement_id = S2!?-->Raise Error
L7.statement_id = S3                    |  L7.statement_id = S3
"""

        self.env.user.company_id = self.company_data_2['company']

        line1 = self.create_bank_transaction(1, '2020-03-01')
        line2 = self.create_bank_transaction(2, '2020-03-02')
        line3 = self.create_bank_transaction(3, '2020-03-03')
        line4 = self.create_bank_transaction(4, '2020-03-04')
        line5 = self.create_bank_transaction(5, '2020-03-05')
        line6 = self.create_bank_transaction(6, '2020-03-06')
        line7 = self.create_bank_transaction(7, '2020-03-07')
        line8 = self.create_bank_transaction(8, '2020-03-08')

        statement1 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line2.id,
            'end_statement_line_id': line5.id,
        })
        statement2 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line6.id,
            'end_statement_line_id': line6.id,
        })
        statement3 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line7.id,
            'end_statement_line_id': line7.id,
        })

        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': statement1.id},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement1.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement1.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': statement1.id},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )

        # case 1, new statement on a line with statement
        line2.action_create_statement()
        statement4 = line2.statement_id

        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': statement1.id},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement1.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement1.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': statement2.id},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )

        # case 1 cleanup
        statement4.unlink()
        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': statement1.id},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement1.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement1.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': False},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )

        statement1.start_statement_line_id = line1
        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': statement1.id},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement1.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement1.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': statement1.id},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )
        # case 2, new statement on a line with statement
        line2.statement_id = statement2

        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': statement2.id},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement2.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement2.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': statement1.id},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )

        # case 3, new statement on a line with statement
        with self.assertRaises(UserError):
            line2.statement_id = statement3
        self.env.cr.rollback()
    # def test_statement_line_set_statement_2(self):
        """
Scenario 2:                     |   The user sets L3.statement_id = S4
Before change:                  |   Result:

L1.statement_id = False         |   L1.statement_id = False
L2.statement_id = S1            |   L2.statement_id = S1      or S4  ?
L3.statement_id = S1            |   L3.statement_id = S4         S4
L4.statement_id = S1            |   L4.statement_id = S4         S1
L5.statement_id = False         |   L5.statement_id = False
L6.statement_id = S2            |   L6.statement_id = S2
L7.statement_id = S3            |   L7.statement_id = S3
"""
        self.env.user.company_id = self.company_data_2['company']

        line1 = self.create_bank_transaction(1, '2020-03-01')
        line2 = self.create_bank_transaction(2, '2020-03-02')
        line3 = self.create_bank_transaction(3, '2020-03-03')
        line4 = self.create_bank_transaction(4, '2020-03-04')
        line5 = self.create_bank_transaction(5, '2020-03-05')
        line6 = self.create_bank_transaction(6, '2020-03-06')
        line7 = self.create_bank_transaction(7, '2020-03-07')
        line8 = self.create_bank_transaction(8, '2020-03-08')

        statement1 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line2.id,
            'end_statement_line_id': line4.id,
        })
        statement2 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line6.id,
            'end_statement_line_id': line6.id,
        })
        statement3 = self.env['account.bank.statement'].create({
            'start_statement_line_id': line7.id,
            'end_statement_line_id': line7.id,
        })
        statement4 = self.env['account.bank.statement'].create({
        })

        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': False},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement1.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement1.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': statement1.id},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )

        line3.statement_id = statement4

        self.assertRecordValues(statement4, [{
                                    'start_statement_line_id': line3.id,
                                    'end_statement_line_id': line4.id,
                                    'balance_start': line4.running_balance_start,
                                    'balance_end': line3.running_balance_end,
        }])

        self.assertRecordValues(
            self.env['account.bank.statement.line'].search([('company_id', '=', self.env.company.id)]),
            [
                # pylint: disable=C0326
                {'amount': 8, 'running_balance_start': 28, 'running_balance_end': 35, 'statement_id': False},
                {'amount': 7, 'running_balance_start': 21, 'running_balance_end': 28, 'statement_id': statement3.id},
                {'amount': 6, 'running_balance_start': 15, 'running_balance_end': 21, 'statement_id': statement2.id},
                {'amount': 5, 'running_balance_start': 10, 'running_balance_end': 15, 'statement_id': False},
                {'amount': 4, 'running_balance_start':  6, 'running_balance_end': 10, 'statement_id': statement4.id},
                {'amount': 3, 'running_balance_start':  3, 'running_balance_end':  6, 'statement_id': statement4.id},
                {'amount': 2, 'running_balance_start':  1, 'running_balance_end':  3, 'statement_id': statement1.id},
                {'amount': 1, 'running_balance_start':  0, 'running_balance_end':  1, 'statement_id': False},
            ],
        )



        self._cr.rollback()
    # def test_statement_line_set_statement_3(self):
        """
Scenario 3:
Before change:

L1.statement_id = False
L2.statement_id = S1
L3.statement_id = S1
L4.statement_id = False
L5.statement_id = False
L6.statement_id = S2
L7.statement_id = S3

Case 1:
The user sets L5.statement_id = S4
Result:

L1.statement_id = False
L2.statement_id = S1
L3.statement_id = S1
L4.statement_id = False? or S4 why may need an extra input or this line maybe we can ask the user
L5.statement_id = S4
L6.statement_id = S2
L7.statement_id = S3

Case 2:
The user sets L4.statement_id = S4 --> same problem as Case 1
Case 3:
The user sets L4.statement_id = S2

L1.statement_id = False
L2.statement_id = S1
L3.statement_id = S1
L4.statement_id = S2
L5.statement_id = S2
L6.statement_id = S2
L7.statement_id = S3

Case 4:
The user sets L5.statement_id = S1 --> similar to Case 3
Case 5:
The user sets (L4 or L5).statement_id = S3 --> Raise error
"""
