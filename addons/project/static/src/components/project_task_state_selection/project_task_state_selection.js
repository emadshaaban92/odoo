/** @odoo-module */

import { StateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";

export class ProjectTaskStateSelection extends StateSelectionField {
    setup() {
        this.icons = {
            in_progress: "fa fa-fw fa-check-circle-o",
            done: "fa fa-fw fa-check-circle",
            pending_approval: "o_status",
            approved: "o_status o_status_green",
            rejected: "o_status o_status_red",
            changes_requested: "fa fa-exclamation-circle",
            waiting_normal: "fa fa-fw fa-hourglass-o",
            waiting_approval: "fa fa-fw fa-hourglass-o",
        };
        this.colorIcons = {
            in_progress: "",
            done: "text-success",
            pending_approval: "",
            approved: "text-success",
            rejected: "text-danger",
            changes_requested: "text-warning",
            waiting_normal: "",
            waiting_approval: "",
        };
        if (this.props.record.activeFields[this.props.name].viewType !== "form") {
            super.setup();
        }
    }

    get options() {
        return [
            ["pending_approval", this.env._t("Pending Approval")],
            ["approved", this.env._t("Approved")],  //exemple trad
            ["rejected", this.env._t("Rejected")],
            ["changes_requested", this.env._t("Request Changes")],
        ];
    }

    get isApproval() {
        return [
            "pending_approval",
            "approved",
            "rejected",
            "changes_requested",
            "waiting_approval",
        ].includes(this.currentValue);
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
        if (this.props.record.activeFields[this.props.name].viewType == "list") {
            await this.props.record.model.root.load();
            this.props.record.model.notify();
        }
    }

    async onSelectedDD(option) {
        //console.log(option);
        //console.log("onSelected");
        //this.props.update(option);
        await this.props.update(option[0]);
        if (this.props.record.activeFields[this.props.name].viewType == "list") {
            await this.props.record.model.root.load();
            this.props.record.model.notify();
        }
    }
}

ProjectTaskStateSelection.template = "project.ProjectTaskStateSelection";

registry.category("fields").add("project_task_state_selection", ProjectTaskStateSelection);