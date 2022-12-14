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
 * @property {T[] | () => T[]} [stickyItems]
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
 * @param {UseVirtualOptions<T>} options
 * @returns {ReturnType<useState<T[]>>}
 */
export function useVirtual(options) {
    const { initialScrollTop, scrollableRef } = options;
    let { itemHeight, items, stickyItems, margin } = options;
    itemHeight = typeof itemHeight === "function" ? itemHeight : (_) => options.itemHeight;
    items = typeof items === "function" ? items : () => items;
    stickyItems = typeof stickyItems === "function" ? stickyItems : () => options.stickyItems || [];
    margin = typeof margin === "number" ? margin : options.margin || "100%";
    const current = {
        allItems: items(),
        scrollTop: initialScrollTop || 0,
    };

    const virtualItems = useState([]);
    function compute() {
        const { allItems, scrollTop } = current;
        const marginPixels = toPixels(margin);

        const vStart = scrollTop - marginPixels;
        const vEnd =
            scrollTop + (scrollableRef.el?.clientHeight || window.innerHeight) + marginPixels;

        let startIndex = 0;
        let endIndex = 0;
        let currentTop = 0;
        for (const item of allItems) {
            const size = toPixels(itemHeight(item));
            if (currentTop + size < vStart) {
                startIndex++;
                endIndex++;
            } else if (currentTop - size <= vEnd) {
                endIndex++;
            } else {
                break;
            }
            currentTop += size;
        }

        const prevItems = toRaw(virtualItems);
        const newItems = [...new Set([...allItems.slice(startIndex, endIndex), ...stickyItems()])];
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
