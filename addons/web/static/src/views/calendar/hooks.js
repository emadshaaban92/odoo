/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { browser } from "@web/core/browser/browser";
import { usePopover } from "@web/core/popover/popover_hook";
import { useService } from "@web/core/utils/hooks";

import { onMounted, onPatched, onWillStart, onWillUnmount, useComponent, useRef } from "@odoo/owl";

export function useCalendarPopover(component) {
    const owner = useComponent();
    const popover = usePopover();
    const dialog = useService("dialog");
    let remove = null;
    function close() {
        if (remove) {
            remove();
            remove = null;
        }
    }
    return {
        close,
        open(target, props, popoverClass) {
            close();
            if (owner.env.isSmall) {
                remove = dialog.add(component, props, { onClose: () => (remove = null) });
            } else {
                remove = popover.add(target, component, props, {
                    popoverClass,
                    position: "right",
                    onClose: () => (remove = null),
                });
            }
        },
    };
}

export function useClickHandler(singleClickCb, doubleClickCb) {
    const component = useComponent();
    let clickTimeoutId = null;
    return function handle(...args) {
        if (clickTimeoutId) {
            doubleClickCb.call(component, ...args);
            browser.clearTimeout(clickTimeoutId);
            clickTimeoutId = null;
        } else {
            clickTimeoutId = browser.setTimeout(() => {
                singleClickCb.call(component, ...args);
                clickTimeoutId = null;
            }, 250);
        }
    };
}

export function useFullCalendar(refName, params) {
    const component = useComponent();
    const ref = useRef(refName);
    let instance = null;

    function boundParams() {
        const newParams = {};
        for (const key in params) {
            const value = params[key];
            newParams[key] = typeof value === "function" ? value.bind(component) : value;
        }
        return newParams;
    }

    async function loadJsFiles() {
        const files = [
            "/web/static/lib/fullcalendar/core/index.global.js",
            "/web/static/lib/fullcalendar/interaction/index.global.js",
            "/web/static/lib/fullcalendar/daygrid/index.global.js",
            "/web/static/lib/fullcalendar/timegrid/index.global.js",
            "/web/static/lib/fullcalendar/list/index.global.js",
            "/web/static/lib/fullcalendar/luxon2/index.global.js",
        ];
        for (const file of files) {
            await loadJS(file);
        }
    }

    onWillStart(() => loadJsFiles());

    onMounted(() => {
        // try {
        instance = new FullCalendar.Calendar(ref.el, boundParams());
        instance.render();
        // } catch (e) {
        //     throw new Error(`Cannot instantiate FullCalendar\n${e.message}`);
        // }
    });
    onPatched(() => {
        instance.refetchEvents();
    });
    onWillUnmount(() => {
        instance.destroy();
    });

    return {
        get api() {
            return instance;
        },
        get el() {
            return ref.el;
        },
    };
}
