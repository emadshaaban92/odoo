/** @odoo-module **/

import { registerMessagingComponent } from '@mail/utils/messaging_component';

const { Component } = owl;

export class ThirdManager extends Component {

    get thirdManager() {
        return this.props.record;
    }
}

Object.assign(ThirdManager, {
    props: { record: Object },
    template: 'mail.ThirdManager',
});

registerMessagingComponent(ThirdManager);
