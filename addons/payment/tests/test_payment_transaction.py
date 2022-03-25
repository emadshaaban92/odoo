# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import tagged

from odoo.addons.payment.tests.common import PaymentCommon


@tagged('-at_install', 'post_install')
class TestPaymentTransaction(PaymentCommon):

    def test_refunds_count(self):
        self.provider.support_refund = 'full_only'  # Should simply not be False
        tx = self._create_transaction('redirect', state='done')
        for reference_index, operation in enumerate(
            ('online_redirect', 'online_direct', 'online_token', 'validation', 'refund')
        ):
            self._create_transaction(
                'dummy',
                reference=f'R-{tx.reference}-{reference_index + 1}',
                state='done',
                operation=operation,  # Override the computed flow
                source_transaction_id=tx.id,
            )._reconcile_after_done()

        self.assertEqual(
            tx.refunds_count,
            1,
            msg="The refunds count should only consider transactions with operation 'refund'."
        )

    def test_refund_transaction_values(self):
        self.provider.support_refund = 'partial'
        tx = self._create_transaction('redirect', state='done')

        # Test the default values of a full refund transaction
        refund_tx = tx._create_child_transaction(operation='refund')
        self.assertEqual(
            refund_tx.reference,
            f'R-{tx.reference}',
            msg="The reference of the refund transaction should be the prefixed reference of the "
                "source transaction."
        )
        self.assertLess(
            refund_tx.amount, 0, msg="The amount of a refund transaction should always be negative."
        )
        self.assertAlmostEqual(
            refund_tx.amount,
            -tx.amount,
            places=2,
            msg="The amount of the refund transaction should be taken from the amount of the "
                "source transaction."
        )
        self.assertEqual(
            refund_tx.currency_id,
            tx.currency_id,
            msg="The currency of the refund transaction should be that of the source transaction."
        )
        self.assertEqual(
            refund_tx.operation,
            'refund',
            msg="The operation of the refund transaction should be 'refund'."
        )
        self.assertEqual(
            tx,
            refund_tx.source_transaction_id,
            msg="The refund transaction should be linked to the source transaction."
        )
        self.assertEqual(
            refund_tx.partner_id,
            tx.partner_id,
            msg="The partner of the refund transaction should be that of the source transaction."
        )

        # Test the values of a partial refund transaction with custom refund amount
        partial_refund_tx = tx._create_child_transaction(amount=11.11, operation='refund')
        self.assertAlmostEqual(
            partial_refund_tx.amount,
            -11.11,
            places=2,
            msg="The amount of the refund transaction should be the negative value of the amount "
                "to refund."
        )

    def test_partial_capture_transaction_values(self):
        self.provider.support_manual_capture = 'partial'
        self.provider.capture_manually = True
        tx = self._create_transaction('redirect', state='authorized')

        capture_tx = tx._create_child_transaction(amount=11.11)
        self.assertEqual(
            capture_tx.reference,
            f'P-{tx.reference}',
            msg="The reference of a partial capture should be the prefixed reference of the source "
                "transaction."
        )
        self.assertEqual(
            capture_tx.amount,
            11.11,
            msg="The amount of a partial capture should be the one passed as argument."
        )
        self.assertEqual(
            capture_tx.currency_id,
            tx.currency_id,
            msg="The currency of the partial capture should be that of the source transaction."
        )
        self.assertEqual(
            capture_tx.operation,
            tx.operation,
            msg="The operation of the partial capture should be the same as the source transaction."
        )
        self.assertEqual(
            tx,
            capture_tx.source_transaction_id,
            msg="The partial capture transaction should be linked to the source transaction."
        )
        self.assertEqual(
            capture_tx.partner_id,
            tx.partner_id,
            msg="The partner of the partial capture should be that of the source transaction."
        )

    def test_child_tx_state_change_to_done_triggers_source_tx_state_change(self):
        self.provider.support_manual_capture = 'partial'
        self.provider.capture_manually = True
        source_tx = self._create_transaction(flow='direct', state='authorized')
        child_tx_1 = source_tx._create_child_transaction(amount=100)
        child_tx_1._set_done()
        self.assertEqual(
            source_tx.state,
            'authorized',
            msg="The whole amount of the source transaction has not been processed yet, it's state "
                "should still be 'authorized'."
        )
        child_tx_2 = source_tx._create_child_transaction(amount=source_tx.amount-100)
        child_tx_2._set_done()
        self.assertEqual(
            source_tx.state,
            'done',
            msg="The whole amount of the source transaction has been processed, it's state is now "
                "'done'."
        )

    def test_child_tx_state_change_to_cancel_triggers_source_tx_state_change(self):
        self.provider.support_manual_capture = 'partial'
        self.provider.capture_manually = True
        source_tx = self._create_transaction(flow='direct', state='authorized')
        child_tx_1 = source_tx._create_child_transaction(amount=100)
        child_tx_1._set_done()
        child_tx_2 = source_tx._create_child_transaction(amount=source_tx.amount-100)
        child_tx_2._set_canceled()
        self.assertEqual(
            source_tx.state,
            'done',
            msg="The whole amount of the source transaction has been processed, it's state is now "
                "'done'."
        )
