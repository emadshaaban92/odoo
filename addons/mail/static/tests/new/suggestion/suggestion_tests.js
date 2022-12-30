/** @odoo-module **/

import { Composer } from "@mail/new/composer/composer";
import { makeDeferred } from "@mail/utils/deferred";
import { click, insertText, start, startServer } from "@mail/../tests/helpers/test_utils";
import { getFixture, nextTick, patchWithCleanup } from "@web/../tests/helpers/utils";

let target;

QUnit.module("suggestion", {
    async beforeEach() {
        target = getFixture();
        // Simulate real user interactions
        patchWithCleanup(Composer.prototype, {
            isEventTrusted() {
                return true;
            },
        });
    },
});

QUnit.test('display partner mention suggestions on typing "@"', async function (assert) {
    const pyEnv = await startServer();
    const resPartnerId1 = pyEnv["res.partner"].create({
        email: "testpartner@odoo.com",
        name: "TestPartner",
    });
    const resPartnerId2 = pyEnv["res.partner"].create({
        email: "testpartner2@odoo.com",
        name: "TestPartner2",
    });
    pyEnv["res.users"].create({ partner_id: resPartnerId1 });
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "general",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: resPartnerId1 }],
            [0, 0, { partner_id: resPartnerId2 }],
        ],
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion");

    await insertText(".o-mail-composer-textarea", "@");
    assert.containsN(target, ".o-composer-suggestion", 3);
});

QUnit.test('display partner mention suggestions on typing "@" in chatter', async function (assert) {
    const pyEnv = await startServer();
    const { openFormView } = await start();
    await openFormView({
        res_id: pyEnv.currentPartnerId,
        res_model: "res.partner",
    });
    await click(".o-mail-chatter-topbar-send-message-button");
    assert.containsNone(target, ".o-composer-suggestion");
    await insertText(".o-mail-composer-textarea", "@");
    assert.containsOnce(target, ".o-composer-suggestion:contains(Mitchell Admin)");
});

QUnit.test("show other channel member in @ mention", async function (assert) {
    const pyEnv = await startServer();
    const resPartnerId = pyEnv["res.partner"].create({
        email: "testpartner@odoo.com",
        name: "TestPartner",
    });
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "general",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: resPartnerId }],
        ],
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    await insertText(".o-mail-composer-textarea", "@");
    assert.containsOnce(target, ".o-composer-suggestion:contains(TestPartner)");
});

QUnit.test("select @ mention insert mention text in composer", async function (assert) {
    const pyEnv = await startServer();
    const resPartnerId = pyEnv["res.partner"].create({
        email: "testpartner@odoo.com",
        name: "TestPartner",
    });
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "general",
        channel_member_ids: [
            [0, 0, { partner_id: pyEnv.currentPartnerId }],
            [0, 0, { partner_id: resPartnerId }],
        ],
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    await insertText(".o-mail-composer-textarea", "@");
    await click(".o-composer-suggestion:contains(TestPartner)");
    assert.strictEqual($(target).find(".o-mail-composer-textarea").val().trim(), "@TestPartner");
});

QUnit.test('display command suggestions on typing "/"', async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "General",
        channel_type: "channel",
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    await insertText(".o-mail-composer-textarea", "/");
    assert.containsOnce(target, ".o-composer-suggestion-list .o-open");
});

QUnit.test("use a command for a specific channel type", async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({ channel_type: "chat" });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();

    assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    assert.strictEqual(document.querySelector(".o-mail-composer-textarea").value, "");
    await insertText(".o-mail-composer-textarea", "/");
    await click(".o-composer-suggestion");
    assert.strictEqual(
        document.querySelector(".o-mail-composer-textarea").value.replace(/\s/, " "),
        "/who ",
        "text content of composer should have used command + additional whitespace afterwards"
    );
});

QUnit.test(
    "command suggestion should only open if command is the first character",
    async function (assert) {
        const pyEnv = await startServer();
        const mailChannelId1 = pyEnv["mail.channel"].create({
            name: "General",
            channel_type: "channel",
        });
        const { openDiscuss } = await start({
            discuss: {
                context: { active_id: `mail.channel_${mailChannelId1}` },
            },
        });
        await openDiscuss();
        assert.containsNone(target, ".o-composer-suggestion-list .o-open");
        assert.strictEqual(document.querySelector(".o-mail-composer-textarea").value, "");
        await insertText(".o-mail-composer-textarea", "bluhbluh ");
        assert.strictEqual(document.querySelector(".o-mail-composer-textarea").value, "bluhbluh ");
        await insertText(".o-mail-composer-textarea", "/");
        assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    }
);

QUnit.test('display canned response suggestions on typing ":"', async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "Mario Party",
    });
    pyEnv["mail.shortcode"].create({
        source: "hello",
        substitution: "Hello! How are you?",
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    await insertText(".o-mail-composer-textarea", ":");
    assert.containsOnce(target, ".o-composer-suggestion-list .o-open");
});

QUnit.test("use a canned response", async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "Mario Party",
    });
    pyEnv["mail.shortcode"].create({
        source: "hello",
        substitution: "Hello! How are you?",
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    assert.strictEqual(target.querySelector(".o-mail-composer-textarea").value, "");
    await insertText(".o-mail-composer-textarea", ":");
    assert.containsOnce(target, ".o-composer-suggestion");
    await click(".o-composer-suggestion");
    assert.strictEqual(
        target.querySelector(".o-mail-composer-textarea").value.replace(/\s/, " "),
        "Hello! How are you? ",
        "text content of composer should have canned response + additional whitespace afterwards"
    );
});

QUnit.test("use a canned response some text", async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "Mario Party",
    });
    pyEnv["mail.shortcode"].create({
        source: "hello",
        substitution: "Hello! How are you?",
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion");
    assert.strictEqual(document.querySelector(".o-mail-composer-textarea").value, "");
    await insertText(".o-mail-composer-textarea", "bluhbluh ");
    assert.strictEqual(target.querySelector(".o-mail-composer-textarea").value, "bluhbluh ");
    await insertText(".o-mail-composer-textarea", ":");
    assert.containsOnce(target, ".o-composer-suggestion");
    await click(".o-composer-suggestion");
    assert.strictEqual(
        target.querySelector(".o-mail-composer-textarea").value.replace(/\s/, " "),
        "bluhbluh Hello! How are you? ",
        "text content of composer should have previous content + canned response substitution + additional whitespace afterwards"
    );
});

QUnit.test('display channel mention suggestions on typing "#"', async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "General",
        channel_type: "channel",
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    await insertText(".o-mail-composer-textarea", "#");
    assert.containsOnce(target, ".o-composer-suggestion-list .o-open");
});

QUnit.test("mention a channel", async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({
        name: "General",
        channel_type: "channel",
    });
    const { openDiscuss } = await start({
        discuss: {
            context: { active_id: `mail.channel_${mailChannelId1}` },
        },
    });
    await openDiscuss();
    assert.containsNone(target, ".o-composer-suggestion-list .o-open");
    assert.strictEqual(target.querySelector(".o-mail-composer-textarea").value, "");
    await insertText(".o-mail-composer-textarea", "#");
    assert.containsOnce(target, ".o-composer-suggestion");
    await click(".o-composer-suggestion");
    assert.strictEqual(
        target.querySelector(".o-mail-composer-textarea").value.replace(/\s/, " "),
        "#General ",
        "text content of composer should have mentioned channel + additional whitespace afterwards"
    );
});

QUnit.test("Channel suggestions do not crash after rpc returns", async function (assert) {
    const pyEnv = await startServer();
    const mailChannelId1 = pyEnv["mail.channel"].create({ name: "general" });
    const getSuggestionsDeferred = makeDeferred();
    const { openDiscuss } = await start({
        async mockRPC(args, params, originalFn) {
            if (params.method === "get_mention_suggestions") {
                const res = await originalFn(args, params);
                assert.step("get_mention_suggestions");
                assert.strictEqual(res.length, 1, "Should return a thread");
                getSuggestionsDeferred.resolve();
                return res;
            }
            return originalFn(args, params);
        },
        discuss: {
            params: {
                default_active_id: `mail.channel_${mailChannelId1}`,
            },
        },
    });
    await openDiscuss();
    pyEnv["mail.channel"].create({ name: "foo" });
    insertText(".o-mail-composer-textarea", "#");
    await nextTick();
    insertText(".o-mail-composer-textarea", "f");
    await getSuggestionsDeferred;
    assert.verifySteps(["get_mention_suggestions"]);
});
