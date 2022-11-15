/** @odoo-module */

import { useMessaging } from "../messaging_hook";
import { RelativeTime } from "./relative_time";
import { Component, useExternalListener, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Composer } from "@mail/new/composer/composer";
import { MessageDeleteDialog } from "@mail/new/thread/message_delete_dialog";

export class Message extends Component {
    setup() {
        this.state = useState({
            isEditing: false,
        });
        this.ref = useRef("ref");
        this.messaging = useMessaging();
        this.action = useService("action");
        this.user = useService("user");
        this.message = this.props.message;
        this.author = this.messaging.partners[this.message.authorId];
        useExternalListener(document, "click", ({ target }) => {
            // Stop editing the message on click away.
            if (target === this.ref.el || this.ref.el.contains(target)) {
                return;
            }
            this.state.isEditing = false;
        });
    }

    get canBeDeleted() {
        if (!this.props.hasActions) {
            return false;
        }
        if (!this.user.isAdmin && this.message.authorId !== this.user.partnerId) {
            return false;
        }
        if (this.message.type !== "comment") {
            return false;
        }
        return this.message.isNote || this.message.resModel === "mail.channel";
    }

    get canBeEdited() {
        return this.canBeDeleted;
    }

    toggleStar() {
        this.messaging.toggleStar(this.props.message.id);
    }

    onClickDelete() {
        this.env.services.dialog.add(MessageDeleteDialog, {
            message: this.message,
            messageComponent: Message,
        });
    }

    openRecord() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_id: this.message.resId,
            res_model: this.message.resModel,
            views: [[false, "form"]],
        });
    }
}

Object.assign(Message, {
    components: { Composer, RelativeTime },
    defaultProps: { hasActions: true },
    props: ["hasActions?", "message", "squashed?"],
    template: "mail.message",
});
