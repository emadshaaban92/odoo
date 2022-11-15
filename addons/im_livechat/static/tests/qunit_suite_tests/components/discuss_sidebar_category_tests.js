/** @odoo-module **/

import {
    afterNextRender,
    start,
    startServer,
} from '@mail/../tests/helpers/test_utils';

QUnit.module('im_livechat', {}, function () {
QUnit.module('components', {}, function () {
QUnit.module('discuss_sidebar_category_tests.js');

QUnit.skipRefactoring('livechat - counter: should not have a counter if the category is unfolded and without unread messages', async function (assert) {
    assert.expect(1);

    const pyEnv = await startServer();
    pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    const { openDiscuss } = await start();
    await openDiscuss();
    assert.containsNone(
        document.body,
        `.o_DiscussSidebarView_categoryLivechat .o_DiscussSidebarCategory_counter`,
        "should not have a counter if the category is unfolded and without unread messages",
    );
});

QUnit.skipRefactoring('livechat - counter: should not have a counter if the category is unfolded and with unread messages', async function (assert) {
    assert.expect(1);

    const pyEnv = await startServer();
    pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, {
                message_unread_counter: 10,
                partner_id: pyEnv.currentPartnerId,
            }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    const { openDiscuss } = await start();
    await openDiscuss();
    assert.containsNone(
        document.body,
        `.o_DiscussSidebarView_categoryLivechat .o_DiscussSidebarCategory_counter`,
        "should not have a counter if the category is unfolded and with unread messages",
    );
});

QUnit.skipRefactoring('livechat - counter: should not have a counter if category is folded and without unread messages', async function (assert) {
    assert.expect(1);

    const pyEnv = await startServer();
    pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: false,
    });
    const { openDiscuss } = await start();
    await openDiscuss();

    assert.containsNone(
        document.body,
        `.o_DiscussSidebarView_categoryLivechat .o_DiscussSidebarCategory_counter`,
        "should not have a counter if the category is folded and without unread messages"
    );
});

QUnit.skipRefactoring('livechat - counter: should have correct value of unread threads if category is folded and with unread messages', async function (assert) {
    assert.expect(1);

    const pyEnv = await startServer();
    pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, {
                message_unread_counter: 10,
                partner_id: pyEnv.currentPartnerId,
            }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: false,
    });
    const { openDiscuss } = await start();
    await openDiscuss();

    assert.strictEqual(
        document.querySelector(`.o_DiscussSidebarView_categoryLivechat .o_DiscussSidebarCategory_counter`).textContent,
        "1",
        "should have correct value of unread threads if category is folded and with unread messages"
    );
});

QUnit.skipRefactoring('livechat - states: close manually by clicking the title', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: true,
    });
    const { messaging, openDiscuss } = await start();
    await openDiscuss();

    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`
    );

    // fold the livechat category
    await afterNextRender(() =>
        document.querySelector(`.o_DiscussSidebarCategory[data-category-local-id="${
            messaging.discuss.categoryLivechat.localId}"]
            .o_DiscussSidebarCategory_title
        `).click()
    );
    assert.containsNone(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`,
        "Category livechat should be closed and the content should be invisible"
    );
});

QUnit.skipRefactoring('livechat - states: open manually by clicking the title', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: false,
    });
    const { messaging, openDiscuss } = await start();
    await openDiscuss();

    assert.containsNone(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`
    );

    // open the livechat category
    await afterNextRender(() =>
        document.querySelector(`.o_DiscussSidebarCategory[data-category-local-id="${
            messaging.discuss.categoryLivechat.localId}"]
            .o_DiscussSidebarCategory_title
        `).click()
    );
    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`,
        "Category livechat should be open and the content should be visible"
    );
});

QUnit.skipRefactoring('livechat - states: close should update the value on the server', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: true,
    });
    const currentUserId = pyEnv.currentUserId;
    const { messaging, openDiscuss } = await start();
    await openDiscuss();

    const initalSettings = await messaging.rpc({
        model: 'res.users.settings',
        method: '_find_or_create_for_user',
        args: [[currentUserId]],
    });
    assert.strictEqual(
        initalSettings.is_discuss_sidebar_category_livechat_open,
        true,
        "the value in server side should be true"
    );

    await afterNextRender(() =>
        document.querySelector(`.o_DiscussSidebarCategory[data-category-local-id="${
            messaging.discuss.categoryLivechat.localId}"]
            .o_DiscussSidebarCategory_title
        `).click()
    );
    const newSettings = await messaging.rpc({
        model: 'res.users.settings',
        method: '_find_or_create_for_user',
        args: [[currentUserId]],
    });
    assert.strictEqual(
        newSettings.is_discuss_sidebar_category_livechat_open,
        false,
        "the value in server side should be false"
    );
});

QUnit.skipRefactoring('livechat - states: open should update the value on the server', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: false,
    });
    const currentUserId = pyEnv.currentUserId;
    const { messaging, openDiscuss } = await start();
    await openDiscuss();

    const initalSettings = await messaging.rpc({
        model: 'res.users.settings',
        method: '_find_or_create_for_user',
        args: [[currentUserId]],
    });
    assert.strictEqual(
        initalSettings.is_discuss_sidebar_category_livechat_open,
        false,
        "the value in server side should be false"
    );

    await afterNextRender(() =>
        document.querySelector(`.o_DiscussSidebarCategory[data-category-local-id="${
            messaging.discuss.categoryLivechat.localId}"]
            .o_DiscussSidebarCategory_title
        `).click()
    );
    const newSettings = await messaging.rpc({
        model: 'res.users.settings',
        method: '_find_or_create_for_user',
        args: [[currentUserId]],
    });
    assert.strictEqual(
        newSettings.is_discuss_sidebar_category_livechat_open,
        true,
        "the value in server side should be true"
    );
});

QUnit.skipRefactoring('livechat - states: close from the bus', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    const resUsersSettingsId1 = pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: true,
    });
    const { openDiscuss } = await start();
    await openDiscuss();

    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`
    );

    await afterNextRender(() => {
        pyEnv['bus.bus']._sendone(pyEnv.currentPartner, 'mail.record/insert', {
            'res.users.settings': {
                'id': resUsersSettingsId1,
                'is_discuss_sidebar_category_livechat_open': false,
            },
        });
    });
    assert.containsNone(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`,
        "Category livechat should be closed and the content should be invisible"
    );
});

QUnit.skipRefactoring('livechat - states: open from the bus', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    const resUsersSettingsId1 = pyEnv['res.users.settings'].create({
        user_id: pyEnv.currentUserId,
        is_discuss_sidebar_category_livechat_open: false,
    });
    const { openDiscuss } = await start();
    await openDiscuss();

    assert.containsNone(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`
    );

    await afterNextRender(() => {
        pyEnv['bus.bus']._sendone(pyEnv.currentPartner, 'mail.record/insert', {
            'res.users.settings': {
                id: resUsersSettingsId1,
                'is_discuss_sidebar_category_livechat_open': true,
            },
        });
    });
    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`,
        "Category livechat should be open and the content should be visible"
    );
});


QUnit.skipRefactoring('livechat - states: category item should be invisible if the category is closed', async function (assert) {
    assert.expect(2);

    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    const { messaging, openDiscuss } = await start();
    await openDiscuss();

    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`
    );

    await afterNextRender(() =>
        document.querySelector(`.o_DiscussSidebarCategory[data-category-local-id="${
            messaging.discuss.categoryLivechat.localId}"]
            .o_DiscussSidebarCategory_title
        `).click()
    );

    assert.containsNone(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`,
        "inactive item should be invisible if the category is folded"
    );
});

QUnit.skipRefactoring('livechat - states: the active category item should be visble even if the category is closed', async function (assert) {
    assert.expect(3);

    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv['mail.channel'].create({
        anonymous_name: "Visitor 11",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: pyEnv.publicPartnerId }],
        ],
        channel_type: 'livechat',
        livechat_operator_id: pyEnv.currentPartnerId,
    });
    const { messaging, openDiscuss } = await start();
    await openDiscuss();

    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`
    );

    const livechat = document.querySelector(`.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`);
    await afterNextRender(() => {
        livechat.click();
    });
    assert.ok(livechat.classList.contains('o-active'));

    await afterNextRender(() =>
        document.querySelector(`.o_DiscussSidebarCategory[data-category-local-id="${
            messaging.discuss.categoryLivechat.localId}"]
            .o_DiscussSidebarCategory_title
        `).click()
    );

    assert.containsOnce(
        document.body,
        `.o_DiscussSidebarCategory_item[data-channel-id="${mailChannelId1}"]`,
        'the active livechat item should remain open even if the category is folded'
    );
});

});
});
