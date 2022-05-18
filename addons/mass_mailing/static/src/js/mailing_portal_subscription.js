/** @odoo-module alias=mailing.PortalSubscription **/

import core from 'web.core';
import publicWidget from 'web.public.widget';
import { Markup } from 'web.utils';
import { _t } from 'web.core';


publicWidget.registry.MailingPortalSubscription = publicWidget.Widget.extend({
    custom_events: {
        'blacklist_add': '_onBlacklistAdd',
        'blacklist_remove': '_onBlacklistRemove',
        'feedback_sent': '_onFeedbackSent',
        'subscription_updated': '_onSubscriptionUpdated',
    },
    selector: '#o_mailing_portal_subscription',

    /**
     * @override
     */
    start: function () {
        this.customerData = this.$el.data();
        this.customerData.feedbackEnabled = true;

        // nodes for widgets (jquery due to widget implementation)
        this.$bl_elem = this.$('#o_mailing_subscription_blacklist');
        this.$feedback_elem = this.$('#o_mailing_subscription_feedback');
        this.$form_elem = this.$('#o_mailing_subscription_form');
        // nodes for text / ui update
        this.subscriptionInfoNode = document.getElementById('o_mailing_subscription_info');
        this.subscriptionInfoStateNode = document.getElementById('o_mailing_subscription_info_state');

        this._attachBlacklist();
        this._attachFeedback();
        this._attachForm();
        this._updateDisplay();
        return this._super.apply(this, arguments);
    },

    _attachBlacklist: function () {
        if (this.$bl_elem.length) {
            this.blacklistWidget = new publicWidget.registry.MailingPortalSubscriptionBlacklist(
                this,
                {customerData: this.customerData}
            );
            this.blacklistWidget.attachTo(this.$bl_elem);
        }
    },

    _attachFeedback: function () {
        if (this.$feedback_elem.length) {
            this.feedbackWidget = new publicWidget.registry.MailingPortalSubscriptionFeedback(
                this,
                {customerData: this.customerData}
            );
            this.feedbackWidget.attachTo(this.$feedback_elem);
        }
    },

    _attachForm: function () {
        if (this.$form_elem.length) {
            this.formWidget = new publicWidget.registry.MailingPortalSubscriptionForm(
                this,
                {customerData: this.customerData}
            );
            this.formWidget.attachTo(this.$form_elem);
        }
    },

    _onActionDone: function (callKey) {
        this.lastAction = callKey;
        this._updateDisplay(callKey);
        this._updateSubscriptionInfo(callKey);
    },

    _onBlacklistAdd: function (event) {
        const callKey = event.data.callKey;
        this.customerData.isBlacklisted = event.data.isBlacklisted;
        if (callKey == 'blacklist_add') {
            this.customerData.feedbackEnabled = true;
        }
        this._onActionDone(callKey);
    },

    _onBlacklistRemove: function (event) {
        const callKey = event.data.callKey;
        this.customerData.isBlacklisted = false;
        if (callKey == 'blacklist_remove') {
            this.customerData.feedbackEnabled = true;
        }
        this._onActionDone(callKey);
    },

    _onFeedbackSent: function (event) {
        const callKey = event.data.callKey;
        if (callKey == 'feedback_sent') {
            this.customerData.feedbackEnabled = true;
        }
        this._onActionDone(callKey);
    },

    _onSubscriptionUpdated: function (event) {
        const callKey = event.data.callKey;
        if (callKey == 'subscription_updated') {
            this.customerData.feedbackEnabled = true;
        }
        this._onActionDone(callKey);
    },

    _updateDisplay: function (callKey) {
        if (! this.customerData.feedbackEnabled && this.$feedback_elem.length) {
            this.$feedback_elem.hide();
        }
        else if (this.$feedback_elem.length) {
            this.$feedback_elem.show();
        }
        if (this.formWidget) {
            this.formWidget._setReadonly(this.customerData.isBlacklisted);
        }
        if (this.feedbackWidget) {
            this.feedbackWidget._setLastAction(this.lastAction);
        }
    },

    _updateSubscriptionInfo: function (callKey) {
        if (callKey == 'blacklist_add') {
            this.subscriptionInfoStateNode.innerHTMl = Markup(
                _t('You have been successfully <strong>added to our blacklist</strong>. You will not be contacted anymore by our services.')
            );
            this.subscriptionInfoNode.setAttribute('class', 'alert-success');
        }
        else if (callKey == 'blacklist_remove') {
            this.subscriptionInfoStateNode.innerHTMl = Markup(
                _t('You have been successfully <strong>removed from our blacklist</strong>. You are now able to be contacted by our services.')
            );
            this.subscriptionInfoNode.setAttribute('class', 'alert-success');
        }
        else if (callKey == 'feedback_sent') {
            this.subscriptionInfoStateNode.innerHTMl = _t('Thanks for your feedback.');
        }
        else if (callKey == 'subscription_updated') {
            this.subscriptionInfoStateNode.innerHTMl = Markup(
                _t('You have successfully <strong>updated your memberships.</strong>')
            );
            this.subscriptionInfoNode.setAttribute('class', 'alert-success');
        }
        else if (callKey == 'unauthorized') {
            this.subscriptionInfoStateNode.innerHTMl = _t('You are not authorized to do this.');
            this.subscriptionInfoNode.setAttribute('class', 'alert-error');
        }
        else if (callKey == 'error') {
            this.subscriptionInfoStateNode.innerHTMl = _t('An error occurred. Please try again later or contact us.');
            this.subscriptionInfoNode.setAttribute('class', 'alert-error');
        }
        else {
            this.subscriptionInfoStateNode.setAttribute('class', 'd-none');
        }
    },
});

export default publicWidget.registry.MailingPortalSubscription;
