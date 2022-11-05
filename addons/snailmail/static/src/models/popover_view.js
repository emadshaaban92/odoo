/** @odoo-module **/

import { clear, one, Patch } from '@mail/model';

Patch({
    name: 'PopoverView',
    fields: {
        anchorRef: {
            compute() {
                if (this.messageViewOwnerAsSnailmailNotificationContent) {
                    return this.messageViewOwnerAsSnailmailNotificationContent.notificationIconRef;
                }
                return this._super();
            },
        },
        content: {
            compute() {
                if (this.snailmailNotificationPopoverContentView) {
                    return this.snailmailNotificationPopoverContentView;
                }
                return this._super();
            },
        },
        contentComponentName: {
            compute() {
                if (this.snailmailNotificationPopoverContentView) {
                    return 'SnailmailNotificationPopoverContentView';
                }
                return this._super();
            },
        },
        messageViewOwnerAsSnailmailNotificationContent: one('MessageView', {
            identifying: true,
            inverse: 'snailmailNotificationPopoverView',
        }),
        snailmailNotificationPopoverContentView: one('SnailmailNotificationPopoverContentView', {
            compute() {
                if (this.messageViewOwnerAsSnailmailNotificationContent) {
                    return {};
                }
                return clear();
            },
            inverse: 'popoverViewOwner',
        }),
    },
});
