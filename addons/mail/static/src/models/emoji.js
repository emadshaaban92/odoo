/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';
import { clear } from '@mail/model/model_field_command';

registerModel({
    name: 'Emoji',
    recordMethods: {
        _computeEmojiRegistry() {
            if (!this.messaging) {
                return clear();
            }
            return this.messaging.emojiRegistry;
        },
        _computeSearchData() {
            return [...this.shortcodes, ...this.emoticons, ...this.name, ...this.keywords];
        },
        _computeSources() {
            return [...this.shortcodes, ...this.emoticons];
        },
        /**
         * Compares two strings
         *
         * @private
         * @returns {boolean}
         */
        _fuzzySearch(string, search) {
            let i = 0;
            let j = 0;
            while (i < string.length) {
                if (string[i] === search[j]) {
                    j += 1;
                }
                if (j === search.length) {
                    return true;
                }
                i += 1;
            }
            return false;
        },
        /**
         * @private
         * @returns {boolean}
         */
        _isStringInEmojiKeywords(string) {
            for (let index in this.searchData) {
                if (this._fuzzySearch(this.searchData[index], string)) { //If at least one correspondence is found, return true.
                    return true;
                }
            }
            return false;
        },
        _computeEmojiCategories() {
            if (!this.emojiRegistry) {
                return clear();
            }
            return [
                this.emojiRegistry.categoryAll,
                this.emojiDataCategory
            ];
        },
    },
    fields: {
        codepoints: attr({
            identifying: true,
        }),
        emojiCategories: many('EmojiCategory', {
            compute: "_computeEmojiCategories",
            inverse: 'allEmojis',
        }),
        emojiDataCategory: one('EmojiCategory', {
        }),
        emojiRegistry: one('EmojiRegistry', {
            compute: '_computeEmojiRegistry',
            inverse: 'allEmojis',
            readonly: true,
            required: true,
        }),
        emojiViews: many('EmojiView', {
            inverse: 'emoji',
            readonly: true,
            isCausal: true,
        }),
        emoticons: attr(),
        keywords: attr(),
        name: attr({
            readonly: true,
        }),
        searchData: attr({
            compute: '_computeSearchData',
        }),
        shortcodes: attr(),
        sources: attr({
            compute: '_computeSources',
            readonly: true,
        }),
    },
});
