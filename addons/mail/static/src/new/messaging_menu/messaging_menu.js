/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { useMessaging } from "../messaging_hook";
import { PartnerImStatus } from "@mail/new/discuss/partner_im_status";
import { NotificationItem } from "./notification_item";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";

export class MessagingMenu extends Component {
    static components = { Dropdown, NotificationItem, PartnerImStatus };
    static props = [];
    static template = "mail.messaging_menu";

    setup() {
        this.messaging = useMessaging();
        this.chatWindowService = useState(useService("mail.chat_window"));
        this.threadService = useState(useService("mail.thread"));
        this.action = useService("action");
        this.state = useState({
            filter: "all", // can be 'all', 'channels' or 'chats'
        });
    }

    activateTab(ev) {
        const target = ev.target.dataset.tabId;
        if (target) {
            this.state.filter = target;
        }
    }

    get displayedPreviews() {
        /** @type {import("@mail/new/core/thread_model").Thread[]} **/
        const threads = Object.values(this.messaging.state.threads);
        const previews = threads.filter((thread) => thread.is_pinned);

        const filter = this.state.filter;
        if (filter === "all") {
            return previews;
        }
        const target = filter === "chats" ? ["chat", "group"] : "channel";
        return previews.filter((preview) => target.includes(preview.type));
    }

    openDiscussion(thread) {
        this.threadService.open(thread);
        this.close();
    }

    onClickNewMessage() {
        this.chatWindowService.openNewMessage();
        this.close();
    }

    /**
     *
     * @param {import("@mail/new/core/notification_group_model").NotificationGroup} failure
     */
    onClickFailure(failure) {
        const originThreadIds = new Set(
            failure.notifications.map(({ message }) => message.originThread.id)
        );
        if (originThreadIds.size === 1) {
            const message = failure.notifications[0].message;
            if (!message.originThread.type) {
                message.originThread.update({ type: "chatter" });
            }
            if (this.messaging.state.discuss.isActive) {
                this.action.doAction({
                    type: "ir.actions.act_window",
                    res_model: message.originThread.model,
                    views: [[false, "form"]],
                    res_id: message.originThread.id,
                });
                // Close the related chat window as having both the form view
                // and the chat window does not look good.
                this.messaging.state.chatWindows
                    .find(({ thread }) => thread === message.originThread)
                    ?.close();
            } else {
                this.threadService.open(message.originThread);
            }
        } else {
            this.openFailureView(failure);
        }
        this.close();
    }

    openFailureView(failure) {
        if (failure.type !== "email") {
            return;
        }
        this.action.doAction({
            name: this.env._t("Mail Failures"),
            type: "ir.actions.act_window",
            view_mode: "kanban,list,form",
            views: [
                [false, "kanban"],
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
            res_model: failure.resModel,
            domain: [["message_has_error", "=", true]],
            context: { create: false },
        });
    }

    cancelNotifications(failure) {
        return this.env.services.orm.call(failure.resModel, "notify_cancel_by_type", [], {
            notification_type: failure.type,
        });
    }

    close() {
        // hack: click on window to close dropdown, because we use a dropdown
        // without dropdownitem...
        document.body.click();
    }

    get counter() {
        let value =
            this.messaging.state.discuss.inbox.counter +
            Object.values(this.messaging.state.threads).filter(
                (thread) => thread.is_pinned && thread.isUnread
            ).length +
            this.messaging.state.notificationGroups.length;
        if (browser.Notification?.permission === "default") {
            value++;
        }
        return value;
    }
}
