/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { many, one } from '@mail/model/model_field';
import { insertAndReplace, replace } from '@mail/model/model_field_command';
import { emojiCategoriesData, emojisData } from '@mail/models_data/emoji_data';

registerModel({
    name: 'EmojiRegistry',
    identifyingFields: ['messaging'],
    lifecycleHooks: {
        _created() {
            this._populateFromEmojiData();
        },
    },
    recordMethods: {
        _computeAllCategories() {
            return replace([
                this.categoryAll,
                ...this.dataCategories,
            ]);
        },
        _populateFromEmojiData() {
            this.update ({ dataCategories: insertAndReplace(emojiCategoriesData.map(category => {
                    return {
                        name: category.name,
                        title: category.title,
                        sortId: category.sortId,
                    };
                }))
            });
            this.models['Emoji'].insert(emojisData.map(emojiData => {
                return {
                    codepoints: emojiData.codepoints,
                    sources: [...emojiData.shortcodes, ...emojiData.emoticons],
                    name: emojiData.name,
                    emojiDataCategory: insertAndReplace(
                        { name: emojiData.category }
                    ),
                };
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
        categoryAll: one('EmojiCategory', {
            default: insertAndReplace({ name: 'all', title: 'all', sortId: 0 }),
        }),
        dataCategories: many('EmojiCategory', {
        }),
    },
});
