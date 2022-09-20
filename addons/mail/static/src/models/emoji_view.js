/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';
import { increment } from '@mail/model/model_field_command';

registerModel({
    name: 'EmojiView',
    recordMethods: {
        /**
         * @param {MouseEvent} ev
         */
        onClick(ev) {
            if (!this.exists()) {
                return;
            }
            if (!this.emojiGridItemViewOwner.emojiGridRowViewOwner) {
                return;
            }
            const emoji = this.emoji;
            this._onClick(ev);
            emoji.update({ useAmount: increment() });
        },
        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClick(ev) {
            if (this.emojiGridItemViewOwner.emojiGridRowViewOwner.emojiGridViewOwner.emojiPickerViewOwner.popoverViewOwner.messageActionViewOwnerAsReaction) {
                this.emojiGridItemViewOwner.emojiGridRowViewOwner.emojiGridViewOwner.emojiPickerViewOwner.popoverViewOwner.messageActionViewOwnerAsReaction.onClickReaction(ev);
                return;
            }
            if (this.emojiGridItemViewOwner.emojiGridRowViewOwner.emojiGridViewOwner.emojiPickerViewOwner.popoverViewOwner.composerViewOwnerAsEmoji) {
                this.emojiGridItemViewOwner.emojiGridRowViewOwner.emojiGridViewOwner.emojiPickerViewOwner.popoverViewOwner.composerViewOwnerAsEmoji.onClickEmoji(ev);
                return;
            }
        },
        /**
         * @param {MouseEvent} ev
         */
        onMouseenter(ev) {
            if (!this.exists()) {
                return;
            }
            this.update({ isHovered: true });
        },
        /**
         * @param {MouseEvent} ev
         */
        onMouseleave(ev) {
            if (!this.exists()) {
                return;
            }
            this.update({ isHovered: false });
        },
    },
    fields: {
        emoji: one('Emoji', {
            identifying: true,
            inverse: 'emojiViews',
        }),
        emojiGridItemViewOwner: one('EmojiGridItemView', {
            identifying: true,
            inverse: 'emojiView',
        }),
        isHovered: attr({
            default: false,
        }),
    }
});
