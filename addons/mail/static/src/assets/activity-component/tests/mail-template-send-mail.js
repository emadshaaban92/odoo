/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            mail template: send mail
        [Test/model]
            ActivityComponent
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
                                @args
                                .{Dict/get}
                                    method
                                .{=}
                                    activity_send_mail
                            .{then}
                                {Test/step}
                                    activity_send_mail
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
                                        42
                                {Test/assert}
                                    @args
                                    .{Dict/get}
                                        args
                                    .{Collection/second}
                                    .{=}
                                        1
                            .{else}
                                @original
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        res.partner
                    [res.partner/activity_ids]
                        12
                    [res.partner/id]
                        42
                []
                    [Record/models]
                        mail.template
                    [mail.template/id]
                        1
                    [mail.template/name]
                        Dummy mail template
                []
                    [Record/models]
                        mail.activity
                    [mail.activity/activity_type_id]
                        1
                    [mail.activity/id]
                        12
                    [mail.activity/mail_template_ids]
                        1
                    [mail.activity/res_id]
                        42
                    [mail.activity/res_model]
                        res.partner
            @testEnv
            .{Record/insert}
                [Record/models]
                    ChatterContainerComponent
                [ChatterContainerComponent/threadId]
                    42
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
                    .{ActivityComponent/send}
                []
                    should have activity mail template name send button

            @testEnv
            .{UI/click}
                @activity
                .{Activity/mailTemplates}
                .{Collection/first}
                .{MailTemplate/mailTemplateComponents}
                .{Collection/first}
                .{MailTemplateComponent/send}
            {Test/verifySteps}
                []
                    activity_send_mail
                []
                    should have called activity_send_mail rpc
`;
