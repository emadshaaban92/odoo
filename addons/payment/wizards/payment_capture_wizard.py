# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_amount


class PaymentCaptureWizard(models.TransientModel):
    _name = 'payment.capture.wizard'
    _description = "Payment Capture Wizard"

    transaction_ids = fields.Many2many(
        comodel_name='payment.transaction',
        string="Parent transactions that are or were authorized",
        default=lambda self: self.env.context.get('active_ids'),
        readonly=True,
    )
    authorized_amount = fields.Monetary(
        string="Authorized Amount", compute='_compute_authorized_amount',
    )
    amount_available = fields.Monetary(
        string="Maximum Capture Allowed", compute='_compute_amount_available',
    )
    captured_amount = fields.Monetary(string="Already Captured", compute='_compute_captured_amount')
    voided_amount = fields.Monetary(string="Already Voided", compute='_compute_voided_amount')
    amount_to_capture = fields.Monetary(
        string="Capture Amount", compute='_compute_amount_to_capture', store=True, readonly=False,
    )
    currency_id = fields.Many2one(string="Currency", related='transaction_ids.currency_id')
    # TODO edm ask anv: is this okay with ids instead of id? We know it's the same, but what would
    #  happens if it wasn't?
    support_partial_capture = fields.Boolean(
        compute='_compute_support_partial_capture',
        help="Whether all the tx are from a provider that support the partial capture",
        compute_sudo=True,
    )
    has_draft_children = fields.Boolean(
        string="Has a draft children", compute='_compute_has_draft_children',
    )
    has_remaining_amount = fields.Boolean(
        string="Has Remaining Amount", compute='_compute_has_remaining_amount',
    )
    void_remaining_amount = fields.Boolean(string="Void remaining amount")

    #=== COMPUTE METHODS ===#

    @api.depends('transaction_ids')
    def _compute_authorized_amount(self):
        for wizard in self:
            wizard.authorized_amount = sum(wizard.transaction_ids.mapped('amount'))

    @api.depends('transaction_ids')
    def _compute_captured_amount(self):
        for wizard in self:
            captured_src_tx_no_child = wizard.transaction_ids.filtered(
                lambda tx: tx.state == 'done' and not tx.child_transaction_ids
            )
            captured_child_tx = wizard.transaction_ids.child_transaction_ids.filtered(
                lambda tx: tx.state == 'done'
            )
            captured_tx = captured_src_tx_no_child | captured_child_tx
            wizard.captured_amount = sum(tx.amount for tx in captured_tx)

    @api.depends('transaction_ids')
    def _compute_voided_amount(self):
        for wizard in self:
            # As voided source tx are not sent into the wizard, we only look for child tx
            voided_child_tx = wizard.transaction_ids.child_transaction_ids.filtered(
                lambda tx: tx.state == 'cancel'
            )
            wizard.voided_amount = sum(tx.amount for tx in voided_child_tx)

    @api.depends('authorized_amount', 'captured_amount', 'voided_amount')
    def _compute_amount_available(self):
        for wizard in self:
            wizard.amount_available = wizard.authorized_amount \
                                      - wizard.captured_amount \
                                      - wizard.voided_amount

    @api.depends('amount_available')
    def _compute_amount_to_capture(self):
        """ Set the default amount to capture to the amount available for capture. """
        for wizard in self:
            wizard.amount_to_capture = wizard.amount_available

    def _compute_support_partial_capture(self):
        for wizard in self:
            wizard.support_partial_capture = not any(
                tx.provider_id.support_manual_capture != 'partial' for tx in wizard.transaction_ids
            )

    @api.depends('transaction_ids')
    def _compute_has_draft_children(self):
        for wizard in self:
            draft_children = wizard.transaction_ids.child_transaction_ids.filtered(
                lambda tx: tx.state == 'draft'
            )
            wizard.has_draft_children = bool(draft_children)

    @api.depends('amount_available', 'amount_to_capture')
    def _compute_has_remaining_amount(self):
        for wizard in self:
            wizard.has_remaining_amount = wizard.amount_to_capture < wizard.amount_available
            if not wizard.has_remaining_amount:
                wizard.void_remaining_amount = False

    #=== CONSTRAINT METHODS ===#

    @api.constrains('amount_to_capture')
    def _check_amount_to_capture_within_boundaries(self):
        for wizard in self:
            if not 0 < wizard.amount_to_capture <= wizard.amount_available:
                formatted_amount = format_amount(
                    self.env, wizard.amount_available, wizard.currency_id
                )
                raise UserError(_(
                    "The amount to be captured must be positive and cannot be superior to %s.",
                    formatted_amount
                ))
            if not wizard.support_partial_capture \
               and wizard.amount_to_capture != wizard.amount_available:
                raise UserError(_(
                    "At least one of the transaction comes from a provider which doesn't support "
                    "the partial capture. Manage the transactions separately to make a partial "
                    "capture."
                ))

    #=== ACTION METHODS ===#

    def action_capture(self):
        for wizard in self:
            remain_amount_to_capture = wizard.amount_to_capture
            for source_tx in wizard.transaction_ids.filtered(lambda tx: tx.state == 'authorized'):
                captured_children_tx = wizard.transaction_ids.child_transaction_ids.filtered(
                    lambda t: t.source_transaction_id == source_tx and t.state == 'done'
                )  # We can only void all the remaining amount at once => don't check cancel state
                source_tx_remaining_amount = round(source_tx.amount - sum(
                    child_tx.amount for child_tx in captured_children_tx
                ), source_tx.currency_id.decimal_places)
                if remain_amount_to_capture:
                    amount_to_capture = min(source_tx_remaining_amount, remain_amount_to_capture)
                    # In sudo mode because we need to be able to read on provider fields.
                    source_tx.sudo()._send_capture_request(amount_to_capture=amount_to_capture)
                    remain_amount_to_capture -= amount_to_capture
                    source_tx_remaining_amount -= amount_to_capture

                if source_tx_remaining_amount and wizard.void_remaining_amount:
                    # The source tx isn't fully captured and the user wants to void the remaining
                    # In sudo mode because we need to be able to read on provider fields.
                    source_tx.sudo()._send_void_request(amount_to_void=source_tx_remaining_amount)

                elif not remain_amount_to_capture and not wizard.void_remaining_amount:
                    break  # No request needed for the following txs
