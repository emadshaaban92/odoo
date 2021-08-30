/** @odoo-module **/

import { Define } from '@mail/define';

export default Define`
    {Record/insert}
        [Record/models]
            Test
        [Test/name]
            open 2 chat windows: check shift operations are available
        [Test/model]
            ChatWindowManagerComponent
        [Test/assertions]
            9
        [Test/scenario]
            :testEnv
                {Record/insert}
                    [Record/models]
                        Env
            @testEnv
            .{Record/insert}
                {Dev/comment}
                    2 channels are expected to be found in the messaging menu
                    only their existence matters, data are irrelevant
                []
                    [Record/models]
                        mail.channel
                []
                    [Record/models]
                        mail.channel
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
                    .{MessagingMenu/messagingMenuComponents}
                    .{Collection/first}
                    .{MessagingMenuComponent/notificationList}
                    .{NotificationListComponent/threadPreview}
                    .{Collection/first}
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
                    .{MessagingMenu/messagingMenuComponents}
                    .{Collection/first}
                    .{MessagingMenuComponent/notificationList}
                    .{NotificationListComponent/threadPreview}
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
                    should have opened 2 chat windows
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/commandShiftPrev}
                []
                    first chat window should be allowed to shift left
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/first}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/commandShiftNext}
                    .{isFalsy}
                []
                    first chat window should not be allowed to shift right
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/second}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/commandShiftPrev}
                    .{isFalsy}
                []
                    second chat window should not be allowed to shift left
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindowManagerComponents}
                    .{Collection/first}
                    .{ChatWindowManagerComponent/chatWindows}
                    .{Collection/second}
                    .{ChatWindowComponent/header}
                    .{ChatWindowHeaderComponent/commandShiftNext}
                []
                    second chat window should be allowed to shift right

            :initialFirstChatWindow
                @testEnv
                .{ChatWindowManager/chatWindowManagerComponents}
                .{Collection/first}
            :initialSecondChatWindow
                @testEnv
                .{ChatWindowManager/chatWindowManagerComponents}
                .{Collection/second}
            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{ChatWindowManager/chatWindows}
                    .{Collection/second}
                    .{ChatWindow/chatWindowHeaderComponents}
                    .{Collection/first}
                    .{ChatWindowHeaderComponent/commandShiftPrev}
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindows}
                    .{Collection/first}
                    .{=}
                        @initialSecondChatWindow
                []
                    First chat window should be second after it has been shift left
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindows}
                    .{Collection/second}
                    .{=}
                        @initialFirstChatWindow
                []
                    Second chat window should be first after the first has been shifted left

            @testEnv
            .{Component/afterNextRender}
                @testEnv
                .{UI/click}
                    @testEnv
                    .{ChatWindowManager/chatWindows}
                    .{Collection/first}
                    .{ChatWindow/chatWindowHeaderComponents}
                    .{Collection/first}
                    .{ChatWindowHeaderComponent/commandShiftNext}
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindows}
                    .{Collection/first}
                    .{=}
                        @initialFirstChatWindow
                []
                    First chat window should be back at first place after being shifted left then right
            {Test/assert}
                []
                    @testEnv
                    .{ChatWindowManager/chatWindows}
                    .{Collection/second}
                    .{=}
                        @initialSecondChatWindow
                []
                    Second chat window should be back at second place after first one has been shifted left then right
`;
