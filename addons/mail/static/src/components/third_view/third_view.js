/** @odoo-module **/

import { useComponentToModel } from '@mail/component_hooks/use_component_to_model';
import { registerMessagingComponent } from '@mail/utils/messaging_component';

const { Component } = owl;

export class ThirdView extends Component {

    /**
     * @override
     */
    setup() {
        super.setup();
        useComponentToModel({ fieldName: 'component' });
        /*usePosition(
            () => this.popoverView.anchorRef && this.popoverView.anchorRef.el,
            {
                popper: "root",
                margin: 16,
                position: this.popoverView.position,
            }
        );*/
    }

    /**
     * @returns {ThirdView|undefined}
     */
    get thirdView() {
        return this.props.record;
    }

}

Object.assign(ThirdView, {
    props: { record: Object },
    template: 'mail.ThirdView',
});

registerMessagingComponent(ThirdView);
