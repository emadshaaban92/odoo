/** @odoo-module */

import { Dropdown } from "@web/core/dropdown/dropdown";

export class ProjectTaskStateAutoDropdown extends Dropdown {
    onTogglerMouseEnter() {
        if (!this.state.open) {
            this.togglerRef.el.focus();
            this.open();
        }
    }
    onTogglerMouseLeave() {
        this.close();
    }
}

ProjectTaskStateAutoDropdown.template = "project.ProjectTaskStateAutoDropdown";

//registry.category("fields").add("project_task_state_selection", ProjectTaskStateSelection);