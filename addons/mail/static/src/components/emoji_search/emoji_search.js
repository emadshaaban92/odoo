/** @odoo-module **/

import { registerMessagingComponent } from '@mail/utils/messaging_component';

const { Component } = owl;

export class EmojiSearch extends Component {}

Object.assign(EmojiSearch, {
    props: {
        emojiSearch: Object,
    },
    template: 'mail.EmojiSearch',
});

registerMessagingComponent(EmojiSearch);
