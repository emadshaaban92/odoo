/** @odoo-module **/

import { attr, Model } from '@mail/model';
import { _t } from "web.core";

const statusToClassDict = {
    outgoing: 'fa fa-send-o',
    sent: 'fa fa-check',
    open: 'fa fa-check',
    reply: 'fa fa-check',
    bounce: 'fa fa-exclamation',
    error: 'fa fa-exclamation',
    cancel: 'fa fa-trash-o',
};

const statusToIconTitleDict = {
    outgoing: _t("Outgoing"),
    sent: _t("Sent"),
    open: _t("Opened by Recipient"),
    reply: _t("Reply Received"),
    bounce: _t("Bounced"),
    error: _t("Error"),
    cancel: _t("Canceled"),
};

Model({
    name: 'MailingTrace',
    fields: {
        id: attr({ identifying: true }),
        email: attr(),
        failure_type: attr(),
        iconClass: attr({
            compute() {
                return statusToClassDict[this.trace_status] ? statusToClassDict[this.trace_status] : '';
            },
        }),
        iconTitle: attr({
            compute() {
                return statusToIconTitleDict[this.trace_status] ? statusToIconTitleDict[this.trace_status] : '';
            },
        }),
        isFailure: attr({
            compute() {
                return !!this.failure_type || ['bounce', 'cancel'].includes(this.trace_status);
            },
        }),
        mailing_id: attr(),
        trace_type: attr(),
        trace_status: attr(),
    },
});
