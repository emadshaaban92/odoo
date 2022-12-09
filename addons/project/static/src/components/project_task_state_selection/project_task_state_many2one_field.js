/** @odoo-module */

import { StateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ProjectTaskStateSelectionMany2One extends StateSelectionField {
    setup() {
        this.orm = useService("orm");
        this.iconPrefix = "fa-";
        this.icons = {
            "Pending approval": "user",
            Approved: "check-square",
            Rejected: "times-circle",
            "Changes requested": "repeat",
            Waiting: "hourglass-o",
        };
        //console.log(this.props.record.preloadedData);
        super.setup();
        //const obj_sam = reactive(this.props.record.data.state_approval_mode)
    }

    get options() {
        //console.log(this.props.record.preloadedData['state_id'].records);
        return this.props.record.preloadedData["state_id"].records.map(
            ({ id, name, approval_mode }) => {
                return [id, name, approval_mode];
            }
        );
        //return this.stateSelection.map
    }

    get isApproval() {
        return this.props.record.data.state_approval_mode;
    }

    get availableOptions() {
        return this.options.filter((o) => o[2] !== false);
    }

    onSelectedDD(option) {
        //console.log(option);
        //console.log("onSelected");
        this.props.update(option);
    }

    onExternalButtonCLick0() {
        console.log("external click");
    }

    stateIcon(value) {
        console.log(value);
        console.log(this.icons);
        console.log(this.icons[value[1]]);
        return this.icons[value[1]] ? this.iconPrefix + this.icons[value[1]] : "";
    }

    toggleState() {
        console.log(this.props);
        const toggleVal = this.props.value[1] == "Done" ? [1, "In Progress"] : [2, "Done"];
        this.props.update(toggleVal);
    }
}

ProjectTaskStateSelectionMany2One.template = "project.ProjectTaskStateMany2OneField";

registry.category("fields").add("project_task_state_selection", ProjectTaskStateSelectionMany2One);

export function preloadState(orm, record, fieldName) {
    return orm.webSearchRead("project.task.state", [], ["name", "sequence", "approval_mode"]);
}

registry.category("preloadedData").add("project_task_state_selection", {
    loadOnTypes: ["many2one"],
    preload: preloadState,
});
