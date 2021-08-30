/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            do not show message seen indicator if not authored by me
        [Test/model]
            MessageViewComponent
        [Test/assertions]
            2
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
            :author
                @testEnv
                .{Record/insert}
                    [Record/models]
                        Partner
                    [Partner/displayName]
                        Demo User
                    [Partner/id]
                        100
            :thread
                @testEnv
                .{Record/insert}
                    [Record/models]
                        Thread
                    [Thread/channelType]
                        chat
                    [Thread/id]
                        11
                    [Thread/model]
                        mail.channel
                    [Thread/partnerSeenInfos]
                        @testEnv
                        .{Record/insert}
                            [0]
                                [Record/models]
                                    ThreadPartnerSeenInfo
                                [ThreadPartnerSeenInfo/lastFetchedMessage]
                                    @testEnv
                                    .{Record/insert}
                                        [Record/models]
                                            Message
                                        [Message/id]
                                            100
                                [ThreadPartnerSeenInfo/partner]
                                    @testEnv
                                    .{Env/currentPartner}
                            [1]
                                [Record/models]
                                    ThreadPartnerSeenInfo
                                [ThreadPartnerSeenInfo/lastFetchedMessage]
                                    @testEnv
                                    .{Record/insert}
                                        [Record/models]
                                            Message
                                        [Message/id]
                                            100
                                [ThreadPartnerSeenInfo/partner]
                                    @author
            :threadViewer
                @testEnv
                .{Record/insert}
                    [Record/models]
                        ThreadViewer
                    [ThreadViewer/hasThreadView]
                        true
                    [ThreadViewer/thread]
                        @thread
            :message
                @testEnv
                .{Record/insert}
                    [Record/models]
                        Message
                    [Message/author]
                        @author
                    [Message/body]
                        <p>Test</p>
                    [Message/id]
                        100
                    [Message/originThread]
                        @thread
            @testEnv
            .{Record/insert}
                [Record/models]
                    ThreadViewComponent
                [ThreadViewComponent/threadView]
                    @threadViewer
                    .{ThreadViewer/threadView}
            {Test/assert}
                []
                    @message
                    .{Message/messageComponent}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should display a message component
            {Test/assert}
                []
                    @message
                    .{Message/messageComponent}
                    .{Collection/first}
                    .{MessageViewComponent/seenIndicator}
                    .{isFalsy}
                []
                    message component should not have any message seen indicator
`;
