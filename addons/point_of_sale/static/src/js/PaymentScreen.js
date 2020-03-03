odoo.define('point_of_sale.PaymentScreen', function(require) {
    'use strict';

    const { parse } = require('web.field_utils');
    const { is_email } = require('web.utils');
    const { PosComponent } = require('point_of_sale.PosComponent');
    const { Chrome } = require('point_of_sale.chrome');
    const { PaymentMethodButton } = require('point_of_sale.PaymentMethodButton');
    const { PaymentScreenNumpad } = require('point_of_sale.PaymentScreenNumpad');
    const { PaymentScreenPaymentLines } = require('point_of_sale.PaymentScreenPaymentLines');
    const { useNumberBuffer } = require('point_of_sale.custom_hooks');
    const { useListener } = require('web.custom_hooks');
    const { OrderReceipt } = require('point_of_sale.OrderReceipt');
    const { Printer } = require('point_of_sale.Printer');

    class PaymentScreen extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('delete-payment-line', this.deletePaymentLine);
            useListener('select-payment-line', this.selectPaymentLine);
            useListener('new-payment-line', this.addNewPaymentLine);
            useListener('update-selected-paymentline', this._updateSelectedPaymentline);
            useNumberBuffer({
                // The numberBuffer listens to this event to update its state.
                // Basically means 'update the buffer when this event is triggered'
                nonKeyboardEvent: 'input-from-numpad',
                // When the buffer is updated, trigger this event.
                // Note that the component listens to it.
                triggerAtInput: 'update-selected-paymentline',
            });
            this.payment_interface = null;
        }
        mounted() {
            this.env.pos.on(
                'change:selectedOrder',
                () => {
                    this.render();
                },
                this
            );
            this.currentOrder.on(
                'change',
                () => {
                    this.render();
                },
                this
            );
            this.currentOrder.paymentlines.on(
                'change',
                () => {
                    this.render();
                },
                this
            );
        }
        willUnmount() {
            this.env.pos.off('change:selectedOrder', null, this);
            this.currentOrder.off('change', null, this);
            this.currentOrder.paymentlines.off('change', null, this);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get paymentLines() {
            return this.currentOrder.get_paymentlines();
        }
        get selectedPaymentLine() {
            return this.currentOrder.selected_paymentline;
        }
        async selectClient() {
            await this.showTempScreen('ClientListScreen');
        }
        addNewPaymentLine({ detail: paymentMethod }) {
            // original function: click_paymentmethods
            if (this.currentOrder.electronic_payment_in_progress()) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('There is already an electronic payment in progress.'),
                });
                return false;
            } else {
                this.currentOrder.add_paymentline(paymentMethod);
                this.numberBuffer.reset();
                if (paymentMethod.payment_terminal) {
                    this.currentOrder.selected_paymentline.set_payment_status('pending');
                }
                return true;
            }
        }
        _updateSelectedPaymentline() {
            if (this.paymentLines.every(line => line.paid)) {
                this.currentOrder.add_paymentline(this.env.pos.payment_methods[0]);
            }
            if (!this.selectedPaymentLine) return; // do nothing if no selected payment line
            // disable changing amount on paymentlines with running or done payments on a payment terminal
            if (
                this.payment_interface &&
                !['pending', 'retry'].includes(this.selectedPaymentLine.get_payment_status())
            ) {
                return;
            }
            if (this.numberBuffer.get() === null) {
                this.deletePaymentLine({ detail: { cid: this.selectedPaymentLine.cid } });
            } else {
                this.selectedPaymentLine.set_amount(this.numberBuffer.getFloat());
            }
        }
        toggleIsToInvoice() {
            // click_invoice
            this.currentOrder.set_to_invoice(!this.currentOrder.is_to_invoice());
            this.render();
        }
        toggleIsToEmail() {
            // click_email
            this.currentOrder.set_to_email(!this.currentOrder.is_to_email());
            this.render();
        }
        openCashbox() {
            this.env.pos.proxy.printer.open_cashbox();
        }
        async addTip() {
            // click_tip
            const tip = this.currentOrder.get_tip();
            const change = this.currentOrder.get_change();
            let value = tip;

            if (tip === 0 && change > 0) {
                value = change;
            }

            const { confirmed, payload } = await this.showPopup('NumberPopup', {
                title: tip ? this.env._t('Change Tip') : this.env._t('Add Tip'),
                startingValue: value,
            });

            if (confirmed) {
                this.currentOrder.set_tip(parse.float(payload));
            }
        }
        deletePaymentLine(event) {
            const { cid } = event.detail;
            const line = this.paymentLines.find(line => line.cid === cid);

            // If a paymentline with a payment terminal linked to
            // it is removed, the terminal should get a cancel
            // request.
            if (['waiting', 'waitingCard', 'timeout'].includes(line.get_payment_status())) {
                line.payment_method.payment_terminal.send_payment_cancel(this.currentOrder, cid);
            }

            this.currentOrder.remove_paymentline(line);
            this.numberBuffer.reset();
            this.render();
        }
        selectPaymentLine(event) {
            const { cid } = event.detail;
            const line = this.paymentLines.find(line => line.cid === cid);
            this.currentOrder.select_paymentline(line);
            this.numberBuffer.reset();
            this.render();
        }
        async validateOrder(isForceValidate) {
            // TODO jcb: isForceValidate here is wrong.
            // It always receive an Event as value.
            if (await this._isOrderValid(isForceValidate)) {
                // remove pending payments before finalizing the validation
                for (let line of this.paymentLines) {
                    if (!line.is_done()) this.currentOrder.remove_paymentline(line);
                }
                await this._finalizeValidation();
            }
        }
        async _finalizeValidation() {
            if (this.currentOrder.is_paid_with_cash() && this.env.pos.config.iface_cashdrawer) {
                this.env.pos.proxy.printer.open_cashbox();
            }

            this.currentOrder.initialize_validation_date();
            this.currentOrder.finalized = true;

            let syncedOrderBackendIds = [];
            let errorCode;

            try {
                if (this.currentOrder.is_to_invoice()) {
                    syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                        this.currentOrder
                    );
                } else {
                    syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                }
            } catch (error) {
                if (error instanceof Error) {
                    throw error;
                } else {
                    errorCode = error.code;
                    await this._handlePushOrderError(error);
                }
            }
            if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                try {
                    await this._postPushOrderResolve(this.currentOrder, syncedOrderBackendIds);
                } catch (error) {
                    if (error instanceof Error) {
                        throw error;
                    } else {
                        await this.showPopup('ErrorPopup', {
                            title: 'Error: no internet connection. Press okay to proceed.',
                            body: error,
                        });
                    }
                }
            }

            const shouldShowPrintInvoice = errorCode
                ? this.currentOrder.is_to_invoice() && errorCode < 0
                : false;
            this.trigger('show-screen', {
                name: 'ReceiptScreen',
                printInvoiceIsShow: shouldShowPrintInvoice,
            });

            // If we succeeded in syncing the current order, and
            // there are still other orders that are left unsynced,
            // we ask the user if he is willing to wait and sync them.
            if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('There are unsynced orders'),
                    body: this.env._t('Do you want to sync these orders?'),
                });
                if (confirmed) {
                    // NOTE: Not yet sure if this should be awaited or not.
                    // If awaited, some operations like changing screen
                    // might not work.
                    this.env.pos.push_orders();
                }
            }
        }
        async _handlePushOrderError(error) {
            // This error handler receives `error` equivalent to `error.message` of the rpc error.
            if (error.message === 'Backend Invoice') {
                await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Please print the invoice from the backend'),
                    body:
                        this.env._t(
                            'The order has been synchronized earlier. Please make the invoice from the backend for the order: '
                        ) + error.data.order.name,
                });
            } else if (error.code < 0) {
                // XmlHttpRequest Errors
                // TODO jcb: This should be SyncErrorPopup which allows the user to opt on
                // not seeing the error message again.
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('The order could not be sent'),
                    body: this.env._t('Check your internet connection and try again.'),
                });
            } else if (error.code === 200) {
                // OpenERP Server Errors
                await this.showPopup('ErrorTracebackPopup', {
                    title: error.data.message || this.env._t('Server Error'),
                    body:
                        error.data.debug ||
                        this.env._t('The server encountered an error while receiving your order.'),
                });
            } else {
                // ???
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Unknown Error'),
                    body: this.env._t(
                        'The order could not be sent to the server due to an unknown error'
                    ),
                });
            }
        }
        async _isOrderValid(isForceValidate) {
            if (this.currentOrder.get_orderlines().length === 0) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Empty Order'),
                    body: this.env._t(
                        'There must be at least one product in your order before it can be validated'
                    ),
                });
                return false;
            }

            if (this.currentOrder.is_to_invoice() && !this.currentOrder.get_client()) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Please select the Customer'),
                    body: this.env._t(
                        'You need to select the customer before you can invoice an order.'
                    ),
                });
                if (confirmed) {
                    await this.showTempScreen('ClientListScreen');
                }
                return !!this.currentOrder.get_client();
            }

            if (!this.currentOrder.is_paid() || this.invoicing) {
                return false;
            }

            if (this.currentOrder.has_not_valid_rounding()) {
                var line = this.currentOrder.has_not_valid_rounding();
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Incorrect rounding'),
                    body: this.env._t(
                        'You have to round your payments lines.' + line.amount + ' is not rounded.'
                    ),
                });
                return false;
            }

            // The exact amount must be paid if there is no cash payment method defined.
            if (
                Math.abs(
                    this.currentOrder.get_total_with_tax() - this.currentOrder.get_total_paid()
                ) > 0.00001
            ) {
                var cash = false;
                for (var i = 0; i < this.env.pos.payment_methods.length; i++) {
                    cash = cash || this.env.pos.payment_methods[i].is_cash_count;
                }
                if (!cash) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Cannot return change without a cash payment method'),
                        body: this.env._t(
                            'There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'
                        ),
                    });
                    return false;
                }
            }

            var client = this.currentOrder.get_client();
            if (
                this.currentOrder.is_to_email() &&
                (!client || (client && !is_email(client.email)))
            ) {
                var title = !client ? 'Please select the customer' : 'Please provide valid email';
                var body = !client
                    ? 'You need to select the customer before you can send the receipt via email.'
                    : 'This customer does not have a valid email address, define one or do not send an email.';

                this.showPopup('ConfirmPopup', {
                    title: this.env._t(title),
                    body: this.env._t(body),
                }).then(({ confirmed }) => {
                    if (confirmed) this.trigger('show-screen', { name: 'ClientListScreen' });
                });

                return false;
            }

            // if the change is too large, it's probably an input error, make the user confirm.
            if (
                !isForceValidate &&
                this.currentOrder.get_total_with_tax() > 0 &&
                this.currentOrder.get_total_with_tax() * 1000 < this.currentOrder.get_total_paid()
            ) {
                this.showPopup('ConfirmPopup', {
                    title: this.env._t('Please Confirm Large Amount'),
                    body:
                        this.env._t('Are you sure that the customer wants to  pay') +
                        ' ' +
                        this.env.pos.format_currency(this.currentOrder.get_total_paid()) +
                        ' ' +
                        this.env._t('for an order of') +
                        ' ' +
                        this.env.pos.format_currency(this.currentOrder.get_total_with_tax()) +
                        ' ' +
                        this.env._t('? Clicking "Confirm" will validate the payment.'),
                }).then(({ confirmed }) => {
                    if (confirmed) this.validateOrder(true);
                });
                return false;
            }

            return true;
        }
        _postPushOrderResolve(order, order_server_ids) {
            if (order.is_to_email()) {
                return this._sendReceiptToCustomer(order_server_ids);
            } else {
                return Promise.resolve();
            }
        }
        async _sendReceiptToCustomer(order_server_ids) {
            const order = this.currentOrder;
            const fixture = document.createElement('div');
            const orderReceipt = new OrderReceipt(this, { order });
            // Important to mount the component to a HTMLElement.
            // If not properly mounted, HTMLElement (el) corresponding
            // the component is not created.
            await orderReceipt.mount(fixture);
            const receiptString = orderReceipt.el.outerHTML;
            fixture.remove();
            const printer = new Printer();
            const ticketImage = await printer.htmlToImg(receiptString);
            try {
                await this.rpc({
                    model: 'pos.order',
                    method: 'action_receipt_to_customer',
                    args: [order_server_ids, order.get_name(), order.get_client(), ticketImage],
                });
            } catch (error) {
                order.set_to_email(false);
                if (error instanceof Error) {
                    throw error;
                } else {
                    throw 'There is no internet connection, impossible to send the email.';
                }
            }
        }
    }
    PaymentScreen.components = {
        PaymentScreenNumpad,
        PaymentMethodButton,
        PaymentScreenPaymentLines,
    };

    Chrome.addComponents([PaymentScreen]);

    return { PaymentScreen };
});
