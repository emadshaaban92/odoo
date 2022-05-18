/** @odoo-module alias=mailing.PortalSubscriptionFeedback **/

import publicWidget from 'web.public.widget';


publicWidget.registry.MailingPortalSubscriptionFeedback = publicWidget.Widget.extend({
    events: {
        'click #button_feedback': '_onFeedbackClick',
    },

    /**
     * @override
     */
    init: function (parent, options) {
        this.customerData = options.customerData;
        this.allowFeedback = true;
        return this._super.apply(this, arguments);
    },

    /**
     * @override
     */
    start: function () {
        this._updateDisplay();
        return this._super.apply(this, arguments);
    },

    /*
     * Triggers call to give a feedback about current subscription update.
     * Bubble up to let parent handle returned result if necessary.
     */
    _onFeedbackClick: function (event) {
        event.preventDefault();
        const formData = new FormData(document.querySelector('div#o_mailing_subscription_feedback form'));
        console.log(formData);
        return this._rpc({
            route: '/mailing/feedback',
            params: {
                csrf_token: formData.get('csrf_token'),
                document_id: this.customerData.documentId,
                email: this.customerData.email,
                feedback: formData.get('feedback'),
                hash_token: this.customerData.hashToken,
                mailing_id: this.customerData.mailingId,
            }
        }).then((result) => {
            if (result === true) {
                this._updateDisplay(true);
            }
            this.trigger_up(
                'feedback_sent',
                {'callKey': result === true ? 'feedback_sent' : result},
            );
        });
    },

    /*
     * Update display after option changes, notably feedback textarea not being
     * always accessible.
     */
    _updateDisplay: function (cleanFeedback) {
        const feedbackArea = document.querySelector('div#o_mailing_subscription_feedback textarea');
        if (this.allowFeedback) {
            feedbackArea.classList.remove('d-none');
        }
        else {
            feedbackArea.classList.add('d-none');
        }
        if (cleanFeedback) {
            feedbackArea.values = '';
        }
    },
});

export default publicWidget.registry.MailingPortalSubscriptionFeedback;
