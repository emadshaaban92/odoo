/** @odoo-module */

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const { DateTime } = luxon;

function computeDelay(dateStr) {
    const today = DateTime.now().startOf("day");
    const date = DateTime.fromISO(dateStr);
    return date.diff(today, "days").days;
}

export class Activity extends Component {
    setup() {
        this.orm = useService("orm");
        this.activity = useService("mail.activity");
        this.state = useState({
            showDetails: false,
        });
        this.delay = computeDelay(this.props.data.date_deadline);
        onWillUpdateProps((nextProps) => {
            this.delay = computeDelay(nextProps.data.date_deadline);
        });
    }

    toggleDetails() {
        this.state.showDetails = !this.state.showDetails;
    }

    async edit() {
        const { id, res_model, res_id } = this.props.data;
        await this.activity.scheduleActivity(res_model, res_id, id);
        if (this.props.reload) {
            this.props.reload();
        }
    }

    async unlink() {
        await this.orm.unlink("mail.activity", [this.props.data.id]);
        if (this.props.reload) {
            this.props.reload();
        }
    }
}

Object.assign(Activity, {
    props: ["data", "reload?"],
    template: "mail.activity",
});
