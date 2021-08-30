/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            post message on non-mailing channel with "CTRL-Enter" keyboard shortcut for small screen size
        [Test/model]
            ChatWindowManagerComponent
        [Test/assertions]
            1
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
                    [Env/device]
                        [Device/isMobile]
                            {Dev/comment}
                                here isMobile is used for the small screen size,
                                not actually for the mobile devices
                            true
            @testEnv
            .{Record/insert}
                [Record/models]
                    mail.channel
                [mail.channel/id]
                    20
                [mail.channel/is_minimized]
                    true
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{MessagingMenu/messagingMenuComponents}
                    .{Collection/first}
                    .{MessagingMenuComponent/toggler}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{Record/findById}
                        [Thread/id]
                            20
                        [Thread/model]
                            mail.channel
                    .{Thread/threadPreviewComponents}
                    .{Collection/first}
            {Dev/comment}
                insert some HTML in editable
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/focus}
                    @testEnv
                    .{Record/findById}
                        [Thread/id]
                            20
                        [Thread/model]
                            mail.channel
                    .{Thread/composer}
                    .{Composer/composerTextInputComponents}
                    .{Collection/first}
                    .{ComposerTextInputComponent/textarea}
                @testEnv
                .{UI/insertText}
                    Test
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/keydown}
                    [0]
                        @testEnv
                        .{Record/findById}
                            [Thread/id]
                                20
                            [Thread/model]
                                mail.channel
                        .{Thread/composer}
                        .{Composer/composerTextInputComponents}
                        .{Collection/first}
                        .{ComposerTextInputComponent/textarea}
                    [1]
                        [ctrlKey]
                            true
                        [key]
                            Enter
            {Test/assert}
                []
                    @testEnv
                    .{Record/findById}
                        [Thread/id]
                            20
                        [Thread/model]
                            mail.channel
                    .{Thread/cache}
                    .{ThreadCache/messages}
                    .{Collection/length}
                    .{=}
                        1
                []
                    should now have single message in channel after posting message from pressing 'CTRL-Enter' in text input of composer for small screen
`;
