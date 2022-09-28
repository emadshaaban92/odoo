/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { getFixture, patchWithCleanup } from "../helpers/utils";
import {
    applyGroup,
    getFacetTexts,
    isItemSelected,
    isOptionSelected,
    makeWithSearch,
    setupControlPanelServiceRegistry,
    toggleAddCustomGroup,
    toggleGroupByMenu,
    toggleMenuItem,
} from "./helpers";

let target;
let serverData;
QUnit.module("Search", (hooks) => {
    hooks.beforeEach(async () => {
        serverData = {
            models: {
                foo: {
                    fields: {
                        bar: { string: "Bar", type: "many2one", relation: "partner" },
                        birthday: { string: "Birthday", type: "date", store: true, sortable: true },
                        date_field: { string: "Date", type: "date", store: true, sortable: true },
                        float_field: { string: "Float", type: "float", group_operator: "sum" },
                        foo: { string: "Foo", type: "char", store: true, sortable: true },
                    },
                    records: {},
                },
            },
            views: {
                "foo,false,search": `<search/>`,
            },
        };
        setupControlPanelServiceRegistry();
        patchWithCleanup(browser, {
            setTimeout: (fn) => fn(),
            clearTimeout: () => {},
        });
        target = getFixture();
    });

    QUnit.module("CustomGroupByItem");

    QUnit.test("simple rendering", async function (assert) {
        assert.expect(5);

        await makeWithSearch({
            serverData,
            resModel: "foo",
            Component: ControlPanel,
            searchMenuTypes: ["groupBy"],
            searchViewId: false,
        });

        await toggleGroupByMenu(target);

        const customGroupByItem = target.querySelector(".o_add_custom_group_menu");
        assert.strictEqual(customGroupByItem.innerText.trim(), "Add Custom Group");

        assert.containsOnce(customGroupByItem, "button.dropdown-toggle");
        assert.containsNone(customGroupByItem, ".dropdown-menu");

        await toggleAddCustomGroup(target);

        assert.containsOnce(customGroupByItem, ".dropdown-menu");

        assert.deepEqual(
            [...target.querySelectorAll(".o_add_custom_group_menu select option")].map(
                (el) => el.innerText
            ),
            ["Birthday", "Date", "Foo"]
        );
    });

    QUnit.test(
        'the ID field should not be proposed in "Add Custom Group" menu',
        async function (assert) {
            assert.expect(1);

            await makeWithSearch({
                serverData,
                resModel: "foo",
                Component: ControlPanel,
                searchMenuTypes: ["groupBy"],
                searchViewId: false,
                searchViewFields: {
                    foo: { string: "Foo", type: "char", store: true, sortable: true },
                    id: { sortable: true, string: "ID", type: "integer" },
                },
            });

            await toggleGroupByMenu(target);
            await toggleAddCustomGroup(target);

            assert.deepEqual(
                [
                    ...target.querySelectorAll(
                        ".o_add_custom_group_menu .dropdown-menu select option"
                    ),
                ].map((el) => el.innerText),
                ["Foo"]
            );
        }
    );

    QUnit.test(
        'add a date field in "Add Custom Group" activate a groupby with global default option "month"',
        async function (assert) {
            assert.expect(6);

            const controlPanel = await makeWithSearch({
                serverData,
                resModel: "foo",
                Component: ControlPanel,
                searchMenuTypes: ["groupBy"],
                searchViewId: false,
                searchViewFields: {
                    date_field: { string: "Date", type: "date", store: true, sortable: true },
                    id: { sortable: true, string: "ID", type: "integer" },
                },
            });
            await toggleGroupByMenu(target);

            assert.deepEqual(controlPanel.env.searchModel.groupBy, []);
            assert.containsNone(target, ".o_menu_item");

            await toggleAddCustomGroup(target);
            await applyGroup(target);

            assert.deepEqual(controlPanel.env.searchModel.groupBy, ["date_field:month"]);
            assert.deepEqual(getFacetTexts(target), ["Date: Month"]);
            assert.ok(isItemSelected(target, "Date"));

            await toggleMenuItem(target, "Date");

            assert.ok(isOptionSelected(target, "Date", "Month"));
        }
    );

    QUnit.test("click on add custom group toggle group selector", async function (assert) {
        assert.expect(4);

        await makeWithSearch({
            serverData,
            resModel: "foo",
            Component: ControlPanel,
            searchMenuTypes: ["groupBy"],
            searchViewFields: {
                date: { sortable: true, name: "date", string: "Super Date", type: "date" },
            },
        });

        await toggleGroupByMenu(target);

        const addCustomGroupMenu = target.querySelector(".o_add_custom_group_menu");

        assert.strictEqual(addCustomGroupMenu.innerText.trim(), "Add Custom Group");

        await toggleAddCustomGroup(target);

        // Single select node with a single option
        assert.containsOnce(target, ".o_add_custom_group_menu .dropdown-menu select");
        assert.strictEqual(
            target
                .querySelector(".o_add_custom_group_menu .dropdown-menu select option")
                .innerText.trim(),
            "Super Date"
        );

        // Button apply
        assert.containsOnce(target, ".o_add_custom_group_menu .dropdown-menu .btn");
    });

    QUnit.test(
        "select a field name in Add Custom Group menu properly trigger the corresponding field",
        async function (assert) {
            assert.expect(4);

            await makeWithSearch({
                serverData,
                resModel: "foo",
                Component: ControlPanel,
                searchMenuTypes: ["groupBy"],
                searchViewFields: {
                    candle_light: {
                        sortable: true,
                        string: "Candlelight",
                        type: "boolean",
                    },
                },
            });

            await toggleGroupByMenu(target);
            await toggleAddCustomGroup(target);
            await applyGroup(target);

            assert.containsOnce(target, ".o_group_by_menu .o_menu_item");
            assert.containsOnce(target, ".o_add_custom_group_menu .dropdown-toggle");
            assert.containsOnce(target, ".o_add_custom_group_menu .dropdown-menu");
            assert.deepEqual(getFacetTexts(target), ["Candlelight"]);
        }
    );

    QUnit.test(
        "group by properties",
        async function (assert) {
            assert.expect(4);

            // variable set true when we fetch the definition
            let definitionFetched = false;

            async function mockRPC(route, { method, model, args, kwargs }) {
                if (method === "search_read" && model === "parentModel") {
                    definitionFetched = true;

                    return [{
                        display_name: "First Parent",
                        properties_definition: [{
                            name: "my_text",
                            type: "text",
                            string: "My Text",
                        }, {
                            name: "my_partner",
                            type: "many2one",
                            string: "My Partner",
                            comodel: "res.partner",
                        }],
                    }, {
                        display_name: "Second Parent",
                        properties_definition: [{
                            name: "my_integer",
                            type: "integer",
                            string: "My Integer",
                        }],
                    }];
                }
            }

            await makeWithSearch({
                serverData,
                resModel: "foo",
                Component: ControlPanel,
                searchMenuTypes: ["groupBy"],
                searchViewFields: {
                    candle_light: {
                        sortable: true,
                        string: "Candlelight",
                        type: "boolean",
                        name: "candle_light",
                    },
                    properties: {
                        string: "Properties",
                        type: "properties",
                        definition_record: "parent_id",
                        definition_record_field: "properties_definition",
                        name: "properties",
                    },
                    parent_id: {
                        string: "Parent",
                        type: "many2one",
                        relation: "parentModel",
                        name: "parent_id",
                    }
                },
                mockRPC,
            });

            // definition is fetched only when we open the menu
            assert.notOk(definitionFetched);
            await toggleGroupByMenu(target);
            assert.ok(definitionFetched);

            await toggleAddCustomGroup(target);

            const fields = [...target.querySelectorAll(".o_add_custom_group_menu select option")]
                .map(element => element.innerText);

            // should remove the original properties fields,
            // and added the properties from the definition we fetched
            assert.deepEqual(fields, ["Candlelight", "My Text (First Parent)", "My Partner (First Parent)", "My Integer (Second Parent)"])

            // select the second property
            const select = target.querySelector(".o_add_custom_group_menu select");
            select.value = "properties.my_partner";
            select.dispatchEvent(new Event('change'));
            await applyGroup(target);

            assert.deepEqual(getFacetTexts(target), ["My Partner (First Parent)"]);
        }
    );
});
