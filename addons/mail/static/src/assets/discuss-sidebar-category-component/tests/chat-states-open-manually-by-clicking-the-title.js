/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            chat - states: open manually by clicking the title
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
                [0]
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
                [1]
                    [Record/models]
                        res.users.settings
                    [res.users.settings/user_id]
                        @record
                        .{Test/data}
                        .{Data/currentUserId}
                    [res.users.settings/is_discuss_sidebar_category_chat_open]
                        false
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            @testEnv
            .{UI/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{Discuss/categoryChat}
                    .{DiscussSidebarCategory/discussSidebarCategoryComponents}
                    .{Collection/first}
                    .{DiscussSidebarCategoryComponent/title}
            {Test/assert}
                []
                    @testEnv
                    .{Record/findById}
                        [Thread/id]
                            10
                        [Thread/model]
                            mail.channel
                    .{Thread/discussSidebarCategoryItemComponents}
                    .{Collection/length}
                    .{=}
                        1
                []
                    Category chat should be open and the content should be visible
`;
