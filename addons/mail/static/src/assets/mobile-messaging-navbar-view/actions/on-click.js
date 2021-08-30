/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            MobileMessagingNavbarView/onClick
        [Action/params]
            record
                [type]
                    MobileMessagingNavbarView
            tabId
                [type]
                    String
        [Action/behavior]
            {if}
                @record
                .{MobileMessagingNavbarView/discuss}
            .{then}
                {if}
                    @record
                    .{MobileMessagingNavbarView/discuss}
                    .{Discuss/activeMobileNavbarTabId}
                    .{=}
                        @tabId
                .{then}
                    {break}
                {Record/update}
                    [0]
                        @record
                        .{MobileMessagingNavbarView/discuss}
                    [1]
                        [Discuss/activeMobileNavbarTabId]
                            @tabId
                {if}
                    @record
                    .{MobileMessagingNavbarView/discuss}
                    .{Discuss/activeMobileNavbarTabId}
                    .{=}
                        mailbox
                    .{&}
                        @record
                        .{MobileMessagingNavbarView/discuss}
                        .{Discuss/thread}
                        .{isFalsy}
                        .{|}
                            @record
                            .{MobileMessagingNavbarView/discuss}
                            .{Discuss/thread}
                            .{Thread/model}
                            .{!=}
                                mailbox
                .{then}
                    {Record/update}
                        [0]
                            @record
                            .{MobileMessagingNavbarView/discuss}
                        [1]
                            [Discuss/thread]
                                {Env/inbox}
                {if}
                    @record
                    .{MobileMessagingNavbarView/discuss}
                    .{Discuss/activeMobileNavbarTabId}
                    .{!=}
                        mailbox
                .{then}
                    {Record/update}
                        [0]
                            @record
                            .{MobileMessagingNavbarView/discuss}
                        [1]
                            [Discuss/thread]
                                {Record/empty}
                {if}
                    @record
                    .{MobileMessagingNavbarView/discuss}
                    .{Discuss/activeMobileNavbarTabId}
                    .{!=}
                        chat
                .{then}
                    {Record/update}
                        [0]
                            @record
                            .{MobileMessagingNavbarView/discuss}
                        [1]
                            [Discuss/isAddingChat]
                                false
                {if}
                    @record
                    .{MobileMessagingNavbarView/discuss}
                    .{Discuss/activeMobileNavbarTabId}
                    .{!=}
                        channel
                .{then}
                    {Record/update}
                        [0]
                            @record
                            .{MobileMessagingNavbarView/discuss}
                        [1]
                            [Discuss/isAddingChannel]
                                false
            {if}
                @record
                .{MobileMessagingNavbarView/messagingMenu}
            .{then}
                {Record/update}
                    [0]
                        @record
                        .{MobileMessagingNavbarView/messagingMenu}
                    [1]
                        [MessagingMenu/activeTabId]
                            @tabId
`;
