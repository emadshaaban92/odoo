/** @odoo-module **/

import { makeDeferred } from "@mail/utils/deferred";
import { patchUiSize } from "@mail/../tests/helpers/patch_ui_size";
import {
    afterNextRender,
    isScrolledToBottom,
    start,
    startServer,
} from "@mail/../tests/helpers/test_utils";

import { file, dom } from "web.test_utils";
const { createFile, inputFiles } = file;
const { triggerEvent } = dom;

QUnit.module("mail", {}, function () {
    QUnit.module("components", {}, function () {
        QUnit.module("chat_window_manager_tests.js");

        QUnit.skipRefactoring("[technical] messaging not created", async function (assert) {
            /**
             * Creation of messaging in env is async due to generation of models being
             * async. Generation of models is async because it requires parsing of all
             * JS modules that contain pieces of model definitions.
             *
             * Time of having no messaging is very short, almost imperceptible by user
             * on UI, but the display should not crash during this critical time period.
             */
            assert.expect(1);

            const messagingBeforeCreationDeferred = makeDeferred();
            const { afterNextRender } = await start({
                messagingBeforeCreationDeferred,
                waitUntilMessagingCondition: "none",
            });

            // simulate messaging being created
            await afterNextRender(() => messagingBeforeCreationDeferred.resolve());

            assert.containsOnce(
                document.body,
                ".o_ChatWindowManager",
                "should contain chat window manager after messaging has been created"
            );
        });

        QUnit.skipRefactoring("initial mount", async function (assert) {
            assert.expect(1);

            await start();
            assert.containsOnce(
                document.body,
                ".o_ChatWindowManager",
                "should have chat window manager"
            );
        });

        QUnit.skipRefactoring(
            "focus next visible chat window when closing current chat window with ESCAPE [REQUIRE FOCUS]",
            async function (assert) {
                /**
                 * computation uses following info:
                 * ([mocked] global window width: @see `mail/static/tests/helpers/test_utils.js:start()` method)
                 * (others: @see mail/static/src/models/chat_window_manager.js:visual)
                 *
                 * - chat window width: 340px
                 * - start/end/between gap width: 10px/10px/5px
                 * - hidden menu width: 170px
                 * - global width: 1920px
                 *
                 * Enough space for 2 visible chat windows:
                 *  10 + 340 + 5 + 340 + 10 = 705 < 1920
                 */
                assert.expect(4);

                const pyEnv = await startServer();
                pyEnv["mail.channel"].create([
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                    },
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                    },
                ]);
                patchUiSize({ width: 1920 });
                await start();
                assert.containsN(
                    document.body,
                    ".o-mail-chat-window .o-mail-composer-textarea",
                    2,
                    "2 chat windows should be present initially"
                );
                assert.containsNone(
                    document.body,
                    ".o-mail-chat-window.o-folded",
                    "both chat windows should be open"
                );

                await afterNextRender(() => {
                    const ev = new window.KeyboardEvent("keydown", {
                        bubbles: true,
                        key: "Escape",
                    });
                    document.querySelector(".o-mail-composer-textarea").dispatchEvent(ev);
                });
                assert.containsOnce(
                    document.body,
                    ".o-mail-chat-window",
                    "only one chat window should remain after pressing escape on first chat window"
                );
                assert.hasClass(
                    document.querySelector(".o-mail-chat-window"),
                    "o-focused",
                    "next visible chat window should be focused after pressing escape on first chat window"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window: composer state conservation on toggle discuss",
            async function (assert) {
                assert.expect(6);

                const pyEnv = await startServer();
                const mailChannelId = pyEnv["mail.channel"].create({});
                const { click, insertText, messaging, openDiscuss, openView } = await start();
                await click(`.o_MessagingMenu_toggler`);
                await click(`.o_MessagingMenu_dropdownMenu .o_NotificationListView_preview`);
                // Set content of the composer of the chat window
                await insertText(".o-mail-composer-textarea", "XDU for the win !");
                assert.containsNone(
                    document.body,
                    ".o_ComposerView .o_AttachmentCard",
                    "composer should have no attachment initially"
                );
                // Set attachments of the composer
                const files = [
                    await createFile({
                        name: "text state conservation on toggle home menu.txt",
                        content: "hello, world",
                        contentType: "text/plain",
                    }),
                    await createFile({
                        name: "text2 state conservation on toggle home menu.txt",
                        content: "hello, xdu is da best man",
                        contentType: "text/plain",
                    }),
                ];
                await afterNextRender(() =>
                    inputFiles(
                        messaging.chatWindowManager.chatWindows[0].threadView.composerView
                            .fileUploader.fileInput,
                        files
                    )
                );
                assert.strictEqual(
                    document.querySelector(`.o-mail-composer-textarea`).value,
                    "XDU for the win !",
                    "chat window composer initial text input should contain 'XDU for the win !'"
                );
                assert.containsN(
                    document.body,
                    ".o_ComposerView .o_AttachmentCard",
                    2,
                    "composer should have 2 total attachments after adding 2 attachments"
                );

                await openDiscuss({ waitUntilMessagesLoaded: false });
                assert.containsNone(
                    document.body,
                    ".o-mail-chat-window",
                    "should not have any chat window after opening discuss"
                );

                await openView({
                    res_id: mailChannelId,
                    res_model: "mail.channel",
                    views: [[false, "form"]],
                });
                assert.strictEqual(
                    document.querySelector(`.o-mail-composer-textarea`).value,
                    "XDU for the win !",
                    "chat window composer should still have the same input after closing discuss"
                );
                assert.containsN(
                    document.body,
                    ".o_ComposerView .o_AttachmentCard",
                    2,
                    "Chat window composer should have 2 attachments after closing discuss"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window: scroll conservation on toggle discuss",
            async function (assert) {
                assert.expect(2);

                const pyEnv = await startServer();
                const mailChannelId1 = pyEnv["mail.channel"].create({});
                for (let i = 0; i < 100; i++) {
                    pyEnv["mail.message"].create({
                        body: "not empty",
                        model: "mail.channel",
                        res_id: mailChannelId1,
                    });
                }
                const { afterEvent, click, openDiscuss, openView } = await start();
                await click(`.o_MessagingMenu_toggler`);
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () => document.querySelector(".o_NotificationListView_preview").click(),
                    message:
                        "should wait until channel scrolled to its last message after opening it from the messaging menu",
                    predicate: ({ scrollTop, thread }) => {
                        const messageList = document.querySelector(".o_ThreadView_messageList");
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            isScrolledToBottom(messageList)
                        );
                    },
                });
                // Set a scroll position to chat window
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () => {
                        document.querySelector(`.o_ThreadView_messageList`).scrollTop = 142;
                    },
                    message:
                        "should wait until channel scrolled to 142 after setting this value manually",
                    predicate: ({ scrollTop, thread }) => {
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            scrollTop === 142
                        );
                    },
                });

                await openDiscuss({ waitUntilMessagesLoaded: false });
                assert.containsNone(
                    document.body,
                    ".o-mail-chat-window",
                    "should not have any chat window after opening discuss"
                );

                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () =>
                        openView({
                            res_id: mailChannelId1,
                            res_model: "mail.channel",
                            views: [[false, "list"]],
                        }),
                    message:
                        "should wait until channel restored its scroll to 142 after closing discuss",
                    predicate: ({ scrollTop, thread }) => {
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            scrollTop === 142
                        );
                    },
                });
                assert.strictEqual(
                    document.querySelector(`.o_ThreadView_messageList`).scrollTop,
                    142,
                    "chat window scrollTop should still be the same after closing discuss"
                );
            }
        );

        QUnit.skipRefactoring("chat window: switch on TAB", async function (assert) {
            assert.expect(10);

            const pyEnv = await startServer();
            const [mailChannelId1, mailChannelId2] = pyEnv["mail.channel"].create([
                { name: "channel1" },
                { name: "channel2" },
            ]);
            const { click } = await start();

            await click(`.o_MessagingMenu_toggler`);
            await click(`
        .o_MessagingMenu_dropdownMenu
        .o_ChannelPreviewView[data-channel-id="${mailChannelId1}"]`);

            assert.containsOnce(
                document.body,
                ".o-mail-chat-window",
                "Only 1 chatWindow must be opened"
            );
            const chatWindow = document.querySelector(".o-mail-chat-window");
            assert.strictEqual(
                chatWindow.querySelector(".o-mail-chat-window-header-name").textContent,
                "channel1",
                "The name of the only chatWindow should be 'channel1' (channel with ID 1)"
            );
            assert.strictEqual(
                chatWindow.querySelector(".o-mail-composer-textarea"),
                document.activeElement,
                "The chatWindow composer must have focus"
            );

            await afterNextRender(() =>
                triggerEvent(
                    chatWindow.querySelector(".o-mail-chat-window .o-mail-composer-textarea"),
                    "keydown",
                    { key: "Tab" }
                )
            );
            assert.strictEqual(
                chatWindow.querySelector(".o-mail-chat-window .o-mail-composer-textarea"),
                document.activeElement,
                "The chatWindow composer still has focus"
            );

            await click(`.o_MessagingMenu_toggler`);
            await click(`
        .o_MessagingMenu_dropdownMenu
        .o_ChannelPreviewView[data-channel-id="${mailChannelId2}"]`);

            assert.containsN(
                document.body,
                ".o-mail-chat-window",
                2,
                "2 chatWindows must be opened"
            );
            const chatWindows = document.querySelectorAll(".o-mail-chat-window");
            assert.strictEqual(
                chatWindows[0].querySelector(".o-mail-chat-window-header-name").textContent,
                "channel1",
                "The name of the 1st chatWindow should be 'channel1' (channel with ID 1)"
            );
            assert.strictEqual(
                chatWindows[1].querySelector(".o-mail-chat-window-header-name").textContent,
                "channel2",
                "The name of the 2nd chatWindow should be 'channel2' (channel with ID 2)"
            );
            assert.strictEqual(
                chatWindows[1].querySelector(".o-mail-composer-textarea"),
                document.activeElement,
                "The 2nd chatWindow composer must have focus (channel with ID 2)"
            );

            await afterNextRender(() =>
                triggerEvent(chatWindows[1].querySelector(".o-mail-composer-textarea"), "keydown", {
                    key: "Tab",
                })
            );
            assert.containsN(
                document.body,
                ".o-mail-chat-window",
                2,
                "2 chatWindows should still be opened"
            );
            assert.strictEqual(
                chatWindows[0].querySelector(".o-mail-composer-textarea"),
                document.activeElement,
                "The 1st chatWindow composer must have focus (channel with ID 1)"
            );
        });

        QUnit.skipRefactoring(
            "chat window: TAB cycle with 3 open chat windows [REQUIRE FOCUS]",
            async function (assert) {
                /**
                 * InnerWith computation uses following info:
                 * ([mocked] global window width: @see `mail/static/tests/helpers/test_utils.js:start()` method)
                 * (others: @see mail/static/src/models/chat_window_manager.js:visual)
                 *
                 * - chat window width: 340px
                 * - start/end/between gap width: 10px/10px/5px
                 * - hidden menu width: 170px
                 * - global width: 1920px
                 *
                 * Enough space for 3 visible chat windows:
                 *  10 + 340 + 5 + 340 + 5 + 340 + 10 = 1050 < 1920
                 */
                assert.expect(6);

                const pyEnv = await startServer();
                pyEnv["mail.channel"].create([
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                    },
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                    },
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                    },
                ]);
                patchUiSize({ width: 1920 });
                await start();
                assert.containsN(
                    document.body,
                    ".o-mail-chat-window .o-mail-composer-textarea",
                    3,
                    "initialy, 3 chat windows should be present"
                );
                assert.containsNone(
                    document.body,
                    ".o-mail-chat-window.o-folded",
                    "all 3 chat windows should be open"
                );

                await afterNextRender(() => {
                    document
                        .querySelector(
                            ".o-mail-chat-window[data-visible-index='2'] .o-mail-composer-textarea"
                        )
                        .focus();
                });
                assert.strictEqual(
                    document.querySelector(
                        ".o-mail-chat-window[data-visible-index='2'] .o-mail-composer-textarea"
                    ),
                    document.activeElement,
                    "The chatWindow with visible-index 2 should have the focus"
                );

                await afterNextRender(() =>
                    triggerEvent(
                        document.querySelector(
                            ".o-mail-chat-window[data-visible-index='2'] .o-mail-composer-textarea"
                        ),
                        "keydown",
                        { key: "Tab" }
                    )
                );
                assert.strictEqual(
                    document.querySelector(
                        ".o-mail-chat-window[data-visible-index='1'] .o-mail-composer-textarea"
                    ),
                    document.activeElement,
                    "after pressing tab on the chatWindow with visible-index 2, the chatWindow with visible-index 1 should have focus"
                );

                await afterNextRender(() =>
                    triggerEvent(
                        document.querySelector(
                            ".o-mail-chat-window[data-visible-index='1'] .o-mail-composer-textarea"
                        ),
                        "keydown",
                        { key: "Tab" }
                    )
                );
                assert.strictEqual(
                    document.querySelector(
                        ".o-mail-chat-window[data-visible-index='0'] .o-mail-composer-textarea"
                    ),
                    document.activeElement,
                    "after pressing tab on the chat window with visible-index 1, the chatWindow with visible-index 0 should have focus"
                );

                await afterNextRender(() =>
                    triggerEvent(
                        document.querySelector(
                            ".o-mail-chat-window[data-visible-index='0'] .o-mail-composer-textarea"
                        ),
                        "keydown",
                        { key: "Tab" }
                    )
                );
                assert.strictEqual(
                    document.querySelector(
                        ".o-mail-chat-window[data-visible-index='2'] .o-mail-composer-textarea"
                    ),
                    document.activeElement,
                    "the chatWindow with visible-index 2 should have the focus after pressing tab on the chatWindow with visible-index 0"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window with a thread: keep scroll position in message list on folded",
            async function (assert) {
                assert.expect(3);

                const pyEnv = await startServer();
                const mailChannelId1 = pyEnv["mail.channel"].create({});
                for (let i = 0; i < 100; i++) {
                    pyEnv["mail.message"].create({
                        body: "not empty",
                        model: "mail.channel",
                        res_id: mailChannelId1,
                    });
                }
                const { afterEvent, click } = await start();
                await click(`.o_MessagingMenu_toggler`);
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () => document.querySelector(".o_NotificationListView_preview").click(),
                    message:
                        "should wait until channel scrolled to its last message after opening it from the messaging menu",
                    predicate: ({ scrollTop, thread }) => {
                        const messageList = document.querySelector(".o_ThreadView_messageList");
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            isScrolledToBottom(messageList)
                        );
                    },
                });
                // Set a scroll position to chat window
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () => {
                        document.querySelector(`.o_ThreadView_messageList`).scrollTop = 142;
                    },
                    message:
                        "should wait until channel scrolled to 142 after setting this value manually",
                    predicate: ({ scrollTop, thread }) => {
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            scrollTop === 142
                        );
                    },
                });
                assert.strictEqual(
                    document.querySelector(`.o_ThreadView_messageList`).scrollTop,
                    142,
                    "verify chat window initial scrollTop"
                );

                // fold chat window
                await click(".o_ChatWindow_header");
                assert.containsNone(
                    document.body,
                    ".o_ThreadView",
                    "chat window should be folded so no ThreadView should be present"
                );

                // unfold chat window
                await afterNextRender(() =>
                    afterEvent({
                        eventName: "o-component-message-list-scrolled",
                        func: () => document.querySelector(".o_ChatWindow_header").click(),
                        message: "should wait until channel restored its scroll position to 142",
                        predicate: ({ scrollTop, thread }) => {
                            return (
                                thread &&
                                thread.model === "mail.channel" &&
                                thread.id === mailChannelId1 &&
                                scrollTop === 142
                            );
                        },
                    })
                );
                assert.strictEqual(
                    document.querySelector(`.o_ThreadView_messageList`).scrollTop,
                    142,
                    "chat window scrollTop should still be the same when chat window is unfolded"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window should scroll to the newly posted message just after posting it",
            async function (assert) {
                assert.expect(1);

                const pyEnv = await startServer();
                const mailChannelId1 = pyEnv["mail.channel"].create({
                    channel_member_ids: [
                        [
                            0,
                            0,
                            {
                                fold_state: "open",
                                is_minimized: true,
                                partner_id: pyEnv.currentPartnerId,
                            },
                        ],
                    ],
                });
                for (let i = 0; i < 10; i++) {
                    pyEnv["mail.message"].create({
                        body: "not empty",
                        model: "mail.channel",
                        res_id: mailChannelId1,
                    });
                }
                const { insertText } = await start();

                // Set content of the composer of the chat window
                await insertText(".o-mail-composer-textarea", "WOLOLO");
                // Send a new message in the chatwindow to trigger the scroll
                await afterNextRender(() =>
                    triggerEvent(
                        document.querySelector(".o-mail-chat-window .o-mail-composer-textarea"),
                        "keydown",
                        { key: "Enter" }
                    )
                );
                const messageList = document.querySelector(".o_MessageListView");
                assert.ok(
                    isScrolledToBottom(messageList),
                    "chat window should scroll to the newly posted message just after posting it"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window with a thread: keep scroll position in message list on toggle discuss when folded",
            async function (assert) {
                assert.expect(2);

                const pyEnv = await startServer();
                const mailChannelId1 = pyEnv["mail.channel"].create({});
                for (let i = 0; i < 100; i++) {
                    pyEnv["mail.message"].create({
                        body: "not empty",
                        model: "mail.channel",
                        res_id: mailChannelId1,
                    });
                }
                const { afterEvent, click, openDiscuss, openView } = await start();
                await click(`.o_MessagingMenu_toggler`);
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () => document.querySelector(".o_NotificationListView_preview").click(),
                    message:
                        "should wait until channel scrolled to its last message after opening it from the messaging menu",
                    predicate: ({ scrollTop, thread }) => {
                        const messageList = document.querySelector(".o_ThreadView_messageList");
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            isScrolledToBottom(messageList)
                        );
                    },
                });
                // Set a scroll position to chat window
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () =>
                        (document.querySelector(`.o_ThreadView_messageList`).scrollTop = 142),
                    message:
                        "should wait until channel scrolled to 142 after setting this value manually",
                    predicate: ({ scrollTop, thread }) => {
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            scrollTop === 142
                        );
                    },
                });
                // fold chat window
                await click(".o_ChatWindow_header");
                await openDiscuss({ waitUntilMessagesLoaded: false });
                assert.containsNone(
                    document.body,
                    ".o-mail-chat-window",
                    "should not have any chat window after opening discuss"
                );

                await openView({
                    res_id: mailChannelId1,
                    res_model: "mail.channel",
                    views: [[false, "list"]],
                });
                // unfold chat window
                await afterEvent({
                    eventName: "o-component-message-list-scrolled",
                    func: () => document.querySelector(".o_ChatWindow_header").click(),
                    message:
                        "should wait until channel restored its scroll position to the last saved value (142)",
                    predicate: ({ scrollTop, thread }) => {
                        return (
                            thread &&
                            thread.model === "mail.channel" &&
                            thread.id === mailChannelId1 &&
                            scrollTop === 142
                        );
                    },
                });
                assert.strictEqual(
                    document.querySelector(`.o_ThreadView_messageList`).scrollTop,
                    142,
                    "chat window scrollTop should still be the same after closing discuss"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window does not fetch messages if hidden",
            async function (assert) {
                /**
                 * computation uses following info:
                 * ([mocked] global window width: 900px)
                 * (others: @see `mail/static/src/models/chat_window_manager.js:visual`)
                 *
                 * - chat window width: 340px
                 * - start/end/between gap width: 10px/10px/5px
                 * - hidden menu width: 170px
                 * - global width: 1080px
                 *
                 * Enough space for 2 visible chat windows, and one hidden chat window:
                 * 3 visible chat windows:
                 *  10 + 340 + 5 + 340 + 5 + 340 + 10 = 1050 > 900
                 * 2 visible chat windows + hidden menu:
                 *  10 + 340 + 5 + 340 + 10 + 170 + 5 = 880 < 900
                 */
                assert.expect(11);

                const pyEnv = await startServer();
                const [mailChannelId1, mailChannelId2, mailChannelId3] = pyEnv[
                    "mail.channel"
                ].create([
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                        name: "Channel #10",
                    },
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                        name: "Channel #11",
                    },
                    {
                        channel_member_ids: [
                            [
                                0,
                                0,
                                {
                                    fold_state: "open",
                                    is_minimized: true,
                                    partner_id: pyEnv.currentPartnerId,
                                },
                            ],
                        ],
                        name: "Channel #12",
                    },
                ]);
                patchUiSize({ width: 900 });
                const { click } = await start({
                    mockRPC(route, args) {
                        if (route === "/mail/channel/messages") {
                            const { channel_id } = args;
                            assert.step(`rpc:/mail/channel/messages:${channel_id}`);
                        }
                    },
                });

                assert.containsN(
                    document.body,
                    ".o-mail-chat-window",
                    2,
                    "2 chat windows should be visible"
                );
                assert.containsNone(
                    document.body,
                    `.o-mail-chat-window[data-thread-id="${mailChannelId3}"][data-thread-model="mail.channel"]`,
                    "chat window for Channel #12 should be hidden"
                );
                assert.containsOnce(
                    document.body,
                    ".o_ChatWindowHiddenMenuView",
                    "chat window hidden menu should be displayed"
                );
                assert.verifySteps(
                    [
                        `rpc:/mail/channel/messages:${mailChannelId1}`,
                        `rpc:/mail/channel/messages:${mailChannelId2}`,
                    ],
                    "messages should be fetched for the two visible chat windows"
                );

                await click(".o_ChatWindowHiddenMenuView_dropdownToggle");
                assert.containsOnce(
                    document.body,
                    ".o_ChatWindowHiddenMenuItemView",
                    "1 hidden chat window should be listed in hidden menu"
                );

                await click(".o_ChatWindowHiddenMenuItemView_chatWindowHeader");
                assert.containsN(
                    document.body,
                    ".o-mail-chat-window",
                    2,
                    "2 chat windows should still be visible"
                );
                assert.containsOnce(
                    document.body,
                    `.o-mail-chat-window[data-thread-id="${mailChannelId3}"][data-thread-model="mail.channel"]`,
                    "chat window for Channel #12 should now be visible"
                );
                assert.verifySteps(
                    [`rpc:/mail/channel/messages:${mailChannelId3}`],
                    "messages should now be fetched for Channel #12"
                );
            }
        );

        QUnit.skipRefactoring(
            "new message separator is shown in a chat window of a chat on receiving new message if there is a history of conversation",
            async function (assert) {
                assert.expect(3);

                const pyEnv = await startServer();
                const resPartnerId1 = pyEnv["res.partner"].create({ name: "Demo" });
                const resUsersId1 = pyEnv["res.users"].create({
                    name: "Foreigner user",
                    partner_id: resPartnerId1,
                });
                const mailChannelId1 = pyEnv["mail.channel"].create({
                    channel_member_ids: [
                        [
                            0,
                            0,
                            {
                                is_minimized: true,
                                is_pinned: false,
                                partner_id: pyEnv.currentPartnerId,
                            },
                        ],
                        [0, 0, { partner_id: resPartnerId1 }],
                    ],
                    channel_type: "chat",
                    uuid: "channel-10-uuid",
                });
                pyEnv["mail.message"].create({
                    body: "not empty",
                    model: "mail.channel",
                    res_id: mailChannelId1,
                });
                const { messaging } = await start();

                // simulate receiving a message
                await afterNextRender(async () =>
                    messaging.rpc({
                        route: "/mail/chat_post",
                        params: {
                            context: {
                                mockedUserId: resUsersId1,
                            },
                            message_content: "hu",
                            uuid: "channel-10-uuid",
                        },
                    })
                );
                assert.containsOnce(
                    document.body,
                    ".o-mail-chat-window",
                    "a chat window should be visible after receiving a new message from a chat"
                );
                assert.containsN(
                    document.body,
                    ".o-mail-message",
                    2,
                    "chat window should have 2 messages"
                );
                assert.containsOnce(
                    document.body,
                    ".o_MessageListView_separatorNewMessages",
                    "should display 'new messages' separator in the conversation, from reception of new messages"
                );
            }
        );

        QUnit.skipRefactoring(
            "new message separator is not shown in a chat window of a chat on receiving new message if there is no history of conversation",
            async function (assert) {
                assert.expect(1);

                const pyEnv = await startServer();
                const resPartnerId1 = pyEnv["res.partner"].create({ name: "Demo" });
                const resUsersId1 = pyEnv["res.users"].create({
                    name: "Foreigner user",
                    partner_id: resPartnerId1,
                });
                pyEnv["mail.channel"].create({
                    channel_member_ids: [
                        [0, 0, { partner_id: pyEnv.currentPartnerId }],
                        [0, 0, { partner_id: resPartnerId1 }],
                    ],
                    channel_type: "chat",
                    uuid: "channel-10-uuid",
                });
                const { messaging } = await start();

                // simulate receiving a message
                await afterNextRender(async () =>
                    messaging.rpc({
                        route: "/mail/chat_post",
                        params: {
                            context: {
                                mockedUserId: resUsersId1,
                            },
                            message_content: "hu",
                            uuid: "channel-10-uuid",
                        },
                    })
                );
                assert.containsNone(
                    document.body,
                    ".o_MessageListView_separatorNewMessages",
                    "should not display 'new messages' separator in the conversation of a chat on receiving new message if there is no history of conversation"
                );
            }
        );

        QUnit.skipRefactoring(
            "focusing a chat window of a chat should make new message separator disappear [REQUIRE FOCUS]",
            async function (assert) {
                assert.expect(2);

                const pyEnv = await startServer();
                const resPartnerId1 = pyEnv["res.partner"].create({ name: "Demo" });
                const resUsersId1 = pyEnv["res.users"].create({
                    name: "Foreigner user",
                    partner_id: resPartnerId1,
                });
                const mailChannelId1 = pyEnv["mail.channel"].create({
                    channel_member_ids: [
                        [
                            0,
                            0,
                            {
                                is_minimized: true,
                                is_pinned: false,
                                partner_id: pyEnv.currentPartnerId,
                            },
                        ],
                        [0, 0, { partner_id: resPartnerId1 }],
                    ],
                    channel_type: "chat",
                    uuid: "channel-10-uuid",
                });
                pyEnv["mail.message"].create({
                    body: "not empty",
                    model: "mail.channel",
                    res_id: mailChannelId1,
                });
                const { afterEvent, messaging } = await start();

                // simulate receiving a message
                await afterNextRender(() =>
                    messaging.rpc({
                        route: "/mail/chat_post",
                        params: {
                            context: {
                                mockedUserId: resUsersId1,
                            },
                            message_content: "hu",
                            uuid: "channel-10-uuid",
                        },
                    })
                );
                assert.containsOnce(
                    document.body,
                    ".o_MessageListView_separatorNewMessages",
                    "should display 'new messages' separator in the conversation, from reception of new messages"
                );

                await afterNextRender(() =>
                    afterEvent({
                        eventName: "o-thread-last-seen-by-current-partner-message-id-changed",
                        func: () => document.querySelector(".o-mail-composer-textarea").focus(),
                        message:
                            "should wait until last seen by current partner message id changed",
                        predicate: ({ thread }) => {
                            return thread.id === mailChannelId1 && thread.model === "mail.channel";
                        },
                    })
                );
                assert.containsNone(
                    document.body,
                    ".o_MessageListView_separatorNewMessages",
                    "new message separator should no longer be shown, after focus on composer text input of chat window"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window should open when receiving a new DM",
            async function (assert) {
                assert.expect(1);

                const pyEnv = await startServer();
                const resPartnerId1 = pyEnv["res.partner"].create({});
                const resUsersId1 = pyEnv["res.users"].create({ partner_id: resPartnerId1 });
                pyEnv["mail.channel"].create({
                    channel_member_ids: [
                        [
                            0,
                            0,
                            {
                                is_pinned: false,
                                partner_id: pyEnv.currentPartnerId,
                            },
                        ],
                        [0, 0, { partner_id: resPartnerId1 }],
                    ],
                    channel_type: "chat",
                    uuid: "channel11uuid",
                });
                const { messaging } = await start();

                // simulate receiving the first message on channel 11
                await afterNextRender(() =>
                    messaging.rpc({
                        route: "/mail/chat_post",
                        params: {
                            context: {
                                mockedUserId: resUsersId1,
                            },
                            message_content: "new message",
                            uuid: "channel11uuid",
                        },
                    })
                );
                assert.containsOnce(
                    document.body,
                    ".o-mail-chat-window",
                    "a chat window should be open now that current user received a new message"
                );
            }
        );

        QUnit.skipRefactoring(
            "chat window should remain folded when new message is received",
            async function (assert) {
                assert.expect(1);

                const pyEnv = await startServer();
                const resPartnerId1 = pyEnv["res.partner"].create({ name: "Demo" });
                const resUsersId1 = pyEnv["res.users"].create({
                    name: "Foreigner user",
                    partner_id: resPartnerId1,
                });
                pyEnv["mail.channel"].create({
                    channel_member_ids: [
                        [
                            0,
                            0,
                            {
                                fold_state: "folded",
                                is_minimized: true,
                                is_pinned: false,
                                partner_id: pyEnv.currentPartnerId,
                            },
                        ],
                        [
                            0,
                            0,
                            {
                                partner_id: resPartnerId1,
                            },
                        ],
                    ],
                    channel_type: "chat",
                    uuid: "channel-10-uuid",
                });

                const { messaging } = await start();
                // simulate receiving a new message
                await afterNextRender(async () =>
                    messaging.rpc({
                        route: "/mail/chat_post",
                        params: {
                            context: {
                                mockedUserId: resUsersId1,
                            },
                            message_content: "New Message 2",
                            uuid: "channel-10-uuid",
                        },
                    })
                );
                assert.hasClass(
                    document.querySelector(`.o-mail-chat-window`),
                    "o-folded",
                    "chat window should remain folded"
                );
            }
        );

        QUnit.skipRefactoring(
            "should not have chat window hidden menu in mobile (transition from 3 chat windows in desktop to mobile)",
            async function (assert) {
                /**
                 * computation uses following info:
                 * ([mocked] global window width: 900px)
                 * (others: @see `mail/static/src/models/chat_window_manager.js:visual`)
                 *
                 * - chat window width: 340px
                 * - start/end/between gap width: 10px/10px/5px
                 * - hidden menu width: 170px
                 * - global width: 1080px
                 *
                 * Not enough space for 3 visible chat windows:
                 *  10 + 340 + 5 + 340 + 5 + 340 + 10 = 1050 > 900
                 * Enough space for 2 visible chat windows + hidden menu:
                 *  10 + 340 + 5 + 340 + 5 + 170 + 10 = 880 < 900
                 */
                assert.expect(1);

                const pyEnv = await startServer();
                const [mailChannelId1, mailChannelId2, mailChannelId3] = pyEnv[
                    "mail.channel"
                ].create([
                    { name: "mailChannel1" },
                    { name: "mailChannel2" },
                    { name: "mailChannel3" },
                ]);
                patchUiSize({ width: 900 }); // enough to fit 2 chat windows + hidden menu
                const { click, messaging } = await start();
                // open, from systray menu, chat windows of channels with id 1, 2, 3
                await click(".o_MessagingMenu_toggler");
                await click(`
        .o_MessagingMenu_dropdownMenu
        .o_ChannelPreviewView[data-channel-id="${mailChannelId1}"]
    `);
                await click(".o_MessagingMenu_toggler");
                await click(`
        .o_MessagingMenu_dropdownMenu
        .o_ChannelPreviewView[data-channel-id="${mailChannelId2}"]
    `);
                await click(".o_MessagingMenu_toggler");
                await click(`
        .o_MessagingMenu_dropdownMenu
        .o_ChannelPreviewView[data-channel-id="${mailChannelId3}"]
    `);
                // simulate resize to go into mobile
                await afterNextRender(() =>
                    messaging.device.update({
                        globalWindowInnerWidth: 300,
                        isMobileDevice: true,
                        isSmall: true,
                        sizeClass: 0, // XS
                    })
                );
                assert.containsNone(
                    document.body,
                    ".o_ChatWindowManager_hiddenMenu",
                    "should not have any chat window hidden menu in mobile (transition from desktop having 3 chat windows (2 visible, 1 hidden)"
                );
            }
        );
    });
});
