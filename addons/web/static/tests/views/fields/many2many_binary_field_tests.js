/** @odoo-module **/

import { click, getFixture, nextTick } from "@web/../tests/helpers/utils";
import { makeView, setupViewRegistries } from "@web/../tests/views/helpers";
import { registry } from "@web/core/registry";

const serviceRegistry = registry.category("services");

let target;
let serverData;

QUnit.module("Fields", (hooks) => {
    hooks.beforeEach(() => {
        target = getFixture();
        serverData = {
            models: {
                turtle: {
                    fields: {
                        picture_ids: {
                            string: "Pictures",
                            type: "many2many",
                            relation: "ir.attachment",
                        },
                    },
                    records: [
                        {
                            id: 1,
                            picture_ids: [17],
                        },
                    ],
                },
                "ir.attachment": {
                    fields: {
                        name: { string: "Name", type: "char" },
                        mimetype: { string: "Mimetype", type: "char" },
                    },
                    records: [
                        {
                            id: 17,
                            name: "Marley&Me.jpg",
                            mimetype: "jpg",
                        },
                    ],
                },
            },
        };

        setupViewRegistries();
    });

    QUnit.module("Many2ManyBinaryField");

    QUnit.test("widget many2many_binary", async function (assert) {
        assert.expect(23);

        const fakeHTTPService = {
            start() {
                return {
                    post: (route, params) => {
                        assert.strictEqual(route, "/web/binary/upload_attachment");
                        assert.strictEqual(
                            params.ufile[0].name,
                            "fake_file.tiff",
                            "file is correctly uploaded to the server"
                        );
                        const file = {
                            id: 10,
                            name: "fake_file.tiff",
                            mimetype: "text/plain",
                        };
                        serverData.models["ir.attachment"].records.push(file);
                        return JSON.stringify([file]);
                    },
                };
            },
        };
        serviceRegistry.add("http", fakeHTTPService);

        serverData.views = {
            "ir.attachment,false,list": '<tree string="Pictures"><field name="name"/></tree>',
        };

        await makeView({
            serverData,
            type: "form",
            resModel: "turtle",
            arch: `
                <form>
                    <group>
                        <field name="picture_ids" widget="many2many_binary" options="{'accepted_file_extensions': 'image/*'}"/>
                    </group>
                </form>`,
            resId: 1,
            mockRPC(route, args) {
                if (args.method !== "get_views") {
                    assert.step(route);
                }
                if (route === "/web/dataset/call_kw/ir.attachment/read") {
                    assert.deepEqual(args.args[1], ["name", "mimetype"]);
                }
            },
        });

        assert.containsOnce(
            target,
            "div.o_field_widget .oe_fileupload",
            "there should be the attachment widget"
        );
        assert.containsOnce(
            target,
            "div.o_field_widget .oe_fileupload .o_attachments",
            "there should be one attachment"
        );
        assert.containsNone(
            target,
            "div.o_field_widget .oe_fileupload .o_attach",
            "there should not be an Add button (readonly)"
        );
        assert.containsNone(
            target,
            "div.o_field_widget .oe_fileupload .o_attachment .o_attachment_delete",
            "there should not be a Delete button (readonly)"
        );

        // to edit mode
        await click(target, ".o_form_button_edit");
        assert.containsOnce(
            target,
            "div.o_field_widget .oe_fileupload .o_attach",
            "there should be an Add button"
        );
        assert.strictEqual(
            target.querySelector("div.o_field_widget .oe_fileupload .o_attach").textContent.trim(),
            "Pictures",
            "the button should be correctly named"
        );

        assert.strictEqual(
            target.querySelector("input.o_input_file").getAttribute("accept"),
            "image/*",
            'there should be an attribute "accept" on the input'
        );
        assert.verifySteps([
            "/web/dataset/call_kw/turtle/read",
            "/web/dataset/call_kw/ir.attachment/read",
        ]);

        // Set and trigger the change of a file for the input
        const fileInput = target.querySelector('input[type="file"]');
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(new File(["fake_file"], "fake_file.tiff", { type: "text/plain" }));
        fileInput.files = dataTransfer.files;
        fileInput.dispatchEvent(new Event("change", { bubbles: true }));
        await nextTick();

        assert.strictEqual(
            target.querySelector(".o_attachment:nth-child(2) .caption a").textContent,
            "fake_file.tiff",
            'value of attachment should be "fake_file.tiff"'
        );
        assert.strictEqual(
            target.querySelector(".o_attachment:nth-child(2) .caption.small a").textContent,
            "tiff",
            "file extension should be correct"
        );

        // delete the attachment
        await click(
            target.querySelector(
                "div.o_field_widget .oe_fileupload .o_attachment .o_attachment_delete"
            )
        );

        await click(target, ".o_form_button_save");
        assert.containsOnce(
            target,
            "div.o_field_widget .oe_fileupload .o_attachments",
            "there should be only one attachment left"
        );
        assert.verifySteps([
            "/web/dataset/call_kw/ir.attachment/read",
            "/web/dataset/call_kw/turtle/write",
            "/web/dataset/call_kw/turtle/read",
            "/web/dataset/call_kw/ir.attachment/read",
        ]);
    });
});
