/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            Activity/fetchAndUpdate
        [Action/params]
            record
        [Action/behavior]
            :res
                {Env/owlEnv}
                .{Dict/get}
                    services
                .{Dict/get}
                    rpc
                .{Function/call}
                    [0]
                        [model]
                            mail.activity
                        [method]
                            activity_format
                        [arg]
                            @record
                            .{Activity/id}
                    [1]
                        [shadow]
                            true
                .{Promise/catch}
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            e
                        [Function/out]
                            :errorName
                                @e
                                .{Error/message}
                                .{&}
                                    @e
                                    .{Error/message}
                                    .{ErrorMessage/data}
                                .{&}
                                    @e
                                    .{Error/message}
                                    .{ErrorMessage/data}
                                    .{ErrorMessageData/name}
                            {if}
                                @errorName
                                .{=}
                                    odoo.exceptions.MissingError
                            .{then}
                                {Record/insert}
                                    [Record/models]
                                        Collection
                            .{else}
                                {Error/raise}
                                    @e
            :data
                @res
                .{Collection/first}
            :shouldDelete
                false
            {if}
                @data
            .{then}
                {Record/update}
                    [0]
                        @record
                    [1]
                        {Activity/convertData}
                            @data
            .{else}
                :shouldDelete
                    true
            {Thread/fetchData}
                [0]
                    @record
                    .{Activity/thread}
                [1]
                    activities
                    attachments
                    messages
            {if}
                @shouldDelete
            .{then}
                {Record/delete}
                    @record
`;
