/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { TourPointer } from "../tour_pointer/tour_pointer";
import { MacroEngine } from "@web/core/macro";
import { browser } from "@web/core/browser/browser";

const SAMPLE_TOUR_MACRO = {
    steps: [
        {
            trigger: "button.inc",
            action: "click",
        },
        {
            trigger: "button.double",
            action: "click",
        },
        {
            trigger: "button.inc",
            action: "click",
        },
        {
            trigger: "button.double",
            action: "click",
        },
        {
            trigger: "button.dec",
            action: "click",
        },
        {
            trigger: "button.double",
            action: "click",
        },
    ],
};

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
        let listening;
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
            {
                trigger: () => {
                    if (listening) {
                        return res.val;
                    }
                    const moveToNextStep = () => {
                        res.val = stepEl;
                        options.advance();
                        stepEl.removeEventListener(step.action, moveToNextStep);
                    };
                    stepEl.addEventListener(step.action, moveToNextStep);
                    listening = true;
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
         * Update [pointer] to refer to the given [el].
         * @param {Element} el
         */
        function pointTo(el) {
            const rect = el.getBoundingClientRect();
            const top = rect.top - pointerSize.width;
            const left = rect.left + rect.width / 2 - pointerSize.height / 2;
            Object.assign(pointerState, { x: left, y: top });
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
            const tourDesc = SAMPLE_TOUR_MACRO;
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
                    createManualMacro(tourDesc, {
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
