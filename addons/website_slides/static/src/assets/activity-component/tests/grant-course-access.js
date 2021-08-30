/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            grant course access
        [Test/feature]
            website_slides
        [Test/model]
            ActivityComponent
        [Test/assertions]
            8
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
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
                                @args
                                .{Dict/get}
                                    method
                                .{=}
                                    action_grant_access
                            .{then}
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        args
                                    .{Dict/get}
                                        length
                                    .{=}
                                        1
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        args
                                    .{Collection/first}
                                    .{Collection/length}
                                    .{=}
                                        1
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        args
                                    .{Collection/first}
                                    .{Collection/first}
                                    .{=}
                                        100
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        kwargs
                                    .{Dict/get}
                                        partner_id
                                    .{=}
                                        5
                                {Test/step}
                                    access_grant
                            @original
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        res.partner
                    [res.partner/id]
                        5
                []
                    [Record/models]
                        slide.channel
                    [slide.channel/activity_ids]
                        12
                    [slide.channel/id]
                        100
                []
                    [Record/models]
                        mail.activity
                    [mail.activity/can_write]
                        true
                    [mail.activity/id]
                        12
                    [mail.activity/res_id]
                        100
                    [mail.activity/request_partner_id]
                        5
                    [mail.activity/res_model]
                        slide.channel
            @testEnv
            .{Record/insert}
                [Record/models]
                    ChatterContainerComponent
                [ChatterContainerComponent/threadId]
                    100
                [ChatterContainerComponent/threadModel]
                    slide.channel
            {Test/assert}
                []
                    @activity
                    .{Activity/activityComponents}
                    .{ActivityComponent/length}
                    .{=}
                        1
                []
                    should have activity component
            {Test/assert}
                []
                    @activity
                    .{Activity/activityComponents}
                    .{Collection/first}
                    .{ActivityComponent/grantAccessButton}
                []
                    should have grant access button

            @testEnv
            .{UI/click}
                @activity
                .{Activity/activityComponents}
                .{Collection/first}
                .{ActivityComponent/grantAccessButton}
            {Test/verifySteps}
                []
                    access_grant
                []
                    Grant button should trigger the right rpc call
`;
