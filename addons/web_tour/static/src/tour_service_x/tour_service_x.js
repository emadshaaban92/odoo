/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { MacroEngine } from "@web/core/macro";
import { TourPointer } from "../tour_pointer/tour_pointer";
import { browser } from "@web/core/browser/browser";

// TODO-JCB: Replace the following import with the non-legacy version.
import { device } from "web.config";
import { findTrigger } from "web_tour.utils";
import RunningTourActionHelper from "web_tour.RunningTourActionHelper";
// TODO-JCB: Find `config.device.isMobile` from non-legacy module.
import config from "web.config";

const getEdition = () => (odoo.info.isEnterprise ? "enterprise" : "community");
const isMobile = device.isMobile;

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
 * @param {"manual" | "auto"} mode
 * @returns {boolean}
 */
function shouldOmit(step, mode) {
    const correctEdition = isDefined("edition", step) ? step.edition === getEdition() : true;
    const correctDevice = isDefined("mobile", step) ? step.mobile === isMobile : true;
    return (
        !correctEdition ||
        !correctDevice ||
        // `step.auto = true` means omitting a step in a manual tour.
        (mode === "manual" && step.auto)
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
function augmentStepAuto(macroDesc, [stepIndex, step], options) {
    const { mode } = options;

    if (shouldOmit(step, mode)) {
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
                if (skipAction) {
                    browser.localStorage.setItem(macroDesc.name, stepIndex + 1);
                    return;
                }

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
                browser.localStorage.setItem(macroDesc.name, stepIndex + 1);
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
function augmentStepManual(macroDesc, [stepIndex, step], options) {
    const { pointerMethods, advance, intersection, mode } = options;

    if (shouldOmit(step, mode)) {
        return [];
    }

    let proceedWith, stepEl, prevEl, consumeEvent, $anchorEl, currentAnchor;
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
                // dom. [update] takes into account whether [stepEl] is null or not.
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
                    pointerMethods.setState({ isVisible: true });
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
                        advance();
                    });
                    $anchorEl.on("mouseenter.anchor", () => {
                        pointerMethods.setState({ mode: "info" });
                    });
                    $anchorEl.on("mouseleave.anchor", () => {
                        pointerMethods.setState({ mode: "bubble" });
                    });
                }
                const newAnchor = stepEl && $anchorEl[0];
                if (currentAnchor !== newAnchor) {
                    intersection.set({ target: newAnchor });
                }
                pointerMethods.update(intersection, step, newAnchor);
                currentAnchor = newAnchor;
            },
            action: () => {
                // Clean up
                proceedWith = undefined;
                stepEl = undefined;
                consumeEvent = undefined;
                $anchorEl = undefined;
                currentAnchor = undefined;
                options.pointerMethods.setState({ isVisible: false, mode: "bubble" });
                browser.localStorage.setItem(macroDesc.name, stepIndex + 1);
            },
        },
    ];
}

/**
 * @param {*} macroDescription
 * @param {*} options
 * @returns
 */
function augmentMacro(macroDescription, augmenter, options) {
    const { currentStepIndex, pointerMethods } = options;
    return {
        ...macroDescription,
        steps: macroDescription.steps
            .reduce((newSteps, step, i) => {
                if (i < currentStepIndex) {
                    // Don't include the step because it's already done.
                    return newSteps;
                } else {
                    return [...newSteps, ...augmenter(macroDescription, [i, step], options)];
                }
            }, [])
            .concat([
                {
                    action: () => {
                        console.log("Tour done!");
                        pointerMethods.setState({ isVisible: false });
                    },
                },
            ]),
    };
}

/**
 * @param {*} param0
 * @returns {[state: { x, y, isVisible, position, content, mode, fixed }, methods: { update, setState }]}
 */
function createPointerState({ x, y, isVisible, position, content, mode, fixed }) {
    const state = reactive({ x, y, isVisible, position, content, mode, fixed });
    const pointerSize = { width: 28, height: 28 };
    let currentStep, currentAnchor;

    // TODO-JCB: Take into account the rtl config.
    function computeLocation(el, position) {
        let top, left;
        const rect = el.getBoundingClientRect();
        if (position == "top") {
            top = rect.top - pointerSize.height;
            left = rect.left + rect.width / 2 - pointerSize.width / 2;
        } else if (position == "bottom") {
            top = rect.top + rect.height;
            left = rect.left + rect.width / 2 - pointerSize.width / 2;
        } else if (position == "left") {
            top = rect.top + rect.height / 2 - pointerSize.height / 2;
            left = rect.left;
        } else if (position == "right") {
            top = rect.top + rect.height / 2 - pointerSize.height / 2;
            left = rect.left + rect.width;
        }
        return [top, left];
    }

    function updateOnIntersection(intersection) {
        if (currentStep) {
            update(intersection, currentStep, currentAnchor);
        }
    }

    function update(intersection, step, anchor) {
        if (anchor) {
            if (intersection.isIntersecting) {
                const [top, left] = computeLocation(anchor, step.position);
                setState({
                    x: left,
                    y: top,
                    content: step.content || "",
                    position: step.position,
                });
            } else {
                if (intersection.rootBounds) {
                    let x = intersection.rootBounds.width / 2;
                    let y, position, content;
                    const targetBounds = anchor.getBoundingClientRect();
                    if (targetBounds.bottom < intersection.rootBounds.height / 2) {
                        // the target is above the viewport
                        y = 80;
                        position = "bottom";
                        content = "Scroll up to reach the next step.";
                    } else if (targetBounds.top > intersection.rootBounds.height / 2) {
                        // the target is at the bottom of the viewport
                        y = intersection.rootBounds.height - 80 - 28;
                        position = "top";
                        content = "Scroll down to reach the next step.";
                    }
                    setState({ x, y, content, position });
                }
            }
        } else {
            setState({ isVisible: false });
        }
        currentStep = step;
        currentAnchor = anchor;
    }

    function setState(obj) {
        Object.assign(state, obj);
    }

    return [state, { update, setState, updateOnIntersection }];
}

function intersectionService() {
    let root, target, observer, _isIntersecting, _rootBounds;

    function observe(newTarget) {
        unobserve();
        if (newTarget && observer) {
            observer.observe(newTarget);
        }
        target = newTarget;
    }

    function unobserve() {
        if (target && observer) {
            observer.unobserve(target);
        }
        target = undefined;
    }

    function stop() {
        unobserve();
        if (observer) {
            observer.disconnect();
        }
        root = undefined;
        observer = undefined;
    }

    function start(startRoot, customCallback = () => {}) {
        root = startRoot;
        observer = new IntersectionObserver(
            (observations, _observer) => {
                for (const observation of observations) {
                    const { rootBounds } = observation;
                    _rootBounds = rootBounds;
                    if (rootBounds) {
                        _isIntersecting = observation.isIntersecting;
                        customCallback(intersection);
                    }
                }
            },
            { root }
        );
    }
    function set(elements) {
        let sameRoot = true,
            sameTarget = true;
        if ("root" in elements) {
            sameRoot = elements.root === root;
        }
        if ("target" in elements) {
            sameTarget = elements.target === target;
        }
        if (observer) {
            if (sameRoot) {
                if (sameTarget) {
                    // Do nothing
                } else {
                    observe(elements.target);
                }
            } else {
                root = newRoot;
                stop();
                start();
                if (sameTarget) {
                    observe(target);
                } else {
                    observe(elements.target);
                }
            }
        } else {
            root = newRoot;
            target = elements.target;
        }
    }
    const intersection = {
        start,
        stop,
        set,
        get isIntersecting() {
            return _isIntersecting;
        },
        get rootBounds() {
            return _rootBounds;
        },
    };
    return intersection;
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
        const intersection = intersectionService();

        const [pointerState, pointerMethods] = createPointerState({
            content: "",
            position: "top",
            x: 0,
            y: 0,
            isVisible: false,
            mode: "bubble",
            fixed: false,
        });

        intersection.start(null, pointerMethods.updateOnIntersection);

        /**
         * @param {string} tourName
         * @param {"auto" | "manual"} mode
         * @param {number} interval
         */
        function run(tourName, mode, interval) {
            const tourDesc = registry.category("tours").get(tourName);
            const currentStepIndex = parseInt(browser.localStorage.getItem(tourName) || 0);
            if (currentStepIndex >= tourDesc.steps.length) {
                // TODO-JCB: log something here?
                return;
            }

            const augmentedMacro = augmentMacro(
                Object.assign(tourDesc, { interval: mode === "manual" ? 0 : interval }),
                mode === "manual" ? augmentStepManual : augmentStepAuto,
                {
                    advance: () => macroEngine.advanceMacros(),
                    pointerMethods,
                    mode,
                    intersection,
                    currentStepIndex,
                }
            );

            // The pointer points to the trigger and waits for the user to do the action.
            macroEngine.activate(augmentedMacro);
        }

        registry.category("main_components").add("TourPointer", {
            Component: TourPointer,
            props: { pointerState, setPointerState: pointerMethods.setState },
        });

        return { run };
    },
};

registry.category("services").add("tour_service_x", tourService);
