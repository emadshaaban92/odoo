odoo.define('point_of_sale.ClosePosPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');

    const { useState } = owl;

    /**
     * This popup needs to be self-dependent because it needs to be called from different place.
     */
    class ClosePosPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.manualInputCashCount = false;
            this.cashControl = this.env.pos.config.cash_control;
            this.closeSessionClicked = false;
            this.moneyDetails = null;
            Object.assign(this, this.props.info);
            this.state = useState({
                displayMoneyDetailsPopup: false,
            });
            Object.assign(this.state, this.props.info.state);
        }
        //@override
        async confirm() {
            if (!this.cashControl || !this.hasDifference()) {
                this.closeSession();
            } else if (this.hasUserAuthority()) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Payments Difference'),
                    body: this.env._t('Do you want to accept payments difference and post a profit/loss journal entry?'),
                });
                if (confirmed) {
                    this.closeSession();
                }
            } else {
                await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Payments Difference'),
                    body: _.str.sprintf(
                        this.env._t('The maximum difference allowed is %s.\n\
                        Please contact your manager to accept the closing difference.'),
                        this.env.pos.format_currency(this.amountAuthorizedDiff)
                    ),
                    confirmText: this.env._t('OK'),
                })
            }
        }
        //@override
        async cancel() {
            if (this.canCancel()) {
                super.cancel();
            }
        }
        openDetailsPopup() {
            this.state.payments[this.defaultCashDetails.id].counted = 0;
            this.state.payments[this.defaultCashDetails.id].difference = -this.defaultCashDetails.amount;
            this.state.notes = "";
            this.state.displayMoneyDetailsPopup = true;
        }
        closeDetailsPopup() {
            this.state.displayMoneyDetailsPopup = false;
        }
        async downloadSalesReport() {
            await this.env.services.action.doAction('point_of_sale.sale_details_report', {
                additionalContext: {
                    active_ids: [this.env.pos.pos_session.id],
                },
            });
        }
        handleInputChange(paymentId) {
            let expectedAmount;
            if (paymentId === this.defaultCashDetails.id) {
                this.manualInputCashCount = true;
                this.state.notes = '';
                expectedAmount = this.defaultCashDetails.amount;
            } else {
                expectedAmount = this.otherPaymentMethods.find(pm => paymentId === pm.id).amount;
            }
            this.state.payments[paymentId].difference =
                this.env.pos.round_decimals_currency(this.state.payments[paymentId].counted - expectedAmount);
        }
        updateCountedCash({ total, moneyDetailsNotes, moneyDetails }) {
            this.state.payments[this.defaultCashDetails.id].counted = total;
            this.state.payments[this.defaultCashDetails.id].difference =
                this.env.pos.round_decimals_currency(this.state.payments[[this.defaultCashDetails.id]].counted - this.defaultCashDetails.amount);
            if (moneyDetailsNotes) {
                this.state.notes = moneyDetailsNotes;
            }
            this.manualInputCashCount = false;
            this.moneyDetails = moneyDetails;
            this.closeDetailsPopup();
        }
        hasDifference() {
            return Object.entries(this.state.payments).find(pm => pm[1].difference != 0);
        }
        hasUserAuthority() {
            const absDifferences = Object.entries(this.state.payments).map(pm => Math.abs(pm[1].difference));
            return this.isManager || this.amountAuthorizedDiff == null || Math.max(...absDifferences) <= this.amountAuthorizedDiff;
        }
        canCancel() {
            return true;
        }
        closePos() {
            this.trigger('close-pos');
        }
        async closeSession() {
            if (!this.closeSessionClicked) {
                this.closeSessionClicked = true;
                let response;
                if (this.cashControl) {
                    const kwargs = { counted_cash: this.state.payments[this.defaultCashDetails.id].counted };
                    response = await this.orm.call('pos.session', 'post_closing_cash_details', [this.env.pos.pos_session.id], kwargs);
                    if (!response.successful) {
                        return this.handleClosingError(response);
                    }
                }
                await this.orm.call('pos.session', 'update_closing_control_state_session', [this.env.pos.pos_session.id, this.state.notes]);
                try {
                    const bankPaymentMethodDiffPairs = this.otherPaymentMethods
                        .filter((pm) => pm.type == 'bank')
                        .map((pm) => [pm.id, this.state.payments[pm.id].difference]);
                    response = await this.orm.call('pos.session', 'close_session_from_ui', [this.env.pos.pos_session.id, bankPaymentMethodDiffPairs]);
                    if (!response.successful) {
                        return this.handleClosingError(response);
                    }
                    window.location = '/web#action=point_of_sale.action_client_pos_menu';
                } catch (error) {
                    if (isConnectionError(error)) {
                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Network Error'),
                            body: this.env._t('Cannot close the session when offline.'),
                        });
                    } else {
                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Closing session error'),
                            body: this.env._t(
                                'An error has occurred when trying to close the session.\n' +
                                'You will be redirected to the back-end to manually close the session.')
                        })
                        window.location = '/web#action=point_of_sale.action_client_pos_menu';
                    }
                }
                this.closeSessionClicked = false;
            }
        }
        async handleClosingError(response) {
            await this.showPopup('ErrorPopup', {title: 'Error', body: response.message});
            if (response.redirect) {
                window.location = '/web#action=point_of_sale.action_client_pos_menu';
            }
        }
        _getShowDiff(pm) {
            return pm.type == 'bank' && pm.number !== 0;
        }
    }

    ClosePosPopup.template = 'ClosePosPopup';
    Registries.Component.add(ClosePosPopup);

    return ClosePosPopup;
});
