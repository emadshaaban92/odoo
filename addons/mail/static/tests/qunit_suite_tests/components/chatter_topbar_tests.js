/** @odoo-module **/

import {
    afterNextRender,
    nextAnimationFrame,
    start,
    startServer,
} from "@mail/../tests/helpers/test_utils";

import { makeTestPromise } from "web.test_utils";

QUnit.module("mail", {}, function () {
    QUnit.module("components", {}, function () {
        QUnit.module("chatter_topbar_tests.js");

        QUnit.skipRefactoring("attachment loading is delayed", async function (assert) {
            assert.expect(4);

            const pyEnv = await startServer();
            const resPartnerId1 = pyEnv["res.partner"].create({});
            const { advanceTime, openView } = await start({
                hasTimeControl: true,
                loadingBaseDelayDuration: 100,
                async mockRPC(route) {
                    if (route.includes("/mail/thread/data")) {
                        await makeTestPromise(); // simulate long loading
                    }
                },
            });
            await openView({
                res_id: resPartnerId1,
                res_model: "res.partner",
                views: [[false, "form"]],
            });

            assert.strictEqual(
                document.querySelectorAll(`.o-mail-chatter-topbar`).length,
                1,
                "should have a chatter topbar"
            );
            assert.strictEqual(
                document.querySelectorAll(`.o-mail-chatter-topbar-add-attachments`).length,
                1,
                "should have an attachments button in chatter menu"
            );
            assert.strictEqual(
                document.querySelectorAll(`.o_ChatterTopbar_buttonAttachmentsCountLoader`).length,
                0,
                "attachments button should not have a loader yet"
            );

            await afterNextRender(async () => advanceTime(100));
            assert.strictEqual(
                document.querySelectorAll(`.o_ChatterTopbar_buttonAttachmentsCountLoader`).length,
                1,
                "attachments button should now have a loader"
            );
        });

        QUnit.skipRefactoring(
            "composer state conserved when clicking on another topbar button",
            async function (assert) {
                assert.expect(8);

                const pyEnv = await startServer();
                const resPartnerId1 = pyEnv["res.partner"].create({});
                const { click, openView } = await start();
                await openView({
                    res_id: resPartnerId1,
                    res_model: "res.partner",
                    views: [[false, "form"]],
                });

                assert.containsOnce(
                    document.body,
                    `.o-mail-chatter-topbar`,
                    "should have a chatter topbar"
                );
                assert.containsOnce(
                    document.body,
                    `.o-mail-chatter-topbar-send-message-button`,
                    "should have a send message button in chatter menu"
                );
                assert.containsOnce(
                    document.body,
                    `.o-mail-chatter-topbar-log-note-button`,
                    "should have a log note button in chatter menu"
                );
                assert.containsOnce(
                    document.body,
                    `.o-mail-chatter-topbar-add-attachments`,
                    "should have an attachments button in chatter menu"
                );

                await click(`.o-mail-chatter-topbar-log-note-button`);
                assert.containsOnce(
                    document.body,
                    `.o-mail-chatter-topbar-log-note-button.o-active`,
                    "log button should now be active"
                );
                assert.containsNone(
                    document.body,
                    `.o-mail-chatter-topbar-send-message-button.o-active`,
                    "send message button should not be active"
                );

                document.querySelector(`.o-mail-chatter-topbar-add-attachments`).click();
                await nextAnimationFrame();
                assert.containsOnce(
                    document.body,
                    `.o-mail-chatter-topbar-log-note-button.o-active`,
                    "log button should still be active"
                );
                assert.containsNone(
                    document.body,
                    `.o-mail-chatter-topbar-send-message-button.o-active`,
                    "send message button should still be not active"
                );
            }
        );
    });
});
