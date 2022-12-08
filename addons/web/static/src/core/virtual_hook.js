/** @odoo-module **/

import { onWillRender, onWillStart, toRaw, useEffect, useState } from "@odoo/owl";
import { shallowEqual } from "./utils/arrays";
import { throttleForAnimation } from "./utils/timing";

/**
 * @template T
 * @typedef UseVirtualOptions
 * @property {typeof useRef} scrollableRef
 * @property {T[] | () => T[]} items
 * @property {AcceptedPixelValue | (item: T) => AcceptedPixelValue} itemHeight
 * @property {AcceptedPixelValue} [margin="100%"]
 * @property {number} [initialScrollTop=0]
 */

/**
 * @typedef {number | `${string}px` | `${string}%`} AcceptedPixelValue
 */

/**
 * Converts a number,
 *
 * @param {AcceptedPixelValue} value
 * @returns {number}
 */
const toPixels = (value) => {
    if (typeof value === "number") {
        return value;
    }
    if (value.endsWith("%")) {
        return window.innerHeight * (Number(value.slice(0, -1)) / 100);
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
 * @returns {ReturnType<useState<T[]>>}
 */
export function useVirtual({ itemHeight, items, margin, initialScrollTop, scrollableRef }) {
    itemHeight = typeof itemHeight === "function" ? itemHeight : (_) => itemHeight;
    items = typeof items === "function" ? items : () => items;
    margin = typeof margin === "number" ? margin : margin || "100%";
    const current = {
        allItems: items(),
        scrollTop: initialScrollTop || 0,
    };

    const virtualItems = useState([]);
    function compute() {
        const { allItems, scrollTop } = current;
        const marginPixels = toPixels(margin);

        const vStart = scrollTop - marginPixels;
        const vEnd = scrollTop + window.innerHeight + marginPixels;

        let startIndex = 0;
        let endIndex = 0;
        let currentTop = 0;
        for (const item of allItems) {
            if (currentTop < vStart) {
                startIndex++;
                endIndex++;
            } else if (currentTop <= vEnd) {
                endIndex++;
            } else {
                break;
            }
            const size = itemHeight(item);
            currentTop += toPixels(size);
        }

        const prevItems = toRaw(virtualItems);
        const newItems = allItems.slice(startIndex, endIndex);
        if (!shallowEqual(prevItems, newItems)) {
            virtualItems.length = 0;
            virtualItems.push(...newItems);
        }
    }

    onWillStart(compute);
    onWillRender(() => {
        const allItems = items();
        if (!shallowEqual(current.allItems, allItems)) {
            current.allItems = allItems;
            compute();
        }
    });
    const throttledOnScroll = throttleForAnimation((ev) => {
        current.scrollTop = ev.target.scrollTop;
        compute();
    });
    useEffect(
        (el) => {
            if (el) {
                el.addEventListener("scroll", throttledOnScroll);
                return () => el.removeEventListener("scroll", throttledOnScroll);
            }
        },
        () => [scrollableRef.el]
    );

    return virtualItems;
}
