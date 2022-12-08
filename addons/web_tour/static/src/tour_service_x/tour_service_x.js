/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { MacroEngine } from "@web/core/macro";
import { browser } from "@web/core/browser/browser";
import { TourPointer } from "../tour_pointer/tour_pointer";

// TODO-JCB: Replace the following import with the non-legacy version.
import { device } from "web.config";
import { findTrigger } from "web_tour.utils";

/**
 * TODO-JCB: Don't forget the following:
 * - It doesn't seem to work in mobile. For the tour from [planning.js],
 *   the pointer continues to point to the "app" icon even after click.
 * TODO-JCB: Maybe it's better if jQuery is used internally, and methods that return jQuery element should just return normal Elements.
 * - Maybe partially 'hiding' our reliance to jQuery is a good thing?
 */

/**
 * Returns an augmented version of a simple tour that automatically
 * points to a step's trigger, perform the action and advances to the
 * next step after a given [interval]. It calls [pointTo] based
 * on the calculated location of the trigger's element.
 * @param {Object} macroDescription
 * TODO-JCB: Update this type.
 * @param {{ interval: number; pointTo: (el) => void, advance: () => void }} options
 * @returns {Object}
 */
function createAutoMacro(
    macroDescription,
    options = { interval: 500, pointTo: (_el) => {}, advance: () => {} }
) {
    function augmentStep(step) {
        // TODO-JCB: Take into account the possibility of multiple step elements because of the alt_trigger.
        let stepEl;
        let timeout;
        const res = { val: false };
        return [
            { ...step, action: undefined },
            {
                action: () => {
                    res.val = false;
                    stepEl = findTrigger(step.trigger, step.in_modal);
                    options.pointerMethods.pointTo(stepEl);
                },
            },
            step,
            {
                trigger: () => {
                    if (!timeout) {
                        timeout = browser.setTimeout(() => {
                            res.val = stepEl;
                            timeout = undefined;
                            options.advance();
                        }, options.interval);
                    }
                    return res.val;
                },
            },
        ];
    }

    return {
        ...macroDescription,
        steps: macroDescription.steps.reduce(
            (newSteps, step) => [...newSteps, ...augmentStep(step)],
            []
        ),
    };
}

/**
 * TODO-JCB: Make sure to include "edition" and "isMobile" in the type of [options].
 * @param {*} macroDescription
 * @param {*} options
 * @returns
 */
function createManualMacro(macroDescription, options) {
    /**
     * Checks if [key] maps to a defined (non-undefined) value in [obj].
     * @param {string} key
     * @param {object} obj
     * @returns
     */
    function isDefined(key, obj) {
        return key in obj || obj[key] !== undefined;
    }

    /**
     * Returns true if the [step] should not be included in the manual tour.
     * @param {TourStep} step
     * @returns {boolean}
     */
    function shouldOmit(step) {
        const correctEdition = isDefined("edition", step) ? step.edition === options.edition : true;
        const correctDevice = isDefined("mobile", step) ? step.mobile === options.isMobile : true;
        return (
            !correctEdition ||
            !correctDevice ||
            // TODO-JCB: Confirm if [step.auto = true] means omitting a step in a manual tour.
            step.auto
        );
    }

    function queryStep(step) {
        const triggerEl = findTrigger(step.trigger, step.in_modal);
        const altTriggerEl = findTrigger(step.alt_trigger, step.in_modal);
        const skipTriggerEl = findTrigger(step.skip_trigger, step.in_modal);

        // [extraTriggerOkay] should be true when [step.extra_trigger] is undefined.
        const extraTriggerOkay = step.extra_trigger
            ? findTrigger(step.extra_trigger, step.in_modal)
            : true;

        return { triggerEl, altTriggerEl, extraTriggerOkay, skipTriggerEl };
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

    function augmentStep(step) {
        let stepEl;
        /**
         * [consumeEvent] is the event type that [$anchorEl] waits for
         * in order to proceed to the next step.
         */
        let consumeEvent;
        /**
         * [$anchorEl] is the jquery element where the [consumeEvent] be attached.
         */
        let $anchorEl;
        /**
         * [proceedWith] is the element returned by the last inserted step's trigger.
         * - NOTE: Not sure though if the element is important or if it can be used for the
         *   next step.
         */
        let proceedWith;
        if (shouldOmit(step)) {
            return [];
        }
        return [
            step,
            {
                action: () => {
                    proceedWith = false;
                },
            },
            {
                trigger: () => {
                    const { triggerEl, altTriggerEl, extraTriggerOkay, skipTriggerEl } = queryStep(
                        step
                    );

                    // This callback can be called multiple times until it returns true.
                    // We should take into account the fact the element is not in the
                    // dom. [pointTo] takes into account whether [stepEl] is null or not.
                    let prevEl = stepEl;

                    // [alt_trigger] - alternative to [trigger].
                    // [extra_trigger] - should also be present together with the [trigger].
                    stepEl = extraTriggerOkay && (triggerEl || altTriggerEl);

                    consumeEvent = step.consumeEvent || getConsumeEventType($(stepEl));

                    // If [skip_trigger] element is present, immediately return [stepEl] for potential
                    // consumption of this step.
                    if (stepEl && skipTriggerEl) {
                        return stepEl;
                    }

                    if (prevEl) {
                        $anchorEl.off(".anchor");
                    }

                    // TODO-JCB: I think we should only add the listener when [proceedWith] is falsy.
                    if (stepEl) {
                        $anchorEl = getAnchorEl($(stepEl), consumeEvent);
                        $anchorEl.on(`${consumeEvent}.anchor`, () => {
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

                            proceedWith = stepEl;
                            $anchorEl.off(".anchor");
                            stepEl = undefined;
                            consumeEvent = undefined;
                            $anchorEl = undefined;
                            options.pointerMethods.hide();
                            options.advance();
                        });
                    }

                    // Call this everytime so that the pointer is always pointing at the
                    // step's trigger element.
                    // TODO-JCB: Maybe we only point to the trigger when [proceedWith] is falsy.
                    options.pointerMethods.pointTo(stepEl);

                    return proceedWith;
                },
            },
        ];
    }

    return {
        ...macroDescription,
        steps: macroDescription.steps
            .reduce((newSteps, step) => [...newSteps, ...augmentStep(step)], [])
            .concat([
                {
                    action: () => {
                        options.pointerMethods.hide();
                    },
                },
            ]),
    };
}

/**
 * @param {*} param0
 * @returns {[state: { x, y, isVisible, position, text }, methods: { pointTo, hide, setSizeGetter }]}
 */
function createPointerState({ x, y, isVisible, position, text }) {
    const state = reactive({ x, y, isVisible, position, text });

    /**
     * In order for pointer state to be useful, `sizeGetter` needs to
     * be bound to a method that returns the size of the pointer.
     * @see setSizeGetter
     */
    let sizeGetter;

    /**
     * Call this in the component containing the pointer element.
     * The pointer element should provide a method that returns the size
     * of the pointer
     * @param {() => { width: number, height: number }} f
     */
    function setSizeGetter(f) {
        sizeGetter = f;
    }

    function getSize() {
        if (!sizeGetter) {
            throw new Error("Unable to get size of the pointer.");
        }
        return sizeGetter();
    }

    function hide() {
        state.isVisible = false;
    }

    /**
     * Update [state] to refer to the given [el].
     * If [el] is undefined, hide the pointer.
     * @param {Element | undefined} el
     */
    function pointTo(el) {
        if (el) {
            const size = getSize();
            const rect = el.getBoundingClientRect();
            const top = rect.top - size.width;
            const left = rect.left + rect.width / 2 - size.height / 2;
            Object.assign(state, { x: left, y: top, isVisible: true });
        } else {
            hide();
        }
    }

    return [
        state,
        {
            pointTo,
            hide,
            setSizeGetter,
        },
    ];
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
            x: 0,
            y: 0,
            isVisible: false,
            position: "top",
            text: "",
        });

        /**
         * @param {string} _tourName
         * @param {{ kind: "manual" } | { kind: "auto", interval: number }} mode
         */
        function run(params = { tourName: "", mode: { kind: "auto", interval: 0 } }) {
            const { tourName: _tourName, mode } = params;
            const tourDesc = registry.category("tours").get(params.tourName);

            // Modify the steps to be compatible to Macro system.
            for (const step of tourDesc.steps) {
                delete step.content;
            }

            if (mode.kind == "auto") {
                macroEngine.activate(
                    createAutoMacro(tourDesc, {
                        advance: () => macroEngine.advanceMacros(),
                        interval: tourDesc.interval || mode.interval,
                        pointerMethods: pointer.methods,
                    })
                );
            } else if (mode.kind == "manual") {
                // The pointer points to the trigger and waits for the user to do the action.
                macroEngine.activate(
                    createManualMacro(Object.assign(tourDesc, { interval: mode.interval }), {
                        advance: () => macroEngine.advanceMacros(),
                        pointerMethods,
                        edition,
                        isMobile,
                    })
                );
            }
        }

        registry.category("main_components").add("TourPointer", {
            Component: TourPointer,
            props: { pointerState, setSizeGetter: pointerMethods.setSizeGetter },
        });

        return { run };
    },
};

registry.category("services").add("tour_service_x", tourService);
