/** @odoo-module **/

import { drag, dragAndDrop, getFixture, mount, nextTick } from "@web/../tests/helpers/utils";
import { useDraggable } from "@web/core/utils/draggable";

import { Component, reactive, useRef, useState, xml } from "@odoo/owl";

let target;
QUnit.module("Draggable", ({ beforeEach }) => {
    beforeEach(() => (target = getFixture()));

    QUnit.module("Draggable hook");

    QUnit.test("Parameters error handling", async (assert) => {
        assert.expect(5);

        const mountListAndAssert = async (setupList, shouldThrow) => {
            class List extends Component {
                setup() {
                    setupList();
                }
            }

            List.template = xml`
                <div t-ref="root" class="root">
                    <ul class="list">
                        <li t-foreach="[1, 2, 3]" t-as="i" t-key="i" t-esc="i" class="item" />
                    </ul>
                </div>`;

            let err;
            await mount(List, target).catch((e) => (err = e));

            assert.ok(
                shouldThrow ? err : !err,
                `An error should${shouldThrow ? "" : "n't"} have been thrown when mounting.`
            );
        };

        // Incorrect params
        await mountListAndAssert(() => {
            useDraggable({});
        }, true);
        await mountListAndAssert(() => {
            useDraggable({
                ref: useRef("root"),
            });
        }, true);
        await mountListAndAssert(() => {
            useDraggable({
                elements: ".item",
            });
        }, true);

        // Correct params
        await mountListAndAssert(() => {
            useDraggable({
                ref: {},
                elements: ".item",
                enable: false,
            });
        }, false);
        await mountListAndAssert(() => {
            useDraggable({
                ref: useRef("root"),
                elements: ".item",
            });
        }, false);
    });

    QUnit.test("Simple sorting in single group", async (assert) => {
        assert.expect(22);

        class List extends Component {
            setup() {
                useDraggable({
                    ref: useRef("root"),
                    elements: ".item",
                    onDragStart({ element }) {
                        assert.step("start");
                        assert.strictEqual(element.innerText, "1");
                    },
                    onDrag({ element }) {
                        assert.step("drag");
                        assert.strictEqual(element.innerText, "1");
                    },
                    onDragEnd({ element }) {
                        assert.step("stop");
                        assert.strictEqual(element.innerText, "1");
                        assert.containsN(target, ".item", 3);
                    },
                    onDrop({ element, previous, next, parent }) {
                        assert.step("drop");
                        assert.strictEqual(element.innerText, "1");
                        assert.strictEqual(previous.innerText, "2");
                        assert.strictEqual(next.innerText, "3");
                        assert.notOk(parent);
                    },
                });
            }
        }

        List.template = xml`
            <div t-ref="root" class="root">
                <ul class="list">
                    <li t-foreach="[1, 2, 3]" t-as="i" t-key="i" t-esc="i" class="item" />
                </ul>
            </div>`;

        await mount(List, target);

        assert.containsN(target, ".item", 3);
        assert.containsNone(target, ".o_dragged");
        assert.verifySteps([]);

        // First item after 2nd item
        const { drop } = await drag(".item:first-child").moveTo(".item:nth-child(2)");

        assert.hasClass(target.querySelector(".item"), "o_dragged");

        await drop();

        assert.containsN(target, ".item", 3);
        assert.containsNone(target, ".o_dragged");
        assert.verifySteps(["start", "drag", "stop", "drop"]);
    });

    QUnit.test("Simple sorting in multiple groups", async (assert) => {
        assert.expect(20);

        class List extends Component {
            setup() {
                useDraggable({
                    ref: useRef("root"),
                    elements: ".item",
                    onDragStart({ element }) {
                        assert.step("start");
                        assert.strictEqual(element.innerText, "2 1");
                    },
                    onGroupEnter({ group }) {
                        assert.step("groupenter");
                        assert.hasClass(group, "list1");
                    },
                    onDragEnd({ element }) {
                        assert.step("stop");
                        assert.strictEqual(element.innerText, "2 1");
                    },
                    onDrop({ element, previous, next, parent }) {
                        assert.step("drop");
                        assert.strictEqual(element.innerText, "2 1");
                        assert.strictEqual(previous.innerText, "1 3");
                        assert.notOk(next);
                        assert.hasClass(parent, "list1");
                    },
                });
            }
        }

        List.template = xml`
            <div t-ref="root" class="root">
                <ul t-foreach="[1, 2, 3]" t-as="l" t-key="l" t-attf-class="list p-3 list{{ l }}">
                    <li t-foreach="[1, 2, 3]" t-as="i" t-key="i" t-esc="l + ' ' + i" class="item" />
                </ul>
            </div>`;

        await mount(List, target);

        assert.containsN(target, ".list", 3);
        assert.containsN(target, ".item", 9);
        assert.verifySteps([]);

        // First item of 2nd list appended to first list
        await dragAndDrop(".list2 .item:first-child", ".list1");

        assert.containsN(target, ".list", 3);
        assert.containsN(target, ".item", 9);
        assert.verifySteps(["start", "groupenter", "stop", "drop"]);
    });

    QUnit.test("Dynamically disable sortable feature", async (assert) => {
        assert.expect(4);

        const state = reactive({ enableSortable: true });
        class List extends Component {
            setup() {
                this.state = useState(state);
                useDraggable({
                    ref: useRef("root"),
                    elements: ".item",
                    enable: () => this.state.enableSortable,
                    onDragStart() {
                        assert.step("start");
                    },
                });
            }
        }

        List.template = xml`
            <div t-ref="root" class="root">
                <ul class="list">
                    <li t-foreach="[1, 2, 3]" t-as="i" t-key="i" t-esc="i" class="item" />
                </ul>
            </div>`;

        await mount(List, target);

        assert.verifySteps([]);

        // First item before last item
        await dragAndDrop(".item:first-child", ".item:last-child");

        // Drag should have occurred
        assert.verifySteps(["start"]);

        state.enableSortable = false;
        await nextTick();

        // First item before last item
        await dragAndDrop(".item:first-child", ".item:last-child");

        // Drag shouldn't have occurred
        assert.verifySteps([]);
    });

    QUnit.test("Disabled in small environment", async (assert) => {
        assert.expect(2);

        class List extends Component {
            setup() {
                useDraggable({
                    ref: useRef("root"),
                    elements: ".item",
                    onDragStart() {
                        throw new Error("Shouldn't start the sortable feature.");
                    },
                });
            }
        }

        List.template = xml`
            <div t-ref="root" class="root">
                <ul class="list">
                    <li t-foreach="[1, 2, 3]" t-as="i" t-key="i" t-esc="i" class="item" />
                </ul>
            </div>`;

        await mount(List, target, { env: { isSmall: true } });

        assert.containsN(target, ".item", 3);

        // First item after 2nd item
        await dragAndDrop(".item:first-child", ".item:nth-child(2)");

        assert.ok(true, "No drag sequence should have been initiated");
    });

    QUnit.test("Ignore specified elements", async (assert) => {
        assert.expect(6);

        class List extends Component {
            setup() {
                useDraggable({
                    ref: useRef("root"),
                    elements: ".item",
                    ignore: ".ignored",
                    onDragStart() {
                        assert.step("drag");
                    },
                });
            }
        }

        List.template = xml`
            <div t-ref="root" class="root">
                <ul class="list">
                    <li t-foreach="[1, 2, 3]" t-as="i" t-key="i" class="item">
                        <span class="ignored" t-esc="i" />
                        <span class="not-ignored" t-esc="i" />
                    </li>
                </ul>
            </div>`;

        await mount(List, target);

        assert.verifySteps([]);

        // Drag root item element
        await dragAndDrop(".item:first-child", ".item:nth-child(2)");

        assert.verifySteps(["drag"]);

        // Drag ignored element
        await dragAndDrop(".item:first-child .not-ignored", ".item:nth-child(2)");

        assert.verifySteps(["drag"]);

        // Drag non-ignored element
        await dragAndDrop(".item:first-child .ignored", ".item:nth-child(2)");

        assert.verifySteps([]);
    });
});
