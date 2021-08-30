/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            click on mark as done
        [Test/model]
            ActivityComponent
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
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            :today
                {Record/insert}
                    [Record/models]
                        Date
            :tomorrow
                {Record/insert}
                    [Record/models]
                        Date
                .{Date/setDate}
                    @today
                    .{Date/getDate}
                    .{+}
                        1
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        res.partner
                    [res.partner/activity_ids]
                        12
                    [res.partner/id]
                        100
                []
                    [Record/models]
                        mail.activity
                    [mail.activity/activity_category]
                        default
                    [mail.activity/activity_type_id]
                        1
                    [mail.activity/can_write]
                        true
                    [mail.activity/id]
                        12
                    [mail.activity/res_id]
                        100
                    [mail.activity/res_model]
                        res.partner
            @testEnv
            .{Record/insert}
                [Record/models]
                    ChatterContainerComponent
                [ChatterContainerComponent/threadId]
                    100
                [ChatterContainerComponent/threadModel]
                    res.partner
            {Test/assert}
                []
                    @activity
                    .{Activity/activityComponents}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should have activity component
            {Test/assert}
                []
                    @activity
                    .{Activity/activityComponents}
                    .{Collection/first}
                    .{ActivityComponent/markDoneButton}
                []
                    should have activity Mark as Done button

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @activity
                    .{Activity/activityComponents}
                    .{Collection/first}
                    .{ActivityComponent/markDoneButton}
            {Test/assert}
                []
                    @activity
                    .{Activity/activityMarkDonePopoverComponents}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should have opened the mark done popover

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @activity
                    .{Activity/activityComponents}
                    .{Collection/first}
                    .{ActivityComponent/markDoneButton}
            {Test/assert}
                []
                    @activity
                    .{Activity/activityMarkDonePopoverComponents}
                    .{Collection/length}
                    .{=}
                        0
                []
                    should have closed the mark done popover
`;
