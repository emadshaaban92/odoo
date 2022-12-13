/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { MacroEngine } from "@web/core/macro";
import { TourPointer } from "../tour_pointer/tour_pointer";

// TODO-JCB: Replace the following import with the non-legacy version.
import { device } from "web.config";
import { findTrigger } from "web_tour.utils";
import RunningTourActionHelper from "web_tour.RunningTourActionHelper";
// TODO-JCB: Find `config.device.isMobile` from non-legacy module.
import config from "web.config";

/**
 * TODO-JCB: Don't forget the following:
 * - It doesn't seem to work in mobile. For the tour from [planning.js],
 *   the pointer continues to point to the "app" icon even after click.
 * TODO-JCB: Maybe it's better if jQuery is used internally, and methods that return jQuery element should just return normal Elements.
 * - Maybe partially 'hiding' our reliance to jQuery is a good thing?
 * TODO-JCB: Should be able to recover the last performed step after page reload.
 * TODO-JCB: Make sure all the comments are correct.
 */

/**
 * Checks if [key] maps to a defined (non-undefined) value in [obj].
 * @param {string} key
 * @param {object} obj
 * @returns
 */
function isDefined(key, obj) {
    return key in obj && obj[key] !== undefined;
}

/**
 * Based on [step.run] and the trigger.
 * @param {jQuery} $element
 * @param {Runnable} run
 * @returns {string}
 */
function getConsumeEventType($element, run) {
    if ($element.hasClass("o_field_many2one") || $element.hasClass("o_field_many2manytags")) {
        return "autocompleteselect";
    } else if (
        $element.is("textarea") ||
        $element.filter("input").is(function () {
            const type = $(this).attr("type");
            return !type || !!type.match(/^(email|number|password|search|tel|text|url)$/);
        })
    ) {
        // FieldDateRange triggers a special event when using the widget
        if ($element.hasClass("o_field_date_range")) {
            return "apply.daterangepicker input";
        }
        if (
            config.device.isMobile &&
            $element.closest(".o_field_widget").is(".o_field_many2one, .o_field_many2many")
        ) {
            return "click";
        }
        return "input";
    } else if ($element.hasClass("ui-draggable-handle")) {
        return "drag";
    } else if (typeof run === "string" && run.indexOf("drag_and_drop") === 0) {
        // this is a heuristic: the element has to be dragged and dropped but it
        // doesn't have class 'ui-draggable-handle', so we check if it has an
        // ui-sortable parent, and if so, we conclude that its event type is 'sort'
        if ($element.closest(".ui-sortable").length) {
            return "sort";
        }
        if (
            (run.indexOf("drag_and_drop_native") === 0 &&
                $element.hasClass("o_record_draggable")) ||
            $element.closest(".o_record_draggable").length
        ) {
            return "mousedown";
        }
    }
    return "click";
}

/**
 * Returns the element that will be used in listening to the `consumeEvent`.
 * It doesn't necessarily mean the given element, e.g. when listening to drag
 * event, we have to do it to the closest .ui-draggable ancestor.
 *
 * @param {jQuery} $el
 * @param {string} consumeEvent
 * @returns {jQuery}
 */
function getAnchorEl($el, consumeEvent) {
    let $consumeEventAnchors = $el;
    if (consumeEvent === "drag") {
        // jQuery-ui draggable triggers 'drag' events on the .ui-draggable element,
        // but the tip is attached to the .ui-draggable-handle element which may
        // be one of its children (or the element itself)
        $consumeEventAnchors = $el.closest(".ui-draggable");
    } else if (consumeEvent === "input" && !$el.is("textarea, input")) {
        $consumeEventAnchors = $el.closest("[contenteditable='true']");
    } else if (consumeEvent.includes("apply.daterangepicker")) {
        $consumeEventAnchors = $el.parent().children(".o_field_date_range");
    } else if (consumeEvent === "sort") {
        // when an element is dragged inside a sortable container (with classname
        // 'ui-sortable'), jQuery triggers the 'sort' event on the container
        $consumeEventAnchors = $el.closest(".ui-sortable");
    }
    return $consumeEventAnchors;
}

/**
 * Returns true if `step` should *not* be included in a tour.
 * @param {TourStep} step
 * @param {{ mode: "manual" | "auto", edition: boolean, isMobile: boolean }} options
 * @returns {boolean}
 */
function shouldOmit(step, options) {
    const correctEdition = isDefined("edition", step) ? step.edition === options.edition : true;
    const correctDevice = isDefined("mobile", step) ? step.mobile === options.isMobile : true;
    return (
        !correctEdition ||
        !correctDevice ||
        // `step.auto = true` means omitting a step in a manual tour.
        (options.mode === "manual" && step.auto)
    );
}

function queryStep(step) {
    const triggerEl = findTrigger(step.trigger, step.in_modal);
    const altTriggerEl = findTrigger(step.alt_trigger, step.in_modal);
    const skipTriggerEl = findTrigger(step.skip_trigger, step.in_modal);

    // `extraTriggerOkay` should be true when `step.extra_trigger` is undefined.
    const extraTriggerOkay = step.extra_trigger
        ? findTrigger(step.extra_trigger, step.in_modal)
        : true;

    return { triggerEl, altTriggerEl, extraTriggerOkay, skipTriggerEl };
}

/**
 * Augments `step` for a tour for 'auto' (run) mode.
 * @param {*} step
 * @param {*} options
 * @returns
 */
function augmentStepAuto(step, options) {
    if (shouldOmit(step, options)) {
        return [];
    }

    let skipAction = false;
    return [
        {
            ...step,
            ...{
                action: () => {
                    console.log(step.trigger);
                    skipAction = false;
                },
            },
        },
        {
            trigger: () => {
                const { triggerEl, altTriggerEl, extraTriggerOkay, skipTriggerEl } = queryStep(
                    step
                );

                // [alt_trigger] - alternative to [trigger].
                // [extra_trigger] - should also be present together with the [trigger].
                const stepEl = extraTriggerOkay && (triggerEl || altTriggerEl);

                // If [skip_trigger] element is present, immediately return [stepEl] for potential
                // consumption of this step.
                if (stepEl && skipTriggerEl) {
                    skipAction = true;
                }
                return stepEl;
            },
            action: (stepEl) => {
                if (skipAction) return;

                const consumeEvent = step.consumeEvent || getConsumeEventType($(stepEl), step.run);
                const $anchorEl = getAnchorEl($(stepEl), consumeEvent);

                // TODO: Delegate the following routine to the `ACTION_HELPERS` in the macro module.
                const actionHelper = new RunningTourActionHelper({
                    consume_event: consumeEvent,
                    $anchor: $anchorEl,
                });
                if (typeof step.run === "function") {
                    try {
                        // `this.$anchor` is expected in many `step.run`.
                        step.run.call({ $anchor: $anchorEl }, actionHelper);
                    } catch (e) {
                        // TODO-JCB: What to do with the following console.error?
                        // console.error(`Tour ${tour_name} failed at step ${self._describeTip(tip)}: ${e.message}`);
                        throw e;
                    }
                } else if (step.run !== undefined) {
                    const m = step.run.match(/^([a-zA-Z0-9_]+) *(?:\(? *(.+?) *\)?)?$/);
                    try {
                        actionHelper[m[1]](m[2]);
                    } catch (e) {
                        // TODO-JCB: What to do with the following console.error?
                        // console.error(`Tour ${tour_name} failed at step ${self._describeTip(tip)}: ${e.message}`);
                        throw e;
                    }
                } else {
                    actionHelper.auto();
                }
            },
        },
    ];
}

/**
 * Augments `step` of a tour for 'manual' (run) mode.
 * TODO-JCB: Describe the trick here. How does the macro engine able to wait for the user's action?
 * TODO-JCB: Improve the code.
 * @param {*} step
 * @param {*} options
 * @returns
 */
function augmentStepManual(step, options) {
    if (shouldOmit(step, options)) {
        return [];
    }

    let proceedWith, stepEl, prevEl, consumeEvent, $anchorEl;
    return [
        {
            ...step,
            ...{
                action: () => {
                    console.log(step.trigger);
                },
            },
        },
        {
            trigger: () => {
                if (proceedWith) return proceedWith;

                const { triggerEl, altTriggerEl, extraTriggerOkay, skipTriggerEl } = queryStep(
                    step
                );
                // This callback can be called multiple times until it returns true.
                // We should take into account the fact the element is not in the
                // dom. [pointTo] takes into account whether [stepEl] is null or not.
                prevEl = stepEl;
                // [alt_trigger] - alternative to [trigger].
                // [extra_trigger] - should also be present together with the [trigger].
                stepEl = extraTriggerOkay && (triggerEl || altTriggerEl);
                consumeEvent = step.consumeEvent || getConsumeEventType($(stepEl), step.run);
                // If [skip_trigger] element is present, immediately return [stepEl] for potential
                // consumption of this step.
                if (stepEl && skipTriggerEl) {
                    return stepEl;
                }

                if (prevEl) {
                    $anchorEl.off(".anchor");
                }
                if (stepEl) {
                    $anchorEl = getAnchorEl($(stepEl), consumeEvent);
                    // Start waiting for action, or automatically perform `step.run`.
                    // Set `proceedWith` to a non-falsy value as a signal to proceed to the next step.
                    options.pointerMethods.show();
                    $anchorEl.on(`${consumeEvent}.anchor`, async () => {
                        // TODO-JCB: The following logic comes from _getAnchorAndCreateEvent and it might be important to take it into account.
                        // $consumeEventAnchors.on(consumeEvent + ".anchor", (function (e) {
                        //     if (e.type !== "mousedown" || e.which === 1) { // only left click
                        //         if (this.info.consumeVisibleOnly && !this.isShown()) {
                        //             // Do not consume non-displayed tips.
                        //             return;
                        //         }
                        //         this.trigger("tip_consumed");
                        //         this._unbind_anchor_events();
                        //     }
                        // }).bind(this));

                        // stop waiting
                        $anchorEl.off(".anchor");

                        proceedWith = stepEl;

                        // Finally, advance to the next step.
                        // The following will call this `trigger` function which returns the `proceedWith`.
                        options.advance();
                    });
                }
                options.pointerMethods.pointTo($anchorEl[0] || stepEl);
            },
            action: () => {
                // Clean up
                proceedWith = undefined;
                stepEl = undefined;
                consumeEvent = undefined;
                $anchorEl = undefined;
                options.pointerMethods.hide();
            },
        },
    ];
}

/**
 * TODO-JCB: Make sure to include "edition", "mode" and "isMobile" in the type of [options].
 * @param {*} macroDescription
 * @param {*} options
 * @returns
 */
function augmentMacro(macroDescription, augmenter, options) {
    return {
        ...macroDescription,
        steps: macroDescription.steps
            .reduce((newSteps, step) => [...newSteps, ...augmenter(step, options)], [])
            .concat([
                {
                    action: () => {
                        console.log("Tour done!");
                        options.pointerMethods.hide();
                    },
                },
            ]),
    };
}

/**
 * @param {*} param0
 * @returns {[state: { x, y, isVisible, position, content, mode, viewPortState, fixed }, methods: { pointTo, hide, show }]}
 */
function createPointerState({ x, y, isVisible, position, content, mode, viewPortState, fixed }) {
    const state = reactive({ x, y, isVisible, position, content, mode, viewPortState, fixed });
    const pointerSize = { width: 20, height: 20 };

    function hide() {
        state.isVisible = false;
    }

    function show() {
        state.isVisible = true;
    }

    /**
     * Update [state] to refer to the given [el].
     * If [el] is undefined, hide the pointer.
     * @param {Element | undefined} el
     */
    function pointTo(el) {
        if (el) {
            const rect = el.getBoundingClientRect();
            const top = rect.top - pointerSize.width;
            const left = rect.left + rect.width / 2 - pointerSize.height / 2;
            Object.assign(state, { x: left, y: top });
        } else {
            hide();
        }
    }

    return [state, { pointTo, hide, show }];
}

/**
 * TODO-JCB: Not sure of this.
 * @typedef {string} Markup
 * @typedef {string} JQuerySelector
 * TODO-JCB: what is [Actions]?
 * @typedef {string | (actions: Actions) => void | Promise<void>} Runnable
 *
 * @typedef TourMetadata
 * @property {string} url
 * @property {string | () => Markup} [rainbowManMessage]
 * @property {boolean} [rainbowMan]
 * @property {number} [sequence]
 * @property {boolean} [test]
 * @property {Promise<any>} [wait_for]
 * @property {string} [saveAs]
 * @property {boolean} [skip_enabled]
 * // The following is proposed:
 * @property {string} name
 *
 * @typedef TourStep
 * @property {string} [id]
 * @property {JQuerySelector} trigger
 * @property {JQuerySelector} [extra_trigger]
 * @property {JQuerySelector} [alt_trigger]
 * @property {JQuerySelector} [skip_trigger]
 * @property {Markup} [content]
 * @property {"left" | "top" | "right" | "bottom"} [position]
 * @property {"community" | "enterprise"} [edition]
 * @property {Runnable} [run]
 * @property {boolean} [auto]
 * @property {boolean} [in_modal]
 * @property {number} [width]
 * @property {number} [timeout]
 * @property {boolean} [consumeVisibleOnly]
 * @property {boolean} [noPrepend]
 * @property {string} [consumeEvent]
 * @property {boolean} [mobile]
 * @property {string} [title]
 */
export const tourService = {
    start() {
        const macroEngine = new MacroEngine(document);
        const edition = odoo.info.isEnterprise ? "enterprise" : "community";
        const isMobile = device.isMobile;

        const [pointerState, pointerMethods] = createPointerState({
            content: "",
            position: "top",
            x: 0,
            y: 0,
            isVisible: false,
            mode: "bubble",
            viewPortState: "in",
            fixed: false,
        });

        /**
         * @param {string} _tourName
         * @param {{ kind: "manual" } | { kind: "auto", interval: number }} mode
         */
        function run(
            params = { tourName: "", mode: { kind: "auto", interval: 0, showPointer: false } }
        ) {
            const { tourName: _tourName, mode } = params;
            const tourDesc = registry.category("tours").get(params.tourName);

            // Modify the steps to be compatible to Macro system.
            for (const step of tourDesc.steps) {
                delete step.content;
            }

            const augmentedMacro = augmentMacro(
                Object.assign(tourDesc, { interval: mode.kind === "manual" ? 0 : mode.interval }),
                mode.kind === "manual" ? augmentStepManual : augmentStepAuto,
                {
                    advance: () => macroEngine.advanceMacros(),
                    pointerMethods,
                    edition,
                    isMobile,
                    mode: mode.kind,
                    showPointer: mode.showPointer,
                }
            );

            // The pointer points to the trigger and waits for the user to do the action.
            macroEngine.activate(augmentedMacro);
        }

        registry.category("main_components").add("TourPointer", {
            Component: TourPointer,
            props: { pointerState },
        });

        return { run };
    },
};

registry.category("services").add("tour_service_x", tourService);
