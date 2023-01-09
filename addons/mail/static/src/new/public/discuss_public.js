/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { WelcomePage } from "./welcome_page";
import { Discuss } from "./../discuss/discuss";
import { useMessaging, useStore } from "../core/messaging_hook";
import { useService } from "@web/core/utils/hooks";

export class DiscussPublic extends Component {
    static components = { Discuss, WelcomePage };
    static props = ["data"];
    static template = "mail.discuss_public";

    setup() {
        this.messaging = useMessaging();
        this.store = useStore();
        this.state = useState({ welcome: true });
        this.threadService = useService("mail.thread");
        const thread = this.threadService.insert({
            id: this.props.data.channelData.id,
            model: "mail.channel",
            type: this.props.data.channelData.channel.channel_type,
        });
        this.threadService.setDiscussThread(thread);
    }
}
