/** @odoo-module */

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { StatusBarField } from "@web/views/fields/statusbar/statusbar_field";
import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

const { onWillStart } = owl;


export class StatusBarTimeField extends StatusBarField {
    setup() {
        super.setup();
        this.user = useService("user");
        onWillStart(async () => {
            this.showTimeOptions = await this.user.hasGroup("crm.group_use_time_per_stage");
        });
        this.state = useState({ showTimePerStage: browser.localStorage.getItem('showTimePerStage') === 'true' });
    }

    changeTimePerStage() {
        this.state.showTimePerStage = !this.state.showTimePerStage;
        browser.localStorage.setItem('showTimePerStage', this.state.showTimePerStage);
    }

    setTimeInStage(items) {
        const timePerStage = JSON.parse(this.props.record.data.time_per_stage);
        if (Object.keys(timePerStage).length) {
            for (let i = 0; i < items.length; ++i) {
                if (items[i].id in timePerStage) {
                    let dur = moment.duration();
                    dur._milliseconds = timePerStage[items[i].id].ms;
                    dur._days = timePerStage[items[i].id].days;
                    items[i].timeInStage = dur.humanize();
                } else {
                    items[i].timeInStage = false;
                }
            }
        }
    }

    computeItems(grouped=true) {
        let items = super.computeItems(grouped);
        if (this.props.record.data.time_per_stage && this.showTimeOptions && this.state.showTimePerStage && grouped) {
            this.setTimeInStage(items.folded);
            this.setTimeInStage(items.unfolded);
        }
        return items;
    }
}

StatusBarTimeField.template = "crm.StatusBarTimeField";

registry.category("fields").add("statusbartime", StatusBarTimeField);
