/** @odoo-module */

import { throttleForAnimation } from "./utils/timing";

import { onWillUnmount, useEffect, useExternalListener, useRef } from "@odoo/owl";

/**
 * @typedef {{
 *  popper?: string;
 *  container?: HTMLElement;
 *  margin?: number;
 *  position?: Direction | Position;
 *  onPositioned?: (popperElement: HTMLElement, solution: PositioningSolution) => void;
 * }} Options
 *
 * @typedef {keyof DirectionsData} DirectionsDataKey
 * @typedef {{
 *  t: number;
 *  b: number;
 *  l: number;
 *  r: number;
 * }} DirectionsData
 *
 * @typedef {keyof VariantsData} VariantsDataKey
 * @typedef {{
 *  vs: number;
 *  vm: number;
 *  ve: number;
 *  hs: number;
 *  hm: number;
 *  he: number;
 * }} VariantsData
 *
 * @typedef {"top" | "left" | "bottom" | "right"} Direction
 * @typedef {"start" | "middle" | "end"} Variant
 *
 * @typedef {{[direction in Direction]: string}} DirectionFlipOrder
 *  values are successive DirectionsDataKey represented as a single string
 *
 * @typedef {{[variant in Variant]: string}} VariantFlipOrder
 *  values are successive VariantsDataKey represented as a single string
 *
 * @typedef {`${Direction}-${Variant}`} Position
 *
 * @typedef {{
 *  top: number,
 *  left: number,
 *  direction: Direction,
 *  variant: Variant,
 * }} PositioningSolution
 */

/** @type {{[d: string]: Direction}} */
const DIRECTIONS = { t: "top", r: "right", b: "bottom", l: "left" };
/** @type {{[v: string]: Variant}} */
const VARIANTS = { s: "start", m: "middle", e: "end" };
/** @type DirectionFlipOrder */
const DIRECTION_FLIP_ORDER = { top: "tbrl", right: "rltb", bottom: "btrl", left: "lrbt" };
/** @type VariantFlipOrder */
const VARIANT_FLIP_ORDER = { start: "sme", middle: "mse", end: "ems" };

/** @type {Options} */
const DEFAULTS = {
    popper: "popper",
    margin: 0,
    position: "bottom",
};

/**
 * Returns the best positioning solution staying in the container or falls back
 * to the requested position.
 * The positioning data used to determine each possible position is based on
 * the reference, popper, and container sizes.
 * Particularly, a popper must not overflow the container in any direction,
 * it should actually stay at `margin` distance from the border to look good.
 *
 * @param {HTMLElement} reference
 * @param {HTMLElement} popper
 * @param {Options} options
 * @returns {PositioningSolution} the best positioning solution
 */
function getBestPosition(reference, popper, { container, margin, position }) {
    // Retrieve directions and variants
    const [directionKey, variantKey = "middle"] = position.split("-");
    const directions = DIRECTION_FLIP_ORDER[directionKey];
    const variants = VARIANT_FLIP_ORDER[variantKey];

    // Boxes
    const popBox = popper.getBoundingClientRect();
    const refBox = reference.getBoundingClientRect();
    const contBox = container.getBoundingClientRect();

    const containerIsHTMLNode = container === document.firstElementChild;

    // Compute positioning data
    /** @type {DirectionsData} */
    const directionsData = {
        t: refBox.top - popBox.height - margin,
        b: refBox.bottom + margin,
        r: refBox.right + margin,
        l: refBox.left - popBox.width - margin,
    };
    /** @type {VariantsData} */
    const variantsData = {
        vs: refBox.left,
        vm: refBox.left + refBox.width / 2 + -popBox.width / 2,
        ve: refBox.right - popBox.width,
        hs: refBox.top,
        hm: refBox.top + refBox.height / 2 + -popBox.height / 2,
        he: refBox.bottom - popBox.height,
    };

    function getPositioningData(d = directions[0], v = variants[0], containerRestricted = false) {
        const vertical = ["t", "b"].includes(d);
        const variantPrefix = vertical ? "v" : "h";
        const directionValue = directionsData[d];
        const variantValue = variantsData[variantPrefix + v];

        let correctionMin = 0;
        let correctionMax = 0;
        if (containerRestricted) {
            const [directionSize, variantSize] = vertical
                ? [popBox.height + margin, popBox.width]
                : [popBox.width, popBox.height + margin];
            let [directionMin, directionMax] = vertical
                ? [contBox.top, contBox.bottom]
                : [contBox.left, contBox.right];
            let [variantMin, variantMax] = vertical
                ? [contBox.left, contBox.right]
                : [contBox.top, contBox.bottom];

            if (containerIsHTMLNode) {
                if (vertical) {
                    directionMin += container.scrollTop;
                    directionMax += container.scrollTop;
                } else {
                    variantMin += container.scrollTop;
                    variantMax += container.scrollTop;
                }
            }
            // Abort if outside container boundaries
            const directionOverflowMin = Math.floor(directionMin) - Math.ceil(directionValue);
            const directionOverflowMax = Math.floor(directionValue + directionSize) - Math.ceil(directionMax);
            const variantOverflowMin = Math.floor(variantMin) - Math.ceil(variantValue);
            const variantOverflowMax = Math.floor(variantValue + variantSize) - Math.ceil(variantMax);

            const directionOverflow = directionOverflowMin > 0 || directionOverflowMax > 0;
            const variantOverflow = variantOverflowMin > 0 || variantOverflowMax > 0;
            const overflow = variantOverflow || directionOverflow;

            // TODO don't try to fit if the ref isn't even displayed (completely?)
            //const refInCont = Math.floor(directionMin) < Math.ceil();
            if (overflow) {
                const variantWouldFit = Math.ceil(variantMax) - Math.floor(variantMin) >= Math.floor(variantSize);
                if (!directionOverflow && variantWouldFit) {
                    if (variantOverflowMin > 0) {
                        correctionMin = variantOverflowMin;
                    } else if (variantOverflowMax > 0) {
                        correctionMax = variantOverflowMax;
                    }
                } else {
                    return null;
                }
            }
        }

        const positioning = vertical
            ? {
                  top: directionValue,
                  left: variantValue + correctionMin - correctionMax,
              }
            : {
                  top: variantValue + correctionMin - correctionMax,
                  left: directionValue,
              };
        return {
            ...positioning,
            direction: DIRECTIONS[d],
            variant: VARIANTS[v],
            isPerfectFit: !(correctionMin || correctionMax),
        };
    }

    // Find a solution, prefer perfect fit
    let okMatches = [];
    for (const d of directions) {
        for (const v of variants) {
            const match = getPositioningData(d, v, true);
            if (match && match.isPerfectFit) {
                // Perfect match has been found.
                return match;
            } else if (match) {
                okMatches.push(match);
            }
        }
    }
    // Fallback on a position that fits the screen but not at any fixed point
    if (okMatches.length) {
        return okMatches[0];
    }
    // Fallback to default position if no best solution found
    return getPositioningData();
}

/**
 * This method will try to position the popper as requested (according to options).
 * If the requested position does not fit the container, other positions will be
 * tried in different direction and variant flip orders (depending on the requested position).
 * If no position is found that fits the container, the requested position stays used.
 *
 * When the final position is applied, a corresponding CSS class is also added to the popper.
 * This could be used to further styling.
 *
 * @param {HTMLElement} reference
 * @param {HTMLElement} popper
 * @param {Options} options
 */
export function reposition(reference, popper, options) {
    options = {
        container: document.documentElement,
        ...options,
    };

    // Reset popper style
    popper.style.position = "fixed";
    popper.style.top = "0px";
    popper.style.left = "0px";

    // Get best positioning solution and apply it
    const position = getBestPosition(reference, popper, options);
    const { top, left } = position;
    popper.style.top = `${top}px`;
    popper.style.left = `${left}px`;
    if (options.onPositioned) {
        options.onPositioned(popper, position);
    }
}

/**
 * Makes sure that the `popper` element is always
 * placed at `position` from the `reference` element.
 * If doing so the `popper` element is clipped off `container`,
 * sensible fallback positions are tried.
 * If all of fallback positions are also clipped off `container`,
 * the original position is used.
 *
 * Note: The popper element should be indicated in your template with a t-ref reference.
 *       This could be customized with the `popper` option.
 *
 * @param {HTMLElement | (()=>HTMLElement)} reference
 * @param {Options} options
 */
export function usePosition(reference, options) {
    options = { ...DEFAULTS, ...options };
    const { popper } = options;
    const popperRef = useRef(popper);
    const getReference = reference instanceof HTMLElement ? () => reference : reference;
    const update = () => {
        const ref = getReference();
        if (popperRef.el && ref) {
            reposition(ref, popperRef.el, options);
        }
    };
    useEffect(update);
    const throttledUpdate = throttleForAnimation(update);
    useExternalListener(document, "scroll", throttledUpdate, { capture: true });
    useExternalListener(window, "resize", throttledUpdate);
    onWillUnmount(throttledUpdate.cancel);
}
