/** @odoo-module **/

import { attr, one } from '@mail/model/model_field';
import { insertAndReplace } from '@mail/model/model_field_command';
import { registerModel } from '@mail/model/model_core';

registerModel({
    name: 'Emoji',
    identifyingFields: ['unicode'],
    fields: {
        unicode: attr({
            readonly: true,
            required: true,
        }),
        sources: attr({
            readonly: true,
            required: true,
        }),
        description: attr({
            readonly: true,
            required: true,
        }),
        emojiRegistry: one('EmojiRegistry', {
            default: insertAndReplace(),
            inverse: 'allEmojis',
            readonly: true,
            required: true,
        })
    }
});
