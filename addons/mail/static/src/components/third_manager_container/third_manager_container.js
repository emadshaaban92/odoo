/** @odoo-module **/

import { useModels } from '@mail/component_hooks/use_models';
// ensure components are registered beforehand.
import '@mail/components/third_manager/third_manager';
import { getMessagingComponent } from "@mail/utils/messaging_component";

const { Component } = owl;

export class ThirdManagerContainer extends Component {

    /**
     * @override
     */
    setup() {
        console.log("ThirdManagerContainer Initialized");
        useModels();
        super.setup();
    }

    get messaging() {
        return this.env.services.messaging.modelManager.messaging;
    }
}

Object.assign(ThirdManagerContainer, {
    components: { ThirdManager: getMessagingComponent('ThirdManager') },
    template: 'mail.ThirdManagerContainer',
});
