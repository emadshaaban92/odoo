/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            click on partner follower details
        [Test/model]
            FollowerComponent
        [Test/assertions]
            7
        [Test/scenario]
            :openFormDef
                {Record/insert}
                    [Record/models]
                        Deferred
            :bus
                {Record/insert}
                    [Record/models]
                        Bus
            {Bus/on}
                [0]
                    @bus
                [1]
                    do-action
                [2]
                    null
                [3]
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            payload
                        [Function/out]
                            {Test/step}
                                do_action
                            {Test/assert}
                                []
                                    @payload
                                    .{Dict/get}
                                        action
                                    .{Dict/get}
                                        res_id
                                    .{=}
                                        3
                                []
                                    The redirect action should redirect to the right res id (3)
                            {Test/assert}
                                []
                                    @payload
                                    .{Dict/get}
                                        action
                                    .{Dict/get}
                                        res_model
                                    .{=}
                                        res.partner
                                []
                                    The redirect action should redirect to the right res model (res.partner)
                            {Test/assert}
                                []
                                    @payload
                                    .{Dict/get}
                                        action
                                    .{Dict/get}
                                        type
                                    .{=}
                                        ir.actions.act_window
                                []
                                    The redirect action should be of type 'ir.actions.act_window'
                            {Promise/resolve}
                                @openFormDef
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
                    [Env/owlEnv]
                        [bus]
                            @bus
            @testEnv
            .{Record/insert}
                [Record/models]
                    res.partner
                [res.partner/id]
                    100
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            :thread
                @testEnv
                .{Record/insert}
                    [Record/models]
                        Thread
                    [Thread/id]
                        100
                    [Thread/model]
                        res.partner
            :follower
                @testEnv
                .{Record/insert}
                    [Record/models]
                        Follower
                    [Follower/followedThread]
                        @thread
                    [Follower/id]
                        2
                    [Follower/isActive]
                        true
                    [Follower/isEditable]
                        true
                    [Follower/partner]
                        @testEnv
                        .{Record/insert}
                            [Record/models]
                                Partner
                            [Partner/email]
                                bla@bla.bla
                            [Partner/id]
                                @testEnv
                                .{Env/currentPartner}
                                .{Partner/id}
                            [Partner/name]
                                François Perusse
            @testEnv
            .{Record/insert}
                [Record/models]
                    FollowerComponent
                [FollowerComponent/follower]
                    @follower
            {Test/assert}
                []
                    @follower
                    .{Follower/followerComponents}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should have follower component
            {Test/assert}
                []
                    @follower
                    .{Follower/followerComponents}
                    .{Collection/first}
                    .{FollowerComponent/details}
                []
                    should display a details part

            @testEnv
            .{UI/click}
                @follower
                .{Follower/followerComponents}
                .{Collection/first}
                .{FollowerComponent/details}
            {Promise/await}
                @openFormDef
            {Test/verifySteps}
                []
                    do_action
                []
                    clicking on follower should redirect to partner form view
`;
