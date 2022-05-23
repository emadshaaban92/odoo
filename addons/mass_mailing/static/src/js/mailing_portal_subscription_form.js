/** @odoo-module alias=mailing.PortalSubscriptionForm **/

import publicWidget from 'web.public.widget';


publicWidget.registry.MailingPortalSubscriptionForm = publicWidget.Widget.extend({
    events: {
        'click #button_form_send': '_onFormSend',
    },

    /**
     * @override
     */
    init: function (parent, options) {
        this.customerData = options.customerData;
        return this._super.apply(this, arguments);
    },

    /*
     * Triggers call to update list subscriptions. Bubble up to let parent
     * handle returned result if necessary.
     */
    _onFormSend: function (event) {
        event.preventDefault();
        const formData = new FormData(document.querySelector('div#o_mailing_subscription_form form'));
        const mailingListIds = formData.getAll('mailing_list_ids').map(id_str => parseInt(id_str));
        return this._rpc({
            route: '/mailing/list/update',
            params: {
                csrf_token: formData.get('csrf_token'),
                document_id: this.customerData.documentId,
                email: this.customerData.email,
                hash_token: this.customerData.hashToken,
                lists_optin_ids: mailingListIds,
                mailing_id: this.customerData.mailingId,
            }
        }).then((result) => {
            this.trigger_up(
                'subscription_updated',
                {'callKey': result === true ? 'subscription_updated' : result},
            );
        });
    },

    /**
     * Set form elements as hidden / displayed, as this form contains either an
     * informational text when being blacklisted, either the complete form to
     * manage their subscription.
     * @private
     */
    _setBlacklisted: function (isBlacklisted) {
        if (isBlacklisted) {
            document.getElementById('o_mailing_subscription_form_blacklisted').classList.remove('d-none');
            document.getElementById('o_mailing_subscription_form_manage').classList.add('d-none');
        }
        else {
            document.getElementById('o_mailing_subscription_form_blacklisted').classList.add('d-none');
            document.getElementById('o_mailing_subscription_form_manage').classList.remove('d-none');
        }
    },

    /**
     * Set form elements as readonly, e.g. when blacklisted email take precedence
     * over subscription update.
     * @private
     */
    _setReadonly: function (isReadonly) {
        const formInputNodes = document.querySelectorAll('#o_mailing_subscription_form_manage input');
        const formButtonNode = document.getElementById('button_form_send');
        if (isReadonly) {
            formInputNodes.forEach(node => {node.setAttribute('disabled', 'disabled')});
            formButtonNode.setAttribute('disabled', 'disabled');
        }
        else {
            formInputNodes.forEach(node => {node.removeAttribute('disabled')});
            formButtonNode.removeAttribute('disabled');
        }
    },
});

export default publicWidget.registry.MailingPortalSubscriptionForm;
