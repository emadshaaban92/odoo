/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            new messages separator on posting message on channel with no message initially
        [Test/model]
            ThreadViewComponent
        [Test/assertions]
            4
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                [Record/models]
                    mail.channel
                [mail.channel/channel_type]
                    channel
                [mail.channel/id]
                    20
                [mail.channel/is_pinned]
                    true
                [mail.channel/message_unread_counter]
                    0
                [mail.channel/name]
                    General
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            :thread
                @testEnv
                .{Record/findById}
                    [Thread/id]
                        20
                    [Thread/model]
                        mail.channel
            :threadViewer
                @testEnv
                .{Record/insert}
                    [Record/models]
                        ThreadViewer
                    [ThreadViewer/hasThreadView]
                        true
                    [ThreadViewer/thread]
                        @thread
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
                        0
                []
                    should have no messages
            {Test/assert}
                []
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/messageListComponents}
                    .{Collection/first}
                    .{MessageListComponent/separatorNewMessages}
                    .{isFalsy}
                []
                    should not display 'new messages' separator

            @testEnv
            .{UI/focus}
                @threadViewer
                .{ThreadViewer/threadView}
                .{ThreadView/thread}
                .{ThreadView/composer}
                .{Composer/composerTextInputComponents}
                .{Collection/first}
                .{ComposerTextInputComponent/textarea}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/insertText}
                    hey !
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/thread}
                    .{Thread/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/first}
                    .{ComposerViewComponent/buttonSend}
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
                    should have the message current partner just posted
            {Test/assert}
                []
                    @threadViewer
                    .{ThreadViewer/threadView}
                    .{ThreadView/messageListComponents}
                    .{Collection/first}
                    .{MessageListComponent/separatorNewMessages}
                    .{isFalsy}
                []
                    still no separator shown when current partner posted a message
`;
