/** @odoo-module **/

import { onWillStart, reactive, useComponent, useEffect, useRef } from "@odoo/owl";
import { useThrottled } from "./utils/timing";

/**
 * @template T
 * @typedef UseVirtualOptions
 * @property {AcceptedPixelValue | (item: T) => AcceptedPixelValue} itemHeight
 * @property {() => T[]} getItems
 * @property {AcceptedPixelValue} [margin="100%"]
 * @property {number} [initialScrollTop]
 * @property {typeof useRef["name"]} [refName="virtual-zone"]
 */

/**
 * @typedef {number | `${string}px` | `${string}%`} AcceptedPixelValue
 */

/**
 * Converts a number,
 *
 * @param {AcceptedPixelValue} value
 * @param {number} base
 * @returns {number}
 */
const toPixels = (value, base) => {
    if (typeof value === "number") {
        return value;
    }
    if (value.endsWith("%")) {
        return base * (Number(value.slice(0, -1)) / 100);
    }
    if (value.endsWith("px")) {
        return Number(value.slice(0, -2));
    }
};

/**
 * Calculates the displayed items in a virtual list.
 *
 * @template T
 * @param {UseVirtualOptions<T>} param0
 * @returns {import("@odoo/owl").Reactive<T[]>}
 */
export function useVirtual({ itemHeight, getItems, margin, initialScrollTop, refName }) {
    margin = margin || "100%";
    const zoneRef = useRef(refName || "virtual-zone");

    const comp = useComponent();
    const throttledRender = useThrottled(() => comp.render(), 16 * 4);
    const displayedItems = reactive([], throttledRender);

    const throttledCompute = useThrottled(_compute, 16);
    const current = reactive(
        { items: getItems(), scrollTop: initialScrollTop || 0 },
        throttledCompute
    );

    onWillStart(() => throttledCompute());
    useEffect(
        (items) => {
            current.items = items;
        },
        () => [getItems()]
    );
    useEffect(
        (el) => {
            if (el) {
                const onScroll = (ev) => (current.scrollTop = ev.target.scrollTop);
                const scrollParent = el.parentElement;
                scrollParent.addEventListener("scroll", onScroll);
                return () => scrollParent.removeEventListener("scroll", onScroll);
            }
        },
        () => [zoneRef.el]
    );

    function _compute() {
        const { items, scrollTop } = current;
        const zone = zoneRef.el;
        const zoneHeight = zone?.parentElement.clientHeight || window.innerHeight;
        const marginPixels = toPixels(margin, zoneHeight);

        const vStart = scrollTop - marginPixels;
        const vEnd = scrollTop + zoneHeight + marginPixels;

        let startIndex = 0;
        let endIndex = 0;
        let currentTop = 0;
        for (const item of items) {
            if (currentTop < vStart) {
                startIndex++;
                endIndex++;
            } else if (currentTop <= vEnd) {
                endIndex++;
            } else {
                break;
            }
            const size = typeof itemHeight === "function" ? itemHeight(item) : itemHeight;
            currentTop += toPixels(size, zoneHeight);
        }

        const newItems = items.slice(startIndex, endIndex);
        displayedItems.length = 0;
        displayedItems.push(...newItems);
    }
    return displayedItems;
}
