/** @odoo-module */

import { ProjectTaskStateSelection } from "../project_task_state_selection/project_task_state_selection";
import { ProjectTaskStateAutoDropdown } from "../project_task_state_auto_dropdown/project_task_state_auto_dropdown";

import { registry } from "@web/core/registry";

const { useState } = owl;

export class ProjectTaskStateSelectionForm extends ProjectTaskStateSelection {
    setup() {
        super.setup();
        this.state = useState({
            isStateButtonHighlighted: false,
            isStateBoxHighlighted: false,
            isModeSelectionHighlighted: false,
        });
        this.markAsDoneText = "In Progress";
        this.icons = {
            in_progress: "fa fa-check-square-o",
            done: "fa fa-check-square",
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
        this.colorButton = {
            pending_approval: "btn-light border border-dark",
            approved: "btn-success",
            rejected: "btn-danger",
            changes_requested: "btn-warning",
            waiting: "btn-warning",
        };
    }

    get options_approval() {
        return [
            ["pending_approval", "Pending Approval"],
            ["approved", "Approved"],
            ["rejected", "Rejected"],
            ["changes_requested", "Request Changes"],
        ];
    }

    get options_normal() {
        return [
            ["in_progress", "In Progress"],
            ["done", "Done"],
        ];
    }

    get availableOptions() {
        if (["in_progress", "done"].includes(this.currentValue)) {
            return this.options_normal.filter((o) => o !== this.currentValue || o !== "waiting");
        }
        return this.options_approval.filter((o) => o !== this.currentValue || o !== "waiting");
    }

    get switchModeAvailableOptions() {
        if (["in_progress", "done"].includes(this.currentValue)) {
            return this.options_approval.filter((o) => o !== "waiting");
        }
        return this.options_normal.filter((o) => o !== "waiting");
    }

    markAsUndone() {
        return this.env._t("Undone");
    }

    doneText() {
        return this.env._t("Done");
    }

    /**
     * @param {MouseEvent} ev
     */
    onClickState(ev) {
        this.toggleState();
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseEnterStateBox(ev) {
        this.state.isStateBoxHighlighted = true;
    }
    /**
     * @param {MouseEvent} ev
     */
    onMouseLeaveStateBox(ev) {
        this.state.isStateBoxHighlighted = false;
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseEnterStateButton(ev) {
        this.state.isStateButtonHighlighted = true;
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseLeaveStateButton(ev) {
        this.state.isStateButtonHighlighted = false;
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseEnterModeSelection(ev) {
        this.state.isModeSelectionHighlighted = true;
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseLeaveModeSelection(ev) {
        this.state.isModeSelectionHighlighted = false;
    }
}

ProjectTaskStateSelectionForm.template = "project.ProjectTaskStateSelectionForm";
ProjectTaskStateSelectionForm.components = {
    ...ProjectTaskStateSelectionForm.components,
    ProjectTaskStateAutoDropdown,
};
registry.category("fields").add("project_task_state_selection_form", ProjectTaskStateSelectionForm);
