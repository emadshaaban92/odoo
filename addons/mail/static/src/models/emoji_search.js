/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';

registerModel({
    name: 'EmojiSearch',
    identifyingFields: ['emojiPickerView'],
    fields: {
        currentSearch: attr({
            default: "scanning for results...",
        }),
        emojiPickerView: one("EmojiPickerView", {
            inverse: "emojiSearch",
            readonly: true,
            required: true,
        })
    },
});
