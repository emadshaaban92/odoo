/** @odoo-module **/
import { markEventHandled } from '@mail/utils/utils';

import { Patch } from '@mail/model';
// ensure load order
import '@mail/models/message_view';


Patch({
    name: 'MessageView',
    recordMethods: {
        /**
         * @override
         */
        onClickFailure(ev) {
            if (this.message.failureTraces.length > 0) {
                markEventHandled(ev, 'Message.ClickFailure');
                this.message.openMailingView();
                return;
            }
            this._super(ev);
        },
    }
});
