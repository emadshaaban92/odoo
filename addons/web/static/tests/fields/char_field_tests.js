/** @odoo-module **/

import {
    click,
    editInput,
    getFixture,
    makeDeferred,
    nextTick,
    patchWithCleanup,
    triggerEvent,
} from "../helpers/utils";
import { makeView, setupViewRegistries } from "../views/helpers";
import { registry } from "@web/core/registry";
import { makeFakeLocalizationService } from "../helpers/mock_services";
import { session } from "@web/session";

const serviceRegistry = registry.category("services");

let serverData;
let target;

QUnit.module("Fields", (hooks) => {
    hooks.beforeEach(() => {
        target = getFixture();
        serverData = {
            models: {
                partner: {
                    fields: {
                        foo: {
                            string: "Foo",
                            type: "char",
                            default: "My little Foo Value",
                            searchable: true,
                            trim: true,
                        },
                        int_field: {
                            string: "int_field",
                            type: "integer",
                            sortable: true,
                            searchable: true,
                        },
                        p: {
                            string: "one2many field",
                            type: "one2many",
                            relation: "partner",
                            searchable: true,
                        },
                        product_id: {
                            string: "Product",
                            type: "many2one",
                            relation: "product",
                            searchable: true,
                        },
                    },
                    records: [
                        {
                            id: 1,
                            display_name: "first record",
                            foo: "yop",
                            int_field: 10,
                            p: [],
                        },
                        {
                            id: 2,
                            display_name: "second record",
                            foo: "blip",
                            int_field: 0,
                            p: [],
                        },
                        { id: 3, foo: "gnap", int_field: 80 },
                        {
                            id: 4,
                            display_name: "aaa",
                            foo: "abc",
                            int_field: false,
                        },
                        { id: 5, foo: "blop", int_field: -4 },
                    ],
                },
                product: {
                    fields: {
                        name: { string: "Product Name", type: "char", searchable: true },
                    },
                    records: [
                        {
                            id: 37,
                            display_name: "xphone",
                        },
                        {
                            id: 41,
                            display_name: "xpad",
                        },
                    ],
                },
                partner_type: {
                    fields: {
                        name: { string: "Partner Type", type: "char", searchable: true },
                        color: { string: "Color index", type: "integer", searchable: true },
                    },
                    records: [
                        { id: 12, display_name: "gold", color: 2 },
                        { id: 14, display_name: "silver", color: 5 },
                    ],
                },
                currency: {
                    fields: {
                        digits: { string: "Digits" },
                        symbol: { string: "Currency Sumbol", type: "char", searchable: true },
                        position: { string: "Currency Position", type: "char", searchable: true },
                    },
                    records: [
                        {
                            id: 1,
                            display_name: "$",
                            symbol: "$",
                            position: "before",
                        },
                        {
                            id: 2,
                            display_name: "€",
                            symbol: "€",
                            position: "after",
                        },
                    ],
                },
                "ir.translation": {
                    fields: {
                        lang: { type: "char" },
                        value: { type: "char" },
                        res_id: { type: "integer" },
                    },
                    records: [
                        {
                            id: 99,
                            res_id: 37,
                            value: "",
                            lang: "en_US",
                        },
                    ],
                },
            },
        };

        setupViewRegistries();
    });

    QUnit.module("CharField");

    QUnit.test("char field in form view", async function (assert) {
        assert.expect(4);

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                        </group>
                    </sheet>
                </form>
            `,
        });

        assert.strictEqual(
            target.querySelector(".o_field_widget").textContent,
            "yop",
            "the value should be displayed properly"
        );

        // switch to edit mode and check the result
        await click(target, ".o_form_button_edit");
        assert.containsOnce(
            target,
            ".o_field_widget input[type='text']",
            "should have an input for the char field"
        );
        assert.strictEqual(
            target.querySelector(".o_field_widget input[type='text']").value,
            "yop",
            "input should contain field value in edit mode"
        );

        // change value in edit mode
        const input = target.querySelector(".o_field_widget input[type='text']");
        input.value = "limbo";
        await triggerEvent(input, null, "change");

        // save
        await click(target, ".o_form_button_save");
        assert.strictEqual(
            target.querySelector(".o_field_widget").textContent,
            "limbo",
            "the new value should be displayed"
        );
    });

    QUnit.test(
        "setting a char field to empty string is saved as a false value",
        async function (assert) {
            assert.expect(1);

            await makeView({
                type: "form",
                resModel: "partner",
                serverData,
                arch: `
                    <form>
                        <sheet>
                            <group>
                                <field name="foo" />
                            </group>
                        </sheet>
                    </form>
                `,
                resId: 1,
                mockRPC(route, { args, method }) {
                    if (method === "write") {
                        assert.strictEqual(args[1].foo, false, "the foo value should be false");
                    }
                },
            });

            await click(target, ".o_form_button_edit");

            const input = target.querySelector(".o_field_widget input[type='text']");
            input.value = "";
            await triggerEvent(input, null, "change");

            // save
            await click(target, ".o_form_button_save");
        }
    );

    QUnit.test("char field with size attribute", async function (assert) {
        assert.expect(1);

        serverData.models.partner.fields.foo.size = 5; // max length

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                        </group>
                    </sheet>
                </form>
            `,
        });

        await click(target, ".o_form_button_edit");

        assert.hasAttrValue(
            target.querySelector("input"),
            "maxlength",
            "5",
            "maxlength attribute should have been set correctly on the input"
        );
    });

    QUnit.test("char field in editable list view", async function (assert) {
        assert.expect(6);

        await makeView({
            type: "list",
            resModel: "partner",
            serverData,
            arch: `
                <tree editable="bottom">
                    <field name="foo" />
                </tree>
            `,
        });

        assert.containsN(target, "tbody td:not(.o_list_record_selector)", 5, "should have 5 cells");
        assert.strictEqual(
            target.querySelector("tbody td:not(.o_list_record_selector)").textContent,
            "yop",
            "value should be displayed properly as text"
        );

        // Edit a line and check the result
        let cell = target.querySelector("tbody td:not(.o_list_record_selector)");
        await click(cell);
        assert.hasClass(cell.parentElement, "o_selected_row", "should be set as edit mode");
        assert.strictEqual(
            cell.querySelector("input").value,
            "yop",
            "should have the corect value in internal input"
        );

        const input = cell.querySelector("input");
        input.value = "brolo";
        await triggerEvent(input, null, "change");

        // save
        await click(target, ".o_list_button_save");
        cell = target.querySelector("tbody td:not(.o_list_record_selector)");
        assert.doesNotHaveClass(
            cell.parentElement,
            "o_selected_row",
            "should not be in edit mode anymore"
        );
        assert.strictEqual(
            target.querySelector("tbody td:not(.o_list_record_selector)").textContent,
            "brolo",
            "value should be properly updated"
        );
    });

    QUnit.test("char field translatable", async function (assert) {
        assert.expect(12);

        serverData.models.partner.fields.foo.translate = true;
        serviceRegistry.add("localization", makeFakeLocalizationService({ multiLang: true }), {
            force: true,
        });
        patchWithCleanup(session.user_context, {
            lang: "en_US",
        });

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                        </group>
                    </sheet>
                </form>
            `,
            mockRPC(route, { args, method, model }) {
                if (route === "/web/dataset/call_button" && method === "translate_fields") {
                    assert.deepEqual(
                        args,
                        ["partner", 1, "foo"],
                        'should call "call_button" route'
                    );
                    return Promise.resolve({
                        domain: [],
                        context: { search_default_name: "partnes,foo" },
                    });
                }
                if (route === "/web/dataset/call_kw/res.lang/get_installed") {
                    return Promise.resolve([
                        ["en_US", "English"],
                        ["fr_BE", "French (Belgium)"],
                    ]);
                }
                if (method === "search_read" && model === "ir.translation") {
                    return Promise.resolve([
                        { lang: "en_US", src: "yop", value: "yop", id: 42 },
                        { lang: "fr_BE", src: "yop", value: "valeur français", id: 43 },
                    ]);
                }
                if (method === "write" && model === "ir.translation") {
                    assert.deepEqual(
                        args[1],
                        { value: "english value" },
                        "the new translation value should be written"
                    );
                    return Promise.resolve(null);
                }
            },
        });

        await click(target, ".o_form_button_edit");

        assert.containsOnce(
            target,
            ".o_field_char .o_field_translate",
            "should have a translate button"
        );
        assert.strictEqual(
            target.querySelector(".o_field_char .o_field_translate").textContent,
            "EN",
            "the button should have as test the current language"
        );
        await click(target, ".o_field_char .o_field_translate");

        assert.containsOnce(target, ".modal", "a translate modal should be visible");
        assert.containsN(
            target,
            ".modal .o_translation_dialog .translation",
            2,
            "two rows should be visible"
        );

        let enFields = target.querySelectorAll(".modal .o_translation_dialog .translation input");
        assert.strictEqual(enFields[0].value, "yop", "English translation should be filled");
        assert.strictEqual(
            enFields[enFields.length - 1].value,
            "valeur français",
            "French translation should be filled"
        );

        await editInput(enFields[0], null, "english value");
        await click(target, ".modal button.btn-primary"); // save

        assert.strictEqual(
            target.querySelector(`.o_field_char input[type="text"]`).value,
            "english value",
            "the new translation was not transfered to modified record"
        );

        await editInput(target, `.o_field_char input[type="text"]`, "new english value");
        await click(target, ".o_field_char .o_field_translate");

        enFields = target.querySelectorAll(".modal .o_translation_dialog .translation input");
        assert.strictEqual(
            enFields[0].value,
            "new english value",
            "Modified value should be used instead of translation"
        );
        assert.strictEqual(
            enFields[enFields.length - 1].value,
            "valeur français",
            "French translation should be filled"
        );
    });

    QUnit.test("html field translatable", async function (assert) {
        assert.expect(6);

        serverData.models.partner.fields.foo.translate = true;
        serviceRegistry.add("localization", makeFakeLocalizationService({ multiLang: true }), {
            force: true,
        });
        patchWithCleanup(session.user_context, {
            lang: "en_US",
        });

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                        </group>
                    </sheet>
                </form>
            `,
            mockRPC(route, { args, method, model }) {
                if (route === "/web/dataset/call_button" && method === "translate_fields") {
                    assert.deepEqual(
                        args,
                        ["partner", 1, "foo"],
                        `should call "call_button" route`
                    );
                    return Promise.resolve({
                        domain: [],
                        context: {
                            search_default_name: "partner,foo",
                            translation_type: "char",
                            translation_show_src: true,
                        },
                    });
                }
                if (route === "/web/dataset/call_kw/res.lang/get_installed") {
                    return Promise.resolve([
                        ["en_US", "English"],
                        ["fr_BE", "French (Belgium)"],
                    ]);
                }
                if (method === "search_read" && model === "ir.translation") {
                    return Promise.resolve([
                        { lang: "en_US", src: "first paragraph", value: "first paragraph", id: 42 },
                        {
                            lang: "en_US",
                            src: "second paragraph",
                            value: "second paragraph",
                            id: 43,
                        },
                        {
                            lang: "fr_BE",
                            src: "first paragraph",
                            value: "premier paragraphe",
                            id: 44,
                        },
                        {
                            lang: "fr_BE",
                            src: "second paragraph",
                            value: "deuxième paragraphe",
                            id: 45,
                        },
                    ]);
                }
                if (method === "write" && model === "ir.translation") {
                    assert.deepEqual(
                        args[1],
                        { value: "first paragraph modified" },
                        "Wrong update on translation"
                    );
                    return Promise.resolve(null);
                }
            },
        });
        await click(target, ".o_form_button_edit");

        // this will not affect the translate_fields effect until the record is
        // saved but is set for consistency of the test
        await editInput(
            target,
            `.o_field_char input[type="text"]`,
            "<p>first paragraph</p><p>second paragraph</p>"
        );

        await click(target, ".o_field_char .o_field_translate");
        assert.containsOnce(target, ".modal", "a translate modal should be visible");
        assert.containsN(
            target,
            ".modal .o_translation_dialog .translation",
            4,
            "four rows should be visible"
        );

        const enField = target.querySelector(".modal .o_translation_dialog .translation input");
        assert.strictEqual(
            enField.value,
            "first paragraph",
            "first part of english translation should be filled"
        );

        await editInput(enField, null, "first paragraph modified");
        await click(target, ".modal button.btn-primary"); // save

        assert.strictEqual(
            target.querySelector(`.o_field_char input[type="text"]`).value,
            "<p>first paragraph</p><p>second paragraph</p>",
            "the new partial translation should not be transfered"
        );
    });

    QUnit.test("char field translatable in create mode", async function (assert) {
        assert.expect(1);

        serverData.models.partner.fields.foo.translate = true;
        serviceRegistry.add("localization", makeFakeLocalizationService({ multiLang: true }), {
            force: true,
        });

        await makeView({
            type: "form",
            resModel: "partner",
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                        </group>
                    </sheet>
                </form>
            `,
        });

        assert.containsOnce(
            target,
            `.o_field_char .o_field_translate`,
            "should have a translate button in create mode"
        );
    });

    QUnit.test("char field does not allow html injections", async function (assert) {
        assert.expect(1);

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                        </group>
                    </sheet>
                </form>
            `,
        });

        await click(target, ".o_form_button_edit");
        const input = target.querySelector("input");
        input.value = "<script>throw Error();</script>";
        await triggerEvent(input, null, "change");

        await click(target, ".o_form_button_save");
        assert.strictEqual(
            target.querySelector(".o_field_widget").textContent,
            "<script>throw Error();</script>",
            "the value should have been properly escaped"
        );
    });

    QUnit.test("char field trim (or not) characters", async function (assert) {
        assert.expect(2);

        serverData.models.partner.fields.foo2 = { string: "Foo2", type: "char", trim: false };

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <sheet>
                        <group>
                            <field name="foo" />
                            <field name="foo2" />
                        </group>
                    </sheet>
                </form>
            `,
        });

        await click(target, ".o_form_button_edit");

        let input = target.querySelector(".o_field_widget[name='foo'] input");
        input.value = "  abc  ";
        await triggerEvent(input, null, "change");

        input = target.querySelector(".o_field_widget[name='foo2'] input");
        input.value = "  def  ";
        await triggerEvent(input, null, "change");

        await click(target, ".o_form_button_save");

        // edit mode
        await click(target, ".o_form_button_edit");
        assert.strictEqual(
            target.querySelector(".o_field_widget[name='foo'] input").value,
            "abc",
            "Foo value should have been trimmed"
        );
        assert.strictEqual(
            target.querySelector(".o_field_widget[name='foo2'] input").value,
            "  def  ",
            "Foo2 value should not have been trimmed"
        );
    });

    QUnit.test(
        "input field: change value before pending onchange returns",
        async function (assert) {
            serverData.models.partner.onchanges = {
                product_id() {},
            };

            let def;
            await makeView({
                type: "form",
                resModel: "partner",
                resId: 1,
                serverData,
                arch: `
                    <form>
                        <sheet>
                            <field name="p">
                                <tree editable="bottom">
                                    <field name="product_id" />
                                    <field name="foo" />
                                </tree>
                            </field>
                        </sheet>
                    </form>
                `,
                async mockRPC(route, { method }) {
                    if (method === "onchange") {
                        await def;
                    }
                },
            });

            await click(target, ".o_form_button_edit");
            await click(target, ".o_field_x2many_list_row_add a");
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "My little Foo Value",
                "should contain the default value"
            );

            def = makeDeferred();
            await click(target, ".o-autocomplete--input");
            await click(target.querySelector(".o-autocomplete--dropdown-item"));

            // set foo before onchange
            await editInput(target, ".o_field_widget[name='foo'] input", "tralala");
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "tralala",
                "input should contain tralala"
            );

            // complete the onchange
            def.resolve();
            await nextTick();
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "tralala",
                "input should contain the same value as before onchange"
            );
        }
    );

    QUnit.test(
        "input field: change value before pending onchange returns (with fieldDebounce)",
        async function (assert) {
            // this test is exactly the same as the previous one, except that in
            // this scenario the onchange return *before* we validate the change
            // on the input field (before the "change" event is triggered).
            serverData.models.partner.onchanges = {
                product_id(obj) {
                    obj.int_field = obj.product_id ? 7 : false;
                },
            };

            let def;
            await makeView({
                type: "form",
                resModel: "partner",
                serverData,
                arch: `
                    <form>
                        <field name="p">
                            <tree editable="bottom">
                                <field name="product_id"/>
                                <field name="foo"/>
                                <field name="int_field"/>
                            </tree>
                        </field>
                    </form>
                `,
                async mockRPC(route, { method }) {
                    if (method === "onchange") {
                        await def;
                    }
                },
            });

            await click(target, ".o_field_x2many_list_row_add a");
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "My little Foo Value",
                "should contain the default value"
            );

            def = makeDeferred();
            await click(target, ".o-autocomplete--input");
            await click(target.querySelector(".o-autocomplete--dropdown-item"));

            // set foo before onchange
            target.querySelector(".o_field_widget[name='foo'] input").value = "tralala";
            await triggerEvent(target, ".o_field_widget[name='foo'] input", "input");
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "tralala",
                "input should contain tralala"
            );
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='int_field'] input").value,
                ""
            );

            // complete the onchange
            def.resolve();
            await nextTick();
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "tralala",
                "foo should contain the same value as before onchange"
            );
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='int_field'] input").value,
                "7",
                "int_field should contain the value returned by the onchange"
            );
        }
    );

    QUnit.test(
        "input field: change value before pending onchange renaming",
        async function (assert) {
            serverData.models.partner.onchanges = {
                product_id(obj) {
                    obj.foo = "on change value";
                },
            };

            const def = makeDeferred();
            await makeView({
                type: "form",
                resModel: "partner",
                resId: 1,
                serverData,
                arch: `
                    <form>
                        <sheet>
                            <field name="product_id" />
                            <field name="foo" />
                        </sheet>
                    </form>
                `,
                async mockRPC(route, { method }) {
                    if (method === "onchange") {
                        await def;
                    }
                },
            });

            await click(target, ".o_form_button_edit");

            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "yop",
                "should contain the correct value"
            );

            await click(target, ".o-autocomplete--input");
            await click(target.querySelector(".o-autocomplete--dropdown-item"));

            // set foo before onchange
            editInput(target, ".o_field_widget[name='foo'] input", "tralala");
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "tralala",
                "should contain tralala"
            );

            // complete the onchange
            def.resolve();
            await nextTick();
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='foo'] input").value,
                "tralala",
                "input should contain the same value as before onchange"
            );
        }
    );

    QUnit.test("support autocomplete attribute", async function (assert) {
        await makeView({
            type: "form",
            resModel: "partner",
            serverData,
            arch: `<form><field name="display_name" autocomplete="coucou"/></form>`,
            resId: 1,
        });

        await click(target.querySelector(".o_form_button_edit"));
        assert.hasAttrValue(
            target.querySelector('.o_field_widget[name="display_name"] input'),
            "autocomplete",
            "coucou",
            "attribute autocomplete should be set"
        );
    });

    QUnit.test("input autocomplete attribute set to none by default", async function (assert) {
        await makeView({
            type: "form",
            resModel: "partner",
            serverData,
            arch: `<form><field name="display_name"/></form>`,
            resId: 1,
        });

        await click(target.querySelector(".o_form_button_edit"));
        assert.hasAttrValue(
            target.querySelector('.o_field_widget[name="display_name"] input'),
            "autocomplete",
            "off",
            "attribute autocomplete should be set to none by default"
        );
    });

    QUnit.test("support password attribute", async function (assert) {
        await makeView({
            type: "form",
            resModel: "partner",
            serverData,
            arch: `<form><field name="foo" password="True"/></form>`,
            resId: 1,
        });

        assert.strictEqual(
            target.querySelector('.o_field_widget[name="foo"]').innerText,
            "***",
            "password should be displayed with stars"
        );
        await click(target.querySelector(".o_form_button_edit"));
        assert.strictEqual(
            target.querySelector('.o_field_widget[name="foo"] input').value,
            "yop",
            "input value should be the password"
        );
        assert.strictEqual(
            target.querySelector('.o_field_widget[name="foo"] input').type,
            "password",
            "input should be of type password"
        );
    });

    QUnit.test("input field: change password value", async function (assert) {
        assert.expect(4);

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <field name="foo" password="True" />
                </form>
            `,
        });

        assert.notEqual(
            target.querySelector(".o_field_char").textContent,
            "yop",
            "password field value should not be visible in read mode"
        );
        assert.strictEqual(
            target.querySelector(".o_field_char").textContent,
            "***",
            "password field value should be hidden with '*' in read mode"
        );

        await click(target, ".o_form_button_edit");

        assert.hasAttrValue(
            target.querySelector(".o_field_char input"),
            "type",
            "password",
            "password field input should be with type 'password' in edit mode"
        );
        assert.strictEqual(
            target.querySelector(".o_field_char input").value,
            "yop",
            "password field input value should be the (non-hidden) password value"
        );
    });

    QUnit.test("input field: empty password", async function (assert) {
        assert.expect(3);

        serverData.models.partner.records[0].foo = false;

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <field name="foo" password="True" />
                </form>
            `,
        });

        assert.strictEqual(
            target.querySelector(".o_field_char").textContent,
            "",
            "password field value should be empty in read mode"
        );

        await click(target, ".o_form_button_edit");

        assert.hasAttrValue(
            target.querySelector(".o_field_char input"),
            "type",
            "password",
            "password field input should be with type 'password' in edit mode"
        );
        assert.strictEqual(
            target.querySelector(".o_field_char input").value,
            "",
            "password field input value should be the (non-hidden, empty) password value"
        );
    });

    QUnit.test(
        "input field: set and remove value, then wait for onchange",
        async function (assert) {
            assert.expect(2);

            serverData.models.partner.onchanges = {
                product_id(obj) {
                    obj.foo = obj.product_id ? "onchange value" : false;
                },
            };

            await makeView({
                type: "form",
                resModel: "partner",
                serverData,
                arch: `
                    <form>
                        <field name="p">
                            <tree editable="bottom">
                                <field name="product_id"/>
                                <field name="foo"/>
                            </tree>
                        </field>
                    </form>
                `,
            });

            await click(target, ".o_field_x2many_list_row_add a");
            assert.strictEqual(target.querySelector(".o_field_widget[name=foo] input").value, "");

            // set value for foo
            target.querySelector(".o_field_widget[name=foo] input").value = "test";
            await triggerEvent(target, ".o_field_widget[name=foo] input", "input");
            // remove value for foo
            target.querySelector(".o_field_widget[name=foo] input").value = "";
            await triggerEvent(target, ".o_field_widget[name=foo] input", "input");

            // trigger the onchange by setting a product
            await click(target, ".o-autocomplete--input");
            await click(target.querySelector(".o-autocomplete--dropdown-item"));
            assert.strictEqual(
                target.querySelector(".o_field_widget[name=foo] input").value,
                "onchange value",
                "input should contain correct value after onchange"
            );
        }
    );
});
