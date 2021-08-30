/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            switch on TAB
        [Test/model]
            ChatWindowManagerComponent
        [Test/assertions]
            10
        [Test/scenario
            {Dev/comment}
                2 channels are expected to be found in the messaging menu with
                random unique id and name that will be asserted during the test
            :testEnv
                {Record/insert}
                    [Record/trais]
                        Env
            @testEnv
            .{Record/insert}
                [0]
                    [Record/models]
                        mail.channel
                    [mail.channel/id]
                        1
                    [mail.channel/name]
                        channel1
                [1]
                    [Record/models]
                        mail.channel
                    [mail.channel/id]
                        2
                    [mail.channel/name]
                        channel2
            @testEnv
            .{Record/insert}
                [Record/models]
                    Server
                [Server/data]
                    @record
                    .{Test/data}
            @testEnv
            .{Record/insert}
                []
                    [Record/models]
                        ChatWindowManagerComponent
                []
                    [Record/models]
                        MessagingMenuComponent
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
                            1
                        [Thread/model]
                            mail.channel
                    .{Thread/threadPreviewComponents}
                    .{Collection/first}
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/length}
                    .{=}
                        1
                []
                    only 1 chatWindow must be opened
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/name}
                    .{web.Element/textContent}
                    .{=}
                        channel1
                []
                    the name of the only chatWindow should be 'channel1' (channel with ID 1)
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/thread}
                    .{ThreadViewComponent/composer}
                    .{ComposerViewComponent/textInput}
                    .{ComposerTextInputComponent/textarea}
                    .{=}
                        @testEnv
                        .{web.Browser/document}
                        .{web.Document/activeElement}
                []
                    the chatWindow composer must have focus

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/keydown}
                    [0]
                        @testEnv
                        .{ChatWindowManager/chatWindowManagerComponents}
                        .{Collection/first}
                        .{ChatWindowManagerComponent/chatWindows}
                        .{Collection/first}
                        .{ChatWindowComponent/thread}
                        .{ThreadViewComponent/composer}
                        .{ComposerViewComponent/textInput}
                        .{ComposerTextInputComponent/textarea}
                    [1]
                        [key]
                            Tab
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/thread}
                    .{ThreadViewComponent/composer}
                    .{ComposerViewComponent/textInput}
                    .{ComposerTextInputComponent/textarea}
                    .{=}
                        @testEnv
                        .{web.Browser/document}
                        .{web.Document/activeElement}
                []
                    the chatWindow composer still has focus

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
                            2
                        [Thread/model]
                            mail.channel
                    .{Thread/threadPreviewComponents}
                    .{Collection/first}
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/length}
                    .{=}
                        2
                []
                    2 chatWindows must be opened
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/name}
                    .{web.Element/textContent}
                    .{=}
                        channel1
                []
                    the name of the 1st chatWindow should be 'channel1' (channel with ID 1)
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/second}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/name}
                    .{web.Element/textContent}
                    .{=}
                        channel2
                []
                    the name of the 2nd chatWindow should be 'channel2' (channel with ID 2)
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/second}
                    .{ChatWindowComponent/thread}
                    .{ThreadViewComponent/composer}
                    .{ComposerViewComponent/textInput}
                    .{ComposerTextInputComponent/textarea}
                    .{=}
                        @testEnv
                        .{web.Browser/document}
                        .{web.Document/activeElement}
                []
                    the 2nd chatWindow composer must have focus (channel with ID 2)

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/keydown}
                    [0]
                        @testEnv
                        .{ChatWindowManager/chatWindowManagerComponents}
                        .{Collection/first}
                        .{ChatWindowManagerComponent/chatWindows}
                        .{Collection/second}
                        .{ChatWindowComponent/thread}
                        .{ThreadViewComponent/composer}
                        .{ComposerViewComponent/textInput}
                        .{ComposerTextInputComponent/textarea}
                    [1]
                        [key]
                            Tab
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/length}
                    .{=}
                        2
                []
                    2 chatWindows should still be opened
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/thread}
                    .{ThreadViewComponent/composer}
                    .{ComposerViewComponent/textInput}
                    .{ComposerTextInputComponent/textarea}
                    .{=}
                        @testEnv
                        .{web.Browser/document}
                        .{web.Document/activeElement}
                []
                    the 1st chatWindow composer must have focus (channel with ID 1)
`;
