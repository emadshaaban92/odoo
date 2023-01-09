/* @odoo-module */

import { Component } from "@odoo/owl";
import { useStore } from "../core/messaging_hook";

/**
 * @typedef {Object} Props
 * @property {import("@mail/new/core/message_model").Message} message
 * @property {import("@mail/new/core/thread_model").Thread} thread
 * @extends {Component<Props, Env>}
 */
export class MessageSeenIndicator extends Component {
    static template = "mail.message_seen_indicator";
    static components = {};
    static props = ["message", "thread"];
    static defaultProps = {};

    setup() {
        this.store = useStore();
    }

    get hasEveryoneSeen() {
        const otherPartnerSeenInfosDidNotSee = [...this.props.thread.partnerSeenInfos].filter(
            (partnerSeenInfo) => {
                return (
                    partnerSeenInfo.partner.id !== this.props.message.author.id &&
                    (!partnerSeenInfo.lastSeenMessage ||
                        partnerSeenInfo.lastSeenMessage.id < this.props.message.id)
                );
            }
        );
        return otherPartnerSeenInfosDidNotSee.length === 0;
    }

    get isMessagePreviousToLastCurrentPartnerMessageSeenByEveryone() {
        if (!this.props.thread.lastCurrentPartnerMessageSeenByEveryone) {
            return false;
        }
        return this.props.message.id < this.props.thread.lastCurrentPartnerMessageSeenByEveryone.id;
    }

    get hasSomeoneSeen() {
        const otherPartnerSeenInfosSeen = [...this.props.thread.partnerSeenInfos].filter(
            (partnerSeenInfo) =>
                partnerSeenInfo.partner.id !== this.props.message.author.id &&
                partnerSeenInfo.lastSeenMessage &&
                partnerSeenInfo.lastSeenMessage.id >= this.props.message.id
        );
        return otherPartnerSeenInfosSeen.length > 0;
    }

    get hasSomeoneFetched() {
        const otherPartnerSeenInfosFetched = [...this.props.thread.partnerSeenInfos].filter(
            (partnerSeenInfo) =>
                partnerSeenInfo.partner.id !== this.props.message.author.id &&
                partnerSeenInfo.lastFetchedMessage &&
                partnerSeenInfo.lastFetchedMessage.id >= this.props.message.id
        );
        return otherPartnerSeenInfosFetched.length > 0;
    }
}
