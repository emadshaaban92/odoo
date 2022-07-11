/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';
import { clear, replace } from '@mail/model/model_field_command';

registerModel({
    name: 'Emoji',
    identifyingFields: ['codepoints'],
    recordMethods: {
        /**
         * @returns {string|FieldCommand}
         */
        _computeCodepointsRepresentation() {
            if (!this.emojiRegistry) {
                return clear();
            }
            if (!this.hasSkinToneVariations || this.emojiRegistry.skinTone === 0) {
                return this.codepoints;
            }
            const [base, ...rest] = this.codepoints;
            return [base, this.emojiRegistry.skinToneCodepoint, ...rest].join('');
        },
        _computeEmojiRegistry() {
            if (!this.messaging) {
                return clear();
            }
            return replace(this.messaging.emojiRegistry);
        },
        _computeSearchData() {
            return [...this.shortcodes, ...this.emoticons, ...this.name, ...this.keywords];
        },
        _computeSources() {
            return [...this.shortcodes, ...this.emoticons];
        },
        /**
         * @private
         * @returns {boolean}
         * Compares two strings
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
            return replace([
                this.emojiRegistry.categoryAll,
                this.emojiDataCategory
            ]);
        },
    },
    fields: {
        codepoints: attr({
            readonly: true,
            required: true,
        }),
        codepointsRepresentation: attr({
            compute: '_computeCodepointsRepresentation',
        }),
        defaultEmojiCategory: attr({
            default: "all"
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
        hasSkinToneVariations: attr(),
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
