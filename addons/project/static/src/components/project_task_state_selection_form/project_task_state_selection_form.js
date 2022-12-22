/** @odoo-module */

import { StateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { useState } = owl;

export class ProjectTaskStateSelectionForm extends StateSelectionField {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            isStateButtonHighlighted: false,
            isStateBoxHighlighted: false,
            isModeSelectionHighlighted: false
        });
        this.markAsDoneText = 'In Progress';
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
            waiting: "",
        }
        this.isStateButtonHighlighted
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
        return this.props.record.data.state_approval_mode;
    }

    async onSelectedDD(option) {
        await this.props.update(option);
        await this.props.record.model.root.load();
        this.props.record.model.notify();
    }

    onExternalButtonCLick0() {
        console.log("external click");
    }

    stateIcon(value) {
        const fut = this.icons[value] || "";
        return fut;
    }


    stateColor(value) {
        return this.colorIcons[value] || "";
    }

    markAsUndone() {
        return this.env._t("Undone");
    }

    doneText() {
        return this.env._t("Done");
    }

    async toggleState() {
        const toggleVal = this.props.value == "done" ? "in_progress" : "done";
        await this.props.update(toggleVal);

    }

    /**
     * @param {MouseEvent} ev
     */
    onClickState(ev) {
        this.toggleState()
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseEnterStateBox(ev) {

        this.state.isStateBoxHighlighted = true ;
    }
    /**
     * @param {MouseEvent} ev
     */
    onMouseLeaveStateBox(ev) {

        this.state.isStateBoxHighlighted = false ;
    }
    
    /**
     * @param {MouseEvent} ev
     */
    onMouseEnterStateButton(ev) {

        this.state.isStateButtonHighlighted = true ;
    }

    /**
     * @param {MouseEvent} ev
     */
    onMouseLeaveStateButton(ev) {

        this.state.isStateButtonHighlighted = false ;
        
    }

     /**
     * @param {MouseEvent} ev
     */
     onMouseEnterModeSelection(ev) {

        this.state.isModeSelectionHighlighted = true ;
    }

     /**
     * @param {MouseEvent} ev
     */
     onMouseLeaveModeSelection(ev) {

        this.state.isModeSelectionHighlighted = false ;
    }


}

ProjectTaskStateSelectionForm.template = "project.ProjectTaskStateSelectionForm";

registry.category("fields").add("project_task_state_selection_form", ProjectTaskStateSelectionForm);
