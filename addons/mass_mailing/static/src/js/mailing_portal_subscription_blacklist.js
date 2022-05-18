/** @odoo-module alias=mailing.PortalSubscriptionBlacklist **/

import publicWidget from 'web.public.widget';


publicWidget.registry.MailingPortalSubscriptionBlacklist = publicWidget.Widget.extend({
    events: {
        'click #button_blacklist_add': '_onBlacklistAddClick',
        'click #button_blacklist_remove': '_onBlacklistRemoveClick',
    },

    /**
     * @override
     */
    init: function (parent, options) {
        this.customerData = options.customerData;
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
     * Triggers call to add current email in blacklist. Update widget internals
     * and DOM accordingly (buttons display mainly). Bubble up to let parent
     * handle returned result if necessary.
     */
    _onBlacklistAddClick: function (event) {
        event.preventDefault();
        return this._rpc({
            route: '/mailing/blacklist/add',
            params: {
                document_id: this.customerData.documentId,
                email: this.customerData.email,
                hash_token: this.customerData.hashToken,
                mailing_id: this.customerData.mailingId,
            }
        }).then((result) => {
            if (result === true) {
                this.customerData.isBlacklisted = true;
            }
            this._updateDisplay();
            this.trigger_up(
                'blacklist_add',
                {'callKey': result === true ? 'blacklist_add' : result,
                 'isBlacklisted': result === true ? true: this.customerData.isBlacklisted,
                },
            );
        });
    },

    /*
     * Triggers call to remove current email from blacklist. Update widget
     * internals and DOM accordingly (buttons display mainly). Bubble up to let
     * parent handle returned result if necessary.
     */
    _onBlacklistRemoveClick: function (event) {
        event.preventDefault();
        return this._rpc({
            route: '/mailing/blacklist/remove',
            params: {
                document_id: this.customerData.documentId,
                email: this.customerData.email,
                hash_token: this.customerData.hashToken,
                mailing_id: this.customerData.mailingId,
            }
        }).then((result) => {
            if (result === true) {
                this.customerData.isBlacklisted = false;
            }
            this._updateDisplay();
            this.trigger_up(
                'blacklist_remove',
                {'callKey': result === true ? 'blacklist_remove' : result,
                 'isBlacklisted': result === true ? false: this.customerData.isBlacklisted,
                },
            );
        });
    },

    /*
     * Display buttons according to current state. Removing from blacklist is
     * always available when being blacklisted. Adding in blacklist is available
     * when not being blacklisted, if the action is possible (valid email mainly)
     * and if the option is activated.
     */
    _updateDisplay: function () {
        const buttonAddNode = document.getElementById('button_blacklist_add');
        const buttonRemoveNode = document.getElementById('button_blacklist_remove');
        if (this.customerData.blacklistEnabled && this.customerData.blacklistPossible && !this.customerData.isBlacklisted) {
            buttonAddNode.classList.remove('d-none');
        }
        else {
            buttonAddNode.classList.add('d-none');
        }
        if (this.customerData.isBlacklisted) {
            buttonRemoveNode.classList.remove('d-none');
        }
        else {
            buttonRemoveNode.classList.add('d-none');
        }
    },
});

export default publicWidget.registry.MailingPortalSubscriptionBlacklist;
