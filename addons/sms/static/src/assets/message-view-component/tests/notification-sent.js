/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            Notification Sent
        [Test/feature]
            sms
        [Test/model]
            MessageViewComponent
        [Test/assertions]
            9
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        mail.channel
                    [mail.channel/id]
                        11
                []
                    [Record/models]
                        mail.message
                    [mail.message/body]
                        not empty
                    [mail.message/id]
                        10
                    [mail.message/message_type]
                        sms
                    [mail.message/model]
                        mail.channel
                    [mail.message/res_id]
                        11
                []
                    [Record/models]
                        mail.notification
                    [mail.notification/id]
                        11
                    [mail.notification/mail_message_id]
                        10
                    [mail.notification/notification_status]
                        sent
                    [mail.notification/notification_type]
                        sms
                    [mail.notification/res_partner_id]
                        12
                []
                    [Record/models]
                        res.partner
                    [res.partner/id]
                        12
                    [res.partner/name]
                        Someone
                    [res.partner/partner_share]
                        true
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            :threadViewer
                @testEnv
                .{Record/insert}
                    [Record/models]
                        ThreadViewer
                    [ThreadViewer/hasThreadView]
                        true
                    [ThreadViewer/thread]
                        @testEnv
                        .{Record/insert}
                            [Record/models]
                                Thread
                            [Thread/id]
                                11
                            [Thread/model]
                                mail.channel
            @testEnv
            .{Record/insert}
                [Record/models]
                    ThreadViewComponent
                [ThreadViewComponent/threadView]
                    @threadViewer
                    .{ThreadViewer/threadView}
            {Test/assert}
                []
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should display a message component
            {Test/assert}
                []
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/first}
                    .{Message/messageComponents}
                    .{Collection/first}
                    .{MessageViewComponent/notificationIconClickable}
                []
                    should display the notification icon container
            {Test/assert}
                []
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/first}
                    .{Message/messageComponents}
                    .{Collection/first}
                    .{MessageViewComponent/notificationIcon}
                []
                    should display the notification icon
            {Test/assert}
                []
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/first}
                    .{Message/messageComponents}
                    .{Collection/first}
                    .{MessageViewComponent/notificationIconSms}
                []
                    icon should represent sms

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/first}
                    .{Message/messageComponents}
                    .{Collection/first}
                    .{MessageViewComponent/notificationIconClickable}
            {Test/assert}
                []
                    @testEnv
                    .{Record/all}
                        [Record/models]
                            NotificationPopoverComponent
                    .{Collection/length}
                    .{=}
                        1
                []
                    notification popover should be open
            {Test/assert}
                []
                    @testEnv
                    .{Record/all}
                        [Record/models]
                            NotificationPopoverComponent
                    .{Collection/first}
                    .{NotificationPopoverComponent/notificationIcon}
                []
                    popover should have one icon
            {Test/assert}
                []
                    @testEnv
                    .{Record/all}
                        [Record/models]
                            NotificationPopoverComponent
                    .{Collection/first}
                    .{NotificationPopoverComponent/notification}
                    .{Notification/status}
                    .{=}
                        sent
                []
                    popover should have the sent icon
            {Test/assert}
                []
                    @testEnv
                    .{Record/all}
                        [Record/models]
                            NotificationPopoverComponent
                    .{Collection/first}
                    .{NotificationPopoverComponent/notificationPartnerName}
                []
                    popover should have the partner name
            {Test/assert}
                []
                    @testEnv
                    .{Record/all}
                        [Record/models]
                            NotificationPopoverComponent
                    .{Collection/first}
                    .{NotificationPopoverComponent/notificationPartnerName}
                    .{web.Element/textContent}
                    .{=}
                        Someone
                []
                    partner name should be correct
`;
