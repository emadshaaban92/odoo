/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';
import { clear, insertAndReplace, replace } from '@mail/model/model_field_command';
import { htmlToTextContentInline } from '@mail/js/utils';

registerModel({
    name: 'ThreadNeedactionPreviewView',
    identifyingFields: ['notificationListViewOwner', 'thread'],
    recordMethods: {
        /**
         * @param {MouseEvent} ev
         */
        onClick(ev) {
            if (!this.exists()) {
                return;
            }
            const markAsRead = this.markAsReadRef.el;
            if (markAsRead && markAsRead.contains(ev.target)) {
                // handled in `_onClickMarkAsRead`
                return;
            }
            const messaging = this.messaging;
            this.thread.open();
            if (!messaging.device.isSmall) {
                messaging.messagingMenu.close();
            }
        },
        /**
         * @param {MouseEvent} ev
         */
        onClickMarkAsRead(ev) {
            this.messaging.models['Message'].markAllAsRead([
                ['model', '=', this.thread.model],
                ['res_id', '=', this.thread.id],
            ]);
        },
        /**
         * @private
         * @returns {string|FieldCommand}
         */
        _computeImageUrl() {
            if (this.thread.moduleIcon) {
                return this.thread.moduleIcon;
            }
            if (!this.thread.channel) {
                return clear();
            }
            if (this.thread.channel.correspondent) {
                return this.thread.channel.correspondent.avatarUrl;
            }
            return `/web/image/mail.channel/${this.thread.id}/avatar_128?unique=${this.thread.channel.avatarCacheKey}`;
        },
        /**
         * @private
         * @returns {string|FieldCommand}
         */
        _computeInlineLastNeedactionMessageAsOriginThreadBody() {
            if (!this.thread.lastNeedactionMessageAsOriginThread) {
                return clear();
            }
            return htmlToTextContentInline(this.thread.lastNeedactionMessageAsOriginThread.prettyBody);
        },
        /**
         * @private
         * @returns {boolean}
         */
        _computeIsEmpty() {
            return !this.inlineLastNeedactionMessageAsOriginThreadBody && !this.lastTrackingValue;
        },
        /**
         * @private
         * @returns {FieldCommand}
         */
        _computeLastTrackingValue() {
            if (this.thread.lastMessage && this.thread.lastMessage.lastTrackingValue) {
                return replace(this.thread.lastMessage.lastTrackingValue);
            }
            return clear();
        },
        /**
         * @private
         * @returns {FieldCommand}
         */
        _computeMessageAuthorPrefixView() {
            if (
                this.thread.lastNeedactionMessageAsOriginThread &&
                this.thread.lastNeedactionMessageAsOriginThread.author
            ) {
                return insertAndReplace();
            }
            return clear();
        },
        /**
         * @private
         * @returns {FieldCommand}
         */
        _computePersonaImStatusIconView() {
            if (
                this.thread.channel &&
                this.thread.channel.correspondent &&
                this.thread.channel.correspondent.isImStatusSet
            ) {
                return insertAndReplace();
            }
            return clear();
        },
    },
    fields: {
        imageUrl: attr({
            compute: '_computeImageUrl',
            default: '/mail/static/src/img/smiley/avatar.jpg',
        }),
        inlineLastNeedactionMessageAsOriginThreadBody: attr({
            compute: '_computeInlineLastNeedactionMessageAsOriginThreadBody',
            default: "",
            readonly: true,
        }),
        isEmpty: attr({
            compute: '_computeIsEmpty',
            readonly: true,
        }),
        lastTrackingValue: one('TrackingValue', {
            compute: '_computeLastTrackingValue',
            readonly: true,
        }),
        /**
         * Reference of the "mark as read" button. Useful to disable the
         * top-level click handler when clicking on this specific button.
         */
        markAsReadRef: attr(),
        messageAuthorPrefixView: one('MessageAuthorPrefixView', {
            compute: '_computeMessageAuthorPrefixView',
            inverse: 'threadNeedactionPreviewViewOwner',
            isCausal: true,
        }),
        notificationListViewOwner: one('NotificationListView', {
            inverse: 'threadNeedactionPreviewViews',
            readonly: true,
            required: true,
        }),
        personaImStatusIconView: one('PersonaImStatusIconView', {
            compute: '_computePersonaImStatusIconView',
            inverse: 'threadNeedactionPreviewViewOwner',
            isCausal: true,
            readonly: true,
        }),
        thread: one('Thread', {
            inverse: 'threadNeedactionPreviewViews',
            readonly: true,
            required: true,
        }),
    },
});
