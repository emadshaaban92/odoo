/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Action
        [Action/name]
            Thread/promptAddFollower
        [Action/params]
            record
                [type]
                    Thread
        [Action/behavior]
            :action
                {Record/insert}
                    [Record/models]
                        Object
                    [type]
                        ir.actions.act_window
                    [res_model]
                        mail.wizard.invite
                    [view_mode]
                        form
                    [views]
                        {Record/insert}
                            [Record/models]
                                Collection
                            {Record/insert}
                                [Record/models]
                                    Collection
                                [0]
                                    false
                                [1]
                                    form
                    [name]
                        {Locale/text}
                            Invite Follower
                    [target]
                        new
                    [context]
                        [default_res_model]
                            @record
                            .{Thread/model}
                        [default_res_id]
                            @record
                            .{Thread/id}
            @env
            .{Env/owlEnv}
            .{Dict/get}
                bus
            .{Dict/get}
                trigger
            .{Function/call}
                [0]
                    do-action
                [1]
                    [action]
                        @action
                    [options]
                        [on_close]
                            {Record/doAsync}
                                [0]
                                    @record
                                [1]
                                    {Thread/fetchData}
                                        [0]
                                            @record
                                        [1]
                                            followers
                            @env
                            .{Env/owlEnv}
                            .{Dict/get}
                                bus
                            .{Dict/get}
                                trigger
                            .{Function/call}
                                Thread:promptAddFollower-closed
`;
