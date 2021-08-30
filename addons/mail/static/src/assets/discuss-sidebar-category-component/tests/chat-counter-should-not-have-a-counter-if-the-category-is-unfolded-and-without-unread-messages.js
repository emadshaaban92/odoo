/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            chat - counter: should not have a counter if the category is unfolded and without unread messages
        [Test/model]
            DiscussSidebarCategoryComponent
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                [Record/models]
                    mail.channel
                [mail.channel/channel_type]
                    chat
                [mail.channel/id]
                    10
                [mail.channel/message_unread_counter]
                    0
                [mail.channel/public]
                    private
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            {Test/assert}
                []
                    @testEnv
                    .{Discuss/categoryChat}
                    .{DiscussSidebarCategory/counter}
                    .{=}
                        0
                []
                    should not have a counter if the category is unfolded and without unread messages
`;
