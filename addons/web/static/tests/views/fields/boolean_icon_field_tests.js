/** @odoo-module **/

import { getFixture } from "@web/../tests/helpers/utils";
import { makeView, setupViewRegistries } from "@web/../tests/views/helpers";

let serverData;
let target;

QUnit.module("Fields", (hooks) => {
    hooks.beforeEach(() => {
        target = getFixture();
        serverData = {
            models: {
                partner: {
                    fields: {
                        bar: { string: "Bar", type: "boolean", default: true, searchable: true },
                    },
                    records: [
                        { id: 1, bar: true },
                        { id: 2, bar: true },
                        { id: 3, bar: true },
                        { id: 4, bar: true },
                        { id: 5, bar: false },
                    ],
                },
            },
        };

        setupViewRegistries();
    });

    QUnit.module("BooleanIconField");

    QUnit.test("boolean_icon field in form view", async function (assert) {
        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <label for="bar" string="Awesome checkbox" />
                    <field name="bar" />
                </form>`,
        });

        assert.containsOnce(
            target,
            ".o_field_boolean_icon button",
            "icon button should still be checked"
        );
        //todo
    });
});
