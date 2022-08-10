/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { many } from '@mail/model/model_field';
import { insert } from '@mail/model/model_field_command';
import { emojiCategoriesData, emojisData } from '@mail/models_data/emoji_data';
import { executeGracefully } from '@mail/utils/utils';

registerModel({
    name: 'EmojiRegistry',
    lifecycleHooks: {
        _created() {
            this._populateFromEmojiData();
        },
    },
    recordMethods: {
        _computeAllCategories() {
            return [
                ...this.dataCategories,
            ];
        },
        async _populateFromEmojiData() {
            await executeGracefully(emojiCategoriesData.map(category => () => {
                if (!this.exists()) {
                    return;
                }
                this.update({
                    dataCategories: insert({
                        name: category.name,
                        title: category.title,
                        sortId: category.sortId,
                    }),
                });
            }));
            await executeGracefully(emojisData.map(emojiData => () => {
                if (!this.exists()) {
                    return;
                }
                this.models['Emoji'].insert({
                    codepoints: emojiData.codepoints,
                    shortcodes: emojiData.shortcodes,
                    emoticons: emojiData.emoticons,
                    name: emojiData.name,
                    keywords: emojiData.keywords,
                    emojiDataCategory: { name: emojiData.category },
                });
            }));
        },
        _sortAllCategories() {
            return [['smaller-first', 'sortId']];
        },
        _sortAllEmojis() {
            return [['smaller-first', 'codepoints']];
        }
    },
    fields: {
        allCategories: many('EmojiCategory', {
            compute: '_computeAllCategories',
            inverse: 'emojiRegistry',
            sort: '_sortAllCategories',
        }),
        allEmojis: many('Emoji', {
            inverse: 'emojiRegistry',
            sort: '_sortAllEmojis'
        }),
        dataCategories: many('EmojiCategory', {
        }),
    },
});
