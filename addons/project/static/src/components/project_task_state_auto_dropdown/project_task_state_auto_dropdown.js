/** @odoo-module */

import { Dropdown } from "@web/core/dropdown/dropdown";

export class ProjectTaskStateAutoDropdown extends Dropdown {
    onTogglerMouseEnter() {
        if (!this.state.open) {
            this.togglerRef.el.focus();
            this.open();
        }
    }
}
