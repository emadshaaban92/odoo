/** @odoo-module */

import { Component } from "@odoo/owl";
import { useMessaging } from "@mail/new/messaging_hook";

export class CallSettings extends Component {
    setup() {
        this.messaging = useMessaging();
    }
}

Object.assign(CallSettings, {
    template: "mail.settings",
});
