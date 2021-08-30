/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            suggested recipients should not be notified when posting an internal note
        [Test/model]
            ChatterComponent
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        res.fake
                    [res.fake/id]
                        10
                    [res.fake/partner_ids]
                        100
                []
                    [Record/models]
                        res.partner
                    [res.partner/display_name]
                        John Jane
                    [res.partner/email]
                        john@jane.be
                    [res.partner/id]
                        100
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
                [Server/mockRPC]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            route
                            args
                            original
                        [Function/out]
                            {if}
                                @route
                                .{=}
                                    /mail/message/post
                            .{then}
                                {Test/assert}
                                    [0]
                                        @record
                                    [1]
                                        @args
                                        .{Dict/get}
                                            post_data
                                        .{Dict/get}
                                            partner_ids
                                        .{Collection/length}
                                        .{=}
                                            0
                                    [2]
                                        post_data should not contain suggested recipients when posting an internal note
                            @original
            @testEnv
            .{Record/insert}
                [Record/models]
                    ChatterContainerComponent
                [ChatterContainerComponent/threadId]
                    10
                [ChatterContainerComponent/threadModel]
                    res.fake
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @chatter
                    .{Chatter/chatterTopbarComponents}
                    .{Collection/first}
                    .{ChatterTopbarComponent/buttonLogNote}
            @testEnv
            .{UI/focus}
                @chatter
                .{Chatter/composer}
                .{Composer/composerTextInputComponents}
                .{Collection/first}
                .{ComposerTextInputComponent/textarea}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/insertText}
                    Dummy Message
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @chatter
                    .{Chatter/composer}
                    .{Composer/composerViewComponents}
                    .{Collection/first}
                    .{ComposerViewComponent/buttonSend}
`;
