/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { many, one } from '@mail/model/model_field';

registerModel({
    name: 'EmojiPickerHeaderActionListView',
    template: 'mail.EmojiPickerHeaderActionListView',
    fields: {
        __dummyActionView: one('EmojiPickerHeaderActionView', { inverse: '__ownerAsDummy' }),
        actionViews: many('EmojiPickerHeaderActionView', { inverse: 'owner',
            sort: [['smaller-first', 'sequence']],
        }),
        owner: one('EmojiPickerView', { identifying: true, inverse: 'actionListView' }),
    },
});
