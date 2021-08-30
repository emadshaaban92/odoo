/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            message with only subtype should be displayed and not considered as empty
        [Test/model]
            ThreadViewComponent
        [Test/assertions]
            2
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
                    [mail.message/id]
                        101
                    [mail.message/model]
                        mail.channel
                    [mail.message/res_id]
                        11
                    [mail.message/subtype_id]
                        10
                []
                    [Record/models]
                        mail.message.subtype
                    [mail.message.subtype/description]
                        Task created
                    [mail.message.subtype/id]
                        10
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
            .{UI/afterEvent}
                [eventName]
                    o-thread-view-hint-processed
                [func]
                    @testEnv
                    .{Record/insert}
                        [Record/models]
                            ThreadViewComponent
                        [ThreadViewComponent/threadView]
                            @threadViewer
                            .{ThreadViewer/threadView}
                [message]
                    should wait until thread becomes loaded with messages
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
                                    mail.channel
                            .{&}
                                @threadViewer
                                .{ThreadViewer/thread}
                                .{Thread/id}
                                .{=}
                                    11
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
                    should display 1 message (message with subtype description 'task created')
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
                    .{web.Element/textContent}
                    .{=}
                        Task created
                []
                    message should have 'Task created' (from its subtype description)
`;
