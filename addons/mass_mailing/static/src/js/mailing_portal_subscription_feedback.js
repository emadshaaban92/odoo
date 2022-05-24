/** @odoo-module alias=mailing.PortalSubscriptionFeedback **/

import publicWidget from 'web.public.widget';
import { _t } from 'web.core';


publicWidget.registry.MailingPortalSubscriptionFeedback = publicWidget.Widget.extend({
    events: {
        'click #button_feedback': '_onFeedbackClick',
        'click .o_mailing_subscription_opt_out_reason': '_onOptOutReasonClick',
    },

    /**
     * @override
     */
    init: function (parent, options) {
        this.customerData = options.customerData;
        this.allowFeedback = false;
        this.lastAction = false;
        return this._super.apply(this, arguments);
    },

    /**
     * @override
     */
    start: function () {
        this._updateDisplay(true, false);
        return this._super.apply(this, arguments);
    },

    /*
     * Triggers call to give a feedback about current subscription update.
     * Bubble up to let parent handle returned result if necessary.
     */
    _onFeedbackClick: function (event) {
        event.preventDefault();
        const formData = new FormData(document.querySelector('div#o_mailing_subscription_feedback form'));
        const optoutReasonId = parseInt(formData.get('opt_out_reason_id'));
        return this._rpc({
            route: '/mailing/feedback',
            params: {
                csrf_token: formData.get('csrf_token'),
                document_id: this.customerData.documentId,
                email: this.customerData.email,
                feedback: formData.get('feedback'),
                hash_token: this.customerData.hashToken,
                last_action: this.lastAction,
                mailing_id: this.customerData.mailingId,
                opt_out_reason_id: optoutReasonId,
            }
        }).then((result) => {
            if (result === true) {
                this._updateDisplay(false, true);
                this._updateInfo('feedback_sent');
            }
            else {
                this._updateDisplay(false, false);
                this._updateInfo(result);
            }
            this.trigger_up(
                'feedback_sent',
                {'callKey': result === true ? 'feedback_sent' : result},
            );
        });
    },

    /*
     * Toggle feedback textarea display based on reason configuration
     */
    _onOptOutReasonClick: function (event) {
        this.allowFeedback = $(event.currentTarget).data('isFeedback');
        this._updateDisplay()
    },

    /*
     * Update display after option changes, notably feedback textarea not being
     * always accessible.
     */
    _updateDisplay: function (cleanFeedback, setReadonly) {
        const feedbackArea = document.querySelector('div#o_mailing_subscription_feedback textarea');
        const feedbackButton = document.getElementById('button_feedback');
        const feedbackReasons = document.querySelectorAll('div#o_mailing_subscription_feedback input');
        const feedbackInfo = document.getElementById('o_mailing_subscription_feedback_info');
        if (this.allowFeedback) {
            feedbackArea.classList.remove('d-none');
        }
        else {
            feedbackArea.classList.add('d-none');
        }
        if (setReadonly) {
            feedbackArea.setAttribute('disabled', 'disabled');
            feedbackButton.setAttribute('disabled', 'disabled');
            feedbackReasons.forEach(node => node.setAttribute('disabled', 'disabled'));
        }
        else {
            feedbackArea.removeAttribute('disabled');
            feedbackButton.removeAttribute('disabled');
            feedbackReasons.forEach(node => node.removeAttribute('disabled'));
        }
        if (cleanFeedback) {
            feedbackArea.value = '';
            feedbackInfo.innerHTML = "";
        }
    },

    _updateInfo: function (infoKey) {
        const feedbackInfo = document.getElementById('o_mailing_subscription_feedback_info');
        if (infoKey !== undefined) {
            const textSpan = document.createElement('span');
            const info = document.createElement('i');
            if (infoKey === 'feedback_sent') {
                textSpan.textContent = _t('Sent. Thanks you for your feedback !');
                info.setAttribute('class', 'fa fa-check text-success');
            }
            else {
                textSpan.textContent = _t('An error occured. Please retry later or contact us.');
                info.setAttribute('class', 'text-danger');
            }
            info.appendChild(textSpan);
            feedbackInfo.innerHTML = "";
            feedbackInfo.appendChild(info);
            feedbackInfo.classList.remove('d-none');
        }
        else {
            feedbackInfo.classList.add('d-none');
        }
    },

    _setLastAction: function (lastAction) {
        this.lastAction = lastAction;
        if (this.lastAction === 'blacklist_add') {
            document.querySelector('div#o_mailing_subscription_feedback p').innerHTML = _t(
                'Please let us know why you want to be in our block list.'
            );
        }
        else {
            document.querySelector('div#o_mailing_subscription_feedback p').innerHTML = _t(
                'Please let us know why you updated your subscription.'
            );
        }
    },
});

export default publicWidget.registry.MailingPortalSubscriptionFeedback;
