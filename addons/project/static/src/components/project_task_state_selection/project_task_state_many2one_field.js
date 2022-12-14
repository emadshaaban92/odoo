/** @odoo-module */

import { StateSelectionField } from "@web/views/fields/state_selection/state_selection_field";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { EventBus , useBus } = owl;

export class ProjectTaskStateSelectionMany2One extends StateSelectionField {
    setup() {
        this.orm = useService("orm");
        this.iconPrefix = "fa-";
        this.icons = {
            "In Progress": "check-square-o",
            Done: "check-square",
            "Pending approval": "user",
            Approved: "check-circle",
            Rejected: "times-circle",
            "Changes requested": "repeat",
            Waiting: "hourglass-o",
        };
        this.colorIcons = {
            "In Progress": "",
            Done: "text-success",
            "Pending approval": "",
            Approved: "text-success",
            Rejected: "text-danger",
            "Changes requested": "text-warning",
            Waiting: "",
        };
        //this.serv = useService("statisticsServiceMod");
        console.log("this.props.record.preloadedData");
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

        super.setup();
        //const obj_sam = reactive(this.props.record.data.state_approval_mode)
    }

    get options() {
        //console.log(this.props.record.preloadedData['state_id'].records);
        return this.props.record.preloadedData["state_id"].records.map(
            ({ key, name, approval_mode }) => {
                return [key, name, approval_mode];
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
        return this.icons[value[1]] ? this.iconPrefix + this.icons[value[1]] : "";
    }

    stateColor(value) {
        return this.colorIcons[value[1]] || "";
    }

    async toggleState() {
        //const toggleVal = this.props.value[0] == 2 ? 1 : 2;         // those are the id for the 'In Progress' and 'Done' states
        //const toggleState = this.props.record.preloadedData["state_id"].records.find((record) => record.key == toggleVal)
        // This would be a better way to do it but the props.update() only takes a [key, label] value as update because we're in a StateSelection Field

        const toggleVal = this.props.value[1] == "Done" ? [1, "In Progress"] : [2, "Done"];
        await this.props.update(toggleVal);
        await this.props.record.model.root.load();
        this.props.record.model.notify();
    }

    /**
     * @param {MouseEvent} ev
     */
    onGlobalClick(ev) {
        console.log("global click");
        if (ev.target.closest(".button")) {
            return;
        }
        return super.onGlobalClick(ev);
    }
}

ProjectTaskStateSelectionMany2One.template = "project.ProjectTaskStateMany2OneField";

registry.category("fields").add("project_task_state_selection", ProjectTaskStateSelectionMany2One);

export function preloadState(orm, record, fieldName) {
    return orm.webSearchRead("project.task.state", [], ["name", "key", "approval_mode"]);
}

registry.category("preloadedData").add("project_task_state_selection", {
    loadOnTypes: ["many2one"],
    preload: preloadState,
});
