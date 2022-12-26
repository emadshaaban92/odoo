/** @odoo-module */

import { Dropdown } from "@web/core/dropdown/dropdown";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { EventBus , useBus } = owl;

export class ProjectTaskStateAutoDropdown extends Dropdown {
    onTogglerMouseEnter() {
        if (!this.state.open) {
            this.togglerRef.el.focus();
            this.open();
        }
    }
}

registry.category("fields").add("project_task_state_auto_dropdown", ProjectTaskStateAutoDropdown);