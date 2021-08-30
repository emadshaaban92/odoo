/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            clear: should set attribute field the default value
        [Test/model]
            RecordFieldCommand
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            :task
                @testEnv
                .{Record/insert}
                    [Record/models]
                        TestTask
                    [TestTask/id]
                        1
                    [TestTask/difficulty]
                        5
            @testEnv
            .{Record/update}
                [0]
                    @task
                [1]
                    [TestTask/difficulty]
                        @testEnv
                        .{Record/empty}
            {Test/assert}
                []
                    @task
                    .{TestTask/difficulty}
                    .{=}
                        1
                []
                    clear: should set attribute field the default value
`;
