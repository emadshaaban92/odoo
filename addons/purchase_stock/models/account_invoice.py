# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def _stock_account_prepare_cogs_in_lines_vals(self):
        ''' Prepare values used to create the journal items (account.move.line) corresponding to the Cost of Good Sold
        lines (COGS) for vendor bills.

        Example:

        Buy a product having a cost of 9 and a supplier price of 10 and being a storable product and having a perpetual
        valuation in FIFO. The vendor bill's journal entries looks like:

        Account                                     | Debit | Credit
        ---------------------------------------------------------------
        101120 Stock Interim Account (Received)     | 10.0  |
        ---------------------------------------------------------------
        101100 Account Payable                      |       | 10.0
        ---------------------------------------------------------------

        This method computes values used to make two additional journal items:

        ---------------------------------------------------------------
        101120 Stock Interim Account (Received)     |       | 1.0
        ---------------------------------------------------------------
        xxxxxx Price Difference Account             | 1.0   |
        ---------------------------------------------------------------

        :return: A list of Python dictionary to be passed to env['account.move.line'].create.
        '''
        lines_vals_list = []

        for move in self.filtered(lambda move: move.type in ('in_invoice', 'in_refund', 'in_receipt')):
            for line in move.invoice_line_ids:

                # Filter out lines being not eligible for COGS.
                if line.product_id.type != 'product' or line.product_id.valuation != 'real_time':
                    continue

                # Retrieve accounts needed to generate the COGS.
                debit_pdiff_account = line.product_id.property_account_creditor_price_difference \
                                or line.product_id.categ_id.property_account_creditor_price_difference_categ
                debit_pdiff_account = move.fiscal_position_id.map_account(debit_pdiff_account)

                if line.product_id.cost_method != 'standard' and line.purchase_line_id:
                    po_currency = line.purchase_id.currency_id
                    po_company = line.purchase_id.company_id

                    # Retrieve stock valuation moves.
                    valuation_stock_moves = self.env['stock.move'].search([
                        ('purchase_line_id', '=', line.purchase_line_id.id),
                        ('state', '=', 'done'),
                        ('product_qty', '!=', 0.0),
                    ])
                    if move.type == 'in_refund':
                        valuation_stock_moves = valuation_stock_moves.filtered(lambda stock_move: stock_move._is_out())
                    else:
                        valuation_stock_moves = valuation_stock_moves.filtered(lambda stock_move: stock_move._is_in())

                    if valuation_stock_moves:
                        valuation_price_unit_total = 0
                        valuation_total_qty = 0
                        for val_stock_move in valuation_stock_moves:
                            # In case val_stock_move is a return move, its valuation entries have been made with the
                            # currency rate corresponding to the original stock move
                            valuation_date = val_stock_move.origin_returned_move_id.date or val_stock_move.date_expected
                            valuation_price_unit_total += line.company_currency_id._convert(
                                abs(val_stock_move.price_unit) * val_stock_move.product_qty,
                                move.currency_id,
                                move.company_id, valuation_date, round=False,
                            )
                            valuation_total_qty += val_stock_move.product_qty
                        valuation_price_unit = valuation_price_unit_total / valuation_total_qty
                        valuation_price_unit = line.product_id.uom_id._compute_price(valuation_price_unit, line.product_uom_id)

                    elif line.product_id.cost_method == 'fifo':
                        # In this condition, we have a real price-valuated product which has not yet been received
                        valuation_price_unit = po_currency._convert(
                            line.purchase_line_id.price_unit, move.currency_id,
                            po_company, move.date, round=False,
                        )
                    else:
                        # For average/fifo/lifo costing method, fetch real cost price from incoming moves.
                        price_unit = line.purchase_line_id.product_uom._compute_price(line.purchase_line_id.price_unit, line.product_uom_id)
                        valuation_price_unit = po_currency._convert(
                            price_unit, move.currency_id, po_company, move.date, round=False)

                else:
                    # Valuation_price unit is always expressed in invoice currency, so that it can always be computed with the good rate
                    price_unit = line.product_id.uom_id._compute_price(line.product_id.standard_price, line.product_uom_id)
                    valuation_price_unit = line.company_currency_id._convert(
                        price_unit, move.currency_id, move.company_id, fields.Date.today(), round=False)

                invoice_cur_prec = move.currency_id.decimal_places

                if float_compare(valuation_price_unit, line.price_unit, precision_digits=invoice_cur_prec) != 0 \
                        and float_compare(line['price_unit'], line.price_unit, precision_digits=invoice_cur_prec) == 0:

                    price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    if line.tax_ids:
                        price_unit = line.tax_ids.compute_all(price_unit, currency=move.currency_id, quantity=1.0)['total_excluded']

                    price_unit_val_dif = price_unit - valuation_price_unit

                    if move.currency_id.compare_amounts(line.price_unit, valuation_price_unit) != 0 and debit_pdiff_account:
                        # If the unit prices have not changed and we have a
                        # valuation difference, it means this difference is due to exchange rates,
                        # so we don't create anything, the exchange rate entries will
                        # be processed automatically by the rest of the code.
                        price_unit_val_dif = move.currency_id.round(price_unit_val_dif)

                        # Add price difference account line.
                        vals = {
                            'name': line.name[:64],
                            'move_id': move.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom_id.id,
                            'quantity': line.quantity,
                            'price_unit': price_unit_val_dif,
                            'price_subtotal': line.quantity * price_unit_val_dif,
                            'account_id': debit_pdiff_account.id,
                            'analytic_account_id': line.analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                            'display_type': 'cogs',
                        }
                        vals.update(line._compute_balance_from_price_subtotal(
                            vals['price_subtotal'], move.type, line.currency_id, line.company_id, line.date))
                        lines_vals_list.append(vals)

                        # Correct the amount of the current line.
                        vals = {
                            'name': line.name[:64],
                            'move_id': move.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom_id.id,
                            'quantity': line.quantity,
                            'price_unit': -price_unit_val_dif,
                            'price_subtotal': line.quantity * -price_unit_val_dif,
                            'account_id': line.account_id.id,
                            'analytic_account_id': line.analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                            'display_type': 'cogs',
                        }
                        vals.update(line._compute_balance_from_price_subtotal(
                            vals['price_subtotal'], move.type, line.currency_id, line.company_id, line.date))
                        lines_vals_list.append(vals)

            return lines_vals_list

    @api.multi
    def post(self):
        # OVERRIDE
        # Create additional COGS lines for vendor bills.
        self.env['account.move.line'].create(self._stock_account_prepare_cogs_in_lines_vals())
        return super(AccountMove, self).post()

    @api.multi
    def _stock_account_get_last_step_stock_moves(self):
        """ Overridden from stock_account.
        Returns the stock moves associated to this invoice."""
        rslt = super(AccountMove, self)._stock_account_get_last_step_stock_moves()
        for invoice in self.filtered(lambda x: x.type == 'in_invoice'):
            rslt += invoice.mapped('invoice_line_ids.purchase_line_id.move_ids').filtered(lambda x: x.state == 'done' and x.location_id.usage == 'supplier')
        for invoice in self.filtered(lambda x: x.type == 'in_refund'):
            rslt += invoice.mapped('invoice_line_ids.purchase_line_id.move_ids').filtered(lambda x: x.state == 'done' and x.location_dest_id.usage == 'supplier')
        return rslt
