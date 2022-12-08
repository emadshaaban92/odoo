/** @odoo-module **/

import { onWillUnmount, reactive, useEffect, useEnv, useExternalListener } from "@odoo/owl";
import { clamp } from "@web/core/utils/numbers";
import { camelToKebab } from "@web/core/utils/strings";
import { debounce, setRecurringAnimationFrame } from "@web/core/utils/timing";

/**
 * @typedef CleanupManager
 * @property {(cleanupFn: Function) => void} add
 * @property {() => void} cleanup
 */

/**
 * @typedef DOMHelpers
 * @property {(el: HTMLElement, ...classNames: string[]) => void} addClass
 * @property {(el: EventTarget, event: string, callback: (...args: any[]) => any, options?: boolean | Record<string, boolean>) => void} addListener
 * @property {(el: HTMLElement, style: Record<string, string | number>) => void} addStyle
 * @property {(el: HTMLElement, options?: { adjust?: boolean }) => DOMRect} getRect
 * @property {(el: HTMLElement, ...classNames: string[]) => void} removeClass
 */

/**
 * @typedef Position
 * @property {number} x
 * @property {number} y
 */

/**
 * @typedef EdgeScrollingOptions
 * @property {boolean} [enabled=true]
 * @property {number} [speed=10]
 * @property {number} [threshold=20]
 */

/**
 * @typedef DraggableBuilderParams
 *
 * Hook params
 * @property {string} [name="useAnonymousDraggable"]
 * @property {EdgeScrollingOptions} [edgeScrolling]
 * @property {Record<string, string[]>} [acceptedParams]
 * @property {Record<string, any>} [defaultParams]
 *
 * Build hooks
 * @property {(params: DraggableBuilderHookParams) => any} onComputeParams
 *
 * Runtime hooks
 * @property {(params: DraggableBuilderHookParams) => any} onDragStart
 * @property {(params: DraggableBuilderHookParams) => any} onDrag
 * @property {(params: DraggableBuilderHookParams) => any} onDragEnd
 * @property {(params: DraggableBuilderHookParams) => any} onDrop
 * @property {(params: DraggableBuilderHookParams) => any} onWillStartDrag
 */

/**
 * @typedef DraggableHookRunningContext
 * @property {{ el: HTMLElement | null }} ref
 * @property {string | null} [elementSelector=null]
 * @property {string | null} [ignoreSelector=null]
 * @property {string | null} [fullSelector=null]
 * @property {string | null} [cursor=null]
 * @property {HTMLElement | null} [currentContainer=null]
 * @property {DOMRect | null} [currentContainerRect=null]
 * @property {HTMLElement | null} [currentElement=null]
 * @property {DOMRect | null} [currentElementRect=null]
 * @property {HTMLElement | null} [scrollParent=null]
 * @property {boolean} [enabled=false]
 * @property {Position} [mouse={ x: 0, y: 0 }]
 * @property {Position} [offset={ x: 0, y: 0 }]
 * @property {EdgeScrollingOptions} [edgeScrolling]
 */

/**
 * @typedef {DOMHelpers & {
 *  ctx: DraggableHookRunningContext,
 *  callHandler(handlerName: string, arg: Record<any, any>): void,
 * }} DraggableBuilderHookParams
 */

const DEFAULT_ACCEPTED_PARAMS = {
    enable: ["boolean", "function"],
    ref: ["object"],
    elements: ["string"],
    handle: ["string", "function"],
    ignore: ["string", "function"],
    cursor: ["string"],
    edgeScrolling: ["object", "function"],
};
const DEFAULT_DEFAULT_PARAMS = {
    enable: true,
    edgeScrolling: {
        speed: 10,
        threshold: 30,
    },
};
const DRAGGED_CLASS = "o_dragged";
const LEFT_CLICK = 0;
const MANDATORY_PARAMS = ["ref", "elements"];

/**
 * Cache containing the elements in which an attribute has been modified by a hook.
 * It is global since multiple draggable hooks can interact with the same elements.
 * @type {Record<string, Set<HTMLElement>>}
 */
const elCache = {};

/**
 * Cancels the default behavior and propagation of a given event.
 * @param {Event} ev
 */
function cancelEvent(ev) {
    ev.stopPropagation();
    ev.stopImmediatePropagation();
    ev.preventDefault();
}

/**
 * @template T
 * @param {T | () => T} valueOrFn
 * @returns {T}
 */
function getReturnValue(valueOrFn) {
    if (typeof valueOrFn === "function") {
        return valueOrFn();
    }
    return valueOrFn;
}

/**
 * Returns the first scrollable parent of the given element (recursively), or null
 * if none is found. A 'scrollable' element is defined by 2 things:
 *
 * - for either in width or in height: the 'scroll' value is larger than the 'client'
 * value;
 *
 * - its computed 'overflow' property is set to either "auto" or "scroll"
 *
 * If both of these assertions are true, it means that the element can effectively
 * be scrolled on at least one axis.
 * @param {HTMLElement} el
 * @returns {HTMLElement | null}
 */
function getScrollParent(el) {
    if (!el) {
        return null;
    }
    if (el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight) {
        const overflow = getComputedStyle(el).getPropertyValue("overflow");
        if (/\bauto\b|\bscroll\b/.test(overflow)) {
            return el;
        }
    }
    return getScrollParent(el.parentElement);
}

/**
 * @param {Function} [defaultCleanupFn]
 * @returns {CleanupManager}
 */
function makeCleanupManager(defaultCleanupFn) {
    /**
     * Registers the given cleanup function to be called when cleaning up hooks.
     * @param {Function} [cleanupFn]
     */
    const add = (cleanupFn) => typeof cleanupFn === "function" && cleanups.push(cleanupFn);

    /**
     * Runs all cleanup functions while clearing the cleanups list.
     */
    const cleanup = () => {
        while (cleanups.length) {
            cleanups.pop()();
        }
        add(defaultCleanupFn);
    };

    const cleanups = [];

    add(defaultCleanupFn);

    return { add, cleanup };
}

/**
 * @param {CleanupManager} cleanup
 * @returns {DOMHelpers}
 */
function makeDOMHelpers(cleanup) {
    /**
     * @param {HTMLElement} el
     * @param  {...string} classNames
     */
    const addClass = (el, ...classNames) => {
        if (!el || !classNames.length) {
            return;
        }
        cleanup.add(saveAttribute(el, "class"));
        el.classList.add(...classNames);
    };

    /**
     * Adds an event listener to be cleaned up after the next drag sequence
     * has stopped. An additionnal `timeout` param allows the handler to be
     * delayed after a timeout.
     * @param {EventTarget} el
     * @param {string} event
     * @param {(...args: any[]) => any} callback
     * @param {boolean | Record<string, boolean>} [options]
     */
    const addListener = (el, event, callback, options) => {
        if (!el || !event || !callback) {
            return;
        }
        el.addEventListener(event, callback, options);
        if (/pointer|mouse/.test(event)) {
            // Restore pointer events on elements listening on mouse/pointer events.
            addStyle(el, { pointerEvents: "auto" });
        }
        cleanup.add(() => el.removeEventListener(event, callback, options));
    };

    /**
     * Adds style to an element to be cleaned up after the next drag sequence has
     * stopped.
     * @param {HTMLElement} el
     * @param {Record<string, string | number>} style
     */
    const addStyle = (el, style) => {
        if (!el || !style) {
            return;
        }
        cleanup.add(saveAttribute(el, "style"));
        for (const key in style) {
            const [value, priority] = String(style[key]).split(/\s*!\s*/);
            el.style.setProperty(camelToKebab(key), value, priority);
        }
    };

    /**
     * Returns the bounding rect of the given element. If the `adjust` option is set
     * to true, the rect will be reduced by the padding of the element.
     * @param {HTMLElement} el
     * @param {Object} [options={}]
     * @param {boolean} [options.adjust=false]
     * @returns {DOMRect}
     */
    const getRect = (el, options = {}) => {
        if (!el) {
            return {};
        }
        const rect = el.getBoundingClientRect();
        if (options.adjust) {
            const style = getComputedStyle(el);
            const [pl, pr, pt, pb] = [
                "padding-left",
                "padding-right",
                "padding-top",
                "padding-bottom",
            ].map((prop) => pixelValueToNumber(style.getPropertyValue(prop)));

            rect.x += pl;
            rect.y += pt;
            rect.width -= pl + pr;
            rect.height -= pt + pb;
        }
        return rect;
    };

    /**
     * @param {HTMLElement} el
     * @param  {...string} classNames
     */
    const removeClass = (el, ...classNames) => {
        if (!el || !classNames) {
            return;
        }
        cleanup.add(saveAttribute(el, "class"));
        el.classList.remove(...classNames);
    };

    return { addClass, addListener, addStyle, getRect, removeClass };
}

/**
 * Converts a CSS pixel value to a number, removing the 'px' part.
 * @param {string} val
 * @returns {number}
 */
function pixelValueToNumber(val) {
    return Number(val.endsWith("px") ? val.slice(0, -2) : val);
}

function saveAttribute(el, attribute) {
    const restoreAttribute = () => {
        cache.delete(el);
        if (originalValue) {
            el.setAttribute(attribute, originalValue);
        } else {
            el.removeAttribute(attribute);
        }
    };

    if (!(attribute in elCache)) {
        elCache[attribute] = new Set();
    }
    const cache = elCache[attribute];

    if (cache.has(el)) {
        return;
    }

    cache.add(el);
    const originalValue = el.getAttribute(attribute);

    return restoreAttribute;
}

/**
 * @param {DraggableBuilderParams} hookParams
 * @returns {(params: Record<any, any>) => { dragging: boolean }}
 */
export function makeDraggableHook(hookParams) {
    hookParams = getReturnValue(hookParams);

    const hookName = hookParams.name || "useAnonymousDraggable";
    const allAcceptedParams = { ...DEFAULT_ACCEPTED_PARAMS, ...hookParams.acceptedParams };
    const defaultParams = { ...DEFAULT_DEFAULT_PARAMS, ...hookParams.defaultParams };

    /**
     * @param {SortableParams} params
     * @returns {[string, string | boolean][]}
     */
    const computeParams = (params) => {
        const computedParams = { enable: true };
        for (const prop in allAcceptedParams) {
            if (prop in params) {
                computedParams[prop] = getReturnValue(params[prop]);
            }
        }
        return Object.entries(computedParams);
    };

    /**
     * Basic error builder for the hook.
     * @param {string} reason
     * @returns {Error}
     */
    const makeError = (reason) => new Error(`Error in hook ${hookName}: ${reason}.`);

    return {
        [hookName](params) {
            /**
             * Executes a handler from the `hookParams`.
             * @param {string} hookHandlerName
             * @param {Record<any, any>} arg
             */
            const callBuildHandler = (hookHandlerName, arg) => {
                if (typeof hookParams[hookHandlerName] !== "function") {
                    return;
                }
                const returnValue = hookParams[hookHandlerName]({ ctx, ...helpers, ...arg });
                if (returnValue) {
                    callHandler(hookHandlerName, returnValue);
                }
            };

            /**
             * Safely executes a handler from the `params`, so that the drag sequence can
             * be interrupted if an error occurs.
             * @param {string} handlerName
             * @param {Record<any, any>} arg
             */
            const callHandler = (handlerName, arg) => {
                if (typeof params[handlerName] !== "function") {
                    return;
                }
                try {
                    params[handlerName]({ ...dom, ...ctx.mouse, ...arg });
                } catch (err) {
                    dragEnd(true, true);
                    throw err;
                }
            };

            /**
             * Main entry function to start a drag sequence.
             */
            const dragStart = () => {
                state.dragging = true;

                // Compute scrollable parent
                ctx.scrollParent = getScrollParent(ctx.currentContainer);

                updateRects();
                const { x, y, width, height } = ctx.currentElementRect;

                // Adjusts the offset
                ctx.offset.x -= x;
                ctx.offset.y -= y;

                dom.addStyle(ctx.currentElement, {
                    width: `${width}px`,
                    height: `${height}px`,
                });

                // First adjustment
                updateElementPosition();

                dom.addStyle(document.body, {
                    pointerEvents: "none",
                    userSelect: "none",
                });
                if (ctx.cursor) {
                    dom.addStyle(document.body, { cursor: ctx.cursor });
                }

                if (ctx.scrollParent && ctx.edgeScrolling.enabled) {
                    const cleanupFn = setRecurringAnimationFrame(handleEdgeScrolling);
                    cleanup.add(cleanupFn);
                }

                dom.addClass(ctx.currentElement, DRAGGED_CLASS);

                callBuildHandler("onDragStart");
            };

            /**
             * Main exit function to stop a drag sequence. Note that it can be called
             * even if a drag sequence did not start yet to perform a cleanup of all
             * current context variables.
             * @param {boolean} cancelled
             * @param {boolean} [inErrorState] can be set to true when an error
             *  occurred to avoid falling into an infinite loop if the error
             *  originated from one of the handlers.
             */
            const dragEnd = (cancelled, inErrorState) => {
                if (state.dragging) {
                    if (!inErrorState) {
                        callBuildHandler("onDragEnd");
                        if (!cancelled && document.body.contains(ctx.currentElement)) {
                            callBuildHandler("onDrop");
                        }
                    }
                }

                cleanup.cleanup();
            };

            /**
             * Applies scroll to the container if the current element is near
             * the edge of the container.
             */
            const handleEdgeScrolling = (deltaTime) => {
                updateRects();
                const eRect = ctx.currentElementRect;
                const cRect = ctx.currentContainerRect;

                const { speed, threshold } = ctx.edgeScrolling;
                const correctedSpeed = (speed / 16) * deltaTime;
                const maxWidth = cRect.x + cRect.width;
                const maxHeight = cRect.y + cRect.height;

                const diff = {};

                if (eRect.x - cRect.x < threshold) {
                    diff.x = [eRect.x - cRect.x, -1];
                } else if (maxWidth - eRect.x - eRect.width < threshold) {
                    diff.x = [maxWidth - eRect.x - eRect.width, 1];
                }
                if (eRect.y - cRect.y < threshold) {
                    diff.y = [eRect.y - cRect.y, -1];
                } else if (maxHeight - eRect.y - eRect.height < threshold) {
                    diff.y = [maxHeight - eRect.y - eRect.height, 1];
                }

                if ((diff.x && diff.x[0]) || (diff.y && diff.y[0])) {
                    const diffToScroll = ([delta, sign]) =>
                        (1 - clamp(delta, 0, threshold) / threshold) * correctedSpeed * sign;
                    const scrollParams = {};
                    if (diff.x) {
                        scrollParams.left = diffToScroll(diff.x);
                    }
                    if (diff.y) {
                        scrollParams.top = diffToScroll(diff.y);
                    }
                    ctx.scrollParent.scrollBy(scrollParams);
                }
            };

            /**
             * Window "keydown" event handler.
             * @param {KeyboardEvent} ev
             */
            const onKeyDown = (ev) => {
                if (!ctx.enabled || !state.dragging) {
                    return;
                }
                switch (ev.key) {
                    case "Escape":
                    case "Tab": {
                        cancelEvent(ev);
                        dragEnd(true);
                    }
                }
            };

            /**
             * Global (= ref) "mousedown" event handler.
             * @param {MouseEvent} ev
             */
            const onMouseDown = (ev) => {
                updateMousePosition(ev);

                // A drag sequence can still be in progress if the mouseup occurred
                // outside of the window.
                dragEnd(true);

                if (
                    ev.button !== LEFT_CLICK ||
                    !ctx.enabled ||
                    !ev.target.closest(ctx.fullSelector) ||
                    (ctx.ignoreSelector && ev.target.closest(ctx.ignoreSelector))
                ) {
                    return;
                }

                ctx.currentContainer = ctx.ref.el;
                ctx.currentElement = ev.target.closest(ctx.elementSelector);

                Object.assign(ctx.offset, ctx.mouse);

                cleanup.add(() => {
                    ctx.currentContainer = null;
                    ctx.currentContainerRect = null;
                    ctx.currentElement = null;
                    ctx.currentElementRect = null;
                    ctx.scrollParent = null;
                });

                callBuildHandler("onWillStartDrag");
            };

            /**
             * Window "mousemove" event handler.
             * @param {MouseEvent} ev
             */
            const onMouseMove = (ev) => {
                updateMousePosition(ev);

                if (!ctx.enabled || !ctx.currentElement) {
                    return;
                }
                if (state.dragging) {
                    updateElementPosition();
                    callBuildHandler("onDrag");
                } else {
                    dragStart();
                }
            };

            /**
             * Window "mouseup" event handler.
             * @param {MouseEvent} ev
             */
            const onMouseUp = (ev) => {
                updateMousePosition(ev);
                dragEnd(false);
            };

            /**
             * Updates the position of the current dragged element according to
             * the current mouse position.
             */
            const updateElementPosition = () => {
                const { width: ew, height: eh } = ctx.currentElementRect;
                const { x: cx, y: cy, width: cw, height: ch } = ctx.currentContainerRect;

                // Updates the position of the dragged element.
                dom.addStyle(ctx.currentElement, {
                    left: `${clamp(ctx.mouse.x - ctx.offset.x, cx, cx + cw - ew)}px`,
                    top: `${clamp(ctx.mouse.y - ctx.offset.y, cy, cy + ch - eh)}px`,
                });
            };

            /**
             * Updates the current mouse position from a given event.
             * @param {MouseEvent} ev
             */
            const updateMousePosition = (ev) => {
                ctx.mouse.x = ev.clientX;
                ctx.mouse.y = ev.clientY;
            };

            const updateRects = () => {
                // Container rect
                ctx.currentContainerRect = dom.getRect(ctx.currentContainer, { adjust: true });
                if (ctx.scrollParent) {
                    // Adjust container rect according to scrollparent
                    const parentRect = dom.getRect(ctx.scrollParent, { adjust: true });
                    ctx.currentContainerRect.x = Math.max(ctx.currentContainerRect.x, parentRect.x);
                    ctx.currentContainerRect.y = Math.max(ctx.currentContainerRect.y, parentRect.y);
                    ctx.currentContainerRect.width = Math.min(
                        ctx.currentContainerRect.width,
                        parentRect.width
                    );
                    ctx.currentContainerRect.height = Math.min(
                        ctx.currentContainerRect.height,
                        parentRect.height
                    );
                }

                // Element rect
                ctx.currentElementRect = dom.getRect(ctx.currentElement);
            };

            // Initialize helpers
            const cleanup = makeCleanupManager(() => (state.dragging = false));
            const effectCleanup = makeCleanupManager();
            const dom = makeDOMHelpers(cleanup);

            const helpers = {
                ...dom,
                addCleanup: cleanup.add,
                addEffectCleanup: effectCleanup.add,
                callHandler,
            };

            // Component infos
            const env = useEnv();
            const state = reactive({ dragging: false });

            // Basic error handling asserting that the parameters are valid.
            for (const prop in allAcceptedParams) {
                if (params[prop] && !allAcceptedParams[prop].includes(typeof params[prop])) {
                    throw makeError(`invalid type for property "${prop}" in parameters`);
                } else if (!params[prop] && MANDATORY_PARAMS.includes(prop)) {
                    throw makeError(`missing required property "${prop}" in parameters`);
                }
            }

            /** @type {DraggableHookRunningContext} */
            const ctx = {
                ref: params.ref,
                ignoreSelector: null,
                fullSelector: null,
                cursor: null,
                currentContainer: null,
                currentContainerRect: null,
                currentElement: null,
                currentElementRect: null,
                scrollParent: null,
                enabled: false,
                mouse: { x: 0, y: 0 },
                offset: { x: 0, y: 0 },
                edgeScrolling: { enabled: true },
                get dragging() {
                    return state.dragging;
                },
            };

            // Effect depending on the params to update them.
            useEffect(
                (...deps) => {
                    const actualParams = { ...defaultParams, ...Object.fromEntries(deps) };
                    ctx.enabled = Boolean(ctx.ref.el && !env.isSmall && actualParams.enable);
                    if (!ctx.enabled) {
                        return;
                    }

                    // Selectors
                    ctx.elementSelector = actualParams.elements;
                    if (!ctx.elementSelector) {
                        throw makeError(
                            `no value found by "elements" selector: ${ctx.elementSelector}`
                        );
                    }
                    const allSelectors = [ctx.elementSelector];
                    ctx.cursor = actualParams.cursor || null;
                    if (actualParams.handle) {
                        allSelectors.push(actualParams.handle);
                    }
                    if (actualParams.ignore) {
                        ctx.ignoreSelector = actualParams.ignore;
                    }
                    ctx.fullSelector = allSelectors.join(" ");

                    Object.assign(ctx.edgeScrolling, actualParams.edgeScrolling);

                    callBuildHandler("onComputeParams", { params: actualParams });

                    /**
                     * Stops any drag sequence and calls effect cleanup functions when
                     * preparing to re-render.
                     */
                    return effectCleanup.cleanup;
                },
                () => computeParams(params)
            );
            // Effect depending on the `ref.el` to add triggering mouse events listener.
            useEffect(
                (el) => {
                    if (el) {
                        el.addEventListener("mousedown", onMouseDown);
                        return () => el.removeEventListener("mousedown", onMouseDown);
                    }
                },
                () => [ctx.ref.el]
            );
            // Other global mouse event listeners.
            const debouncedOnMouseMove = debounce(onMouseMove, "animationFrame", true);
            useExternalListener(window, "mousemove", debouncedOnMouseMove);
            useExternalListener(window, "mouseup", onMouseUp);
            useExternalListener(window, "keydown", onKeyDown, true);
            onWillUnmount(() => dragEnd(true));

            return state;
        },
    }[hookName];
}
