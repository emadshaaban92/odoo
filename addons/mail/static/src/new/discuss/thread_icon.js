/* @odoo-module */

import { useMessaging } from "@mail/new/messaging_hook";

import { Component } from "@odoo/owl";

export class ThreadIcon extends Component {
    static props = ["thread", "className?"];
    static template = "mail.thread_icon";

    setup() {
        this.messaging = useMessaging();
    }

    get chatPartner() {
        if (this.thread.chatPartnerId) {
            return this.messaging.state.partners[this.thread.chatPartnerId];
        }
        return null;
    }

    get classNames() {
        switch (this.thread.type) {
            case "channel":
                if (this.thread.authorizedGroupFullName) {
                    return "fa-hashtag";
                } else {
                    return "fa-globe";
                }
            case "chat":
                switch (this.chatPartner.im_status) {
                    case "online":
                        return "o-mail-thread-icon-online fa-circle";
                    case "offline":
                        return "o-mail-thread-icon-offline fa-circle-o";
                    case "away":
                        return "o-mail-thread-icon-away fa-circle text-warning";
                    case "bot":
                        return "o-mail-thread-icon-bot fa-heart";
                    default:
                        return "o-mail-thread-icon-unknown fa-question-circle";
                }
            case "group":
                return "fa-users";
            case "mailbox":
                switch (this.thread.id) {
                    case "inbox":
                        return "fa-inbox";
                    case "starred":
                        return "fa-star-o";
                    case "history":
                        return "fa-history";
                }
        }
        return "fa-hashtag";
    }

    get thread() {
        return this.messaging.state.threads[this.props.thread.localId];
    }
}
