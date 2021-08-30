/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            openChat: open new chat for user
        [Test/model]
            Env
        [Test/assertions]
            3
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        res.partner
                    [res.partner/id]
                        14
                []
                    [Record/models]
                        res.users
                    [res.users/id]
                        11
                    [res.users/partner_id]
                        14
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            :existingChat
                @testEnv
                .{Record/find}
                    [Record/models]
                        Thread
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            thread
                        [Function/out]
                            @thread
                            .{Thread/channelType}
                            .{=}
                                chat
                            .{&}
                                @thread
                                .{Thread/correspondent}
                            .{&}
                                @thread
                                .{Thread/correspondent}
                                .{Partner/id}
                                .{=}
                                    14
                            .{&}
                                @thread
                                .{Thread/model}
                                .{=}
                                    mail.channel
                            .{&}
                                @thread
                                .{Thread/public}
                                .{=}
                                    private
            {Test/assert}
                []
                    @existingChat
                    .{isFalsy}
                []
                    a chat should not exist with the target partner initially

            @testEnv
            .{Env/openChat}
                [partnerId]
                    14
            :chat
                @testEnv
                .{Record/find}
                    [Record/models]
                        Thread
                    {Record/insert}
                        [Record/models]
                            Function
                        [Function/in]
                            thread
                        [Function/out]
                            @thread
                            .{Thread/channelType}
                            .{=}
                                chat
                            .{&}
                                @thread
                                .{Thread/correspondent}
                            .{&}
                                @thread
                                .{Thread/correspondent}
                                .{Partner/id}
                                .{=}
                                    14
                            .{&}
                                @thread
                                .{Thread/model}
                                .{=}
                                    mail.channel
                            .{&}
                                @thread
                                .{Thread/public}
                                .{=}
                                    private
            {Test/assert}
                []
                    @chat
                []
                    a chat should exist with the target partner
            {Test/assert}
                []
                    @chat
                    .{Thread/threadViews}
                    .{Collection/length}
                    .{=}
                        1
                []
                    the chat should be displayed in a 'ThreadView'
`;
