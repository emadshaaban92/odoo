/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { TourPointer } from "../tour_pointer/tour_pointer";
import { MacroEngine } from "@web/core/macro";
import { browser } from "@web/core/browser/browser";

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
    const augmentStep = (step) => {
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
    };
    return {
        ...macroDescription,
        steps: macroDescription.steps.reduce(
            (newSteps, step) => [...newSteps, ...augmentStep(step)],
            []
        ),
    };
}

function createManualMacro(macroDescription, options) {
    const augmentStep = (step) => {
        let stepEl;
        const res = { val: false };
        const moveToNextStep = () => {
            res.val = stepEl;
            options.advance();
            stepEl.removeEventListener(step.action, moveToNextStep);
        };
        return [
            { ...step, action: undefined },
            {
                action: () => {
                    res.val = false;
                },
            },
            {
                trigger: () => {
                    // This callback can be called multiple times until it returns true.
                    // We should take into account the fact the element is not in the
                    // dom. [pointTo] takes into account whether [stepEl] is null or not.
                    let prevEl = stepEl;
                    stepEl = document.querySelector(step.trigger);
                    if (prevEl) {
                        prevEl.removeEventListener(step.action, moveToNextStep);
                    }
                    if (stepEl) {
                        stepEl.addEventListener(step.action, moveToNextStep);
                    }
                    // Call this everytime so that the pointer is always pointing at the
                    // step's trigger element.
                    options.pointTo(stepEl);
                    return res.val;
                },
            },
        ];
    };
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

        const pointerState = reactive({
            x: 0,
            y: 0,
            isVisible: false,
            position: "top",
            text: "",
        });

        function activate(macroDescription) {
            const originalOnFirstStep = macroDescription.onFirstStep;
            macroDescription.onFirstStep = (...args) => {
                pointerState.isVisible = true;
                if (originalOnFirstStep) {
                    originalOnFirstStep(...args);
                }
            };
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
                step.action = "click";
                delete step.content;
                delete step.extra_trigger;
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
