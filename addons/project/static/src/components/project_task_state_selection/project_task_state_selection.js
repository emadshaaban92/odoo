/** @odoo-module */

import { StateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { EventBus , useBus } = owl;

export class ProjectTaskStateSelection extends StateSelectionField {
    setup() {
        this.orm = useService("orm");
        this.icons = {
            in_progress: "fa fa-check-circle-o",
            done: "fa fa-check-circle",
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
        //this.serv = useService("statisticsServiceMod");
        //console.log("this.props.record.preloadedData");
        /*
        setInterval(() => {
            
            this.props.record.model.notify();
            //this.props.load();
            console.log(this.props.record.data.name);
            console.log(this.props.value);
            //this.props.record.update();
            this.render();
        }, 10000);
        */
        if (this.props.record.activeFields[this.props.name].viewType !== "form") {
            super.setup();
        }
        //const obj_sam = reactive(this.props.record.data.state_approval_mode)
    }

    get options() {
        //console.log(this.props.record.preloadedData['state_id'].records);
        //return this.props.record.preloadedData["state_id"].records.map(
        //    ({ key, name, approval_mode }) => {
        //        return [key, name];
        //    }
        //);
        //return this.stateSelection.map
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
        //console.log(option);
        //console.log("onSelected");
        await this.props.update(option);
        await this.props.record.model.root.load();
        this.props.record.model.notify();
    }

    onExternalButtonCLick0() {
        console.log("external click");
    }

    stateIcon(value) {
        //console.log(value);
        //console.log(this.icons[value[1]]);
        const fut = this.icons[value] || "";
        return fut;
    }


    stateColor(value) {
        return this.colorIcons[value] || "";
    }

    async toggleState() {
        //const toggleVal = this.props.value[0] == 2 ? 1 : 2;         // those are the id for the 'In Progress' and 'Done' states
        //const toggleState = this.props.record.preloadedData["state_id"].records.find((record) => record.key == toggleVal)
        // This would be a better way to do it but the props.update() only takes a [key, label] value as update because we're in a StateSelection Field

        const toggleVal = this.props.value == "done" ? "in_progress" : "done";
        await this.props.update(toggleVal);
        //await this.props.record.model.root.load();
        //this.props.record.model.notify();
    }
}

ProjectTaskStateSelection.template = "project.ProjectTaskStateSelection";

registry.category("fields").add("project_task_state_selection", ProjectTaskStateSelection);

export function preloadState(orm, record, fieldName) {
    return orm.webSearchRead("project.task.state", [], ["name", "key", "approval_mode"]);
}

registry.category("preloadedData").add("project_task_state_selection", {
    loadOnTypes: ["many2one"],
    preload: preloadState,
});
