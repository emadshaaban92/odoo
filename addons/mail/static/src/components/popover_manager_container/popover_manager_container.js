/** @odoo-module **/

import { useMessagingContainer } from '@mail/component_hooks/use_messaging_container';

import { Component } from '@odoo/owl';

export class PopoverManagerContainer extends Component {

    /**
     * @override
     */
    setup() {
        useMessagingContainer();
        console.log("PopoverManager container initialized");
    }

    get messaging() {
        return this.env.services.messaging.modelManager.messaging;
    }
}
PopoverManagerContainer.props = {};

Object.assign(PopoverManagerContainer, {
    template: 'mail.PopoverManagerContainer',
});
