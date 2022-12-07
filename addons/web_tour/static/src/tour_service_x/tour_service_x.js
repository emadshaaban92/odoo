/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { MacroEngine } from "@web/core/macro";
import { browser } from "@web/core/browser/browser";
import { TourPointer } from "../tour_pointer/tour_pointer";

// TODO-JCB: Replace the following import with the non-legacy version.
import { device } from "web.config";

/**
 * TODO-JCB: Don't forget the following:
 * - It doesn't seem to work in mobile. For the tour from [planning.js],
 *   the pointer continues to point to the "app" icon even after click.
 */

/**
 * Returns an augmented version of a simple tour that automatically
 * points to a step's trigger, perform the action and advances to the
 * next step after a given [interval]. It calls [pointTo] based
 * on the calculated location of the trigger's element.
 * @param {Object} macroDescription
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
                    stepEl = document.querySelector(step.trigger);
                    options.pointTo(stepEl);
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
     * Checks if [key] maps to a non-undefined value in [obj].
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

    function hasExtraTrigger(sourceEl, extraTriggerSelector) {
        if (extraTriggerSelector) {
            return sourceEl.querySelector(extraTriggerSelector);
        } else {
            return true;
        }
    }

    function hasSkipTrigger(sourceEl, skipTriggerSelector) {
        if (skipTriggerSelector) {
            return sourceEl.querySelector(skipTriggerSelector);
        } else {
            return false;
        }
    }

    function getModal(doc) {
        // TODO-JCB: need to take into account :visible pseudo class.
        return doc.querySelector(".modal") || doc;
    }

    /**
     * Based on [step.run] and the trigger.
     * @param {Element} el
     * @param {Runnable} run
     * @returns {string}
     */
    function getConsumeEventType(el, run) {
        const $element = $(el);
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

    function getAnchorEl(el, consumeEvent) {
        const $anchor = $(el);
        let $consumeEventAnchors = $anchor;
        if (consumeEvent === "drag") {
            // jQuery-ui draggable triggers 'drag' events on the .ui-draggable element,
            // but the tip is attached to the .ui-draggable-handle element which may
            // be one of its children (or the element itself)
            $consumeEventAnchors = $anchor.closest(".ui-draggable");
        } else if (consumeEvent === "input" && !$anchor.is("textarea, input")) {
            $consumeEventAnchors = $anchor.closest("[contenteditable='true']");
        } else if (consumeEvent.includes("apply.daterangepicker")) {
            $consumeEventAnchors = $anchor.parent().children(".o_field_date_range");
        } else if (consumeEvent === "sort") {
            // when an element is dragged inside a sortable container (with classname
            // 'ui-sortable'), jQuery triggers the 'sort' event on the container
            $consumeEventAnchors = $anchor.closest(".ui-sortable");
        }
        return $consumeEventAnchors;
    }

    function augmentStep(step) {
        let stepEl;
        /**
         * [consumeEvent] is the event type that [anchorEl] waits for
         * in order to proceed to the next step.
         */
        let consumeEvent;
        /**
         * [anchorEl] is the element where the [consumeEvent] be attached.
         */
        let anchorEl;
        const res = { val: false };
        if (shouldOmit(step)) {
            return [];
        }
        return [
            { ...step, action: undefined },
            {
                action: () => {
                    res.val = false;
                },
            },
            {
                trigger: () => {
                    // [in_modal] - if true, look for the element in the modal (fallback to the document)
                    const sourceEl = step.in_modal !== false && getModal(document);

                    // This callback can be called multiple times until it returns true.
                    // We should take into account the fact the element is not in the
                    // dom. [pointTo] takes into account whether [stepEl] is null or not.
                    let prevEl = stepEl;

                    // [alt_trigger] - alternative to [trigger].
                    // [extra_trigger] - should also be present together with the [trigger].
                    stepEl =
                        (hasExtraTrigger(sourceEl, step.extra_trigger) &&
                            sourceEl.querySelector(step.trigger)) ||
                        sourceEl.querySelector(step.alt_trigger);

                    consumeEvent = step.consumeEvent || getConsumeEventType(stepEl);

                    // [skip_trigger] - if present, immediately consume the [trigger].
                    if (stepEl && hasSkipTrigger(sourceEl, step.skip_trigger)) {
                        return stepEl;
                    }

                    if (prevEl) {
                        anchorEl.off(".anchor");
                    }

                    // TODO-JCB: I think we should only add the listener when [res.val] is falsy.
                    if (stepEl) {
                        anchorEl = getAnchorEl(stepEl, consumeEvent);
                        anchorEl.on(`${consumeEvent}.anchor`, () => {
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

                            res.val = stepEl;
                            anchorEl.off(".anchor");
                            stepEl = undefined;
                            anchorEl = undefined;
                            consumeEvent = undefined;
                            options.advance();
                        });
                    }

                    // Call this everytime so that the pointer is always pointing at the
                    // step's trigger element.
                    // TODO-JCB: Maybe we only point to the trigger when [res.val] is falsy.
                    options.pointTo(stepEl);

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

        const pointerState = reactive({
            x: 0,
            y: 0,
            isVisible: false,
            position: "top",
            text: "",
        });

        function activate(macroDescription) {
            const originalOnComplete = macroDescription.onComplete;
            macroDescription.onComplete = (...args) => {
                browser.setTimeout(() => {
                    pointerState.isVisible = false;
                }, macroDescription.interval || 0);
                if (originalOnComplete) {
                    originalOnComplete(...args);
                }
            };
            macroEngine.activate(macroDescription);
        }

        // TODO-JCB: Should be computed from the pointer component.
        const pointerSize = { width: 20, height: 20 };

        /**
         * Update [pointerState] to refer to the given [el].
         * If [el] is undefined, hide the pointer.
         * @param {Element | undefined} el
         */
        function pointTo(el) {
            if (el) {
                const rect = el.getBoundingClientRect();
                const top = rect.top - pointerSize.width;
                const left = rect.left + rect.width / 2 - pointerSize.height / 2;
                Object.assign(pointerState, { x: left, y: top, isVisible: true });
            } else {
                Object.assign(pointerState, { isVisible: false });
            }
        }

        function advanceMacros() {
            return macroEngine.advanceMacros();
        }

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
                activate(
                    createAutoMacro(tourDesc, {
                        advance: advanceMacros,
                        interval: tourDesc.interval || mode.interval,
                        pointTo,
                    })
                );
            } else if (mode.kind == "manual") {
                // The pointer points to the trigger and waits for the user to do the action.
                activate(
                    createManualMacro(Object.assign(tourDesc, { interval: mode.interval }), {
                        advance: advanceMacros,
                        pointTo,
                        edition,
                        isMobile,
                    })
                );
            }
        }

        registry.category("main_components").add("TourPointer", {
            Component: TourPointer,
            props: { pointerState },
        });

        return { run };
    },
};

registry.category("services").add("tour_service_x", tourService);
