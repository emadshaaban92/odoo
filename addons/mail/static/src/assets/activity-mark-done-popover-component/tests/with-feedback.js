/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            with feedback
        [Test/model]
            ActivityMarkDonePopoverComponent
        [Test/assertions]
            7
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
                                @route
                                .{=}
                                    /web/dataset/call_kw/mail.activity/action_feedback
                            .{then}
                                {Test/step}
                                    action_feedback
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        args
                                    .{Collection/length}
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
                                        12
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        kwargs
                                    .{Dict/get}
                                        attachment_ids
                                    .{Collection/length}
                                    .{=}
                                        0
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        kwargs
                                    .{Dict/get}
                                        feedback
                                    .{=}
                                        This task is done
                                {break}
                            {if}
                                @route
                                .{=}
                                    /web/dataset/call_kw/mail.activity/unlink
                            .{then}
                                {Dev/comment}
                                    'unlink' on non-existing record raises a
                                    server crash
                                {Error/raise}
                                    'unlink' RPC on activity must not be called (already unlinked from mark as done)
                            @original
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
                        not_upload_file
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
            @testEnv
            .{UI/click}
                @activity
                .{Activity/activityComponents}
                .{Collection/first}
                .{ActivityComponent/markDoneButton}
            {UI/focus}
                @activity
                .{Activity/activityMarkDonePopoverComponents}
                .{Collection/first}
                .{ActivityMarkDonePopoverComponent/feedback}
            @testEnv
            .{UI/insertText}
                This task is done
            @testEnv
            .{UI/click}
                @activity
                .{Activity/activityMarkDonePopoverComponents}
                .{Collection/first}
                .{ActivityMarkDonePopoverComponent/doneButton}
            {Test/verifySteps}
                []
                    action_feedback
                []
                    Mark done and schedule next button should call the right rpc
`;
