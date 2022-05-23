/** @odoo-module alias=mailing.PortalSubscriptionBlacklist **/

import publicWidget from 'web.public.widget';
import { _t } from 'web.core';


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
            this._updateDisplay(result === true ? 'blacklist_add' : 'error');
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
            this._updateDisplay(result === true ? 'blacklist_remove' : 'error');
            this.trigger_up(
                'blacklist_remove',
                {'callKey': result === true ? 'blacklist_remove' : result,
                 'isBlacklisted': result === true ? false: this.customerData.isBlacklisted,
                },
            );
        });
    },

    /*
     * Display buttons and info according to current state. Removing from blacklist
     # is always available when being blacklisted. Adding in blacklist is available
     * when not being blacklisted, if the action is possible (valid email mainly)
     * and if the option is activated.
     */
    _updateDisplay: function (infoKey) {
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

        // update state info
        this._updateInfo(infoKey);
    },

    _updateInfo: function (infoKey) {
        const blacklistInfo = document.getElementById('o_mailing_subscription_blacklist_info');
        if (infoKey !== undefined) {
            const textSpan = document.createElement('span');
            const info = document.createElement('i');
            if (infoKey === 'blacklist_remove') {            
                textSpan.textContent = _t('Email removed from our blocklist.');
                info.setAttribute('class', 'fa fa-check text-success');
            }
            else if (infoKey === 'blacklist_add') {
                textSpan.textContent = _t('Email added to our blocklist.');
                info.setAttribute('class', 'fa fa-check text-success');
            }
            else {
                textSpan.textContent = _t('An error occured. Please retry later.');
                info.setAttribute('class', 'fa fa-check text-danger');
            }
            info.appendChild(textSpan);
            blacklistInfo.innerHTML = "";
            blacklistInfo.appendChild(info);
            blacklistInfo.setAttribute('class', '');
        }
        else {
            blacklistInfo.setAttribute('class', 'd-none');
        }
    },
});

export default publicWidget.registry.MailingPortalSubscriptionBlacklist;
