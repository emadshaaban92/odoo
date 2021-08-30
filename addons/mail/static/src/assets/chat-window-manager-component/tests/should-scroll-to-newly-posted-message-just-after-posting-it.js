/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            should scroll to the newly posted message just after posting it
        [Test/model]
            ChatWindowManagerComponent
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                [0]
                    [Record/models]
                        mail.channel
                    [mail.channel/id]
                        20
                    [mail.channel/is_minimized]
                        true
                    [mail.channel/state]
                        open
                {foreach}
                    {Record/insert}
                        [Record/models]
                            Range
                        [start]
                            0
                        [end]
                            10
                .{as}
                    i
                .{do}
                    {entry}
                        [Record/models]
                            mail.message
                        [mail.message/body]
                            not empty
                        [mail.message/model]
                            mail.channel
                        [mail.message/res_id]
                            20
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
                    ChatWindowManagerComponent
            {Dev/comment}
                Set content of the composer of the chat window
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/focus}
                    @testEnv
                    .{Record/findById}
                        [Thread/id]
                            20
                        [Thread/model]
                            mail.channel
                    .{Thread/composer}
                    .{Composer/composerTextInputComponents}
                    .{Collection/first}
                    .{ComposerTextInputComponent/textarea}
                @testEnv
                .{UI/insertText}
                    WOLOLO
            {Dev/comment}
                Send a new message in the chatwindow to trigger the scroll
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/keydown}
                    [0]
                        @testEnv
                        .{Record/findById}
                            [Thread/id]
                                20
                            [Thread/model]
                                mail.channel
                        .{Thread/composer}
                        .{Composer/composerTextInputComponents}
                        .{Collection/first}
                        .{ComposerTextInputComponent/textarea}
                    [1]
                        [key]
                            Enter
            {Test/assert}
                []
                    @testEnv
                    .{Record/findById}
                        [Thread/id]
                            20
                        [Thread/model]
                            mail.channel
                    .{Thread/threadViews}
                    .{Collection/first}
                    .{ThreadView/messageListComponents}
                    .{Collection/first}
                    .{web.Element/clientHeight}
                    .{=}
                        @testEnv
                        .{Record/findById}
                            [Thread/id]
                                20
                            [Thread/model]
                                mail.channel
                        .{Thread/threadViews}
                        .{Collection/first}
                        .{ThreadView/messageListComponents}
                        .{Collection/first}
                        .{web.Element/scrollHeight}
                        .{-}
                            @testEnv
                            .{Record/findById}
                                [Thread/id]
                                    20
                                [Thread/model]
                                    mail.channel
                            .{Thread/threadViews}
                            .{Collection/first}
                            .{ThreadView/messageListComponents}
                            .{Collection/first}
                            .{web.Element/scrollTop}
                []
                    chat window should scroll to the newly posted message just after posting it
`;
