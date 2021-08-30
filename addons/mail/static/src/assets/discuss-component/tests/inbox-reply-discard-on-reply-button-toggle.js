/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            inbox reply: discard on reply button toggle
        [Test/model]
            DiscussComponent
        [Test/assertions]
            3
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                [0]
                    [Record/models]
                        mail.message
                    [mail.message/body]
                        not empty
                    [mail.message/id]
                        100
                    [mail.message/model]
                        res.partner
                    [mail.message/needaction]
                        true
                    [mail.message/needaction_partner_ids]
                        @record
                        .{Test/data}
                        .{Data/currentPartnerId}
                    [mail.message/res_id]
                        20
                [1]
                    [Record/models]
                        mail.notification
                    [mail.notification/mail_message_id]
                        100
                    [mail.notification/notification_status]
                        sent
                    [mail.notification/notification_type]
                        inbox
                    [mail.notification/res_partner_id]
                        @record
                        .{Test/data}
                        .{Data/currentPartnerId}
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            @testEnv
            .{Record/insert}
                [Record/models]
                    DiscussComponent
            @testEnv
            .{Utils/waitUntilEvent}
                [eventName]
                    o-thread-view-hint-processed
                [message]
                    should wait until inbox displayed its messages
                [predicate]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            hint
                            threadViewer
                        [Function/out]
                            @hint
                            .{Hint/type}
                            .{=}
                                messages-loaded
                            .{&}
                                @threadViewer
                                .{ThreadViewer/thread}
                                .{Thread/model}
                                .{=}
                                    mail.box
                            .{&}
                                @threadViewer
                                .{ThreadViewer/thread}
                                .{Thread/id}
                                .{=}
                                    inbox
            {Test/assert}
                []
                    @testEnv
                    .{Discuss/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should display a single message

            @testEnv
            .{UI/click}
                @testEnv
                .{Discuss/thread}
                .{Thread/cache}
                .{ThreadCache/messages}
                .{Collection/first}
                .{Message/messageComponents}
                .{Collection/first}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{Discuss/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/first}
                    .{Message/actionList}
                    .{MessageActionList/messageActionListComponents}
                    .{Collection/first}
                    .{MessageActionListComponent/actionReply}
            {Test/assert}
                []
                    @testEnv
                    .{Discuss/thread}
                    .{Thread/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should have composer after clicking on reply to message

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{Discuss/thread}
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/first}
                    .{Message/actionList}
                    .{MessageActionList/messageActionListComponents}
                    .{Collection/first}
                    .{MessageActionListComponent/actionReply}
            {Test/assert}
                []
                    @testEnv
                    .{Discuss/thread}
                    .{Thread/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/length}
                    .{=}
                        0
                []
                    reply composer should be closed after clicking on reply button again
`;
