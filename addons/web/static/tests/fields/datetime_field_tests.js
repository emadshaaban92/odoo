/** @odoo-module **/

import { registry } from "@web/core/registry";
import { makeFakeLocalizationService } from "../helpers/mock_services";
import {
    click,
    editInput,
    getFixture,
    patchTimeZone,
    triggerEvent,
    triggerEvents,
} from "../helpers/utils";
import { makeView, setupViewRegistries } from "../views/helpers";

let serverData;
let target;

QUnit.module("Fields", (hooks) => {
    hooks.beforeEach(() => {
        target = getFixture();
        serverData = {
            models: {
                partner: {
                    fields: {
                        date: { string: "A date", type: "date", searchable: true },
                        datetime: { string: "A datetime", type: "datetime", searchable: true },
                        display_name: { string: "Displayed name", type: "char", searchable: true },
                        foo: {
                            string: "Foo",
                            type: "char",
                            default: "My little Foo Value",
                            searchable: true,
                            trim: true,
                        },
                        bar: { string: "Bar", type: "boolean", default: true, searchable: true },
                        empty_string: {
                            string: "Empty string",
                            type: "char",
                            default: false,
                            searchable: true,
                            trim: true,
                        },
                        txt: {
                            string: "txt",
                            type: "text",
                            default: "My little txt Value\nHo-ho-hoooo Merry Christmas",
                        },
                        int_field: {
                            string: "int_field",
                            type: "integer",
                            sortable: true,
                            searchable: true,
                        },
                        qux: { string: "Qux", type: "float", digits: [16, 1], searchable: true },
                        p: {
                            string: "one2many field",
                            type: "one2many",
                            relation: "partner",
                            searchable: true,
                        },
                        trululu: {
                            string: "Trululu",
                            type: "many2one",
                            relation: "partner",
                            searchable: true,
                        },
                        timmy: {
                            string: "pokemon",
                            type: "many2many",
                            relation: "partner_type",
                            searchable: true,
                        },
                        product_id: {
                            string: "Product",
                            type: "many2one",
                            relation: "product",
                            searchable: true,
                        },
                        sequence: { type: "integer", string: "Sequence", searchable: true },
                        currency_id: {
                            string: "Currency",
                            type: "many2one",
                            relation: "currency",
                            searchable: true,
                        },
                        selection: {
                            string: "Selection",
                            type: "selection",
                            searchable: true,
                            selection: [
                                ["normal", "Normal"],
                                ["blocked", "Blocked"],
                                ["done", "Done"],
                            ],
                        },
                        document: { string: "Binary", type: "binary" },
                        hex_color: { string: "hexadecimal color", type: "char" },
                    },
                    records: [
                        {
                            id: 1,
                            date: "2017-02-03",
                            datetime: "2017-02-08 10:00:00",
                            display_name: "first record",
                            bar: true,
                            foo: "yop",
                            int_field: 10,
                            qux: 0.44444,
                            p: [],
                            timmy: [],
                            trululu: 4,
                            selection: "blocked",
                            document: "coucou==\n",
                            hex_color: "#ff0000",
                        },
                        {
                            id: 2,
                            display_name: "second record",
                            bar: true,
                            foo: "blip",
                            int_field: 0,
                            qux: 0,
                            p: [],
                            timmy: [],
                            trululu: 1,
                            sequence: 4,
                            currency_id: 2,
                            selection: "normal",
                        },
                        {
                            id: 4,
                            display_name: "aaa",
                            foo: "abc",
                            sequence: 9,
                            int_field: false,
                            qux: false,
                            selection: "done",
                        },
                        { id: 3, bar: true, foo: "gnap", int_field: 80, qux: -3.89859 },
                        { id: 5, bar: false, foo: "blop", int_field: -4, qux: 9.1, currency_id: 1 },
                    ],
                    onchanges: {},
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

    QUnit.module("DatetimeField");

    QUnit.test("DatetimeField in form view", async function (assert) {
        assert.expect(7);

        patchTimeZone(120);

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <field name="datetime" />
                </form>
            `,
        });

        const expectedDateString = "02/08/2017 12:00:00"; // 10:00:00 without timezone
        assert.strictEqual(
            target.querySelector(".o_field_datetime").textContent,
            expectedDateString,
            "the datetime should be correctly displayed in readonly"
        );

        // switch to edit mode
        await click(target, ".o_form_button_edit");
        assert.strictEqual(
            target.querySelector(".o_datepicker_input").value,
            expectedDateString,
            "the datetime should be correct in edit mode"
        );

        // datepicker should not open on focus
        assert.containsNone(document.body, ".bootstrap-datetimepicker-widget");

        await click(target, ".o_datepicker_input");
        assert.containsOnce(document.body, ".bootstrap-datetimepicker-widget");

        // select 22 February at 8:25:35
        await click(
            document.body.querySelectorAll(".bootstrap-datetimepicker-widget .picker-switch")[0]
        );
        await click(
            document.body.querySelectorAll(".bootstrap-datetimepicker-widget .picker-switch")[1]
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .year")[8]);
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .month")[3]);
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .day[data-day*='/22/']")
        );
        await click(document.body.querySelector(".bootstrap-datetimepicker-widget .fa-clock-o"));
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-hour")
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .hour")[8]);
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-minute")
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .minute")[5]);
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-second")
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .second")[7]);

        assert.containsNone(
            document.body,
            ".bootstrap-datetimepicker-widget",
            "datepicker should be closed"
        );

        const newExpectedDateString = "04/22/2017 08:25:35";
        assert.strictEqual(
            target.querySelector(".o_datepicker_input").value,
            newExpectedDateString,
            "the selected date should be displayed in the input"
        );

        // save
        await click(target, ".o_form_button_save");
        assert.strictEqual(
            target.querySelector(".o_field_datetime").textContent,
            newExpectedDateString,
            "the selected date should be displayed after saving"
        );
    });

    QUnit.test(
        "DatetimeField does not trigger fieldChange before datetime completly picked",
        async function (assert) {
            assert.expect(6);

            patchTimeZone(120);

            serverData.models.partner.onchanges = {
                datetime() {},
            };
            await makeView({
                type: "form",
                resModel: "partner",
                resId: 1,
                serverData,
                arch: `
                    <form>
                        <field name="datetime" />
                    </form>
                `,
                mockRPC(route, { method }) {
                    if (method === "onchange") {
                        assert.step("onchange");
                    }
                },
            });

            await click(target, ".o_form_button_edit");

            await click(target, ".o_datepicker_input");
            assert.containsOnce(document.body, ".bootstrap-datetimepicker-widget");

            // select a date and time
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .picker-switch")[0]
            );
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .picker-switch")[1]
            );
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .year")[8]
            );
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .month")[3]
            );
            await click(
                document.body.querySelector(
                    ".bootstrap-datetimepicker-widget .day[data-day*='/22/']"
                )
            );
            await click(
                document.body.querySelector(".bootstrap-datetimepicker-widget .fa-clock-o")
            );
            await click(
                document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-hour")
            );
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .hour")[8]
            );
            await click(
                document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-minute")
            );
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .minute")[5]
            );
            await click(
                document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-second")
            );
            assert.verifySteps([], "should not have done any onchange yet");
            await click(
                document.body.querySelectorAll(".bootstrap-datetimepicker-widget .second")[7]
            );

            assert.containsNone(document.body, ".bootstrap-datetimepicker-widget");
            assert.strictEqual(
                target.querySelector(".o_datepicker_input").value,
                "04/22/2017 08:25:35"
            );
            assert.verifySteps(["onchange"], "should have done only one onchange");
        }
    );

    QUnit.test("DatetimeField with datetime formatted without second", async function (assert) {
        assert.expect(2);

        patchTimeZone(0);

        serverData.models.partner.fields.datetime.default = "2017-08-02 12:00:05";
        serverData.models.partner.fields.datetime.required = true;

        registry.category("services").add(
            "localization",
            makeFakeLocalizationService({
                dateFormat: "MM/dd/yyyy",
                timeFormat: "HH:mm",
                dateTimeFormat: "MM/dd/yyyy HH:mm",
            }),
            { force: true }
        );

        await makeView({
            type: "form",
            resModel: "partner",
            serverData,
            arch: `
                <form>
                    <field name="datetime"/>
                </form>
            `,
        });

        const expectedDateString = "08/02/2017 12:00";
        assert.strictEqual(
            target.querySelector(".o_field_datetime input").value,
            expectedDateString,
            "the datetime should be correctly displayed in readonly"
        );

        await click(target, ".o_form_button_cancel");
        assert.containsNone(document.body, ".modal", "there should not be a Warning dialog");
    });

    QUnit.test("DatetimeField in editable list view", async function (assert) {
        patchTimeZone(120);

        await makeView({
            serverData,
            type: "list",
            resModel: "partner",
            arch: `<tree editable="bottom"><field name="datetime"/></tree>`,
        });

        const expectedDateString = "02/08/2017 12:00:00"; // 10:00:00 without timezone
        const cell = target.querySelector("tr.o_data_row td:not(.o_list_record_selector)");
        assert.strictEqual(
            cell.textContent,
            expectedDateString,
            "the datetime should be correctly displayed in readonly"
        );

        // switch to edit mode
        await click(target.querySelector(".o_data_row .o_data_cell"));
        assert.containsOnce(
            target,
            "input.o_datepicker_input",
            "the view should have a date input for editable mode"
        );
        assert.strictEqual(
            target.querySelector("input.o_datepicker_input"),
            document.activeElement,
            "date input should have the focus"
        );

        assert.strictEqual(
            target.querySelector("input.o_datepicker_input").value,
            expectedDateString,
            "the date should be correct in edit mode"
        );

        assert.containsNone(document.body, ".bootstrap-datetimepicker-widget");
        await click(target, ".o_datepicker_input");
        assert.containsOnce(document.body, ".bootstrap-datetimepicker-widget");

        // select 22 February at 8:25:35
        await click(
            document.body.querySelectorAll(".bootstrap-datetimepicker-widget .picker-switch")[0]
        );
        await click(
            document.body.querySelectorAll(".bootstrap-datetimepicker-widget .picker-switch")[1]
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .year")[8]);
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .month")[3]);
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .day[data-day*='/22/']")
        );
        await click(document.body.querySelector(".bootstrap-datetimepicker-widget .fa-clock-o"));
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-hour")
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .hour")[8]);
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-minute")
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .minute")[5]);
        await click(
            document.body.querySelector(".bootstrap-datetimepicker-widget .timepicker-second")
        );
        await click(document.body.querySelectorAll(".bootstrap-datetimepicker-widget .second")[7]);

        assert.containsNone(
            document.body,
            ".bootstrap-datetimepicker-widget",
            "datepicker should be closed"
        );

        const newExpectedDateString = "04/22/2017 08:25:35";
        assert.strictEqual(
            target.querySelector(".o_datepicker_input").value,
            newExpectedDateString,
            "the selected datetime should be displayed in the input"
        );

        // save
        await click(target.querySelector(".o_list_button_save"));
        assert.strictEqual(
            target.querySelector("tr.o_data_row td:not(.o_list_record_selector)").textContent,
            newExpectedDateString,
            "the selected datetime should be displayed after saving"
        );
    });

    QUnit.test(
        "multi edition of DatetimeField in list view: edit date in input",
        async function (assert) {
            assert.expect(4);
            await makeView({
                serverData,
                type: "list",
                resModel: "partner",
                arch: '<tree multi_edit="1">' + '<field name="datetime"/>' + "</tree>",
            });

            const rows = target.querySelectorAll(".o_data_row");

            // select two records and edit them
            await click(rows[0], ".o_list_record_selector input");
            await click(rows[1], ".o_list_record_selector input");

            await click(rows[0], ".o_data_cell");

            assert.containsOnce(target, "input.o_datepicker_input");
            await editInput(target, ".o_datepicker_input", "10/02/2019 09:00:00");

            assert.containsOnce(document.body, ".modal");
            await click(target.querySelector(".modal .modal-footer .btn-primary"));

            assert.strictEqual(
                target.querySelector(".o_data_row:first-child .o_data_cell").textContent,
                "10/02/2019 09:00:00"
            );
            assert.strictEqual(
                target.querySelector(".o_data_row:nth-child(1) .o_data_cell").textContent,
                "10/02/2019 09:00:00"
            );
        }
    );

    QUnit.test("DatetimeField remove value", async function (assert) {
        assert.expect(4);

        patchTimeZone(120);

        await makeView({
            type: "form",
            resModel: "partner",
            resId: 1,
            serverData,
            arch: `
                <form>
                    <field name="datetime" />
                </form>
            `,
            mockRPC(route, { args }) {
                if (route === "/web/dataset/call_kw/partner/write") {
                    assert.strictEqual(
                        args[1].datetime,
                        false,
                        "the correct value should be saved"
                    );
                }
            },
        });

        // switch to edit mode
        await click(target, ".o_form_button_edit");
        assert.strictEqual(
            target.querySelector(".o_datepicker_input").value,
            "02/08/2017 12:00:00",
            "the date time should be correct in edit mode"
        );

        const input = target.querySelector(".o_datepicker_input");
        input.value = "";
        await triggerEvents(input, null, ["input", "change", "focusout"]);
        assert.strictEqual(
            target.querySelector(".o_datepicker_input").value,
            "",
            "should have an empty input"
        );

        // save
        await click(target, ".o_form_button_save");
        assert.strictEqual(
            target.querySelector(".o_field_datetime").textContent,
            "",
            "the selected date should be displayed after saving"
        );
    });

    QUnit.test(
        "DatetimeField with date/datetime widget (with day change)",
        async function (assert) {
            assert.expect(2);

            patchTimeZone(-240);

            serverData.models.partner.records[0].p = [2];
            serverData.models.partner.records[1].datetime = "2017-02-08 02:00:00"; // UTC

            await makeView({
                type: "form",
                resModel: "partner",
                resId: 1,
                serverData,
                arch: `
                    <form>
                        <field name="p">
                            <tree>
                                <field name="datetime" />
                            </tree>
                            <form>
                                <!-- display datetime in readonly as modal will open in edit -->
                                <!-- WOWL: no longer necessary: no more quick edit -->
                                <field name="datetime" widget="date" attrs="{'readonly': 1}" />
                            </form>
                        </field>
                    </form>
                `,
            });

            const expectedDateString = "02/07/2017 22:00:00"; // local time zone
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='p'] .o_data_cell").textContent,
                expectedDateString,
                "the datetime (datetime widget) should be correctly displayed in tree view"
            );

            // switch to form view
            await click(target, ".o_field_widget[name='p'] .o_data_cell");
            assert.strictEqual(
                document.body.querySelector(".modal .o_field_date[name='datetime']").textContent,
                "02/07/2017",
                "the datetime (date widget) should be correctly displayed in form view"
            );
        }
    );

    QUnit.test(
        "DatetimeField with date/datetime widget (without day change)",
        async function (assert) {
            assert.expect(2);

            patchTimeZone(-240);

            serverData.models.partner.records[0].p = [2];
            serverData.models.partner.records[1].datetime = "2017-02-08 10:00:00"; // without timezone

            await makeView({
                type: "form",
                resModel: "partner",
                resId: 1,
                serverData,
                arch: `
                    <form>
                        <field name="p">
                            <tree>
                                <field name="datetime" />
                            </tree>
                            <form>
                                <!-- display datetime in readonly as modal will open in edit -->
                                <field name="datetime" widget="date" attrs="{'readonly': 1}" />
                            </form>
                        </field>
                    </form>
                `,
            });

            const expectedDateString = "02/08/2017 06:00:00"; // with timezone
            assert.strictEqual(
                target.querySelector(".o_field_widget[name='p'] .o_data_cell").textContent,
                expectedDateString,
                "the datetime (datetime widget) should be correctly displayed in tree view"
            );

            // switch to form view
            await click(target, ".o_field_widget[name='p'] .o_data_cell");
            assert.strictEqual(
                document.body.querySelector(".modal .o_field_date[name='datetime']").textContent,
                "02/08/2017",
                "the datetime (date widget) should be correctly displayed in form view"
            );
        }
    );

    QUnit.test("datepicker option: daysOfWeekDisabled", async function (assert) {
        assert.expect(42);

        serverData.models.partner.fields.datetime.default = "2017-08-02 12:00:05";
        serverData.models.partner.fields.datetime.required = true;

        await makeView({
            type: "form",
            resModel: "partner",
            serverData,
            arch: `
                <form>
                    <field name="datetime" options="{'datepicker': { 'daysOfWeekDisabled': [0, 6] }}" />
                </form>
            `,
        });

        await click(target, ".o_datepicker_input");

        for (const el of document.body.querySelectorAll(".day:nth-child(2), .day:last-child")) {
            assert.hasClass(el, "disabled", "first and last days must be disabled");
        }

        // the assertions below could be replaced by a single hasClass classic on the jQuery set using the idea
        // All not <=> not Exists. But we want to be sure that the set is non empty. We don't have an helper
        // function for that.
        for (const el of document.body.querySelectorAll(
            ".day:not(:nth-child(2)):not(:last-child)"
        )) {
            assert.doesNotHaveClass(el, "disabled", "other days must stay clickable");
        }
    });

    QUnit.test("datetime field: hit enter should update value", async function (assert) {
        /*
        This test verifies that the field datetime is correctly computed when:
            - we press enter to validate our entry
            - we click outside the field to validate our entry
            - we save
        */
        patchTimeZone(120);

        registry.category("services").add(
            "localization",
            makeFakeLocalizationService({
                dateFormat: "%m/%d/%Y",
                timeFormat: "%H:%M:%S",
            }),
            { force: true }
        );

        await makeView({
            serverData,
            type: "form",
            resModel: "partner",
            arch: '<form string="Partners"><field name="datetime"/></form>',
            resId: 1,
        });

        await click(target, ".o_form_button_edit");

        const datetime = target.querySelector(".o_field_datetime input");

        // Enter a beginning of date and press enter to validate
        await editInput(datetime, null, "01/08/22 14:30:40");
        await triggerEvent(datetime, null, "keydown", { key: "Enter" });

        const datetimeValue = `01/08/2022 14:30:40`;

        assert.strictEqual(datetime.value, datetimeValue);

        // Click outside the field to check that the field is not changed
        await click(target);
        assert.strictEqual(datetime.value, datetimeValue);

        // Save and check that it's still ok
        await click(target, ".o_form_button_save");

        const { textContent } = target.querySelector(".o_field_datetime span");
        assert.strictEqual(textContent, datetimeValue);
    });
});
