/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            display reason for suggested recipient on mouse over
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
                [0]
                    [Record/models]
                        res.fake
                    [res.fake/id]
                        10
                    [res.fake/partner_ids]
                        100
                [1]
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
                    .{ChatterTopbarComponent/buttonSendMessage}
            {Test/assert}
                []
                    @testEnv
                    .{Record/all}
                        [Record/models]
                            ComposerSuggestedRecipientComponent
                    .{Collection/first}
                    .{web.Element/title}
                    .{=}
                        Add as recipient and follower (reason: Email partner)
                []
                    must display reason for suggested recipient on mouse over
`;
