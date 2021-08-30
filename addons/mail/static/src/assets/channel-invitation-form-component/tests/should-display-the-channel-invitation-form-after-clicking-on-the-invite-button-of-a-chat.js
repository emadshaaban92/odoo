/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            should display the channel invitation form after clicking on the invite button of a chat
        [Test/model]
            ChannelInvitationFormComponent
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        mail.channel
                    [mail.channel/channel_type]
                        chat
                    [mail.channel/id]
                        13
                    [mail.channel/members]
                        []
                            {Record/insert}
                                [Record/models]
                                    res.partner
                                [res.partner/id]
                                    @test
                                    .{Test/data}
                                    .{Data/currentPartnerId}
                        []
                            {Record/insert}
                                [Record/models]
                                    res.partner
                                [res.partner/id]
                                    11
                    [mail.channel/public]
                        private
                []
                    [Record/models]
                        res.partner
                    [res.partner/id]
                        11
                    [res.partner/email]
                        testpartner@odoo.com
                    [res.partner/name]
                        TestPartner
                []
                    [Record/models]
                        res.users
                    [res.users/partner_id]
                        11
            :server
                {Record/insert}
                    [Record/models]
                        Server
                    [Server/data]
                        @test
                        .{Test/data}
            @testEnv
            .{Record/update}
                [0]
                    @testEnv
                    .{Env/discuss}
                [1]
                    [Discuss/activeId]
                        13
            @testEnv
            .{Record/insert}
                [Record/models]
                    DiscussComponent
            @testEnv
            .{UI/afterNextRender}
                {UI/click}
                    @testEnv
                    .{Discuss/thread}
                    .{Thread/threadViewTopbarComponents}
                    .{Collection/first}
                    .{ThreadViewTopbarComponent/inviteButton}
            {Test/assert}
                [0]
                    @test
                [1]
                    @testEnv
                    .{Discuss/threadView}
                    .{ThreadView/channelInvitationForm}
                    .{ChannelInvitationForm/channelInvitationFormComponents}
                    .{Collection/length}
                    .{=}
                        1
                [2]
                    should display the channel invitation form after clicking on the invite button of a chat
`;
