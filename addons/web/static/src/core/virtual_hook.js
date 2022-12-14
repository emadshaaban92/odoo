/** @odoo-module **/

import { onWillRender, onWillStart, toRaw, useEffect, useState } from "@odoo/owl";
import { shallowEqual } from "./utils/arrays";
import { throttleForAnimation } from "./utils/timing";

/**
 * @template T
 * @typedef VirtualHookParams
 * @property {T[] | () => T[]} items
 * @property {PixelValue | (item: T) => PixelValue} itemHeight
 * @property {typeof useRef} scrollableRef
 * @property {number} [initialScrollTop=0]
 * @property {PixelValue} [margin="100%"]
 */

/** @typedef {number | `${string}px` | `${string}%`} PixelValue */

/**
 * Converts a number,
 *
 * @param {PixelValue} value
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
 * @param {VirtualHookParams<T>} params
 * @returns {ReturnType<useState<T>>}
 */
export function useVirtual({ items, itemHeight, scrollableRef, initialScrollTop, margin }) {
    const computeVirtualItems = () => {
        const { items, scrollTop } = current;
        const marginPixels = toPixels(marginPx);

        const vStart = scrollTop - marginPixels;
        const vEnd =
            scrollTop + (scrollableRef.el?.clientHeight || window.innerHeight) + marginPixels;

        let startIndex = 0;
        let endIndex = 0;
        let currentTop = 0;
        for (const item of items) {
            const size = toPixels(getItemHeight(item));
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
        const newItems = items.slice(startIndex, endIndex);

        if (!shallowEqual(prevItems, newItems)) {
            virtualItems.length = 0;
            virtualItems.push(...newItems);
        }
    };

    const getItems = typeof items === "function" ? items : () => items;

    const getItemHeight = typeof itemHeight === "function" ? itemHeight : () => itemHeight;

    const marginPx = toPixels(typeof margin === "number" ? margin : margin || "100%");
    const current = {
        items: getItems(),
        scrollTop: initialScrollTop || 0,
    };

    const virtualItems = useState([]);

    onWillStart(computeVirtualItems);
    onWillRender(() => {
        const previousItems = current.items;
        current.items = getItems();
        if (!shallowEqual(previousItems, current.items)) {
            computeVirtualItems();
        }
    });
    const throttledOnScroll = throttleForAnimation((/** @type {Event} */ ev) => {
        current.scrollTop = ev.target.scrollTop;
        computeVirtualItems();
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
