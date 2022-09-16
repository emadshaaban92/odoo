/** @odoo-module */

import { FieldMatching } from "@spreadsheet/field_matching/field_matching";

QUnit.module("spreadsheet > field matching", {}, () => {
    QUnit.test("Object registering", async (assert) => {
        const fieldMatching = new FieldMatching();
        assert.throws(() => fieldMatching.getDomain("1"));
        fieldMatching.register("1");
        assert.strictEqual(fieldMatching.getDomain("1").toString(), "");
        fieldMatching.unregister("1");
        assert.throws(() => fieldMatching.getDomain("1"));
    });

    QUnit.test("Object registering", async (assert) => {
        const fieldMatching = new FieldMatching();
        assert.throws(() => fieldMatching.getDomain("1"));
        fieldMatching.register("1");
        assert.strictEqual(fieldMatching.getDomain("1").toString(), "");
        fieldMatching.unregister("1");
        assert.throws(() => fieldMatching.getDomain("1"));
    });
});
