/** @odoo-module */

import { Component, onMounted, onWillUpdateProps, useEffect, useRef, useState } from "@odoo/owl";
import { useMessaging } from "../messaging_hook";
import { useEmojiPicker } from "./emoji_picker";
import { convertBrToLineBreak, isEventHandled, onExternalClick } from "@mail/new/utils";

export class Composer extends Component {
    setup() {
        this.messaging = useMessaging();
        this.ref = useRef("textarea");
        this.state = useState({
            autofocus: 0,
            value: this.props.message ? convertBrToLineBreak(this.props.message.body) : "",
        });
        useEmojiPicker("emoji-picker", {
            onSelect: (str) => this.addEmoji(str),
        });
        useEffect(
            (focus) => {
                if (focus && this.ref.el) {
                    this.ref.el.focus();
                }
            },
            () => [this.props.autofocus + this.state.autofocus, this.props.placeholder]
        );
        useEffect(
            (messageToReplyTo) => {
                if (messageToReplyTo && messageToReplyTo.resId === this.props.threadId) {
                    this.state.autofocus++;
                }
            },
            () => [this.messaging.discuss.messageToReplyTo]
        );
        onWillUpdateProps(({ message }) => {
            this.state.value = message ? convertBrToLineBreak(message.body) : "";
        });
        useEffect(
            () => {
                this.ref.el.style.height = "1px";
                this.ref.el.style.height = this.ref.el.scrollHeight + "px";
            },
            () => [this.state.value, this.ref.el]
        );
        onMounted(() => this.ref.el.scrollTo({ top: 0, behavior: "instant" }));
        onExternalClick("composer", async (ev) => {
            // Let event be handled by bubbling handlers first.
            await new Promise(setTimeout);
            if (isEventHandled(ev, "message.replyTo") || isEventHandled(ev, "emoji.selectEmoji")) {
                return;
            }
            this.messaging.cancelReplyTo();
        });
    }

    get hasReplyToHeader() {
        const { messageToReplyTo } = this.messaging.discuss;
        if (!messageToReplyTo) {
            return false;
        }
        return (
            messageToReplyTo.resId === this.props.threadId ||
            (this.props.threadId === "inbox" && messageToReplyTo.needaction)
        );
    }

    onKeydown(ev) {
        if (ev.key === "Enter") {
            const shouldPost = this.props.mode === "extended" ? ev.ctrlKey : !ev.shiftKey;
            if (!shouldPost) {
                return;
            }
            ev.preventDefault(); // to prevent useless return
            if (this.props.message) {
                this.editMessage();
            } else {
                this.sendMessage();
            }
        } else if (ev.key === "Escape") {
            this.props.onDiscardCallback();
        }
    }

    async sendMessage() {
        const el = this.ref.el;
        if (el.value.trim()) {
            const { messageToReplyTo } = this.messaging.discuss;
            const { id: parentId, isNote, resId, resModel } = messageToReplyTo || {};
            const postData = {
                isNote: this.props.type === "note" || isNote,
                parentId,
            };
            if (messageToReplyTo && this.props.threadId === this.messaging.discuss.inbox.id) {
                await this.messaging.postInboxReply(resId, resModel, el.value, postData);
            } else {
                await this.messaging.postMessage(this.props.threadId, el.value, postData);
            }
            this.messaging.cancelReplyTo();
            if (this.props.onPostCallback) {
                this.props.onPostCallback();
            }
        }
        this.state.value = "";
        el.focus();
    }

    async editMessage() {
        const el = this.ref.el;
        if (el.value.trim()) {
            await this.messaging.updateMessage(this.props.message.id, this.ref.el.value);
            if (this.props.onPostCallback) {
                this.props.onPostCallback();
            }
        }
        this.state.value = "";
        el.focus();
    }

    addEmoji(str) {
        this.state.value += str;
        this.state.autofocus++;
    }
}

Object.assign(Composer, {
    defaultProps: {
        mode: "normal",
        onDiscardCallback: () => {},
        type: "message",
    }, // mode = compact, normal, extended
    props: [
        "threadId?",
        "message?",
        "autofocus?",
        "highlightReplyTo?",
        "onDiscardCallback?",
        "onPostCallback?",
        "mode?",
        "placeholder?",
        "type?",
    ],
    template: "mail.composer",
});
