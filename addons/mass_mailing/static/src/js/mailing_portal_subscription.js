/** @odoo-module alias=mailing.PortalSubscription **/

import core from 'web.core';
import publicWidget from 'web.public.widget';
import { Markup } from 'web.utils';


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
        this.lastAction = this.customerData.lastAction;

        // nodes for widgets (jquery due to widget implementation)
        this.$bl_elem = this.$('#o_mailing_subscription_blacklist');
        this.$feedback_elem = this.$('#o_mailing_subscription_feedback');
        this.$form_elem = this.$('#o_mailing_subscription_form');

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
            this.feedbackWidget._setLastAction(this.lastAction);
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
        this._updateDisplay();
    },

    _onBlacklistAdd: function (event) {
        const callKey = event.data.callKey;
        this.customerData.isBlacklisted = event.data.isBlacklisted;
        if (callKey === 'blacklist_add') {
            this.customerData.feedbackEnabled = true;
        }
        this._onActionDone(callKey);
    },

    _onBlacklistRemove: function (event) {
        const callKey = event.data.callKey;
        this.customerData.isBlacklisted = false;
        if (callKey === 'blacklist_remove') {
            this.customerData.feedbackEnabled = false;
        }
        this._onActionDone(callKey);
    },

    _onFeedbackSent: function (event) {
        const callKey = event.data.callKey;
        this.lastAction = callKey;
    },

    _onSubscriptionUpdated: function (event) {
        const callKey = event.data.callKey;
        if (callKey === 'subscription_updated') {
            this.customerData.feedbackEnabled = true;
        }
        this._onActionDone(callKey);
    },

    _updateDisplay: function () {
        if (! this.customerData.feedbackEnabled && this.$feedback_elem.length) {
            this.$feedback_elem.addClass('d-none');
        }
        else if (this.$feedback_elem.length) {
            this.$feedback_elem.removeClass('d-none');
        }
        if (this.formWidget) {
            this.formWidget._setBlacklisted(this.customerData.isBlacklisted);
            this.formWidget._setReadonly(this.customerData.isBlacklisted);
        }
        if (this.feedbackWidget) {
            this.feedbackWidget._updateDisplay(true, false);
            this.feedbackWidget._setLastAction(this.lastAction);
        }
    },
});

export default publicWidget.registry.MailingPortalSubscription;
