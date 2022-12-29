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
        this.colorButton = {
            pending_approval: "btn-light border border-dark",
            approved: "btn-success",
            rejected: "btn-danger",
            changes_requested: "btn-warning",
            waiting_normal: "",
            waiting_approval: "border border-dark",
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
        if (["in_progress", "done", "waiting_normal"].includes(this.currentValue)) {
            return this.options_normal.filter(
                (o) =>
                    o !== this.currentValue || !["waiting_normal", "waiting_approval"].includes(o)
            );
        }
        return this.options_approval.filter(
            (o) => o !== this.currentValue || !["waiting_normal", "waiting_approval"].includes(o)
        );
    }

    get switchModeAvailableOptions() {
        if (["in_progress", "done", "waiting_normal"].includes(this.currentValue)) {
            return this.options_approval.filter(
                (o) => !["waiting_normal", "waiting_approval"].includes(o)
            );
        }
        return this.options_normal.filter(
            (o) => !["waiting_normal", "waiting_approval"].includes(o)
        );
    }

    _onClickModeSelection(arg1, arg2) {
        this.props.update(arg1);
        this.state.isStateButtonHighlighted = false;
        this.state.isStateBoxHighlighted = false;
        
    }

    /**
     * @param {MouseEvent} ev
     */
    onClickState(ev) {
        this.toggleState();
        //this.state.isStateButtonHighlighted = false;
        //this.state.isStateBoxHighlighted = false;
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
