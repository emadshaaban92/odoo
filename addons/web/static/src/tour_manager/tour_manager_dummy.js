/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted, xml, useState } from "@odoo/owl";

const MACRO_DESC = {
    steps: [
        {
            trigger: "button.inc",
            action: "click",
        },
        {
            trigger: "button.double",
            action: "click",
        },
        {
            trigger: "button.inc",
            action: "click",
        },
        {
            trigger: "button.double",
            action: "click",
        },
        {
            trigger: "button.dec",
            action: "click",
        },
        {
            trigger: "button.double",
            action: "click",
        },
    ],
    interval: 250,
};

export class TourManagerDummy extends Component {
    setup() {
        this.state = useState({ value: 0 });
        onMounted(() => {
            // this.env.services.tour_service_x.run({ mode: { kind: "manual" } });
            this.env.services.tour_service_x.run({ mode: { kind: "auto", interval: 500 } });
        });
    }
    onDecrement() {
        this.state.value--;
        console.log("decrement");
    }
    onIncrement() {
        this.state.value++;
        console.log("increment");
    }
    onDouble() {
        this.state.value *= 2;
        console.log("double");
    }
    getMacroDescription() {
        return MACRO_DESC;
    }
}

TourManagerDummy.props = ["action", "actionId", "className"];
TourManagerDummy.template = xml`
    <t>
        <div>
            <button class="dec" t-on-click="onDecrement">Decrement</button>
            <button class="inc" t-on-click="onIncrement">Increment</button>
            <button class="double" t-on-click="onDouble">Double</button>
            <span t-esc="state.value" />
        </div>
    </t>
`;

registry.category("actions").add("tour_manager_dummy", TourManagerDummy);
