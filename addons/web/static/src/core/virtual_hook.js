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
 * @property {T[] | () => T[]} [stickyItems]
 */

/** @typedef {number | `${string}px` | `${string}%`} PixelValue */

/**
 * @template T
 * @param {T[]} items
 * @param {T[]} stickyItems
 * @returns {T[]}
 */
const combineItems = (items, stickyItems) => [...new Set([...items, ...stickyItems])];

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
export function useVirtual({
    items,
    itemHeight,
    scrollableRef,
    initialScrollTop,
    margin,
    stickyItems,
}) {
    const computeVirtualItems = () => {
        const { items, stickyItems, scrollTop } = current;
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
        const newItems = combineItems(items.slice(startIndex, endIndex), stickyItems);

        if (!shallowEqual(prevItems, newItems)) {
            virtualItems.length = 0;
            virtualItems.push(...newItems);
        }
    };

    const getItems = typeof items === "function" ? items : () => items;

    const getItemHeight = typeof itemHeight === "function" ? itemHeight : () => itemHeight;

    const getStickyItems =
        typeof stickyItems === "function" ? stickyItems : () => stickyItems || [];

    const marginPx = toPixels(typeof margin === "number" ? margin : margin || "100%");
    const current = {
        items: getItems(),
        stickyItems: getStickyItems(),
        scrollTop: initialScrollTop || 0,
    };

    const virtualItems = useState([]);

    onWillStart(computeVirtualItems);
    onWillRender(() => {
        const prevItems = combineItems(current.items, current.stickyItems);
        current.items = getItems();
        current.stickyItems = getStickyItems();
        if (!shallowEqual(prevItems, combineItems(current.items, current.stickyItems))) {
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
