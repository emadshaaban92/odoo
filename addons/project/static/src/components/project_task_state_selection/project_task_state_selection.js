/** @odoo-module */

import { StateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { EventBus , useBus } = owl;

export class ProjectTaskStateSelection extends StateSelectionField {
    setup() {
        this.icons = {
            in_progress: "fa fa-check-circle-o",
            done: "fa fa-check-circle",
            pending_approval: "o_status",
            approved: "o_status o_status_green",
            rejected: "o_status o_status_red",
            changes_requested: "fa fa-repeat",
            waiting: "fa fa-hourglass-o",
        };
        this.colorIcons = {
            in_progress: "",
            done: "text-success",
            pending_approval: "",
            approved: "text-success",
            rejected: "text-danger",
            changes_requested: "text-warning",
            waiting: "",
        };
        if (this.props.record.activeFields[this.props.name].viewType !== "form") {
            super.setup();
        }
    }

    get options() {
        return [
            ["pending_approval", "Pending Approval"],
            ["approved", "Approved"],
            ["rejected", "Rejected"],
            ["changes_requested", "Request Changes"],
        ];
    }

    get isApproval() {
        return !["in_progress", "done"].includes(this.currentValue);
    }

    stateIcon(value) {
        return this.icons[value] || "";
    }

    stateColor(value) {
        return this.colorIcons[value] || "";
    }

    async toggleState() {
        const toggleVal = this.props.value == "done" ? "in_progress" : "done";
        await this.props.update(toggleVal);
    }
}

ProjectTaskStateSelection.template = "project.ProjectTaskStateSelection";

registry.category("fields").add("project_task_state_selection", ProjectTaskStateSelection);