/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { one } from '@mail/model/model_field';
import { increment } from '@mail/model/model_field_command';

import session from 'web.session';
import utils from 'web.utils';

registerModel({
    name: 'PublicLivechatGlobalNotificationHandler',
    identifyingFields: ['publicLivechatGlobalOwner'],
    lifecycleHooks: {
        _created() {
            this.env.services['bus_service'].addChannel(this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.uuid);
            this.env.services['bus_service'].startPolling();
            this.env.services['bus_service'].onNotification(this._onNotification);
        },
    },
    recordMethods: {
        /**
         * @private
         * @param {Object} notification
         * @param {Object} notification.payload
         * @param {string} notification.type
         */
        _handleNotification({ payload, type }) {
            switch (type) {
                case 'im_livechat.history_command': {
                    if (payload.id !== this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.legacyPublicLivechat._id) {
                        return;
                    }
                    const cookie = utils.get_cookie(this.messaging.publicLivechatGlobal.LIVECHAT_COOKIE_HISTORY);
                    const history = cookie ? JSON.parse(cookie) : [];
                    session.rpc('/im_livechat/history', {
                        pid: this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.operator.id,
                        channel_uuid: this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.uuid,
                        page_history: history,
                    });
                    return;
                }
                case 'mail.channel.member/typing_status': {
                    if (payload.channel_id !== this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.legacyPublicLivechat._id) {
                        return;
                    }
                    const partnerID = payload.partner_id;
                    if (partnerID === this.messaging.publicLivechatGlobal.livechatButtonView.currentPartnerId) {
                        // ignore typing display of current partner.
                        return;
                    }
                    if (payload.is_typing) {
                        this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.legacyPublicLivechat.registerTyping({ partnerID });
                    } else {
                        this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.legacyPublicLivechat.unregisterTyping({ partnerID });
                    }
                    return;
                }
                case 'mail.channel/new_message': {
                    if (payload.id !== this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.legacyPublicLivechat._id) {
                        return;
                    }
                    const notificationData = payload.message;
                    // If message from notif is already in chatter messages, stop handling
                    if (this.messaging.publicLivechatGlobal.livechatButtonView.messages.some(message => message.getID() === notificationData.id)) {
                        return;
                    }
                    notificationData.body = utils.Markup(notificationData.body);
                    this.messaging.publicLivechatGlobal.livechatButtonView.widget._addMessage(notificationData);
                    if (this.messaging.publicLivechatGlobal.livechatButtonView.chatWindow.legacyChatWindow._thread._folded || !this.messaging.publicLivechatGlobal.livechatButtonView.chatWindow.legacyChatWindow._publicLivechatView.isAtBottom()) {
                        this.messaging.publicLivechatGlobal.livechatButtonView.publicLivechat.update({ unreadCounter: increment() });
                    }
                    this.messaging.publicLivechatGlobal.livechatButtonView.widget._renderMessages();
                    return;
                }
                case 'mail.message/insert': {
                    const message = this.messaging.publicLivechatGlobal.livechatButtonView.messages.find(message => message._id === payload.id);
                    if (!message) {
                        return;
                    }
                    message._body = utils.Markup(payload.body);
                    this.messaging.publicLivechatGlobal.livechatButtonView.widget._renderMessages();
                    return;
                }
            }
        },
        /**
         * @private
         * @param {Array[]} notifications
         */
        _onNotification(notifications) {
            for (const notification of notifications) {
                this._handleNotification(notification);
            }
        },
    },
    fields: {
        publicLivechatGlobalOwner: one('PublicLivechatGlobal', {
            inverse: 'notificationHandler',
            readonly: true,
            required: true,
        }),
    },
});
